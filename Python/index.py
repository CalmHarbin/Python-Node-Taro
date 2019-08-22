import requests
import random
from pymongo import MongoClient
from time import sleep
from concurrent.futures import ThreadPoolExecutor  # 线程池

# 连接数据库
client = MongoClient('127.0.0.1', 27017)
db = client.db  # 连接mydb数据库，没有则自动创建
ip_client = client.ip  # 连接mydb数据库，没有则自动创建
ip_table = ip_client.ip  # 有效ip表

# 线程池
spider_poll_max = 7  # 爬虫线程池最大数量
# 爬虫线程池 max_workers最大数量
spider_poll = ThreadPoolExecutor(max_workers=spider_poll_max)

# 请求头的cookie和UserAgent
UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
# 武汉
city = '%E6%AD%A6%E6%B1%89'


def getRandomIp():
    '''
        @method 有效ip表中随机取一个ip
    '''
    global ip_table
    # 获取总数量
    count = ip_table.count_documents({})  # 查询一共有多少数据
    # 随机取一个
    index = random.randint(0, count)  # 获取0到count的随机整数
    print(count, index)
    data = ip_table.find().skip(index).limit(1)

    for item in data:
        print({'ip': item['ip'], 'port': item['port']})
        return {'ip': item['ip'], 'port': item['port']}


def getCookie(key_world):
    '''
        @method 获取cookie
    '''
    global UserAgent, city, ip_table

    # 随机获取一个代理,防止被封ip
    row = getRandomIp()
    print(50, row)
    try:
        proxies = {
            'http': row['ip'] + ':' + row['port'],
            'https': row['ip'] + ':' + row['port']
        }

        data = requests.get('https://www.lagou.com/jobs/list_' + key_world + '?px=default&city=' + city, timeout=10, proxies=proxies, headers={
            "User-Agent": UserAgent
        })
        cookies = data.cookies.get_dict()
        COOKIE = ''
        for key, val in cookies.items():
            COOKIE += (key + '=' + val + '; ')
        return COOKIE
    except:
        print('获取cookie失败,无效代理', row['ip'] + ':' + row['port'])
        # 删除无效代理
        ip_table.delete_one({"ip": row['ip'], "port": row['port']})
        # 重新获取cookie
        return getCookie(key_world)


def getData(obj):
    '''
        @method 抓取一页数据
    '''
    global UserAgent, client, db

    key_world = obj['key_world']  # 关键词
    page = obj['page']  # 分页

    print('开始抓取')

    # 连接数据表,前端需要转为web表,
    if key_world == '%E5%89%8D%E7%AB%AF':
        table = db.web  # 连接mydb数据库，没有则自动创建
    else:
        table = db[key_world]  # 连接mydb数据库，没有则自动创建

    # 随机获取一个代理,防止被封ip
    row = getRandomIp()
    print(102, row)
    proxies = {
        'http': row['ip'] + ':' + row['port'],
        'https': row['ip'] + ':' + row['port']
    }

    try:
        # 因为请求接口需要cookie,先获取cookie
        cookie = getCookie(key_world)

        # 抓取数据开始
        data = {
            "first": "false",
            "pn": page + 1,
            "kd": key_world == '%E5%89%8D%E7%AB%AF' and '前端' or key_world
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Connection": "keep-alive",
            "Host": "www.lagou.com",
            "Referer": 'https://www.lagou.com/jobs/list_' + key_world + '?px=default&city=' + city,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": UserAgent,
            "Cookie": cookie
        }
        response = requests.post('https://www.lagou.com/jobs/positionAjax.json?px=default&city=武汉&needAddtionalResult=false',
                                 data=data, timeout=10, proxies=proxies, headers=headers)
        response.encoding = 'utf-8'
        res = response.json()
        print(res)

        # 如果请求成功存入数据库中
        if res['msg'] == None:
            # 工作岗位
            position = res['content']['positionResult']['result']
            # 记录当前的数据
            one_data = []
            for idx, item in enumerate(position):
                one_data.append({
                    'positionName': item['positionName'],
                    'workYear': item['workYear'],
                    'salary': item['salary'],
                    'education': item['education'],
                    'companySize': item['companySize'],
                    'companyFullName': item['companyFullName'],
                    'formatCreateTime': item['formatCreateTime'],
                    'positionId': item['positionId']
                })
            # 没有数据了
            if len(one_data) == 0:
                print(key_world + '第'+page+'页数据为空')
                return

            # 存储当前数据
            table.insert_many(one_data)
            print(key_world + '第'+page+'页存入成功')
        else:
            print(key_world + '第'+page+'页存入失败')
            # 写日志
            with open('./log.txt', 'a', -1, 'utf-8') as f:
                f.write('key_world:'+key_world+',page:'+page+'\n')
                f.write(str(res))
                f.write('\n')
            # 删除无效代理
            ip_table.delete_one({"ip": row['ip'], "port": row['port']})

            # 重新添加到任务中
            spider_poll.submit(
                getData, ({'key_world': key_world, 'page': page}))
    except:
        print('超时代理', row['ip'] + ':' + row['port'])
        # 删除无效代理
        ip_table.delete_one({"ip": row['ip'], "port": row['port']})
        # 重新添加到任务中
        spider_poll.submit(getData, ({'key_world': key_world, 'page': page}))


# 搜索的关键词, 第一个为前端
key_worlds = ['%E5%89%8D%E7%AB%AF', 'Python', 'Java', 'PHP', 'C', 'C++', 'C#']
# 添加任务
for idx, key_world in enumerate(key_worlds):
    # 每种搜索关键词爬取100页
    for page in range(1, 100):
        # 添加一个任务
        spider_poll.submit(getData, ({'key_world': key_world, 'page': page}))

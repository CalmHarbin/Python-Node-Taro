import requests
from pymongo import MongoClient
from time import sleep
# 连接数据库
client = MongoClient('127.0.0.1', 27017)
db = client.db  # 连接mydb数据库，没有则自动创建
# 请求头的cookie和UserAgent
COOKIE = ''
UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
# 武汉
city = '%E6%AD%A6%E6%B1%89'

# 获取cookie


def getCookie(key_world):
    global COOKIE, UserAgent, city
    data = requests.get('https://www.lagou.com/jobs/list_' + key_world + '?px=default&city=' + city, headers={
        "User-Agent": UserAgent
    })
    cookies = data.cookies.get_dict()
    COOKIE = ''
    for key, val in cookies.items():
        COOKIE += (key + '=' + val + '; ')


# 请求数据
def getList(page, key_world):
    global COOKIE, UserAgent
    data = {
        "first": "false",
        "pn": page + 1,
        "kd": key_world == 'web' and '前端' or key_world
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Connection": "keep-alive",
        "Host": "www.lagou.com",
        "Referer": 'https://www.lagou.com/jobs/list_' + key_world + '?px=default&city=' + city,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": UserAgent,
        "Cookie": COOKIE
    }
    response = requests.post(
        'https://www.lagou.com/jobs/positionAjax.json?px=default&city=武汉&needAddtionalResult=false', data=data, headers=headers)
    response.encoding = 'utf-8'
    res = response.json()
    return res

# 抓取数据


def getData(key_world):
    global COOKIE, UserAgent, client, db
    print('开始抓取'+key_world)
    # 前端需要转为web
    if key_world == '%E5%89%8D%E7%AB%AF':
        table = db.web  # 连接mydb数据库，没有则自动创建
    else:
        table = db[key_world]  # 连接mydb数据库，没有则自动创建

    # key_world = '%E5%89%8D%E7%AB%AF'

    # 因为请求接口需要cookie,先获取cookie
    getCookie(key_world)

    # 抓取数据
    for page in range(1, 100):
        # 请求数据
        res = getList(page, key_world)
        # 如果请求成功存入数据库中
        if res['msg'] == None:
            print('成功')
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
                break
            # 存储当前数据
            table.insert_many(one_data)
        else:
            print('失败')
            # 写日志
            with open('./log.txt', 'a', -1, 'utf-8') as f:
                f.write(str(res))
                f.write('\n')
            # 重新获取cookie
            getCookie(key_world)
            # 再爬取当页数据
            res_once = getList(page, key_world)
            # 工作岗位
            position_once = res_once['content']['positionResult']['result']
            # 记录当前的数据
            one_data = []
            for idx, item in enumerate(position_once):
                one_data.append({
                    'positionName': item['positionName'],
                    'workYear': item['workYear'],
                    'salary': item['salary'],
                    'education': item['education'],
                    'companySize': item['companySize'],
                    'companyFullName': item['companyFullName'],
                    'formatCreateTime': item['formatCreateTime']
                })
            # 没有数据了
            if len(one_data) == 0:
                print(key_world + '存入成功')
                sleep(60)
                return
            # 存储当前数据
            table.insert_many(one_data)
    print(key_world + '存入成功')
    sleep(60)

# %E5%89%8D%E7%AB%AF


# 'web',
key_worlds = ['Python', 'Java', 'PHP', 'C', 'C++', 'C#']
# key_worlds = ['web']
for idx, key_world in enumerate(key_worlds):
    getData(key_world)

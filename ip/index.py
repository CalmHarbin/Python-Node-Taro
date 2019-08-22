import requests
import random
from pymongo import MongoClient
from lxml import etree  # xpath解析模块
from concurrent.futures import ThreadPoolExecutor  # 线程池


# 数据库连接
client = MongoClient('127.0.0.1', 27017)
db = client.ip  # 连接mydb数据库，没有则自动创建
table = db.table  # 将抓取的ip全部存到table表中
ip_table = db.ip  # 有效ip表

# 线程池
spider_poll_max = 50  # 爬虫线程池最大数量
# 爬虫线程池 max_workers最大数量
spider_poll = ThreadPoolExecutor(max_workers=spider_poll_max)


def getRandomIp():
    '''
        @method 有效ip表中随机取一个ip
    '''
    global ip_table
    # 获取总数量
    count = ip_table.count_documents({})  # 查询一共有多少数据
    # 随机取一个
    index = random.randint(0, count)  # 获取0到count的随机整数
    # print(count, index)
    data = ip_table.find().skip(index).limit(1)

    for item in data:
        return {'ip': item['ip'], 'port': item['port']}


def getIp(page):
    '''
        @method 爬取数据
    '''
    # 随机获取一个代理,防止被封ip
    row = getRandomIp()
    proxies = {
        'http': row['ip'] + ':' + row['port'],
        'https': row['ip'] + ':' + row['port']
    }

    try:
        # 抓取代理
        response = requests.get(
            'http://www.xiladaili.com/gaoni/' + str(page + 1)+'/', timeout=10, proxies=proxies)
        # 设置编码
        response.encoding = 'utf-8'
        # 解析
        s = etree.HTML(response.text)
        # 获取ip和请求类型
        ips = s.xpath(
            '/html/body/div[1]/div[3]/div[2]/table/tbody/tr/td[1]/text()')
        types = s.xpath(
            '/html/body/div[1]/div[3]/div[2]/table/tbody/tr/td[2]/text()')
        if (len(ips) == 0):
            print('抓取数据为空')
            # 写日志
            with open('./log.txt', 'a', -1, 'utf-8') as f:
                f.write(response.text)
                f.write('--------------------------------------------------')
                f.write('\n')
                f.write('\n')
                f.write('\n')
                f.write('\n')
            # 删除无效代理
            ip_table.delete_one({"ip": row['ip'], "port": row['port']})
        else:
            print('抓取数据成功, 正在存入数据库...')
            # 存储ip
            for index, ip in enumerate(ips):
                host = ip.split(':')[0]
                port = ip.split(':')[1]
                table.insert_one(
                    {"ip": host, "port": port, "type": types[index]})
    except:
        print('超时')
        # 删除无效代理
        ip_table.delete_one({"ip": row['ip'], "port": row['port']})


# 抓取网页的数量
for page in range(0, 100):
    # 添加一个线程
    spider_poll.submit(getIp, (page))

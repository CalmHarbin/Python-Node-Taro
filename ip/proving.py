import requests
from pymongo import MongoClient
from bson import ObjectId
from concurrent.futures import ThreadPoolExecutor  # 线程池

REQ_TIMEOUT = 5  # 超时时间

# 数据库连接
client = MongoClient('127.0.0.1', 27017)
db = client.ip  # 连接mydb数据库，没有则自动创建
table = db.table  # 使用test_set集合，没有则自动创建

spider_poll_max = 20  # 爬虫线程池最大数量
proving_poll = ThreadPoolExecutor(
    max_workers=spider_poll_max)  # 爬虫线程池 max_workers最大数量


def proving(ip):
    global table, ObjectId
    host = ip[0]
    port = ip[1]
    id = ip[2]

    proxies = {
        'http': host+':'+port,
        'https': host+':'+port
    }
    print(proxies)
    try:
        # 通过比较ip是否相同来判断代理是否有效
        OrigionalIP = requests.get(
            "http://icanhazip.com", timeout=REQ_TIMEOUT).content
        MaskedIP = requests.get("http://icanhazip.com",
                                timeout=REQ_TIMEOUT, proxies=proxies).content
        # 删除代理
        if OrigionalIP == MaskedIP:
            # table.delete_one({'_id': host, 'port': port})
            table.delete_one({'_id': ObjectId(id)})
        else:
            print('通过')
    except:
        # 删除代理
        # table.delete_one({'host': host, 'port': port})
        table.delete_one({'_id': ObjectId(id)})


# 查询数据库的所有ip
ips = table.find({}, {'ip': 1, 'port': 1})

# 有效性验证
for index, data in enumerate(ips):
    # 添加一个线程
    proving_poll.submit(proving, ((data['ip'], data['port'], data['_id'])))

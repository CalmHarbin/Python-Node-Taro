import requests
from pymongo import MongoClient
from lxml import etree  # xpath解析模块
import threading
import time
from concurrent.futures import ThreadPoolExecutor  # 线程池

# 数据库连接
client = MongoClient('127.0.0.1', 27017)
db = client.ip  # 连接mydb数据库，没有则自动创建
table = db.table  # 使用test_set集合，没有则自动创建

spider_poll_max = 5  # 爬虫线程池最大数量
spider_poll = ThreadPoolExecutor(
    max_workers=spider_poll_max)  # 爬虫线程池 max_workers最大数量


# 获取id


def getIp(page):
    print(page)
    # ['112.85.151.3:9999', '103.114.10.246:8080', '36.89.192.115:60297', '14.207.31.178:8080', '202.61.49.52:48713', '119.82.253.210:58069', '47.106.59.75:3128', '189.26.121.206:3128']
    proxies = {
        # 'http': '112.85.151.3:9999',
        # 'https': '112.85.151.3:9999'
    }
    # 请求数据
    response = requests.get(
        'http://www.xiladaili.com/gaoni/' + str(page + 1)+'/', proxies=proxies)
    # 设置编码
    response.encoding = 'utf-8'
    # 解析
    s = etree.HTML(response.text)
    # 获取ip和请求类型
    ips = s.xpath(
        '/html/body/div[1]/div[3]/div[2]/table/tbody/tr/td[1]/text()')
    types = s.xpath(
        '/html/body/div[1]/div[3]/div[2]/table/tbody/tr/td[2]/text()')
    print(ips)
    print(types)
    # 验证ip的有效性
    for index, ip in enumerate(ips):
        host = ip.split(':')[0]
        port = ip.split(':')[1]
        table.insert_one({"ip": host, "port": port, "type": types[index]})


def getRandomIp():
    global table
    # 获取总数量
    count = table.find({}, {'ip': 1}).count()  # 查询name为lisi的数据的数量
    # 随机取一个

    # 爬取1000页


for page in range(0, 5):
    # 添加一个线程
    spider_poll.submit(getIp, (page))

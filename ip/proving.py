import requests
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor  # 线程池

REQ_TIMEOUT = 3  # 超时时间

# 数据库连接
client = MongoClient('127.0.0.1', 27017)
db = client.ip  # 连接mydb数据库，没有则自动创建
table = db.table  # 所有的ip表
ip_table = db.ip  # 有效ip表

# 线程池
spider_poll_max = 100  # 爬虫线程池最大数量
# 爬虫线程池 max_workers最大数量
proving_poll = ThreadPoolExecutor(max_workers=spider_poll_max)


def proving(ip):
    '''
        @method 检测所有ip中有效的ip
    '''
    global table, ip_table
    host = ip['ip']
    port = ip['port']
    _id = ip['_id']
    types = ip['type']

    proxies = {
        'http': host+':'+port,
        'https': host+':'+port
    }

    try:
        requests.get('https://www.lagou.com/jobs/list_Python?px=default&city=武汉', timeout=5, proxies=proxies, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
        })
        # # 通过比较ip是否相同来判断代理是否有效
        # OrigionalIP = requests.get(
        #     "http://icanhazip.com", timeout=REQ_TIMEOUT).content
        # MaskedIP = requests.get("http://icanhazip.com",
        #                         timeout=REQ_TIMEOUT, proxies=proxies).content
        # # 删除代理
        # if OrigionalIP == MaskedIP:
        #     table.delete_one({"ip": host, "port": port, "type": types})
        #     # print('删除成功', result.deleted_count)
        # else:
        #     print('新增有效代理', host+':'+port)
        #     # 有效代理则存到ip表中
        #     ip_table.insert_one({"ip": host, "port": port, "type": types})
        #     # 同时删除原数据中的数据,防止下次重复添加到ip表中
        #     table.delete_one({"ip": host, "port": port, "type": types})
        print('有效')
        # 有效代理则存到ip表中
        ip_table.insert_one({"ip": host, "port": port, "type": types})
        # 同时删除原数据中的数据,防止下次重复添加到ip表中
        table.delete_one({"ip": host, "port": port, "type": types})
    except:
        # 删除代理
        print('删除成功')
        table.delete_one({"ip": host, "port": port, "type": types})
        # print(result.deleted_count)


def proving_ip(ip):
    '''
        @method 检测有效ip中无效ip
    '''
    global ip_table
    host = ip['ip']
    port = ip['port']
    _id = ip['_id']
    types = ip['type']

    proxies = {
        'http': host+':'+port,
        'https': host+':'+port
    }

    try:
        data = requests.get('https://www.lagou.com/jobs/list_Python?px=default&city=武汉', timeout=5, proxies=proxies, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
        })
        cookies = data.cookies.get_dict()
        COOKIE = ''
        for key, val in cookies.items():
            COOKIE += (key + '=' + val + '; ')
        print(COOKIE)
        print('有效代理', host+':'+port)
        # # 通过比较ip是否相同来判断代理是否有效
        # OrigionalIP = requests.get(
        #     "http://icanhazip.com", timeout=REQ_TIMEOUT).content
        # MaskedIP = requests.get("http://icanhazip.com",
        #                         timeout=REQ_TIMEOUT, proxies=proxies).content
        # # 删除代理
        # if OrigionalIP == MaskedIP:
        #     ip_table.delete_one(
        #         {"ip": host, "port": port, "type": types})
        #     # print('删除成功', result.deleted_count)
        # else:
        #     print('有效代理', host+':'+port)

    except:
        # 删除代理
        print('失效代理')
        ip_table.delete_one({"ip": host, "port": port, "type": types})
        # print(result.deleted_count)


# 先检测有效ip表中无效的ip
proving_ips = ip_table.find({})
print('开始清理无效ip...')
# 有效性验证
for data in proving_ips:
    # 添加一个线程
    proving_poll.submit(proving_ip, (data))


ips = table.find({})
print('开始代理有效性验证...')
# 有效性验证
for data in ips:
    # 添加一个线程
    proving_poll.submit(proving, (data))

import requests
UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
COOKIE = ''


def getCookie():
    '''
        @method 获取cookie
    '''
    global UserAgent
    response = requests.get('https://www.lagou.com/jobs/list_Python?px=default&city=%E6%AD%A6%E6%B1%89', headers={
        "User-Agent": UserAgent
    })
    # 获取的cookie是字典类型的
    cookies = response.cookies.get_dict()
    # 因为请求头中cookie需要字符串,将字典转化为字符串类型
    COOKIE = ''
    for key, val in cookies.items():
        COOKIE += (key + '=' + val + '; ')
    return COOKIE


# 请求头
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Connection": "keep-alive",
    "Host": "www.lagou.com",
    "Referer": 'https://www.lagou.com/jobs/list_Python?px=default&city=%E6%AD%A6%E6%B1%89',
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": UserAgent,
    "Cookie": getCookie()
}
print(headers)
# 请求数据
data = {
    'first': False,  # 这个参数固定可以写False
    'pn': 2,         # pn表示页码
    'kd': 'Python'  # kd表示搜索关键测
}
response = requests.post(
    'https://www.lagou.com/jobs/positionAjax.json?px=default&city=武汉&needAddtionalResult=false', data=data, headers=headers)
# 编码
response.encoding = 'utf-8'
# 获取json
res = response.json()
print(res)

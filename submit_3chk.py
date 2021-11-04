#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import os
from datetime import datetime
import urllib.parse
import random


def pushToWeChat(msg):
    timeStamp = datetime.today().strftime('%Y-%m-%d')
    pushURL = "https://sctapi.ftqq.com/" + \
        os.getenv("sckey") + ".send?title=" + \
        urllib.parse.quote(timeStamp + str(msg))
    requests.post(pushURL)


# Check if disabled
if os.path.exists("NOSUBMIT"):
    exit()

isWeChatAvail = True

# Check if WeChat push service available
if os.getenv("sckey") == None or os.getenv("sckey") == "aaa":
    print("WeChat Push Disabled")
    isWeChatAvail = False

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
           "Referer": "https://xxcapp.xidian.edu.cn/site/ncov/xidiandailyup"}
data = {"sfzx": '1',
        'tw': '1',
        'area': '陕西省 西安市 长安区',
        'city': '西安市',
        'province': '陕西省',
        'address': '陕西省西安市长安区兴隆街道竹园三路西安电子科技大学南校区',
        'geo_api_info':
        '{"type":"complete","position":{"Q":34.12618733724,"R":108.84139458550402,"lng":108.841395,"lat":34.126187},"location_type":"html5","message":"Get ipLocation failed.Get geolocation success.Convert Success.Get address success.","accuracy":83,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"雷甘路","streetNumber":"238号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道竹园三路西安电子科技大学南校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}', 'sfcyglq': '0', 'sfyzz': '0', 'qtqk': '', 'ymtys': '0'}

tempStr = data['geo_api_info'].replace(
    "34.12618733724", "34.1261873" + str(random.randint(1024, 9876))).replace(
        "108.84139458550402", "108.8413945" + str(random.randint(1145141, 9198100)))

conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
                   data={'username': os.getenv("username"), 'password': os.getenv("pswd")})
if result.status_code != 200:
    print('认证大失败')
    if not isWeChatAvail:
        pushToWeChat(" 认证失败")
    exit()

result = conn.post(
    'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save', data=data)
if result.status_code != 200:
    print('获取页面大失败')
    if not isWeChatAvail:
        pushToWeChat(" 获取页面失败")
    exit()
print(result.text)
pushToWeChat(" 填报成功")

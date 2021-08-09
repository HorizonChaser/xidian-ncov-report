import json
import requests
import re
import sys
import os
from datetime import datetime
import urllib.parse

username = input("学号\n")
pswd = input("密码\n")

conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
                   data={'username': username, 'password': pswd})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Get Page
result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
if result.status_code != 200:
    print('获取页面大失败')
    exit()

predef = json.loads(re.search('var def = ({.*});', result.text).group(1))
geoInfo = json.loads(predef['geo_api_info'].replace("\"", "\\\"").replace("'", "\""))

print("-------以下是你的位置信息 (不要复制这一行)-------")
print(geoInfo['geo_api_info'].encode("unicode_escape").decode())
print("-------以上是你的位置信息 (不要复制这一行)-------")

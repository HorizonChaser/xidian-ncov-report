#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import os
from datetime import datetime
import urllib.parse

if os.path.exists("NOSUBMIT"):
    exit()

data = {}

with open("./data.json", "r") as fd:
    data = json.load(fd)
    data['geo_api_info'] = os.getenv("geo_info")
    geo = json.loads(data["geo_api_info"])
    data.update({"address": geo["formattedaddress"]})
    data.update({"city": geo["addresscomponent"]["city"]})
    data.update({"province": geo["addresscomponent"]["province"]})
    data.update({"area": geo["addresscomponent"]["province"] + ' ' +
                geo["addresscomponent"]["city"] + ' ' + geo["addresscomponent"]["district"]})
    if data["city"].strip() == "" and data["province"] in ["北京市", "上海市", "重庆市", "天津市"]:
        data["city"] = data["province"]

conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',
                   data={'username': os.getenv("username"), 'password': os.getenv("pswd")})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Submit
result = conn.get('https://xxcapp.xidian.edu.cn/ncov/wap/default/index')
if result.status_code != 200:
    print('获取页面大失败')
    exit()

if os.path.exists("last_get.html"):
    os.remove("last_get.html.1")
    os.rename("last_get.html", "last_get.html.1")

with open("last_get.html", "w") as fd:
    fd.write(result.text)

# TODO: diff those two files to determine whether submission form has been updated, then delay the submission when necessary

predef = json.loads(re.search('var def = ({.*});', result.text).group(1))

if "dump_geo" in sys.argv:
    print(predef['geo_api_info'])
    exit()

try:
    del predef['jrdqtlqk']
    del predef['jrdqjcqk']
except:
    pass
del data['_u']
del data['_p']
predef.update(data)

result = conn.post(
    'https://xxcapp.xidian.edu.cn/ncov/wap/default/save', data=predef)

print(result.text)

pushMsg = datetime.today().strftime('%H:%M:%S')
pushURL = "https://sctapi.ftqq.com/" + \
    os.getenv("sckey") + ".send?title=" + \
    urllib.parse.quote(pushMsg + " 填报成功 @ ")
requests.post(pushURL + pushMsg)

# if "成功" in result.text:
#     pushMsg = urllib.parse.quote(pushMsg + " 填报成功")
#     requests.post(pushURL + pushMsg)
# elif "填报" in result.text:
#     pushMsg = urllib.parse.quote(pushMsg + " 已经填报过了")
#     requests.post(pushURL + pushMsg)
# else:
#     pushMsg = urllib.parse.quote(
#         pushMsg + " 发生了点儿意外, 请查看详情" + "&desp=" + result.text)
#     requests.post(pushURL + pushMsg)

#!/usr/bin/python3
# encoding: utf-8
"""
@author: Yancy Yue
@contact: yancyyue@gmail.com
@file: AntFundSui.py
@time: 2018/4/27
@desc: Export fund records from Ant Fortune to sui.com
"""

import requests
import sys
import XueqiuUtils

postdata = {
    'beginYear': '2007',
    'endYear': '2019',
    'opt': 'someYearSum'
}
print(postdata)

cookiesMap = XueqiuUtils.parseSuiCookie()
cookies = {
    'JSESSIONID': cookiesMap[XueqiuUtils.sui_jsessionid_key],
    'SESSION_COOKIE': cookiesMap[XueqiuUtils.sui_sessionCookie_key],
    'SESSION': cookiesMap[XueqiuUtils.sui_session_key],
}

headers = {
    'Host': 'www.sui.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://www.sui.com/tally/new.do',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
    #  'Connection': 'keep-alive'
}
request = requests.post('https://www.sui.com/tally/new.rmi',
                        data=postdata,
                        headers=headers,
                        cookies=cookies)
print('request.code/text:', request.status_code, '/', request.text)

#!/usr/bin/python3
# encoding: utf-8
"""
@author: Yancy Yue
@contact: yancyyue@gmail.com
@file: AntFundSui.py
@time: 2018/1/20 22:10
@desc: Export fund records from Ant Fortune to sui.com
"""

import requests
import csv
import sys
from urllib import parse,request
from datetime import datetime

import XueqiuUtils

print("Python3 is expected.Current Version is:" + sys.version)


# https://consumeprod.alipay.com/record/standard.htm  高级筛选，搜索“蚂蚁财富”
with open(XueqiuUtils.filename) as csv_file:
    rows = csv.reader(csv_file)
    rownumber = 1
    for row in rows:
        # print(row)
        # print(count)
        # to read 15 lines in which the first 4 lines are useless and the 5th line is title.
        if (rownumber >XueqiuUtils.processTopNRecords):
            exit()

        rownumber += 1
        fundName = ''
        if row != "":  # add other needed checks to skip titles
            # cols = row.split("','")
            # print(len(row))
            if (len(row) < 8):
                continue
            elif (len(row[8].split("-")) > 1):
                fundName = row[8].split("-")[1]
                #print(fundName)
            else:
                continue
            transfertime = row[2].strip()
            transfertime = datetime.strptime(transfertime, '%Y-%m-%d %H:%M:%S').strftime('%Y.%m.%d') + ' 23:'+str(59-rownumber)
            # print(row[8])
            print("Processing Row #"+str(rownumber)+": "+fundName)

            postdata = {
                'id': '0',
                'store': '0',
                'project': '0',
                'member': '0',
                'out_account': '16760911192',
                'in_account': '32546913',
                'account': '0',
                'time': transfertime,
                'memo': row[8].strip().split("-")[1],
                'price': row[9].strip(),
                'debt_account': '',
                'price2': ''
            }
            print(postdata)
            # postdata = urllib.parse.urlencode(postdata, 'utf-8')
            # postdata = params.encode('utf-8')

            cookies = {
                'JSESSIONID': XueqiuUtils.sui_jsessionid,
                'SESSION_COOKIE': XueqiuUtils.sui_sessionCookie,
            }

            headers = {
                # 'Host': 'www.sui.com',
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
                # 'Accept': '*/*',
                # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                # 'Referer': 'https://www.sui.com/tally/new.do',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                # 'X-Requested-With': 'XMLHttpRequest',
                #  'Connection': 'keep-alive'
            }
            request = requests.post('https://www.sui.com/tally/transfer.rmi',
                                    data=postdata,
                                    headers=headers,
                                    cookies=cookies)
            print('request.text:', request.text)

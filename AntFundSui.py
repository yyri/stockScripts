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


print("Python3 is expected.Current Version is:" + sys.version)

jsessionid = '3770EAA80D813701D2B0463993A473BE'
sessionCookie = '14ef1450ea7d6f4f82ef548c622dde6d'
filename = "C:/downloads/alipay_record_20180120_2135/alipay_record_20180120_2135_1.csv"

# https://consumeprod.alipay.com/record/standard.htm  高级筛选，搜索“蚂蚁财富”
with open(filename) as csv_file:
    rows = csv.reader(csv_file)
    count = 11
    for row in rows:
        # print(row)
        count -= 1
        # print(count)
        if (count < 0):
            exit()

        if row != "":  # add other needed checks to skip titles
            # cols = row.split("','")
            if (len(row[8].split("-")) > 1):
                print(row[8].split("-")[1])
            else:
                continue
            transfertime = row[2]
            transfertime = datetime.strptime(transfertime, '%Y/%m/%d %H:%M').strftime('%Y.%m.%d') + ' 23:59'
            # print(row[8])
            print(row[9])

            postdata = {
                'id': '0',
                'store': '0',
                'project': '0',
                'member': '0',
                'out_account': '16760911192',
                'in_account': '32546913',
                'account': '0',
                'time': transfertime,
                'memo': row[8].split("-")[1],
                'price': row[9],
                'debt_account': '',
                'price2': ''
            }
            print(postdata)
            # postdata = urllib.parse.urlencode(postdata, 'utf-8')
            # postdata = params.encode('utf-8')

            cookies = {
                # '__vistor': 'DBFAC5281c1lhem71',
                # 'Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4': '1515662855,1515726830,1515728528,1515813996',
                # '__nick': 'yyri"%"40163.com',
                # '_bookTabSwitchList': 'f8bb35fce3a08671b3ae2ed6c33e69c8|0|0&eaf0f8eee8ac43901d493221d4db8cd0|0|0&',
                # '__utma': '121176714.950744407.1513591643.1516352533.1516414389.48',
                # '__utmz': '121176714.1514086705.5.3.utmcsr=lc.ssjlicai.com|utmccn=(referral)|utmcmd=referral|utmcct=/index',
                'JSESSIONID': jsessionid,
                'SESSION_COOKIE': sessionCookie,
                # '__utmc': '121176714',
                # 'Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4': '1516352533',
                # '__utmb': '121176714.1.10.1516445514',
                # '__utmt': '1'
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
            # print(len(row[8].split("-")))
            # print(row[8].split("-"))
            # print(len(row[8].split("-")))
            # s = requests.session()
            # s.headers = headers
            # s.cookies = cookies
            request = requests.post('https://www.sui.com/tally/transfer.rmi',
                                    data=postdata,
                                    headers=headers,
                                    cookies=cookies)
            print('request.text:', request.text)
            # curltext = " curl \"https://www.sui.com/tally/transfer.rmi\""
            # curltext += " -H \"Content-Type: application/x-www-form-urlencoded; charset=UTF-8\""
            # curltext += "  -H \"Cookie:    JSESSIONID=6D61B78E15F71CCE264953D3A2680E07;"
            # curltext += " SESSION_COOKIE=14ef1450ea7d6f4f82ef548c622dde6d\""
            # curltext += "  --data \"";
            # curltext += parse.urlencode(postdata) + "\"";
            # print(curltext)

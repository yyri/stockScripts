#!/usr/bin/python3
# encoding: utf-8
"""
@author: Yancy Yue
@contact: yancyyue@gmail.com
@file: AntFundXueqiu.py
@time: 2018/1/20 22:10
@desc: Export fund records from Ant Fortune to xueqiu.com/performance
"""

import csv
import sys
from datetime import datetime
from math import floor

import requests

import XueqiuUtils

if __name__ == "__main__":

    print('Python3 is expected.\nCurrent Version is:' + sys.version)
    errorLines = 0

    with open(XueqiuUtils.filename) as csv_file:
        rows = csv.reader(csv_file)
        rownumber = 0
        for row in rows:
            # print(row)
            # to read 15 lines in which the first 4 lines are useless and the 5th line is title.
            if (rownumber >= XueqiuUtils.processTopNRecords):
                exit()

            rownumber += 1
            fundName = ''
            sumMoney = 0

            if row != "":  # add other needed checks to skip titles
                # cols = row.split("','")
                if (len(row) < 8):
                    continue
                elif (len(row[8].split("-")) > 1):
                    fundName =row[8].split("-")[1]
                    print(fundName)
                else:
                    continue

                formData = XueqiuUtils.xq_formData
                transfertime = row[2].strip()
                transfertime = datetime.strptime(transfertime, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
                # print(row[8])
                print("Processing Row #" + str(rownumber) + ": " + fundName)

                sumMoney = row[9].strip()
                print('sumMoney:'+sumMoney)

                if fundName in XueqiuUtils.fundList:
                    print("Code/Rate of \'" + fundName + "\' is " + XueqiuUtils.fundList[fundName][0] + "/" + str(
                        XueqiuUtils.fundList[fundName][1]))
                else:
                    print(fundName + "not found in fundList.")
                    errorLines += 1

                # trans data
                formData['data[date]'] = transfertime

                # fund code
                formData['data[symbol]'] = XueqiuUtils.fundList[fundName][0]

                # trans cost
                commission = floor(float(sumMoney) * XueqiuUtils.fundList[fundName][1]*100)/100
                formData['data[commission]'] = commission

                # fund price on trans date
                jjjz = XueqiuUtils.getpriceFromSina(formData['data[symbol]'], formData['data[date]'])
                formData['data[price]'] = jjjz

                # trans shares
                shares = (float(sumMoney) - commission)/ jjjz
                shares = floor(shares*100)/100
                formData['data[shares]'] = shares

                #
                formData['data[comment]'] = 'AutoImport'

                print(formData)

                request = requests.post('https://xueqiu.com/service/poster',
                                        data=formData,
                                        headers=XueqiuUtils.xq_headerData,
                                        cookies=XueqiuUtils.xq_cookieData)

                if(request.status_code != 200):
                    print("ERROR！"+". Request return code:"+request.status_code)
                    exit(1)
                else:
                    print('Return Code:',request.status_code)
                    print('request.result:', request.text)

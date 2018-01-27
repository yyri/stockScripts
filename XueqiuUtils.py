#!/usr/bin/python3
# encoding: utf-8
"""
@author: Yancy Yue
@contact: yancyyue@gmail.com
@file: XueqiuUtils.py
@time: 2018/1/21 8:55
@desc:
"""
import requests
import json
from urllib import parse, request
from datetime import datetime


sui_jsessionid = '9AA43A46A085C64B21E2C61696C64F43'
sui_sessionCookie = '14ef1450ea7d6f4f82ef548c622dde6d'
filename = "C:\downloads\\alipay_record_20180127_1922\\alipay_record_20180127_1922_1.csv"

cookieData = {
    'xq_a_token': 'e39d420f30c251f6778a2f394341cf89fa77b392',
    'xq_a_token.sig': 'wCFLnsMbz-uU5s9grLNI9KSZ-QI',
    'xq_is_login': '1',
    'xq_is_login.sig': 'J3LxgPVPUzbBg3Kee_PquUfih7Q',
    'xq_r_token': '1adc1236349428753242dc24173b2451b265b3d4',
    'xq_r_token.sig': 'lmBuAzU4LnsSe128lC4ergOK9Ug',
}

fundList = {
    '华夏恒生ETF联接(QDII)': ['F000071', 0.0012],
    '景顺长城沪深300增强': ['F000311', 0.0012],
    '工银瑞信国企改革主题股票': ['F001008', 0.0015],
    '建信中证500指数增强': ['F000478', 0.0015],
    '博时中证淘金大数据100I': ['F001243', 0.0006],
    '易方达消费行业股票': ['F110022', 0.0015],
    '易方达中小盘混合': ['F110011', 0.0015],
    '易方达上证50指数A': ['F110003', 0.0015],
    '工银瑞信全球精选股票(QDII)': ['F486002', 0.0016],
    '华宝海外中国成长混合(QDII)': ['F241001', 0.0015],
    '富国中证国有企业改革': ['F161026', 0.0015],
    '易方达纳斯达克100': ['F161130', 0.0015],
    '交银施罗德中证海外中国互联网指数(QDII': ['SZ164906', 0.0012],
}

headerData = {
    'Host': 'xueqiu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://xueqiu.com/performance',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cache-control': 'no-cache',
    # 'X-Requested-With': 'XMLHttpRequest',
}


formData = {
    'url': '/stock/portfolio/addtrans.json',
    'data[type]': '1',
    'data[date]': '2018-01-20',  # Dynamic
    'data[comment]': '',
    'data[symbol]': 'F110022',  # Dynamic
    'data[groupId]': '3147879',
    'data[price]': '1.5',  # Dynamic
    'data[shares]': '100',  # Dynamic
    'data[commission]': '0.4',  # Dynamic
    'data[taxRate]': '',
    'data[_]': '1516457868626',
}




def getprice(fundcode, transdate):
    xqPriceUrl = "http://fund.xueqiu.com/dj/open/fund/growth/FUNDCODE.json?day=7"
    fundcode = fundcode[len(fundcode)-6:len(fundcode)]
    xqPriceUrl = xqPriceUrl.replace('FUNDCODE',fundcode)
    print(xqPriceUrl)
    #get the date of next Thursday
    request = requests.get(xqPriceUrl, headers=headerData, cookies=cookieData)
    print('request.text:', request.text)
    return fundcode+transdate;

def getpriceFromSina(fundcode, transdate):
    sinaPriceUrl = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?symbol=FUNDCODE&datefrom=TRANSDATE&dateto=TRANSDATE"
    fundcode = fundcode[len(fundcode)-6:len(fundcode)]
    sinaPriceUrl = sinaPriceUrl.replace('FUNDCODE',fundcode)
    sinaPriceUrl = sinaPriceUrl.replace('TRANSDATE', transdate)
    print(sinaPriceUrl)
    #get the date of next Thursday
    request = requests.get(sinaPriceUrl)
    print('request.text:', request.text)

    jjjzjson = json.loads(request.text)
    jjjz =jjjzjson["result"]['data']['data'][0]['jjjz']
    print(jjjz)
    return float(jjjz);




if __name__ == "__main__":
    # test
    print(getpriceFromSina("F110022", "2018-1-18"))
    print(getpriceFromSina("SZ164906", "2018-1-17"))

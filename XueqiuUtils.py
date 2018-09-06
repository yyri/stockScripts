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

# cookie get from firefox GET /tally/new.do
sui_cookies='__vistor=DBFAC5281c1lhem71; Hm_lvt_3db4e52bb5797afe0faaa2fde5c96ea4=1534401815,1534402093; __nick=yyri%40163.com; __utma=121176714.950744407.1513591643.1535608862.1535676985.302; __utmz=121176714.1514086705.5.3.utmcsr=lc.ssjlicai.com|utmccn=(referral)|utmcmd=referral|utmcct=/index; _bookTabSwitchList=f8bb35fce3a08671b3ae2ed6c33e69c8|0|0&578a9f2dae10be157cdef89d0c38243c|0|0&; SESSION_COOKIE=14ef1450ea7d6f4f82ef548c622dde6d; __utmc=121176714; JSESSIONID=4DBED8E974B909B69C17E047614636FB; Hm_lpvt_3db4e52bb5797afe0faaa2fde5c96ea4=1535676982; SESSION=3cbba359-4a2f-453b-bd19-631846ffac68; __utmb=121176714.1.10.1535676985; __utmt=1'
sui_jsessionid_key = 'JSESSIONID'
sui_sessionCookie_key = 'SESSION_COOKIE'
sui_session_key = 'SESSION'
filename = "C:\downloads\\alipay_record.csv"

processTopNRecords = 15  # 5 Useless Rows included.

xq_cookies = 'Hm_lvt_1db88642e346389874251b5a1eded6e3=1534292692; device_id=0f130389a94383e2368d5d55e43adf3d; s=fd11clw10r; bid=7d61d477a90d923192ee705a2d8777db_jbh841ja; __utma=1.1924959979.1513905273.1534393408.1534408052.334; __utmz=1.1520496770.113.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E6%95%B0%E5%BA%93%E7%A7%91%E6%8A%80; xq_a_token=1d834a627efbed22d48b263216be6f4781c90a01; xq_r_token=75f0aa06f318c2c844e5cfb79dd3a086f47c2dd5; u=7309855904; _ga=GA1.2.1924959979.1513905273; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token.sig=CWsqwQw03hO3azVdp8tbY4b-SA8; xq_r_token.sig=RB3D7qvOwM7KPveTDNko5CroRU0; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=Xh0hW3oFsp-9FsZnngYrdcQFc8Y; aliyungf_tc=AQAAAJNbDStDvQYAqqdBfNBd8yjSj6Ug; __utmc=1; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1534393402; __utmb=1.1.10.1534408052; __utmt=1'
xq_cookieData = {
    'xq_a_token': '',
    'xq_r_token': '',
    'xq_a_token.sig': '',
    'xq_is_login': '1',
    'xq_is_login.sig': '',
    'xq_r_token.sig': '',
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

xq_headerData = {
    'Host': 'xueqiu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Referer': 'https://xueqiu.com/performance',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cache-control': 'no-cache',
    # 'X-Requested-With': 'XMLHttpRequest',
}


xq_formData = {
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


def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""

    delimiters = tuple(delimiters)
    stack = [string, ]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i + j, _substring)

    return stack


def parseCookieText(cookieText):
    result = tsplit(cookieText, (';'))
    resultmap = {}
    for kvstr in result:
        kv=tsplit(kvstr, '=')
        resultmap[kv[0].strip()] = kv[1].strip()
    return resultmap


def parseSuiCookie():
    return parseCookieText(sui_cookies)


def parseXueqiuCookie():
    resultMap = parseCookieText(xq_cookies)
    xq_cookieData['xq_a_token'] = resultMap['xq_a_token']
    xq_cookieData['xq_r_token'] = resultMap['xq_r_token']
    xq_cookieData['xq_a_token.sig'] = resultMap['xq_a_token.sig']
    xq_cookieData['xq_r_token.sig'] = resultMap['xq_a_token.sig']
    xq_cookieData['xq_is_login'] = resultMap['xq_is_login']
    xq_cookieData['xq_is_login.sig'] = resultMap['xq_is_login.sig']
    print(xq_cookieData)


def getprice(fundcode, transdate):
    xqPriceUrl = "http://fund.xueqiu.com/dj/open/fund/growth/FUNDCODE.json?day=7"
    fundcode = fundcode[len(fundcode)-6:len(fundcode)]
    xqPriceUrl = xqPriceUrl.replace('FUNDCODE',fundcode)
    print(xqPriceUrl)
    #get the date of next Thursday
    request = requests.get(xqPriceUrl, headers=xq_headerData, cookies=xq_cookieData)
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
    if(len(jjjzjson["result"]['data']['data'])>0):
        jjjz =jjjzjson["result"]['data']['data'][0]['jjjz']
        print(jjjz)
        return float(jjjz);
    else:
        print("Error! No Data Return.")
        return 9999;



if __name__ == "__main__":
    # test
    # print(getpriceFromSina("F110022", "2018-1-18"))
    # print(getpriceFromSina("SZ164906", "2018-1-17"))
    # parseSuiCookie()
    parseXueqiuCookie()

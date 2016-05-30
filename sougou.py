#!/usr/bin/env python3
# coding: utf-8
from get_proxy import *
import datetime
import hashlib
import http.cookiejar
import json
import urllib.parse
import urllib.request
import random
import re
import time
import xml.etree.cElementTree as cET


def get_content_from_url(type='2',
                        query='浙江旅游',
                        ie='utf8',
                        _sug_='n',
                        _sug_type_=''
                         ):

    # start
    url_xhr = "http://weixin.sogou.com/weixin?type=1&query=%E6%B5%99%E6%B1%9F%E6%97%85%E6%B8%B8&ie=utf8&_sug_=n&_sug_type_="

    # deal with form data
    form_data = urllib.parse.urlencode({
        'type':type,
        'query':query,
        'ie':ie,
        '_sug_':_sug_,
        '_sug_type_':_sug_type_
    }).encode()

    # deal with headers
    ori_headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        #'Cookie':'SUID=7726B5272E08990A0000000056FB617F; SUV=1459315071849677; CXID=A479D3D3FAB4AFC030E5DC7A315431B1; pgv_pvi=5460460544; weixinIndexVisited=1; wuid=AAFstWvfEAAAAAqTCRoQ0wYANwI=; usid=FIWrCrYlAETO_QEw; ABTEST=6|1462180330|v1; SUIR=E395F49BF4F6C52B9480065AF477BA1A; ld=gkllllllll2gJefTlllllVtXq5tlllllbZxuVZllllwllllllklll5@@@@@@@@@@; ad=Olllllllll2g3jI6lllllVtrUk7lllllJEUX@lllll9lllllxylll5@@@@@@@@@@; SNUID=68009200262214732147BAE927FA7458; sct=11; JSESSIONID=aaaFGzRdHVnMF7PGm-mrv; IPLOC=CN; LSTMV=98%2C236; LCLKINT=16392',
        'DNT':'1',
        'Host':'weixin.sogou.com',
        #'Referer':'http://weixin.sogou.com/weixin?type=2&query=%E6%B5%99%E6%B1%9F%E6%97%85%E6%B8%B8&ie=utf8&_sug_=y&_sug_type_=&w=01015002&oq=zjly&ri=7&sourceid=sugg&stj=7%3B4%3B0%3B0&stj2=0&stj0=7&stj1=4&hp=40&hp1=&sut=7552&sst0=1462715659910&lkt=1%2C1462715659807%2C1462715659807',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    }

    req = urllib.request.Request(url_xhr)

    # add headers to req
    for key, value in ori_headers.items():
        req.add_header(key, value)

    # deal with cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)

    # 验证码html长度:4878
    proxyList=[]
    file = open("available.txt")

    for line in file:
        line = line.replace('\n','')
        proxyList.append(line)
    file.close()
    if len(proxyList)==0:
        print('暂无可用IP,即将退出程序')
        return '暂无可用IP,即将退出程序'

    list_l = len(proxyList)
    data_str = 'xx'
    while list_l > -1:
        ind = random.randint(0,len(proxyList)-1)
        proxy = proxyList[ind].strip('.')
        proxy_p = urllib.request.ProxyHandler(proxies={'http': proxy})
        opener = urllib.request.build_opener(proxy_p,pro)
    #    op = opener.open(req, form_data)
        try:
            op = opener.open(req,timeout=3)

            data_bytes = op.read()
            data_str = bytes.decode(data_bytes)
        except Exception as error:data_str = 'xx'
        if len(data_str) > 5000:
            print('抓取成功')
            break
        else:
            print('IP: '+str(proxy)+' 被封,正在更换IP')
            list_l -= 1

    return data_str


def store_to_html(data_str):
    # write to data_str.html
    file_name = 'data_str.html'
    if len(data_str)>5000:
        with open(file_name, 'w') as f:
            f.write(data_str)
            f.close()
    else:
        print('暂无可用IP')

    return file_name


def formatted(file_name):
    pass


def main():
    get_proxy()
    check_proxy()
    data_str = get_content_from_url()
    file_name = store_to_html(data_str)
    formatted(file_name)


if __name__ == '__main__':
    for x in range(20):
        main()


'''
首先抓取http://www.xicidaili.com/nn/前3页的高匿IP保存到'proxy.txt'
每次程序运行时,若当前时间与'proxy.txt'文件的最近一次修改时间相差大于10分钟或'proxy.txt'文件内无内容则重新抓取
再检测'proxy.txt'文件内IP的可用性保存到'available.txt'
每次程序运行时,若当前时间与'available.txt'文件的最近一次修改时间相差大于10分钟或'available.txt'文件内无内容则重新抓取

根据'available.txt'内的IP数量生成随机数,随机挑选一个IP用于微信公众号搜索,若该IP需要验证码,则再随机选择一个IP,若在一定次数内无法抓取,则输出'暂无可用IP'
若成功抓取,则输出'抓取成功'
'''
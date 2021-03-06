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
    file_name = 'data_str.txt'
    if len(data_str)>5000:
        with open(file_name, 'w',encoding='utf-8') as f:
            f.write(data_str)
            f.close()
    else:
        print('暂无可用IP')
        exit(-1)

    return file_name


def get_gzh_url(file_name):
    with open('data_str.txt','r',encoding='utf-8') as f:
        x = f.read()
        ar = re.findall('<div target="_blank" href="(.*)" class="wx-rb bg-blue wx-rb_v1 _item"',x)
        urlink = ar[0].replace('amp;','')
        print('公众号url为: '+urlink)
    f.close()
    return urlink


def get_weixin_content(urlink):
    # start
    url_xhr = urlink
    req = urllib.request.Request(url_xhr)

    # deal with cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)

    opener = urllib.request.build_opener(pro)
    op = opener.open(req,timeout=3)

    data_bytes = op.read()
    data_str = bytes.decode(data_bytes)

    return data_str


def get_title(weixin_data):
    data = weixin_data
    ar = re.findall(r'{&quot;title&quot;:&quot;(.*?)&quot;,&quot;digest&quot;:&quot;',data)
    innertitle = ar
    title = []
    for ti in innertitle:
        ti = ti.replace('&nbsp;','')
        title.append(ti)
    return title

def main():
    get_proxy()
    check_proxy()
    data_str = get_content_from_url()
    # 如果长时间不能获得有效ip,去除下面那一行的注释,用本机ip......
#    data_str = get_weixin_content("http://weixin.sogou.com/weixin?type=1&query=%E6%B5%99%E6%B1%9F%E6%97%85%E6%B8%B8&ie=utf8&_sug_=n&_sug_type_=")
    file_name = store_to_html(data_str)
#    urlink='http://mp.weixin.qq.com/profile?src=3&timestamp=1464597512&ver=1&signature=Tc58R6gWs7bU40Nufl15g2eoW9WQMjxcjMPsgf2T25ML4M22as2qs*rtCGIow2gDn7b1r*bkXpHWDmRAkFOdLQ=='
    urlink = get_gzh_url(file_name)
    weixin_data = get_weixin_content(urlink)
    title = get_title(weixin_data)

    # 试试
    for ti in title:
        print(ti)




if __name__ == '__main__':
        main()


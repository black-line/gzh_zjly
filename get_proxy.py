from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
import re
import threading
import os
import time

# get the proxy


def get_proxy():
    if not os.path.exists('proxy.txt'):
        f = open('proxy.txt', 'w')
        f.close()
    cur_time = time.time()
    file_time = os.path.getmtime('proxy.txt')

    if  int(abs(cur_time-file_time)) > 600 or os.path.getsize('proxy.txt') == 0:
        print('重新抓取待测IP')

        of = open('proxy.txt', 'w+')
        for page in range(1,4):

            # start
            url = 'http://www.xicidaili.com/nn/%d' % page
            if page==1:
                url = 'http://www.xicidaili.com/nn/'
            req = urllib.request.Request(url)

            # deal with headers
            ori_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
            }

            req = urllib.request.Request(url)

            # add headers to req
            for key, value in ori_headers.items():
                req.add_header(key, value)

            # deal with cookies
            cj = http.cookiejar.CookieJar()
            pro = urllib.request.HTTPCookieProcessor(cj)

            opener = urllib.request.build_opener(pro)

            proxyList = (
                '202.106.16.36:3128'
            )
            proxy = proxyList[0]
            proxy = urllib.request.ProxyHandler(proxies={'http': proxy})
        #    opener = urllib.request.build_opener(pro, proxy)
            opener = urllib.request.build_opener(pro)
            op = opener.open(req)

            data_bytes = op.read()
            data_str = bytes.decode(data_bytes)

            soup = BeautifulSoup(data_str, "html.parser")
            trs = soup.find('table', {"id":"ip_list"}).findAll('tr')

        #    for tr in trs[1:]:
            for tr in trs[1:]:

                tr = str(tr)
                tds = re.findall(r'<td>(.+)</td>',tr)
                ip = tds[0]
                port = tds[1]
                protocol = tds[2]
                if protocol == 'HTTP' or protocol == 'HTTPS':
                    of.write('%s=%s:%s\n' % (protocol, ip, port))
                    #print('%s://%s:%s' % (protocol, ip, port))
        of.close()
    return None


def check_proxy():
    if not os.path.exists('available.txt'):
        f = open('available.txt', 'w')
        f.close()
    cur_time = time.time()
    file_time = os.path.getmtime('available.txt')

    if  int(abs(cur_time-file_time)) > 600 or os.path.getsize('available.txt') == 0:
        print('重新检测IP可用性')

        inFile = open('proxy.txt', 'r')
        outFile = open('available.txt', 'w')
        url = 'http://www.lindenpat.com/search/detail/index?d=CN03819011@CN1675532A@20050928'
        lock = threading.Lock()


        def test():
            lock.acquire()
            line = inFile.readline().strip()
            lock.release()
            # if len(line) == 0: break
            if not line.find("=")==-1:
                (protocol, proxy) = line.split(sep='=',maxsplit=1)
            else:
                protocol='HTTP';proxy=0
            cookie = "PHPSESSID=5f7mbqghvk1kt5n9illa0nr175; kmsign=56023b6880039; KMUID=ezsEg1YCOzxg97EwAwUXAg=="
            try:
                proxy_support = urllib.request.ProxyHandler({protocol.lower():'://'.join(line.split('='))})
                opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
                urllib.request.install_opener(opener)
                request = urllib.request.Request(url)
                request.add_header("cookie",cookie)
                content = urllib.request.urlopen(request,timeout=4).read()
                if len(content) >= 1000:
                    lock.acquire()
                    print('add proxy', proxy)
                    outFile.write('%s\n' %proxy)
                    lock.release()
                else:pass
                    #print('出现验证码或IP被封杀')
            except Exception as error:pass
                #print(error)
        all_thread = []
        for i in range(400):
            t = threading.Thread(target=test)
            all_thread.append(t)
            t.start()

        for t in all_thread:
            t.join()

        inFile.close()
        outFile.close()


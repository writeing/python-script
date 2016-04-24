# -*- coding:utf-8 -*-

import sys
import json
import requests
import urllib
import time
from lxml import etree
import socket
socket.setdefaulttimeout(3)
page = '/%s'
pagenum = 1
baseUrl = 'http://ip84.com/gn'
checkUrl = "http://blog.csdn.net/u010650281/article/details/51219481"
def getHtml(url):
    html = requests.get(url).content    
    sou = etree.HTML(html)
    return sou
   
class showLog(object):
    def __init__(self,msg):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fileName = datetime.datetime.now().strftime('%Y-%m-%d')
        msg = time+':'+msg
        fileLog = open("douban"+fileName+'.log','a')
        fileLog.write(msg+'\n')
        fileLog.close()   

def downHtml(htmlUrl,fileName='index'):
    if htmlUrl == '':
        return False
    if fileName == 'index':
        t = time.gmtime()
        fileName = time.strftime('%Y-%m-%d',t)
        urllib.urlretrieve(htmlUrl,fileName+'.html')
    else:
        urllib.urlretrieve(htmlUrl,fileName+'.html')

def combi(IP):
    IPinfo = []
    # proxy_temp = {}
    for info in IP:
        proxy_host = "http://"+info['ipAdress']+":"+info['ipPort']
        proxy_temp = {"http":proxy_host}
        IPinfo.append(proxy_temp)
    return IPinfo
def checkIP(proxy):
    try:
        res = urllib.urlopen(checkUrl,proxies = proxy).read()
        sleep(2)
        # FF = open('IP.txt','a')
        # FF.write(res)
        # FF.close()
        # print res.encode('utf-8').decode('gbk')
    except Exception,e:
        print proxy
        print e
def main():
    IP = []
    for i in range(1,10):
        sou = getHtml(baseUrl+page %i)
        print baseUrl+page %i
        ipList = sou.xpath(u'//div[@class="left"]/table/tr')
        # print ipList
        for ipinfo in ipList:
            info = {}
            info['ipAdress'] =  ipinfo.getchildren()[0].text.encode('utf-8')
            info['ipPort'] = ipinfo.getchildren()[1].text.encode('utf-8')
            info['ipAgreen'] = ipinfo.getchildren()[4].text.encode('utf-8')
            IP.append(info)            
        # print IP
        del IP[0]        
        map(checkIP,combi(IP))
        # time.sleep(2)        
    # document = json.dumps(IP)
    
    # FF = open('IP.json','w')
    # FF.write(document)
    # FF.close()
if __name__ == '__main__':
    main()       
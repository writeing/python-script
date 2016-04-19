# -*- coding:utf-8 -*-

import re
import sys
import lxml
import requests
import urllib
import time
from lxml import etree,html
reload(sys)
sys.setdefaultencoding('utf-8')
serachUrl = "http://dict.baidu.com/s?wd=%s&ptype=english"

class showLog(object):
    def __init__(self,msg):
        filetime = str(time.localtime().tm_year)
        msg = filetime+':'+msg
        fileLog = open(filetime+'.log','a')
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

def getSource(urlText):    
    html = requests.get(urlText).content
    sou = etree.HTML(html)
    return sou



def main(key):
    sou = getSource(serachUrl %key)
    html = sou.xpath(u'//div[@id="simple_means-wrapper"]/div/div/p')  
    for data in html:
        print data.getchildren()[0].text,data.getchildren()[1].text.encode('gbk')        
        showLog(data.getchildren()[0].text)
if __name__ == '__main__':
    while True:        
        key = raw_input("input english word(end is '#'):")
        if key == '#':
            break
        main(key)
    raw_input("procedure end")
        
        
    
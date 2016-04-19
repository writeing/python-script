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


biqu1 = "http://www.biquge.tw"
biqu = "http://www.biquge.la"
dingdian = "http://www.23wx.com"

class showLog(object):
    def __init__(self,msg):
        filetime = time.strftime('%Y-%m-%d-%h',time.gmtime())
        msg = filetime+':'+msg
        fileLog = open(filetime+'.log','a')
        fileLog.write(msg)
        fileLog.close()

class wxcWarre(object):
    '"this is a shell, could down novel every website,only inout the link"'
    _FileHadle = ''
    _findPath = ''
    _filtpath = ''
    _titlePath = ''
    def downHtml(self,htmlUrl,fileName='index'):
        if htmlUrl == '':
            return False
        if fileName == 'index':
            t = time.gmtime()
            fileName = time.strftime('%Y-%m-%d',t)
            urllib.urlretrieve(htmlUrl,fileName+'.html')
        else:
            urllib.urlretrieve(htmlUrl,fileName+'.html')

    def getSource(self,urlText):
        html = requests.get(urlText).content
        sou = etree.HTML(html)
        return sou

    def regular(self,str):
        regyu = r'<br />'
        reg =  re.compile(regyu)
        context = re.sub(reg,'',str)              
        regyu = r'<br/>'
        reg =  re.compile(regyu)
        context = re.sub(reg,'',context)              
                
        
        return context
    def downnove(self,url): 
        try:                   
            html = requests.get(url).content
        except:
            html = urllib2.urlopen(url).read()
        context = self.regular(html)        
        sou = etree.HTML(context)
        context = sou.xpath(self._filtpath)
        print url+'\n'
#        print context
        return context[0].text
    
    def getNovelName(self,sou):       
        title = sou.xpath(self._titlePath)        
#        showLog(title)
        return title[0].text
    
    def getUrl(self,url,baseurl):        
        sou = self.getSource(url)
        list = sou.xpath(self._findPath)   
#        print list
        file = open(self.getNovelName(sou)+'.txt','a')
        for novel in list:
            title = novel.text
            context = self.downnove(baseurl+novel.attrib['href'])                                            
            time.sleep(1)            
            file.write(title+'\n'+context+'\n')
        file.close()
        
    def downNovelForLink(self,url):        
        baseUrl = url[:url.find('/',7)]
        discern = baseUrl.replace('.com','')
        print discern
        if discern == biqu or discern == biqu1: 
            self._titlePath = u'//div[@id="info"]/h1'
            self._filtpath = u'//div[@id="content"]'
            self._findPath = u'//div[@id="list"]/dl/dd/a'
            self.getUrl(url,baseUrl)
        if baseUrl == dingdian:
            self._findPath = u'//table[@id="at"]/tr/td/a'
            self._filtpath = u'//dd[@id="contents"]'            
            self._titlePath = u'//div[@class="bdsub"]/dl/dd/h1'
            self.getUrl(url,url)

    def getIndexUrl(self,serach,name):
        sou = self.getSource(serach)
        url = sou.xpath(u'//a[@cpos="title"]')        
        for list in url:    
            print list.attrib['title'].encode('gbk')
            if list.attrib['title'].encode('gbk') == name:                
                print list.attrib['href']
                self.downNovelForLink(list.attrib['href'])
    def downNovelForName(self,name):
        urlcode = urllib.quote(name)
        urlSerach = 'http://zhannei.baidu.com/cse/search?s=8353527289636145615&entry=1&ie=gbk&q=%s' %urlcode
        self.getIndexUrl(urlSerach,name)
        
if __name__ == '__main__':
    wxc = wxcWarre()
    name = raw_input('please input novel name:')
    urlcode = urllib.quote(name)
    urlSerach = 'http://zhannei.baidu.com/cse/search?s=8353527289636145615&entry=1&ie=gbk&q=%s' %urlcode
    wxc.getIndexUrl(urlSerach,name)
#    wxc.downNovel(str(sys.argv[1]))
#    wxc.downHtml(str(sys.argv[1]),'dd')
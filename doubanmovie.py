# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re
import sys
import lxml
import requests
import time
import datetime
import random
import json
import login
from lxml import etree,html
reload(sys)
sys.setdefaultencoding('utf-8')

urlRoot = 'https://movie.douban.com/tag/'

loadUrl = 'https://movie.douban.com/tag/%s'

serachUrl = ""
opener = ""
currentName = ''
my_userAgent=[
    "Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"]

class showLog(object):        
    info = []
    nameMovie = []
    def __init__(self):
        print "create showLog"
        
    def showlog(self,msginfo):
        fileName = datetime.datetime.now().strftime('%Y-%m-%d')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msginfo = time+':'+msginfo
        fileLog = open("douban"+fileName+'.log','a')
        fileLog.write(msginfo)
        fileLog.close()
		
    def saveasjson(self,msg):
        self.info.append(msg)
        # print self.info
    def curNameMovie(self):
        global currentName
        curMovie = {currentName:self.info}
        self.nameMovie.append(curMovie)
        curMovie = {}
        self.info = []
    def saveforName(self,name):            
            
            movieinfo = {"movie":self.nameMovie}
            fileLog = open(name+'.json','a')
            temp = json.dumps(movieinfo)
            fileLog.write(temp)
            fileLog.close()
            
show = showLog()        

def downHtml(htmlUrl,fileName='index'):
    if htmlUrl == '':
        return False
    if fileName == 'index':
        t = time.gmtime()
        fileName = time.strftime('%Y-%m-%d',t)
        urllib.urlretrieve(htmlUrl,fileName+'.html')
    else:
        urllib.urlretrieve(htmlUrl,fileName+'.html')

def cookieSave():
    global opener
    loginUrl = "https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/people/130969145/"
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode({
    			'stuid':'853976858@qq.com',
    			'pwd':'wang853976858'
    		})
    result = opener.open(loginUrl,postdata)

    cookie.save(ignore_discard=True, ignore_expires=True)
    result = opener.open(gradeUrl)
def getSource(urlText):
    global opener
    global my_userAgent
    content = opener.open(urlText).read()
    sou = etree.HTML(content)
    return sou
def checkgrade(grade,people):
    print float(grade)
    pat = '(\d+)'
    reg = re.compile(pat)   
    print people
    if float(grade) >= 8.0:       
        people = re.findall(reg,people)[0]
        if int(people) > 100000:
            return True
    return False
        
def loadMovie(url):
    global show
    global serachUrl
    print url
    sou = getSource(url)
    if int(sou.xpath(u'//span[@class="thispage"]')[0].text) == 50:
        return    
    movielist = sou.xpath(u'//td[@valign="top"]/div[@class="pl2"]')
    for movie in movielist:
        try:            
            moviedict = {}
            moviedict['link'] = movie.getchildren()[0].attrib['href']            
            moviedict['name'] = movie.getchildren()[0].text
            
            moviedict['name'] = ''.join(moviedict['name'].split()).replace('/','')
            
            moviedict['info'] = movie.getchildren()[2].text
            moviedict['grade'] = movie.getchildren()[3].getchildren()[1].text      
            people = movie.getchildren()[3].getchildren()[2].text                     
        except:
            try:
                moviedict = {}
                moviedict['link'] = movie.getchildren()[0].attrib['href']            
                moviedict['name'] = movie.getchildren()[0].text
                moviedict['name'] = ''.join(moviedict['name'].split()).replace('/','')
                moviedict['info'] = movie.getchildren()[1].text
                moviedict['grade'] = movie.getchildren()[2].getchildren()[1].text      
                people = movie.getchildren()[2].getchildren()[2].text
            except:
                print "this is error"   
        try:
            print moviedict['name']
            if checkgrade(moviedict['grade'],people):             
                show.showlog('\n'+moviedict['name'].encode('utf-8')+"\n"+moviedict['info']+"\n"+moviedict['grade']+"\n"+moviedict['link']+"\n")
                show.saveasjson(moviedict)       
        except:
            print url.encode('utf-8') + 'error'
                  
    try:
        time.sleep(5)  
        loadMovie(sou.xpath(u'//span[@class="next"]/a')[0].attrib['href'])        
    except:
        return        
def begin():
    global loadUrl
    global serachUrl    
    i= 0
    proNum = 0
    try:
        proFile = open('config.ini','r')
        proNum = int(proFile.read())
        proFile.close()                
    except:
        print "this is a new thread"
    sou = getSource(urlRoot)
    movieCate = sou.xpath(u'//table[@class="tagCol"]/tbody/tr/td/a')
    for name in movieCate:
        global currentName
#        print name.text            
        serachUrl = loadUrl %name.text        
        if name.text == u'美国':
            break        
        else:
            print name.text
        i = i+1 
        if i < proNum:   
            continue
        nowNum = open('config.ini','w')
        nowNum.write(str(i))
        nowNum.close()                            
        loadMovie(serachUrl)
        currentName = name.text
        show.curNameMovie()
    show.saveforName('movie')                
        
def loginSite():
    global opener
    login.loginurl = "https://accounts.douban.com/login"
    douban = login.Login()
    username = "853976858@qq.com"
    password = "wang853976858"
    douban.setLoginInfo(username,password)
    opener = douban.login()
    
if __name__ == '__main__':
    loginSite()
    begin()
    print "the end"

# -*- coding: UTF-8 -*-
string = '中文'
'''#string.decode('gb2313').encode('utf-8')
'''

import urllib2
import urllib
import time
import socket 
import sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
sys.setdefaultencoding( "utf-8" )


timeout = 35
socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置  
sleep_download_time = 2
time.sleep(sleep_download_time) #这里时间自己设定  

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Referer': 'http://www.zngirls.com/'} 

name = raw_input('please input a name :')
name = name.decode('gbk')
fname = name
first_url = 'http://www.zngirls.com/girl/search.aspx?name=' + name
print first_url
first_req = urllib2.Request(url = first_url,headers = headers)
first_code = urllib2.urlopen(first_req).read()
b = first_code.find("target='_blank' href='")
str2 = first_code[b+len("target='_blank' href='"):b+len("target='_blank' href='")+12]
url2 = 'http://www.zngirls.com'+str2
req2=urllib2.Request(url=url2,headers=headers)
data2=urllib2.urlopen(req2)

#找到这个人的页面
homepape_url = url2
homepape_req = urllib2.Request(url=homepape_url, headers=headers)
homepape_code = urllib2.urlopen(homepape_req).read()


#找到有这个人多少个专辑
str3 = "class='title'>共"
foralbum = homepape_code.find(str3)
foralbumlen = len(str3)
album = homepape_code[foralbum + foralbumlen:foralbum + foralbumlen+2]
print album

#进入列出所有专辑的页面,上面的连接最多只有6个，有一些要点开下面连接才显示
homepape_url = url2 + 'album/'
homepape_req = urllib2.Request(url=homepape_url, headers=headers)
homepape_code = urllib2.urlopen(homepape_req).read()


#找到这些专辑的超链接
album_save = []
str1 = "<a class='igalleryli_link' href='"
i = 0
while i < len(homepape_code)-42:
    if homepape_code[i:i+33] == str1:
        album_url = "http://www.zngirls.com" + homepape_code[i+33:i+42]
        album_save.append(album_url)
        if len(album_save) == album :
            break
    i = i + 1

for eachalbum in album_save:
    print eachalbum 



 

#对某一个专辑开始爬
for eachalbum in album_save:
    req = urllib2.Request(url=eachalbum, headers=headers)
    code = urllib2.urlopen(req).read()  

#该专辑的照片数目w
    head = code.find('#DB0909')
    tail = code.find('张照片')
    print '该专辑照片数目',code[head+9:tail]
    w = int(code[head+9:tail])

    i = 0

    #print code
#picurl 为该上层页面点进一张图片后的大图页面
    ch = code.find('''<ul id="hgallery"><img src=''')
    #print len('''<ul id="hgallery"><img src=''')
    if code[ch+35:ch+38] == 't1.':
        picurl = "http://www.zngirls.com/img.html?img=" + code[ch+28:ch+70]
    else:
        picurl = "http://www.zngirls.com/img.html?img=" + code[ch+28:ch+71]
    print picurl
    while i < w:
        if i >= 10:
            q = '0' + str(i)
        elif i == 0:
            q = '0'
        else:
            q = '00' + str(i)
        url = picurl  + q + '.jpg'
        #print "url:",url

#获取src地址
        req2 = urllib2.Request(url=url, headers=headers)
        code2 = urllib2.urlopen(req2).read()
        head2 = code2.find("<img src='")
        tail2 = code2.find(".jpg'/>")
        furl = code2[head2+10:tail2+4]
        print "furl:",furl
        #urllib2.urlopen(req2).close()

        
        req3 = urllib2.Request(url = furl,headers = headers)
        code3 = urllib2.urlopen(req3).read()
        #urllib2.urlopen(req3).close()
        name = "test\\" + eachalbum[-6:-1] + '_' + str(i)+'.jpg'
        f = open(name,'wb')
        f.write(code3)
        f.close()
    #urllib.urlretrieve(furl,"pic\\b"+str(i) + ".jpg")

        i = i + 1
        time.sleep(sleep_download_time)
        #time.sleep(1)
    print '------------------------------------------------------------'


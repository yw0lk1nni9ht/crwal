#-*- coding: UTF-8 -*-
import sys
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr
reload(sys)
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
sys.setdefaultencoding( "utf-8" )
import urllib2
import scrapy
from second.items import SecondItem
class DmozSpider(scrapy.spiders.Spider):
    def addalbum():
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
        'Referer': 'http://www.zngirls.com/'}
        name = raw_input('please input a name :')
        name = name.decode('gbk')
        first_url = 'http://www.zngirls.com/girl/search.aspx?name=' + name
        first_req = urllib2.Request(url = first_url,headers = headers)
        first_code = urllib2.urlopen(first_req).read()
        b = first_code.find("target='_blank' href='")
        str2 = first_code[b+len("target='_blank' href='"):b+len("target='_blank' href='")+12]
        url2 = 'http://www.zngirls.com'+str2
        req2=urllib2.Request(url=url2,headers=headers)
        data2=urllib2.urlopen(req2)

        homepape_url = url2
        homepape_req = urllib2.Request(url=homepape_url, headers=headers)
        homepape_code = urllib2.urlopen(homepape_req).read()

        str3 = "class='title'>共"
        foralbum = homepape_code.find(str3)
        foralbumlen = len(str3)
        album = homepape_code[foralbum + foralbumlen:foralbum + foralbumlen+2]

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
        print album_save
        return album_save

    name = "try"
    allowed_domains = ["zngirls.com"]
    a = []
    a = addalbum()
    start_urls = a

    def parse(self, response):
        item = SecondItem()
        for sel in response.xpath('//ul[@id="hgallery"]//img'):
            item['image_urls'] = sel.xpath('.//@src').extract()
            yield item
        np = u'下一页'
        url = response.xpath("//a[contains(text(),'%s')]/@href"%(np))
        print url.extract()
        print url.extract()[0]
        if url :
            page = 'http://www.zngirls.com' + url.extract()[0]
            yield scrapy.Request(page,callback=self.parse)

    

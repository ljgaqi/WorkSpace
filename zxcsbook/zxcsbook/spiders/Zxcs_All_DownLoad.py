'''
知轩藏书网站的整站抓取爬虫
使用的框架：scrapy
作者：liaqi@163.com
完成时间：2020-12-02
需要了解的知识点：1.LinkExtractor的使用方法，特别是初始化中的几个重要参数，restrict_xpaths，deny，allow等
              2.re的基础知识，如何在一个字符串中进行对比，提取出需要的字符串
              3.scrapy的基础知识，pipelines中的file_path，get_media_requests，item_completed方法的重写。
                settings文件的设定，
运行程序的命令：scrapy crawl Zxcs_All_DownLoad -o book.csv -s OFF_FILE=scrapy.log
运行程序的结果：将所有书籍的信息保存在book.csv中，书籍的压缩包下载到BOOK目录下。控制台输出信息放在scrapy.log中保存
'''
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from zxcsbook.items import ZxcsbookItem
class ZxcsAllDownloadSpider(scrapy.Spider):
    name = 'Zxcs_All_DownLoad'                      #设置爬虫名称
    #allowed_domains = ['www.zxcs.me']
    #start_urls = ['http://www.zxcs.me/map.html/']   #设置爬虫开始页面
    #设置了一组网址，将zxcs中的每一个分类的网址都添加了进去
    start_urls = ['http://www.zxcs.me/sort/23/',
                  'http://www.zxcs.me/sort/25/',
                  'http://www.zxcs.me/sort/26/',
                  'http://www.zxcs.me/sort/27/',
                  'http://www.zxcs.me/sort/28/',
                  'http://www.zxcs.me/sort/29/',
                  'http://www.zxcs.me/sort/36/',
                  'http://www.zxcs.me/sort/37/',
                  'http://www.zxcs.me/sort/38/',
                  'http://www.zxcs.me/sort/39/',
                  'http://www.zxcs.me/sort/40/',
                  'http://www.zxcs.me/sort/41/',
                  'http://www.zxcs.me/sort/42/',
                  'http://www.zxcs.me/sort/43/',
                  'http://www.zxcs.me/sort/44/',
                  'http://www.zxcs.me/sort/45/',
                  'http://www.zxcs.me/sort/55/']
    #爬取方法，将分类页面中的每一本书的链接用linkExtractor提取出来，放入parse_page中进行详细信息抓取。
    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//*[@id="plist"]/dt/a')     #对一个LinkExtractor对象进行初始化
        links = le.extract_links(response)
        for link in links:                                              #对每一个链接进行循环，将网址放入到下一个抓取方法中
            yield scrapy.Request(link.url, callback=self.parse_page)
        #为了抓取页面中的下一页链接，利用re对页面进行对比，将特定字符中包含的网址提取出来
        next_temp = response.xpath('//*[@id="pagenavi"]').extract_first()
        next_page_patten = re.compile('</span>  <a href="(.+?)">')
        next_page = next_page_patten.findall(next_temp)
        if next_page:
        #因为提取出来的next_page是一个list，所以在传递参数时，需要提取list里面包含的网址字符，并指定encoding
            yield scrapy.Request(next_page[0],callback=self.parse,encoding='utf-8')
        #parse_page方法是对书籍详情页面的信息进行抓取，并提取出书籍下载链接，传入parse_down进行解析。
    def parse_page(self, response):
        item = ZxcsbookItem()                                   #初始化一个bookitem对象，将抓取的信息保存进去
        item['book_url'] = response.url
        #用re模块对提取出来的text进行解析，提取出书名和作者名，分别储存。
        bookname = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/text()').extract_first()
        patten = re.compile('《(.+)》')
        item['book_name'] = patten.findall(bookname)
        item['book_author'] = bookname.split("：")[-1]
        item['book_downurl'] = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/@href').extract_first()
        #提取出书籍下载页面，传入parse_download进行进一步解析，并将item作为meta参数也传入parse_download中，进一步完善。
        yield scrapy.Request(item['book_downurl'], meta={'item': item}, callback=self.parse_download)
        #parse_download是将书籍下载页面进行解析，提取出书籍文件的链接，进行保存下载。
    def parse_download(self, response):
        item = response.meta['item']
        item['file_urls'] = [response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/span[1]/a/@href').extract_first()]
        yield item


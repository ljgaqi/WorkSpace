import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from zxcs.items import ZxcsItem

class ZxbookSpider(scrapy.Spider):
    name = 'zxbook'
    start_urls = ['http://www.zxcs.info/sort/3/',
                  'http://www.zxcs.info/sort/4/',
                  'http://www.zxcs.info/sort/8/',
                  'http://www.zxcs.info/sort/11/',
                  'http://www.zxcs.info/sort/14/',
                  'http://www.zxcs.info/sort/17/',
                  'http://www.zxcs.info/sort/20/',]

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//*[@id="plist"]/dt/a')  # 对一个LinkExtractor对象进行初始化
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_page)

        next_temp = response.xpath('//*[@id="pagenavi"]').extract_first()
        next_page_patten = re.compile('</span>  <a href="(.+?)">')
        next_page = next_page_patten.findall(next_temp)
        if next_page:
            scrapy.Request(next_page[0],callback=self.parse,encoding='utf-8')

    def parse_page(self, response):
        item = ZxcsItem()
        item['book_url'] = response.url
        item['book_sn'] = int(response.url.split("/")[-1])
        item['book_class']=response.xpath('//*[@id="ptop"]/a[2]/text()').extract_first()

        bookname = response.xpath('//*[@id="content"]/h1/text()').extract_first()
        patten = re.compile('《(.+)》')
        item['book_name'] = patten.search(bookname).group(1)
        patten_author=re.compile('作者: (.*?)</a>')
        item['book_author'] = patten_author.search(response.text).group(1)

        down_url = response.xpath('//*[@id="content"]/div[2]/div[3]/div[2]/p[1]/a/@href').extract_first()
        item['book_down_url']='http://www.zxcs.info'+down_url
        yield scrapy.Request(item['book_down_url'], meta={'item': item}, callback=self.parse_download)

    def parse_download(self, response):
        item = response.meta['item']
        item['file_urls'] = [response.xpath('/html/body/div[2]/div[4]/div[3]/span/a/@href').extract_first()]
        yield item
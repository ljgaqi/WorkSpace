import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from zxcsbook.items import ZxcsbookItem



class BookSpider(scrapy.Spider):
    name = 'book'
    # allowed_domains = ['http://www.zxcs.me/sort/23']
    start_urls = ['http://www.zxcs.me/sort/23/']

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//*[@id="plist"]/dt/a')
        links=le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_page)

    def parse_page(self, response):
        item=ZxcsbookItem()
        item['book_url']=response.url
        bookname=response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/text()').extract_first()
        patten=re.compile('《(.+)》')
        item['book_name']=patten.findall(bookname)
        item['book_downurl']=response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/@href').extract_first()
        yield scrapy.Request(item['book_downurl'],meta={'item':item},callback=self.parse_down)

    def parse_down(self,response):
        item=response.meta['item']
        item['file_url']=response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/span[1]/a/@href').extract_first()
        yield item





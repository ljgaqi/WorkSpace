import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from zxcsbook.items import ZxcsbookItem



class BookSpider(scrapy.Spider):
    name = 'book'
    # allowed_domains = ['http://www.zxcs.me/sort/23']
    #都市.娱乐：http://www.zxcs.me/sort/23
    #奇幻.玄幻：http://www.zxcs.me/sort/26
    start_urls = ['http://www.zxcs.me/sort/26/']
    page=2
    next_page=start_urls[0]+'page/'
    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//*[@id="plist"]/dt/a')
        links=le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_page)

        # if self.page<93:
        #     next_url=self.next_page+str(self.page)
        #     self.page+=1
        #     yield scrapy.Request(next_url,callback=self.parse)

    def parse_page(self, response):
        item=ZxcsbookItem()
        item['book_url']=response.url
        bookname=response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/text()').extract_first()
        patten=re.compile('《(.+)》')
        item['book_name']=patten.findall(bookname)
        item['book_author']=bookname.split("：")[-1]
        item['book_downurl']=response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/@href').extract_first()
        yield scrapy.Request(item['book_downurl'],meta={'item':item},callback=self.parse_down)

    def parse_down(self,response):
        item=response.meta['item']
        item['file_urls']=[response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/span[1]/a/@href').extract_first()]
        yield item

import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from zxcsbook.items import ZxcsbookItem


class ZxcsAllDownloadSpider(scrapy.Spider):
    name = 'Zxcs_All_DownLoad'                      #设置爬虫名称
    #allowed_domains = ['www.zxcs.me']
    #start_urls = ['http://www.zxcs.me/map.html/']   #设置爬虫开始页面
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

    def parse(self, response):
        le = LinkExtractor(restrict_xpaths='//*[@id="plist"]/dt/a')
        links = le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url, callback=self.parse_page)

        next_temp = response.xpath('//*[@id="pagenavi"]').extract_first()
        next_page_patten = re.compile('</span>  <a href="(.+?)">')
        next_page = next_page_patten.findall(next_temp)
        if next_page:
            print('************************************')
            print(next_page)
            print('开始抓取下一页')
            print('************************************')
            yield scrapy.Request(next_page[0],callback=self.parse,encoding='utf-8')

    def parse_page(self, response):
        item = ZxcsbookItem()
        item['book_url'] = response.url
        bookname = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/text()').extract_first()
        patten = re.compile('《(.+)》')
        item['book_name'] = patten.findall(bookname)
        item['book_author'] = bookname.split("：")[-1]
        item['book_downurl'] = response.xpath('//*[@id="content"]/div[2]/div[2]/p[1]/a/@href').extract_first()
        yield scrapy.Request(item['book_downurl'], meta={'item': item}, callback=self.parse_download)

    def parse_download(self, response):
        item = response.meta['item']
        item['file_urls'] = [response.xpath('/html/body/div[2]/div[2]/div[3]/div[2]/span[1]/a/@href').extract_first()]
        yield item


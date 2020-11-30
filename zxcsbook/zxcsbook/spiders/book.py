import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['http://www.zxcs.me/sort/23']
    start_urls = ['http://www.zxcs.me/sort/23/']

    def parse(self, response):
        pass

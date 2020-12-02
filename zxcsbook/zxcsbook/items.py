# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZxcsbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name=scrapy.Field()        #书名
    book_author=scrapy.Field()      #作者名
    book_url=scrapy.Field()         #书籍详情页
    book_downurl=scrapy.Field()     #书籍下载页
    file_urls=scrapy.Field()        #书籍下载地址


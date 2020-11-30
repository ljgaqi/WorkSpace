# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZxcsbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name=scrapy.Field()
    book_url=scrapy.Field()
    book_downurl=scrapy.Field()
    file_urls=scrapy.Field()


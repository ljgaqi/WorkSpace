import scrapy
import re
import math
import random
from scrapy.linkextractors import LinkExtractor
from javbus.items import JavbusItem


class JavbusDownSpider(scrapy.Spider):
    name = 'javbus_down'
    # allowed_domains = ['https://www.fanbus.in/']
    start_urls = ['https://www.fanbus.in']

    def parse(self, response):
        le=LinkExtractor(restrict_xpaths='//*[@id="waterfall"]')
        links=le.extract_links(response)
        for link in links:
            yield scrapy.Request(link.url,callback=self.parse_info)

        next_url = response.xpath('//*[@id="next"]/@href').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_info(self,response):
        item=JavbusItem()
        item['jav_id']=response.xpath('//*[@class="col-md-3 info"]/p/span/text()').extract()[1]
        item['jav_time']=response.xpath('//*[@class="col-md-3 info"]/p/text()').extract()[3]
        item['jav_update']=response.xpath('//*[@class="col-md-3 info"]/p/text()').extract()[2]
        item['jav_url']=response.url
        item['image_urls']=response.xpath('//*[@class="bigImage"]/@href').extract()

        meg_patten=response.xpath('/html/body/script[3]').extract_first()
        gid_patten=re.compile('gid = (.*?);')
        uc_patten=re.compile('uc = (.*?);')
        img_patten=re.compile("img = '(.*?)';")
        gid=gid_patten.findall(meg_patten)[0]
        uc=uc_patten.findall(meg_patten)[0]
        img=img_patten.findall(meg_patten)[0]
        magnet_url="https://www.fanbus.in/ajax/uncledatoolsbyajax.php?gid=" \
                   "{}&lang=zh&img={}&uc=0&floor={}".format(gid,img,math.floor(random.random()*1000+1))
        yield scrapy.Request(magnet_url,meta={'item':item},callback=self.parse_magnet)

    def parse_magnet(self,response):
        item = response.meta.get("item")
        elements = response.xpath("//tr")
        info = []
        if len(elements)>=1:
            for i in range(len(elements)):
                sourceInfo = {}
                #磁力链接
                mangetUrl = elements[i].xpath("td[1]/a/@href").extract_first()
                sourceInfo["magnetUrl"] = mangetUrl
                # #番号
                # fanhao = elements[i].xpath("td[1]/a/text()").extract_first().strip() if elements[i].xpath("td[1]/a/text()").extract_first() else ""
                # sourceInfo["fanao"] = fanhao

                #视频大小
                size = elements[i].xpath("td[2]/a/text()").extract_first().strip() if  elements[i].xpath("td[2]/a/text()").extract_first() else ""
                sourceInfo["size"] = size
                # #时间
                # openTime = elements[i].xpath("td[3]/a/text()").extract_first().strip() if elements[i].xpath("td[3]/a/text()").extract_first() else ""
                # sourceInfo["openTime"] = openTime
                info.append(sourceInfo)
        item["jav_magnet"] = info
        yield item




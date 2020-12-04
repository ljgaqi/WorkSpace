# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import os
from javbus.settings import IMAGES_STORE

class JavbusPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)
    def item_completed(self, results, item, info):
        image_paths=[x['path']for ok,x in results if ok]
        newname=item['jav_id']+'.jpg'
        print(image_paths)
        print(newname)
        filepath=IMAGES_STORE
        os.rename(filepath+'/'+image_paths[0],filepath+'/'+newname)
        return item

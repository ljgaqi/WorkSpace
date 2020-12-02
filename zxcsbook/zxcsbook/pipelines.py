# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename,dirname,join
import scrapy
from zxcsbook.zxcsbook.settings import FILES_STORE
import os

class ZxcsbookPipeline(FilesPipeline):
    def process_item(self, item, spider):
        return item
    #以url的最后几个网址作为目录名和文件名保存
    # def file_path(self, request, response=None, info=None):
    #     path=urlparse(request.url).path
    #     return join(basename(dirname(path)),basename(path))
'''以书名-作者名的格式将下载的文件保存在预设的目录下'''
    # def get_media_requests(self, item, info):
    #     for file_url in item['file_urls']:
    #         yield scrapy.Request(file_url)
    #
    # def item_completed(self, results, item, info):
    #     file_paths=[x['path']for ok,x in results if ok]
    #     newname=item['book_name'][0]+'-'+item['book_author']+'.rar'
    #     print(file_paths)
    #     print(newname)
    #     filepath=FILES_STORE
    #     os.rename(filepath+'/'+file_paths[0],filepath+'/'+newname)
    #     return item
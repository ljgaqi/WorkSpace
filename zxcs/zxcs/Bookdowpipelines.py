from scrapy.pipelines.files import FilesPipeline
import scrapy

class Bookdowpipelines(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        file=request.meta.get('filename','')
        filename=file
        return filename

    def get_media_requests(self, item, info):
        file_url=item['file_urls']
        book_name=item['book_name']
        book_author=item['book_author']
        filename=book_name+'-'+book_author
        meta = {'filename': filename}
        yield scrapy.Request(url=file_url[0], meta=meta)
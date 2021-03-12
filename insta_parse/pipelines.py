

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class InstaParsePipeline:

    def __init__(self):
        client = MongoClient()
        self.db = client["gb_parse_16_02_2021"]

    def process_item(self, item, spider):
        self.db[type(item).__name__].insert_one(item)
        return item


class GbImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get("photos", []):
            yield Request(url)
        image = item["data"].get("profile_pic_url") or item["data"].get("display_url")
        if image:
            yield Request(image)

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results]
        return item

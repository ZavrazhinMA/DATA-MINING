# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstaParsePipeline:

    def __init__(self):
        client = MongoClient()
        self.db = client["parse_insta_followers"]

    def process_item(self, item, spider):
        collection = f'{type(item).__name__}_{item["main"]}'
        self.db[collection].insert_one(item)
        return item

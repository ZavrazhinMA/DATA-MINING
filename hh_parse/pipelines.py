from pymongo import MongoClient


class HhParsePipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client["parse_hh_db"]

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item

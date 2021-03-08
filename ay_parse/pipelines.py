from pymongo import MongoClient


class AyParsePipeline:
    def process_item(self, item, spider):
        return item


class ParseMongoPipeline:
    def __init__(self):
        client = MongoClient()
        self.db = client["parse_youla_db"]

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item

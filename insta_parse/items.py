# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy


class InstaParseItem(scrapy.Item):
    _id = scrapy.Field()
    date_parse = scrapy.Field()
    data = scrapy.Field()
    photos = scrapy.Field()


class InstaTag(InstaParseItem):
    pass


class InstaPost(InstaParseItem):
    pass

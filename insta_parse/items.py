# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaParseItem(scrapy.Item):
    _id = scrapy.Field()
    date = scrapy.Field()
    data = scrapy.Field()
    main = scrapy.Field()
    flw_status = scrapy.Field()


class MainUser(InstaParseItem):
    pass




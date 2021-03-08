# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AyParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GbAutoYoulaItem(scrapy.Item):
    _id = scrapy.Field()
    car_model = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    characteristics = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()

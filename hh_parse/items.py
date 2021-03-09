# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HhParseItem(scrapy.Item):
    _id = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    key_skills = scrapy.Field()
    employer_url = scrapy.Field()
    employer_name = scrapy.Field()
    employer_description = scrapy.Field()
    employer_website = scrapy.Field()
    business_segments = scrapy.Field()

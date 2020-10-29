# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FinderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HumanInfo(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    patronymic = scrapy.Field()
    city = scrapy.Field()
    place = scrapy.Field()
    comments = scrapy.Field()


class ListInfo(scrapy.Item):
    origin = scrapy.Field()
    date = scrapy.Field()
    items = scrapy.Field()

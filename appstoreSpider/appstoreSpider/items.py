# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppItem(scrapy.Item):
    rank = scrapy.Field() # app 排名
    name = scrapy.Field() # app 名
    url = scrapy.Field()  # app URL
    size = scrapy.Field() # app 大小
    pass

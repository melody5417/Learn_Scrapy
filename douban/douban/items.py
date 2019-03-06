# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# 定义item数据结构

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    serial_number = scrapy.Field()

    movie_name  = scrapy.Field()

    introduce = scrapy.Field()

    star = scrapy.Field()

    evalutate = scrapy.Field()

    describe = scrapy.Field()

    pass

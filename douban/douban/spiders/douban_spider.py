# -*- coding: utf-8 -*-
import scrapy


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        pass

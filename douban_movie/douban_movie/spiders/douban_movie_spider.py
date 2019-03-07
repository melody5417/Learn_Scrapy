# -*- coding: utf-8 -*-
import scrapy


class DoubanMovieSpiderSpider(scrapy.Spider):
    name = 'douban_movie_spider'
    allowed_domains = ['https://movie.douban.com/top250?start=25&filter=']
    start_urls = ['http://https://movie.douban.com/top250?start=25&filter=/']

    def parse(self, response):
        pass

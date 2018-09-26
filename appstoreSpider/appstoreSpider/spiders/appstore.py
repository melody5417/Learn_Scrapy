# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import AppItem

class AppstoreSpider(scrapy.Spider):
    name = 'appstore'
    allowed_domains = ['apple.com', 'itunes.apple.com']
    start_urls = ['https://www.apple.com/cn/itunes/charts/free-apps/']

    def parse(self, response):
        le = LinkExtractor(restrict_css='#main > section > ul > li')
        count = len(le.extract_links(response))
        self.logger.info('parse length = %s', count)

        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_appItem)

    # app页面的解析函数
    def parse_appItem(self, response):
        appItem = AppItem()
        # appItem['rank'] = response.css()

        appItem['url'] = response.url
        appItem['name'] = response.css('section div h1::text').extract_first()
        if not appItem['name'] is None:
            appItem['name'] = appItem['name'].strip()
        appItem['size'] = response.css('section dl >div:nth-child(2) dd::text').extract_first()
        yield appItem

# encoding: utf-8
import scrapy
from ..items import BookItem
from scrapy.linkextractors import LinkExtractor

class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    name = "books" # 在一个项目中不能有同名的
    
    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    start_urls = ['http://books.toscrape.com/']
    
    # 当一个页面下载完成后，Scrapy引擎会回调一个我们指定的页面解析函数，默认为parse方法解析页面。
    # 通常需要完成两个任务：1 提取页面中的数据，用Xpath或css选择器
    # 2 提取页面中的链接，并产生对链接页面的下载请求。
    # parse通常被实现成一个生成器函数，每一项从页面中提取的数据以及每一个
    # 对链接页面的下载请求都由 yield 语句提交给scrapy引擎。
    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的article元素，并依次迭代
        for sel in response.css('article.product_pod'):
            book = BookItem()

            # 书名信息在article-> h3 -> a元素的title属性里
            book['name'] = sel.xpath('./h3/a/@title').extract_first()
            
            # 书价信息在 <p class="price_color">的Text中。
            book['price'] = sel.css('p.price_color::text').extract_first()
            
            yield book
            
            # # 1. Selector 提取链接
            # # 下一页的url在ul.pager -> li.next -> a里面
            # next_url = response.css('ul.paper li.next a::attr(href)').extract_first()
            # if next_url:
            #     # 如果找到下一页的URL，得到绝对路径，构造新的Request对象
            #     next_url = response.urljoin(next_url)
            #     yield scrapy.Request(next_url, callback=self.parse)
            
            # 2. LinkExtractor 提取链接
            le = LinkExtractor(restrict_css='ul.pager li.next')
            links = le.extract_links(response)
            if links:
                next_url = links[0].url
                yield scrapy.Request(next_url, callback=self.parse)

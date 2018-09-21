from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor

html1 = open('example1.html').read()
response1 = HtmlResponse(url='http://example1.com', body=html1, encoding='utf8')
le = LinkExtractor()
links = le.extract_links(response1)
print([link.url for link in links])

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class PriceConverterPipeline(object):
    # 英镑兑换人民币汇率
    exchange_rate = 8.5309
    
    # 一个Item Pipeline不需要继承特定基类，只需要实现某些特定方法。
    # 1 如果process_item在处理某项item时返回一项数据（item或字典）
    #   返回的数据回传递给下一级pipeline继续处理
    # 2 如果在处理某项item时抛出一个DropItem异常，该项item便会被抛弃
    #   不再递送给后面的ItemPipeline继续处理，也不会再导出到文件
    def process_item(self, item, spider):
        # 提取item的price字段
        # 去掉前面英镑符号，转换为float类型，乘以汇率
        price = float(item['price'][1:])*self.exchange_rate
        
        # 保留2位小数，赋值回item的price字段
        item['price'] = '¥%.2f' % price
        return item

    # Spider打开时 处理数据前 回调该方法 通常用于处理某些初始化工作，如链接数据库
    def open_spider(self, spider):
        print()

    # Spider关闭时，处理数据后，回调该方法 通常用于某些清理工作 如关闭数据库
    def close_spider(self, spider):
        print()

    # 创建pipeline对象时回调该方法 通常 在该方法中通过settings读取配置
    # 根据配置创建pipeline对象
    # def from_crawler(cls, crawler):
    #     print()



class DuplicatesPipeline(object):

    # 增加构造器方法，初始化用于对书名去重的集合
    def __init__(self):
        self.book_set = set()

    # 去重
    def process_item(self, item, spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem('Duplicate book found: %s' %item)
        self.book_set.add(name)
        return item



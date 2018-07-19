#encoding:utf-8
'''运行对应爬虫'''
from scrapy.cmdline import execute
execute("scrapy crawl article".split())
# execute("scrapy crawl comment".split())
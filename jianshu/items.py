# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#用户表
class UserItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()

#文章表
class ArticleItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    auth = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    in_time = scrapy.Field()

class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    content = scrapy.Field()
    time = scrapy.Field()
    id = scrapy.Field()
    article = scrapy.Field()
    user_slug = scrapy.Field()
    title = scrapy.Field()
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import jianshu.settings as settings
from .items import UserItem
from .items import ArticleItem

class JianshuPipeline(object):
    def process_item(self, item, spider):
        return item


class Article(object):
    
    
    def process_item(self, item, spider):
        
        try:
            db = pymysql.connect( settings.MYSQL_HOST,settings.MYSQL_USER,settings.MYSQL_PASSWORD,settings.MYSQL_DBNAME, charset='utf8mb4' )
            cursor = db.cursor()
            # sql = "INSERT INTO article ( title, url, content, time, in_time) VALUES ('%s', '%s', '%s', '%d', '%d')"%(item['title'],item['url'],item['content'],item['time'],item['in_time'])
            # sql = "INSERT INTO article ( title, auth, url, content, time, in_time) VALUES ('%s','%s', '%s', '%s', '%d', '%d') where not exists (select * from article where url = '%s');"
            sql = "INSERT INTO article (`title`,`auth`,`url`,`content`,`time`,`in_time`) SELECT	'%s','%s', '%s', '%s', '%d', '%d' FROM DUAL WHERE NOT EXISTS ( SELECT url FROM article WHERE url = '%s')"
            cursor.execute(sql % (pymysql.escape_string(item['title']), item['auth'], item['url'], pymysql.escape_string(item['content']), item['time'], item['in_time'],item['url']))
            # db.query(sql)
            db.commit()

        except Exception as e:
            print("插入数据出错")
            raise e
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from jianshu.items import CommentItem
import pymysql.cursors
import time,re
class JianshuPipeline(object):
    def __init__(self):
        # self.settings=get_project_settings() 
        self.connect = pymysql.Connect(
            host = '123.207.161.209',
            user = 'root',
            passwd = 'zhouxu.123',
            db = 'jianshu',
            port = 3306,
            charset = 'utf8mb4'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if isinstance(item,CommentItem):
            self.insert_comment(item)
        return item
    
    def insert_comment(self,items):
        sql = "INSERT INTO comment (content, time, user_slug,article,content_id,title) VALUES ( '%s', %d, '%s','%s','%s','%s')"
        # try:  
        #     # python UCS-4 build的处理方式  
        #     highpoints = re.compile(u'[\U00010000-\U0010ffff]')  
        # except re.error:  
        #     # python UCS-2 build的处理方式  
        #     highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')  
        
        # resovle_value = highpoints.sub(u'', items['content'])
        data = (items['content'], items['time'], items['user_slug'],items['article'],items['id'],items['title'])
        self.cursor.execute(sql % data)
        self.connect.commit()
        # print('成功插入', self.cursor.rowcount, '条数据')

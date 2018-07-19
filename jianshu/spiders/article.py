import scrapy
import json
import pymysql
import time
import datetime
import jianshu.settings as settings
from ..items import UserItem
from ..items import ArticleItem

USER = []
URL = 'https://www.jianshu.com'

# class Spider(scrapy.Spider):
#     name = 'ip'
#     allowed_domains = []

#     def start_requests(self):

#         url = 'http://ip.chinaz.com/getip.aspx'

#         for i in range(4):
#             yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

#     def parse(self,response):
#         print(response.text)

class Article(scrapy.Spider):

    custom_settings = {
        'ITEM_PIPELINES': {
            'jianshu.pipelines.Article': 300
        }
    }
    db = pymysql.connect( settings.MYSQL_HOST,settings.MYSQL_USER,settings.MYSQL_PASSWORD,settings.MYSQL_DBNAME,charset='utf8mb4' )
    cursor = db.cursor()
    sql = "select id,name,url from user where del = 0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for item in results:
            if item is not None:
                temp = UserItem()
                temp['id'] = item[0]
                temp['name'] = item[1]
                temp['url'] = item[2]+'?order_by=shared_at&page=1&per_page=99999'
                USER.append(temp)
    except Exception as e:
        raise e
        print("得到用户信息出错")
    finally:
        cursor.close()
        db.close()
    
    #https://www.jianshu.com/u/192ee953c33d?order_by=shared_at&page=2&per_page=20
    #https://www.jianshu.com/u/4c37355883d7?order_by=shared_at&page=1&per_page=9999

    name = 'article'
    start_urls = [ x['url'] for x in USER ]
    # start_urls = ['https://www.jianshu.com/u/192ee953c33d?order_by=shared_at&page=1&per_page=9999']

    def parse(self,response):

        oLis = response.css('#list-container .note-list li')
        
        for item in oLis:
            
            
            
            url = item.css('.title::attr(href)').extract_first()
            url = URL+url
            
            yield scrapy.Request(url, self.getDate, dont_filter=True)
            # yield scrapy.Request(url, self.getDate, dont_filter=True)
            # yield scrapy.Request(url, self.getDate, dont_filter=True)
            # yield scrapy.Request(url, self.getDate, dont_filter=True)
            # yield scrapy.Request(url, self.getDate, dont_filter=True)


        

    def getDate(self,response):
        # print(response.request.headers)


        content = response.css('.article')
        
        

        if content is None:
            yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)

        item = ArticleItem()
        temp_time = content.css('.publish-time::text').extract_first()

        if  temp_time is not None:
            item['url'] = response.url.split('/')[-1]
            temp_title = content.css('.title::text').extract_first()
            item['title'] = temp_title if temp_title is not None else "无题"
            item['auth'] = content.css('.name a::attr(href)').extract_first().split('/')[-1]
            temp_content = content.extract_first()
            item['content'] = temp_content if temp_content is not None else "无内容"
            # print(temp_time)
            temp_time = temp_time.replace("*","")           #2017.11.19 12:04* 转换为2017.11.19 12:04
            # print(temp_time)
            item['time'] = int(time.mktime(time.strptime(temp_time, "%Y.%m.%d %H:%M")))
            item['in_time'] = int(time.time())

            ytd_star = int(time.mktime(time.strptime(str(datetime.date.today() - datetime.timedelta(days=1)), '%Y-%m-%d'))) #昨天0.00
            ytd_end = int(time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))) - 1                           #昨天23.59
            
            # if( ytd_star <= item['time'] and item['time'] <= ytd_end ):
                #print("昨天")
            yield item
            # else:
                #print("不是昨天")
                # pass

        else:
            yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)
            # yield scrapy.Request(response.url, self.getDate, dont_filter=True)


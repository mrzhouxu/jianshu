import scrapy
import re,time,datetime
from scrapy.http import Request
from jianshu.items import CommentItem
class JianshuSpider(scrapy.Spider):
    name = "comment"
    allowed_domains = ["www.jianshu.com"]
    start_urls = [
        "https://www.jianshu.com/users/4c37355883d7/timeline",
        "https://www.jianshu.com/users/22052dde7f8e/timeline",
        "https://www.jianshu.com/users/a487ed6d5e51/timeline",
        "https://www.jianshu.com/users/0a03cc659f64/timeline",
        "https://www.jianshu.com/users/88d14cee730d/timeline",
        "https://www.jianshu.com/users/ca47f67c49c3/timeline",
        "https://www.jianshu.com/users/d1c6ff90a948/timeline"
    ]
    # def start_requests(self):
    #     yield Request("https://www.jianshu.com/u/d1c6ff90a948?order_by=id&page=1&per_page=1",self.parse)

    # 抓取昨天
    def parse(self,response):
        items = CommentItem()
        all_li = response.css('.note-list>li')
        max_id = int(all_li[-1].css('li[id*=feed]::attr(id)').re_first(r'feed\-(\d*)'))-1
        flag = True
        user_slug = response.css('a[class=avatar]::attr(href)').re_first(r'\/u\/(.*)')
        for index,li in enumerate(all_li):
            is_comment = len(li.css('span[data-type="comment_note"]').extract())!=0
            if is_comment :
                items['content'] = li.css('p[class="comment"]').extract_first()
                time_str = li.css('span[data-type="comment_note"]::attr(data-datetime)').extract_first()
                items['time'] = int(time.mktime(time.strptime(time_str[:19],'%Y-%m-%dT%H:%M:%S')))
                items['id'] = li.css('li[id*=feed]::attr(id)').re_first(r'feed\-(\d*)')
                items['article'] = li.css('a[class=title]::attr(href)').re_first(r'\/p\/(.*)')
               #user_slug = li.css('a[class=nickname]::attr(href)').re_first(r'\/u\/(.*)')
                items['user_slug'] =  li.css('a[class=nickname]::attr(href)').re_first(r'\/u\/(.*)')
                items['title'] =  li.css('a[class=title]::text').extract_first()
                # 判断年月是否相等
                year_month = int(time_str[:4])==datetime.datetime.now().year and int(time_str[5:7])==datetime.datetime.now().month
                day1 = datetime.datetime.now().day
                day2 = int(time_str[8:10])
                if  year_month and day2 >= day1:
                    flag = True
                elif year_month and day2 == day1-1:
                    yield items
                else:
                    flag = False
        if flag:
            yield Request('https://www.jianshu.com/users/'+user_slug+'/timeline?max_id='+str(max_id)+'&page=1',self.parse)

    # # 抓取今天除外的
    # def parse(self,response):
    #     items = CommentItem()
    #     all_li = response.css('.note-list>li')
    #     max_id = int(all_li[-1].css('li[id*=feed]::attr(id)').re_first(r'feed\-(\d*)'))-1
    #     user_slug = response.css('a[class=avatar]::attr(href)').re_first(r'\/u\/(.*)')
    #     # flag = True
    #     for index,li in enumerate(all_li):
    #         is_comment = len(li.css('span[data-type="comment_note"]').extract())!=0
    #         if is_comment :
    #             items['content'] = li.css('p[class="comment"]').extract_first()
    #             time_str = li.css('span[data-type="comment_note"]::attr(data-datetime)').extract_first()
    #             items['time'] = int(time.mktime(time.strptime(time_str[:19],'%Y-%m-%dT%H:%M:%S')))
    #             items['id'] = li.css('li[id*=feed]::attr(id)').re_first(r'feed\-(\d*)')
    #             items['article'] = li.css('a[class=title]::attr(href)').re_first(r'\/p\/(.*)')
    #             # user_slug = li.css('a[class=nickname]::attr(href)').re_first(r'\/u\/(.*)')
    #             items['user_slug'] =  li.css('a[class=nickname]::attr(href)').re_first(r'\/u\/(.*)')
    #             items['title'] =  li.css('a[class=title]::text').extract_first()
    #             # 判断年月是否相等
    #             year_month = int(time_str[:4])==datetime.datetime.now().year and int(time_str[5:7])==datetime.datetime.now().month
    #             day1 = datetime.datetime.now().day
    #             day2 = int(time_str[8:10])
    #             if  year_month and day2 >= day1:
    #                 pass
    #                 # yield items
    #             else :
    #                 yield items
    #     yield Request('https://www.jianshu.com/users/'+user_slug+'/timeline?max_id='+str(max_id)+'&page=1',self.parse)
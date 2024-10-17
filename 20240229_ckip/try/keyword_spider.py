#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:46:21 2024

@author: JayHung
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class KeywordSpider(CrawlSpider):
    name = 'keywordspider'   # 定義spider名稱
    custom_settings={
      'DOWNLOAD_DELAY':'3',  # 設定爬蟲時間延遲
      'FEED_EXPORT_ENCODING':'utf-8', # 設定文字編碼
    }
    allowed_domains = ['spirit.tku.edu.tw']  # 爬蟲執行網域

    start_urls = ['http://spirit.tku.edu.tw/tku/home.jsp',
                  'http://spirit.tku.edu.tw/tku/main.jsp?sectionId=8',
                  'http://spirit.tku.edu.tw/tku/main.jsp?sectionId=3',
                  'http://spirit.tku.edu.tw/tku/main.jsp?sectionId=6',
                  'http://spirit.tku.edu.tw/tku/main.jsp?sectionId=4']  #爬蟲起始網頁
  
    allow_list = ['http://spirit\.tku\.edu\.tw/tku/.+\.jsp.*',
                  'http://spirit\.tku\.edu\.tw/tku/service_news_detail\.jsp\?sectionId=1&newsId=.+',
                  'http://spirit\.tku\.edu\.tw/tku/service_qa_detail\.jsp\?sectionId=8&qaId=.+'] #需要分析之網址格式

    # 當網址的格式符合allow_list的格式時，使用parse_item函式解析網頁，
    # 把網頁內的所有超連結加入追蹤清單中
    rules = [Rule(LinkExtractor(allow=allow_list), callback='parse_item', follow=True)]
    

    def parse_detail(self, response):
        # 在這裡解析下一層的資料
        # 取出網頁標題
        detail_title = response.css('a div td#Content th::text').get()
        
        # 取出網頁內容
        ps = response.css('a div td th::text').getall()
        detail_content = ''.join(ps)
        
        # 取出網址
        url = response.url    
        yield {
            'detail_title': detail_title,
            'detail_content': detail_content,
            'detail_url': url,
        }

    def parse_item(self, response):
        # 取出網頁標題
        title = response.css('div.FontPageStrong::text').get()

        # 取出網址
        url = response.url
        yield {
          'title':title,
          'url':url,
        }
        
        # 繼續跟進下一層的連結
        # .mastertablecell
        next_links = response.css('td::attr(href)').getall()
        for next_link in next_links:
            yield response.follow(next_link, callback=self.parse_detail)
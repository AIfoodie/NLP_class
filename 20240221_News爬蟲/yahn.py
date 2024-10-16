# -*- coding: utf-8 -*-
"""yahn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19AVMzLPS85eqv7E8pYkEctqLcVjhXsSN
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# yahoo!新聞，https://tw.news.yahoo.com/

#class 名稱Spider(CrawlSpider):
class YAHNSpider(CrawlSpider):
    name = 'yahn' # 定義spider 新聞名稱
    custom_settings={
      'DOWNLOAD_DELAY':'3',  # 設定爬蟲時間延遲，數字可以再設定的大一點，但也不要讓自己等太久
      'FEED_EXPORT_ENCODING':'utf-8', # 設定文字編碼
      'SPIDER_LOADER_WARN_ONLY': True # 除錯用
    }
    allowed_domains = ['tw.news.yahoo.com']  # 爬蟲執行網域，設定一個範圍，限定才不會抓到一堆不相干的事物

    start_urls = ['https://tw.news.yahoo.com']  # 爬蟲起始網頁 | start_urls
    allow_list = ['https://tw\.news\.yahoo\.com/.*\d+\.html'] # 需要分析之網址格式，用的是正規化(\d+/\d+) | allow_list

    # 當網址的格式符合allow_list的格式時，使用parse_item函式解析網頁，
    # 把網頁內的所有超連結加入追蹤清單中
    rules = [Rule(LinkExtractor(allow=allow_list), callback='parse_item', follow=True)]

    def parse_item(self, response):
        # 取出網頁新聞標題
        title = response.css('h1#caas-lead-header-undefined::text').get()
        # ::text 要記得打，才會只抓字
        # 利用開發者工具，看原網頁中，那標題的HTML、CSS寫法：h1 id = "caas-lead-header-undefined"

        # 取出網頁新聞內容
        ps = response.css('div.caas-body p::text').getall() # getall() 全部抓下來
        # div. p 之間的空白是為了抓到上下文都有
        # 利用開發者工具，看原網頁中，那標題的HTML、CSS寫法，class => '.' ; id => '#'
        content = ''.join(ps) # .join(ps) 將文本組合起來

        # 取出網址
        url = response.url
        yield {
          'title':title,
          'content':content,
          'url':url,
        }
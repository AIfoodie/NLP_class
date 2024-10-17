#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 20:49:40 2024

@author: JayHung
"""

import scrapy
import jieba
import pandas as pd
from ckiptagger import WS, NER

class KeywordSpider(scrapy.Spider):
    name = 'keyword_spider'
    start_urls = ['http://spirit.tku.edu.tw/tku/home.jsp']  #爬蟲起始網頁
    allow_list = ['http://spirit\.tku\.edu\.tw/tku/.+\.jsp.*'] #需要分析之網址格式
    
    def __init__(self):
        super(KeywordSpider, self).__init__()
        self.ws = WS("./data")
        self.ner = NER("./data")

    def parse(self, response):
        # 提取網頁內容
        text = " ".join(response.css('::text').getall())

        # 使用 CKIP 套件處理文本
        word_sentence_list = self.ws([text])
        entity_sentence_list = self.ner(word_sentence_list)

        # 提取關鍵字
        keywords = [word for word, entity in zip(word_sentence_list[0], entity_sentence_list[0]) if entity != 'O']

        # 輸出網址和關鍵字
        yield {
            'url': response.url,
            'keywords': keywords,
        }

        # 此處您可以添加其他爬取邏輯，例如爬取更多頁面的連結

    def closed(self, reason):
        # 在爬蟲結束時將結果保存為 CSV 檔案
        df = pd.DataFrame(self.results)
        df.to_csv('output_keywords.csv', index=False, encoding='utf-8-sig')


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 01:59:40 2024

@author: JayHung
"""

# 學生事務處各組
urls = ["http://spirit.tku.edu.tw/tku/main.jsp?sectionId=1", # 學務長室
      "http://spirit.tku.edu.tw/tku/main.jsp?sectionId=2", # 生活輔導組
      "http://spirit.tku.edu.tw/tku/main.jsp?sectionId=3", # 課外活動輔導組
      "http://spirit.tku.edu.tw/tku/main.jsp?sectionId=4", # 諮商輔導中心
      "http://spirit.tku.edu.tw/tku/main.jsp?sectionId=6", # 衛生保衛組
      ]

import requests
from bs4 import BeautifulSoup
from ckiptagger import WS, POS, NER
import numpy as np

for url in urls:
  print("網址:", url)
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  sentence_list = soup.get_text()
  word_sentence_list = ws([sentence_list])
  pos_sentence_list = pos(word_sentence_list)
  entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
  # print(entity_sentence_list[0])
  # print(np.shape(entity_sentence_list))

  keywords = []
  for entity in entity_sentence_list[0]:
    if entity[2] != 'PRODUCT' and entity[2] != 'DATE' and entity[2] != 'CARDINAL' and entity[2] != 'ORDINAL':
      keywords.append(entity[3])
  print("關鍵字：",keywords)
  print()


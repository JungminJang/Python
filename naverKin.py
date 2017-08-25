#-*- coding: utf-8 -*-
import sys
import numpy as np

import Util as util
import encoding as encoding
import unicodecsv as csv

import csv

import urllib.request
from bs4 import BeautifulSoup


TARGET_SEARCH_STARTDATE = '&startDate='
TARGET_SEARCH_ENDDATE = '&endDate='
TARGET_URL_PAGENUM = 1
TARGET_SEARCH_DISPLAY = 25
TYPE = 'euc-kr'

kin_lists = []
answer = ['', '', '', '', '', '', '', '', '', '', '']
SUB_MENU = ['정치', '경제', '사회', '생활/문화', '세계']


def get_link_from_kin_title(page_num, URL):
    ARTICLE_NO = 0
    for i in range(page_num):

        current_page_num = 1 + i
        max_page_num = 0
        URLlink = URL + util.TARGET_URL_NAVER_NEWS_PAGES + str(i+1)
        soup = encoding.soup(URLlink)

        paging = soup.select('div.paging')
        if len(paging) == 0:
            return

        pageArray = util.re.findall(r"[0-9]", paging[0].text)

        max_page_num = int(max(pageArray))
        if current_page_num > max_page_num:
            return

        kinn_section = soup.find('div', class_='kinn section _kinBase')

        for index, title in enumerate(kinn_section.select('li')):

            title_link = title.find('a')
            title_text = title_link.text.strip()
            answercnt = title.find('span', class_='item').text.replace('답변수 ', '')
            # print(title_text)

            if answercnt != None:
                ARTICLE_NO += 1
                article_URL = title_link['href']
                get_kin_text(article_URL, title_text, answercnt)

           

def get_kin_text(URL, title, answercnt):
    
    try:

        source_code_from_url = urllib.request.urlopen(URL)
        soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
        contents = soup.select('div._endContentsText')

        info = soup.select('div.tit_cont')
        date = info[0].select('dd.date')
        writeDate = date[3].text

        question = util.cleantext(contents[0].text)

        if len(contents) > 1:
            answer = ['', '', '', '', '', '', '', '', '', '', '']
            for index, content in enumerate(contents):
                if index > 0:
                    answer[index-1] = util.cleantext(content.text)

            kin_lists.append({'작성일':writeDate, '제목':title, 'URL':URL, '질문':question, '답변1':answer[0], '답변2':answer[1], '답변3':answer[2], '답변4':answer[3], '답변5':answer[4], '답변6':answer[5]})


    except Exception as e:
        print(e)
    
def make_files():

    dir = 'NAVERKIN/'
    filename = 'naverKin_' + util.TODAY + '.csv'
    try:
        
        with open(dir + filename, 'wt', newline='', encoding='cp949') as news:
            cw = csv.DictWriter(news, ['작성일', '제목', 'URL', '질문', '답변1', '답변2', '답변3', '답변4', '답변5', '답변6'])
            cw.writeheader()
            cw.writerows(kin_lists)
            

    except Exception as e:
        print(e)


def main():
    keyword = util.TARGET_SEARCH_KEYWORD
    page_num = int(TARGET_URL_PAGENUM)

    for index, item in enumerate(keyword):

        target_URL = util.TARGET_URL_KIN + encoding.urlencode(item, TYPE) + util.TARGET_URL_KIN_REST
        get_link_from_kin_title(page_num, target_URL)

    make_files()
   

if __name__ == '__main__':
    main()

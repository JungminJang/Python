#-*- coding: utf-8 -*-
import sys
import numpy as np

import Util as util
import encoding as encoding
import writeArticles as acrticle

import csv

import urllib.request
from bs4 import BeautifulSoup

import re

# 검색어 query=%B1%B9%B9%CE%C2%F7
# 정렬 so=datetime.dsc
# 기간 시작일 startDate=2017-04-19
# 기간 종료일 endDate=2017-04-26
# PD=3 최근 일주일간, PD=4 직접입력



TARGET_SEARCH_STARTDATE = '&startDate='
TARGET_SEARCH_ENDDATE = '&endDate='
TARGET_URL_PAGENUM = 100
TARGET_SEARCH_DISPLAY = 25
TYPE = 'euc-kr'

news_lists = []
SUB_MENU = ['정치', '경제', '사회', '생활/문화', '세계']


def get_link_from_news_title(page_num, URL):
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

        for index, title in enumerate(soup.select('ul.srch_lst')):

            title_link = title.find('a', class_='go_naver')
            newpaper = title.find('span', class_='press').text

            if title_link != None:
                ARTICLE_NO += 1
                article_URL = title_link['href']

                if article_URL.find('sid1=') != -1:
                    url_arr = article_URL.split('&')
                    sub_menucd = url_arr[2].replace('sid1=', '')
                    if int(sub_menucd) < 106:
                        get_naver_text(article_URL, newpaper, sub_menucd)
            
           

def get_naver_text(URL, newpaper, sub_menucd):
    
    try:

        source_code_from_url = urllib.request.urlopen(URL)
        soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='cp949')
        main_content = soup.find('div', id='main_content')

        title = main_content.find('h3', id='articleTitle')
        content = main_content.find('div', id='articleBodyContents')
        date = main_content.find('span', class_='t11')
        sub_menu = get_sub_menu(sub_menucd)

        chk_title = title.text.replace(' ', '')
        chk_content = content.text.replace(' ', '')
        if chk_title.find('해리포터') == -1 and chk_content.find('해리포터') == -1:

            # print(date.text)
            # print(URL)
            # print(title.text)
            # content = util.cleantext(util.cleanhtml(content.text)).strip()
            # print(content)
            # print(newpaper)
            # print(sub_menu)
            # print('--------------------------------------------------------------------------------------------------------------------')



            news_lists.append({'작성일':date.text, '제목':util.cleantext(title.text), '내용':content, '신문사':newpaper, '영역':sub_menu, '조회일':util.TODAY, 'URL':URL})
        

    except Exception as e:
        print(e)
    
def get_sub_menu(menucd):
    return SUB_MENU[int(menucd[2])]

def make_files():

    dir = 'NAVER/'
    filename = 'navernews_' + util.TODAY + '.csv'
    try:
        
        with open(dir + filename, 'wt', newline='', encoding='cp949') as news:
            cw = csv.DictWriter(news, ['작성일', '제목', '내용', '신문사', '영역', '조회일', 'URL'])
            cw.writeheader()
            cw.writerows(news_lists)
            

    except Exception as e:
        print(e)


def main():
    keyword = util.TARGET_SEARCH_KEYWORD
    page_num = int(TARGET_URL_PAGENUM)

    for index, item in enumerate(keyword):

        target_URL = util.TARGET_URL_NAVER_NEWS + encoding.urlencode(item, TYPE) + util.TARGET_URL_NAVER_REST + util.TARGET_URL_NAVER_NEWS_DISPLAY + str(TARGET_SEARCH_DISPLAY) + TARGET_SEARCH_STARTDATE + str(util.STARTDT) + TARGET_SEARCH_ENDDATE + str(util.ENDDT)
        get_link_from_news_title(page_num, target_URL)
        
    make_files()
   

if __name__ == '__main__':
    main()

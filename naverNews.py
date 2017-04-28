import sys
import numpy as np

import Util as util
import encoding as encoding
import writeArticles as acrticle

# 검색어 query=%B1%B9%B9%CE%C2%F7
# 정렬 so=datetime.dsc
# 기간 시작일 startDate=2017-04-19
# 기간 종료일 endDate=2017-04-26
# PD=3 최근 일주일간, PD=4 직접입력



TARGET_SEARCH_STARTDATE = '&startDate='
TARGET_SEARCH_ENDDATE = '&endDate='
TARGET_URL_PAGENUM = 10
TARGET_SEARCH_DISPLAY = 10
TYPE = 'euc-kr'


def get_link_from_news_title(page_num, URL, keytype):
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
            ARTICLE_NO += 1
            title_link = title.select('a')
            article_URL = title_link[0]['href']
            article_TITLE = title_link[1].text
            
            acrticle.get_text(article_URL, ARTICLE_NO, article_TITLE, keytype)
            
            


def main():
    keyword = util.TARGET_SEARCH_KEYWORD
    page_num = int(TARGET_URL_PAGENUM)
    
    for index, item in enumerate(keyword):
        target_URL = util.TARGET_URL_NAVER_NEWS + encoding.urlencode(item, TYPE) + util.TARGET_URL_NAVER_REST + util.TARGET_URL_NAVER_NEWS_DISPLAY + str(TARGET_SEARCH_DISPLAY) + TARGET_SEARCH_STARTDATE + str(util.STARTDT) + TARGET_SEARCH_ENDDATE + str(util.ENDDT)
        get_link_from_news_title(page_num, target_URL, index+1)
    
   

if __name__ == '__main__':
    main()

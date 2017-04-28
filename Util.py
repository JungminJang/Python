import datetime
import re

TARGET_SEARCH_KEYWORD = ['%B1%B9%B9%CE%C2%F7', '%C6%F7%C5%CD']  # 국민차, 포터

# 네이버뉴스
TARGET_URL_NAVER_NEWS = 'http://news.naver.com/main/search/search.nhn?query='
TARGET_URL_NAVER_NEWS_DISPLAY = '&display='
TARGET_URL_NAVER_NEWS_PAGES = '&page='
TARGET_URL_NAVER_REST = '&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=all.basic&ic=all&so=datetime.dsc&detail=1&pd=4&dnaSo=datetime.dsc'


TODAY = datetime.datetime.today().strftime('%Y-%m-%d')
BEFOREDAY = datetime.datetime.today() - datetime.timedelta(days=1) # 시작일 선정
STARTDT = BEFOREDAY.strftime('%Y-%m-%d')
ENDDT = TODAY


def cleanhtml(raw_html):
    cleantext = re.sub(r"<.*?>", '', raw_html)
    cleantext = re.sub(r"\\[n|r|t]", '', cleantext)
    item = re.findall(r"[a-zA-Z0-9ㄱ-힣]+", cleantext)
    cleantext = ''
    
    for text in item:
        cleantext = cleantext + ' ' + text
    return cleantext

def cleantext(text):
    text = text.replace('"', '')
    text = text.replace('?', '')
    text = text.replace('\n', '')
    text = text.replace('/', '')
    text = text.replace('*', '')
    text = text.replace('<', '')
    text = text.replace('>', '')
    text = text.replace('|', '')
    return text


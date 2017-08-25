import datetime
import re

TARGET_SEARCH_KEYWORD = ['국민차', '포터']  # 국민차, 포터

# 네이버뉴스
TARGET_URL_NAVER_NEWS = 'http://news.naver.com/main/search/search.nhn?query='
TARGET_URL_NAVER_NEWS_DISPLAY = '&display='
TARGET_URL_NAVER_NEWS_PAGES = '&page='
TARGET_URL_NAVER_REST = '&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&sm=all.basic&ic=all&so=datetime.dsc&detail=1&pd=4&dnaSo=datetime.dsc'


# 네이버 지식인
TARGET_URL_KIN = 'https://search.naver.com/search.naver?where=kin&query='
TARGET_URL_KIN_REST = '&kin_sort=1&nso=so%3Ar%2Ca%3Aall%2Cp%3A1d'
TARGET_URL_KIN_SEARCHDAY = '1일'


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
    text = text.replace('flash 오류를 우회하기 위한 함수 추가', '')
    text = text.replace('function flash removeCallback', '')
    text = text.replace('\u2027', '')
    text = text.replace('\u2219', '')
    text = text.replace('\xa0', '')
    text = text.replace('\u2714', '')
    text = text.replace('\u274c', '')

    return text


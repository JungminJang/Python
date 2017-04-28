import requests
import urllib.parse

from bs4 import BeautifulSoup

def spider(max_pages, mnfcnm):
    page = 1
    
    while page < max_pages:
        url = 'http://www.google.com/?#q=' + urllib.parse.quote(mnfcnm, safe='')
        print(url)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        
        print(soup)
        page += 1

spider(2, '국민차')
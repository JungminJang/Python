import urllib.request
import Util as util
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_text(URL, ARTICLE_NO, article_TITLE, keytype):
    output_file_name = str(keytype) + '-' + str(ARTICLE_NO) + '.' + util.cleantext(article_TITLE) + '.txt'
    output_file = open(output_file_name, 'w', encoding="utf8")
    
    try:

        source_code_from_url = urllib.request.urlopen(URL)
        soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
        body = soup.select('body')
        for text in body:
            string_item = str(text.find_all(text=True))
            output_file.write(util.cleanhtml(string_item))
    except Exception as e:
        print(e)

    output_file.close()
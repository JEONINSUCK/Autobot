import urllib.request
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib import parse

TARGET_URL = "https://search.naver.com/search.naver?&where=news&query="

class html_parser():
    def __init__(self):
        self.debug = 0
        self.site = TARGET_URL
        self.keyword = "비트코인"
        self.new_titles = []

    def get_title(self):
        with urllib.request.urlopen(TARGET_URL + quote(self.keyword)) as self.response:
            self.soup = BeautifulSoup(self.response.read(), "html.parser")
            self.first_divs = self.soup.select("a._sp_each_title")
            for self.first_div in self.first_divs:
                print(self.first_div.text)

    def run(self):
        pass


    

    

if __name__ == "__main__":
    test = html_parser()
    test.get_title()

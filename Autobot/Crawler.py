import urllib.request
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from urllib import parse

TARGET_URL = "https://www.coindeskkorea.com/"
SEARCH_PATH = "news/articleList.html?sc_word="
PAGE_PATH = "page="

class html_parser():
    def __init__(self,keyword="커피",day=0,search=1,debug=1):
        self.is_search = search
        if day: self.is_day = 1
        else: self.day_set = 0 
        self.debug = debug
        
        self.keyword = keyword
        self.title_link_dicts= {}
        self.page_num = 0

    def Run(self):
        self.article_num = 0

        if self.is_search:
            self.url = TARGET_URL + SEARCH_PATH + quote(self.keyword)
        
        self.PageParser(self.url)
        self.page_num = self.PageNumSet()
        
        if self.page_num > 1:
            for i in range(2, self.page_num+1):
                self.url = TARGET_URL + SEARCH_PATH + quote(self.keyword) + "&" + PAGE_PATH + str(i)
                self.PageParser(self.url)

        print(len(self.title_link_dicts))

    def PageNumSet(self):
        url = self.soup.find("li","pagination-end").find("a").attrs['href']
        parse_data = parse.parse_qs(urlparse(url).query)
        page_num = int((parse_data['page'][0]))
        if self.debug:
            print(page_num)
        return page_num

    def PageParser(self, url):
        with urllib.request.urlopen(url) as self.response:
                self.soup = BeautifulSoup(self.response.read(), "html.parser")
                self.first_divs = self.soup.select("a.links")
                for self.first_div in self.first_divs:
                    self.article_num += 1
                    if(self.first_div.find("strong")):
                        self.title_link_dicts.update({self.article_num:
                                                                        {"article": self.first_div.text,
                                                                        "url" : self.first_div.attrs['href']}
                                                                        })

    def UrlParser(self):
        pass



if __name__ == "__main__":
    test = html_parser()
    test.Run()

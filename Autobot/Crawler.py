import urllib.request
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from urllib import parse
import threading

TARGET_URL = "https://www.coindeskkorea.com/"
SEARCH_PATH = "news/articleList.html?sc_word="
PAGE_PATH = "&page="
DAY_PATH = "&sc_day="

class html_parser():
    def __init__(self,keyword="비트코인",day=80,search=1,debug=1):
        self.is_search = search
        if day: self.is_day = 1
        else: self.day_set = 0 
        self.debug = debug
        
        self.keyword = keyword
        self.title_link_dicts= {}
        self.page_num = 0
        self.day = day

    def Run(self):
        self.article_num = 0
        self.thread_name_lists = []

        if self.is_search:
            self.url = self.UrlSet(keyword=self.keyword, day=self.day, page=self.page_num+1)
        
        self.PageParser(self.url)
        self.page_num = self.PageNumSet()
        
        if self.page_num > 1:
            for i in range(2, self.page_num+1):
                self.url = self.UrlSet(keyword=self.keyword, day=self.day, page=i)
                thread_name = "t" + str(i)
                thread_name = threading.Thread(target=self.PageParser, args=(self.url,))
                thread_name.start()
                self.thread_name_lists.append(thread_name)

            for self.thread_name_list in self.thread_name_lists:
                self.thread_name_list.join()

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
                    if self.debug:  print(self.first_div.text)                    

    def UrlSet(self, keyword=None, day=None, page=None, path=None):
        if keyword:
            url_set = TARGET_URL + SEARCH_PATH + quote(self.keyword) + PAGE_PATH + str(page) + DAY_PATH + str(day)
        else:
            url_set = TARGET_URL + path
        return url_set


    def UrlParser(self):
        pass



if __name__ == "__main__":
    test = html_parser()
    test.Run()

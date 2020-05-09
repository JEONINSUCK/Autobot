import urllib.request
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse
from urllib import parse
import threading
import time

TARGET_URL = "https://www.coindeskkorea.com"
SEARCH_PATH = "/news/articleList.html?sc_word="
PAGE_PATH = "&page="
DAY_PATH = "&sc_day="

class SearchMachine():
    def __init__(self,keyword,day=0,search=1,debug=1):
        self.is_search = search
        if day: self.is_day = 1
        else: self.day_set = 0 
        self.debug = debug
        
        self.keyword = keyword
        self.tit_lin_day_dict= {}
        self.page_num = 0
        self.day = day

    def run(self):
        if self.debug: print("SearchMachine() runing....")
        self.article_num = 0
        self.thread_name_lists = []

        if self.is_search:
            self.url = self.UrlSet(keyword=self.keyword, day=self.day, page=self.page_num+1)
        self.Art_Tit_Parser(self.url)
        self.page_num = self.PageNumSet()
        
        if self.page_num > 1:
            for i in range(2, self.page_num+1):
                self.url = self.UrlSet(keyword=self.keyword, day=self.day, page=i)
                self.thread_name_lists.append(threading.Thread(target=self.Art_Tit_Parser, args=(self.url,)))
                self.thread_name_lists[i-2].start()
                
            for self.thread_name_list in self.thread_name_lists:
                self.thread_name_list.join()
        
        if self.debug: print("SearchMachine() finished....\n")

    def PageNumSet(self):
        url = self.soup.find("li","pagination-end").find("a").attrs['href']
        parse_data = parse.parse_qs(urlparse(url).query)
        page_num = int((parse_data['page'][0]))
        return page_num

    def Art_Tit_Parser(self, url):
        with urllib.request.urlopen(url) as self.response:
                self.soup = BeautifulSoup(self.response.read(), "html.parser")
                self.first_divs = self.soup.select("div.table-row")
                for self.first_div in self.first_divs:
                    self.article_num += 1
                    if self.first_div.find("strong"):
                        self.art_day = self.first_div.find("div", "list-dated").get_text()
                        self.tit_lin_day_dict.update({self.article_num: 
                                                                        {"article" : self.first_div.find("a", "links").get_text(),
                                                                        "url" : TARGET_URL + self.first_div.find("a", "links").attrs['href'],
                                                                        "day" : self.art_day}
                                                                        })

    def UrlSet(self, keyword=None, day=None, page=None, path=None):
        if keyword:
            url_set = TARGET_URL + SEARCH_PATH + quote(self.keyword) + PAGE_PATH + str(page) + DAY_PATH + str(day)
        else:
            url_set = TARGET_URL + path
        return url_set

    def ArtDayParser(self, data):
        return data.split("|")[1]

    def GetArtInfo(self):
        return self.tit_lin_day_dict

    def ShowArtList(self, article=0, url=0, day=0):
        print("article num: ", len(self.tit_lin_day_dict))
        # if article:
        #     for i in range(1, len(self.tit_lin_day_dict)+1):
        #         print("article: ", self.tit_lin_day_dict[i]['article'])
        # if link:
        #     for i in range(1, len(self.tit_lin_day_dict)+1):
        #         print("url: ", self.tit_lin_day_dict[i]['url'])
        # if url:
        #     for i in range(1, len(self.tit_lin_day_dict)+1):
        #         print("day: ", self.tit_lin_day_dict[i]['day'])
        for i in range(1, len(self.tit_lin_day_dict)+1):
            if article: print("article: ", self.tit_lin_day_dict[i]['article'])
            if url: print("url: ", self.tit_lin_day_dict[i]['url'])
            if day: print("day: ", self.tit_lin_day_dict[i]['day'])

if __name__ == "__main__":
    start = time.time()
    test = SearchMachine("비트코인", day=30, debug=1)
    test.run()
    test.ShowArtList(article=1)
    print("time: {0} 초".format(time.time() - start))

import urllib.request
from bs4 import BeautifulSoup
import time
import jpype
from konlpy.tag import Okt
from collections import Counter


from SearchMachine import SearchMachine

okt = Okt()

class Analysis():
    def __init__(self,debug=0):
        super().__init__()
        # jpype.attachThreadToJVM()
        self.debug = debug
        self.okt = okt

    def GetNoun(self, page):
        if self.debug: print("GetNoun() started...")
        self.buff = ""
        self.tag_count_list = []
        self.tags_list = []
        # jpype.attachThreadToJVM()

        with urllib.request.urlopen(page) as self.response:
            self.soup = BeautifulSoup(self.response.read(), "html.parser")
            self.nouns = self.soup.select("p")
            for self.noun in self.nouns:
                self.buff += self.noun.text
            
            self.okt = Okt()
            self.nouns = self.okt.nouns(self.buff)

            self.count = Counter(self.nouns)
            for i,j in self.count.most_common():
                dicts = {"tag": i, "count": j}
                self.tag_count_list.append(dicts)
                self.tags_list.append(dicts['tag'])

        print(self.tag_count_list)
        if self.debug: print("GetNoun() finished...\n")
        return self.tag_count_list

    def Show_Nouns(self,tag_count_lists):
        for tag_count_list in tag_count_lists:
            print("{0} {1}".format(tag_count_list['tag'], tag_count_list['count']))
        print("list num: {0}\n".format(len(tag_count_lists)))

if __name__ == "__main__":
    start = time.time()
    search_machine = SearchMachine(keyword="비트코인", day=7, debug=0)
    search_machine.run()
    site_pages = search_machine.GetArtInfo()
    
    test = Analysis(debug=1)
    result = test.GetNoun(page=site_pages[1]['url'])
    print(result)
    # for re in result:
    #     print("{0} : {1}".format(re['tag'], re['count']))
    
    print("time: {0}".format(time.time() - start))
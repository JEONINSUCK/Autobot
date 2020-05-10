import urllib.request
from bs4 import BeautifulSoup
import time
from konlpy.tag import Okt
from collections import Counter
import jpype
# from threading import Thread
import sys
sys.path.append(".")

okt = Okt()

class Analysis():
    def __init__(self,debug=0):
        super().__init__()
        self.debug = debug

    def GetNoun(self, page):
        if self.debug: print("GetNoun() started...")
        self.buff = ""
        self.tag_count_list = []
        self.tags_list = []

        with urllib.request.urlopen(page) as self.response:
            self.soup = BeautifulSoup(self.response.read(), "html.parser")
            self.nouns = self.soup.select("p")
            for self.noun in self.nouns:
                self.buff += self.noun.text

            path = jpype.getDefaultJVMPath()
            if jpype.isJVMStarted():
                jpype.attachThreadToJVM()
            else:
                jpype.startJVM(path)

            self.nouns = okt.nouns(self.buff)

            self.count = Counter(self.nouns)
            for i,j in self.count.most_common():
                dicts = {"tag": i, "count": j}
                self.tag_count_list.append(dicts)
                self.tags_list.append(dicts['tag'])

        if self.debug: print("GetNoun() finished...\n")
        return self.tag_count_list

    def Show_Nouns(self,tag_count_lists):
        for tag_count_list in tag_count_lists:
            print("{0} {1}".format(tag_count_list['tag'], tag_count_list['count']))
        print("list num: {0}\n".format(len(tag_count_lists)))

if __name__ == "__main__":
    start = time.time()
    # search_machine = SearchMachine(keyword="비트코인", day=7, debug=0)
    # search_machine.run()
    # site_pages = search_machine.GetArtInfo()
    
    # test = Analysis(debug=1)

    # t1 = Thread(target=test.GetNoun, args=(site_pages[3]['url'],))
    # t1.start()
    # t1.join()
    # pro = Process(target=test.GetNoun, args=(site_pages[1]['url'],))
    # pro.start()
    # pro.join()

    # result = test.GetNoun(page=site_pages[1]['url'])
    # print(result)
    # for re in result:
    #     print("{0} : {1}".format(re['tag'], re['count']))
    
    print("time: {0}".format(time.time() - start))
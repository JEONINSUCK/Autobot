import threading
import time
import jpype
import sys
try:
    from Lib_v1 import SearchMachine, ArtiAnalysis
except ImportError:
    import SearchMachine, ArtiAnalysis
from multiprocessing import Process
from multiprocessing import Pool

class Crawler():
    def __init__(self, keyword, day=0, debug=0):
        super().__init__()
        self.keyword = keyword
        self.day =  day
        self.debug = debug
        self.nouns_list = []
        self.thread_name = []
    
    def run(self):
        self.process_list = []
        self.url_list = []

        self.search_machine = SearchMachine(keyword=self.keyword, day=self.day, debug=self.debug)
        self.search_machine.run()
        self.art_info_list = self.search_machine.GetArtInfo()
        # self.search_machine.ShowArtList(article=1, url=1, day=1)

        # self.analysis = analysister.Analysis(debug=1)
        
        # pro = Process(target=self.analysis.GetNoun, args=(self.art_info_list[1]['url'],))
        # pro.start()
        # pro.join()

        # for index in range(len(self.art_info_list)):
        #     self.url_list.append(self.art_info_list[index+1]['url'])
        
        # self.multi_pool = Pool(processes=4)
        # self.multi_pool.map(self.analysis.GetNoun, self.url_list[1])
        # self.multi_pool.close()
        # self.multi_pool.join()

        
        # result = self.analysis.GetNoun(page=self.art_info_list[1]['url'])
        # for i in range(1,len(self.art_info_list)+1):
        #     thread_name = "t" + str(i)
        #     thread_name = threading.Thread(target=self.analysis.GetNoun, args=(self.art_info_list[i]['url'],))
        #     thread_name.start()
        #     self.thread_name.append(thread_name)
        
        # self.nouns = 

        

if __name__ == "__main__":
    start = time.time()
    test = Crawler("비트코인",day=7, debug=1)
    test.run()
    print("time: {0}".format(time.time() - start))
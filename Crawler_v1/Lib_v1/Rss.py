#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : hdh0926@naver.com
import datetime
import time
import feedparser
from pprint import pprint
from Protocol import news, news_collection
from threading import Thread
import json

class RssService(Thread):
  debug   = False
  url  = ""
  last    = ""

  def __init__(self, debug = False, target = "", last = ""):
    super().__init__(self, target, last)
    self.debug = debug
    self.url = target
    self.last = last

  def run(self):
    print("{} started!".format(self.getName()))        # "Thread-x started!"
    start = time.time()
    rss = feedparser.parse(self.url)

    # start parser
    newsList = []
    try:
      if self.last == "":
        for row in rss["entries"]:
          _news = news( title = row["title"], content = ''.join(row["summary"].split("\n")), published = row["published"] )
          # if self.debug : print(_news.published)
          newsList.append(_news)
        self.last = timestamp = time.mktime(datetime.datetime.now().timetuple()) 
      else:
        for row in rss["entries"]:
          _news = news( title = row["title"], content = ''.join(row["summary"].split("\n")), published = row["published"] )
          if self.last > published:
            continue
          if self.debug : print("[+] new " + _news.published)
          newsList.append(_news)
          self.last = time.mktime(datetime.strptime(_news.published, '%y-%m-%d %H:%m:%S').timetuple)

      print("[+] news count : {}".format(len(newsList)))
      print("[+] only run function time: {0}".format(time.time() - start))
      print("[+] {}".format(self.last))
    except Exception as e:
      print(e)

class RssWatcher(object):
  # define
  debug = False
  th_list = []
  rs_data = []

  def __init__(self, debug = False):
    self.debug = debug
  
  # all wait
  def wait(self):
    for th in self.th_list:
      th.join()
  
  # all start
  def start(self):
    for th in self.th_list:
      th.start()
  
  def runner(self):
    try:
      # read file
      with open('config.dev.json') as json_file:
        config = json.load(json_file)

      # check config data
      if(config == ""):
        print("[-] not found config file")
        sys.exit()
        
      # read data file
      r = open("data/rss_kr.txt", mode='r', encoding='utf-8')
      for x in r.readlines():
        if(x.startswith("#")):
          print("[DEBUG]"+x)
        else:
          print("[INFO][RUN]"+x)
          target, interval = x.split(",")
          th = RssWatcher(target = target, interval = interval, debug = True)
          self.th_list.append(th)
        # start wait
        print("[+] load count : {0}".format(self.th_list))
        self.start()
        self.wait()
    except Exception as e:
      print("[-] Error: unable to start thread", e)
    while 1:
      print("run main")
      time.sleep(1)
      pass

if __name__ == "__main__":
    start = time.time()
    target = "http://www.coindeskkorea.com/rss/allArticle.xml"
    r_service = RssWatcher(debug = True)
    r_service.runner()
    print("time: {0}".format(time.time() - start))
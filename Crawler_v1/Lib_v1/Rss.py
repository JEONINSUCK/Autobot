#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : hdh0926@naver.com

import datetime, feedparser, time
from pprint import pprint
from Protocol import news, news_collection
from threading import Thread
import json, sys,hashlib, queue

class RssWatcher(object):
  # define
  debug = False
  jobs_list = {}
  q = queue.Queue()

  def __init__(self, debug = False):
    super().__init__()
    self.debug = debug
  
  def LastParser(self, row):
    try:
      updated_at = row["published"]
      last = time.mktime(datetime.datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S').timetuple())
      return last
    except Exception as e:
      print("[LastParser][ERROR] ", e)
      return 0

  def NewsParser(self, target, last, key):
    rss = feedparser.parse(target)
    last_time = last
    try:
      if self.jobs_list[key]["last"] != 0:
        last_time = self.jobs_list[key]["last"]
      print("[INFO][NewsParser_1] ", last_time, "is_last")
    except Exception as e:
      print("[ERROR][NewsParser_1] : ", e)
      pass

    # start parser
    newsList = []
    try:
      if last_time <= 0 :
        # new init
        for row in rss["entries"]:
          _news = news( title = row["title"], content = ''.join(row["summary"].split("\n")), published = self.LastParser(row) )
          newsList.append(_news)
      else:
        # update init
        for row in rss["entries"]:
          _news = news( title = row["title"], content = ''.join(row["summary"].split("\n")), published = self.LastParser(row) )
          newsList.append(_news)
          timestamp = self.LastParser(row)
          if last_time > timestamp:
            continue
      # last action
      last_news = newsList[len(newsList) - 1]
      if len(newsList) > 0:
        self.jobs_list[key]["last"] = last_news.published

      # send to result
      self.q.put({ "newsList" : newsList, "target" : target, "key" : key, "last" : time.time() })

      # logging
      print("[INFO][NewsParser_2] Last : {0}, Count : {1}, key : {2}".format(self.jobs_list[key]["last"], str(len(newsList)), key))
      print("[INFO][NewsParser_2] Runtime : {0}".format(str(time.time() - start)))
    except Exception as e:
      print("[ERROR][newsParser_2] ", e)
  
  def run(self):
    try:
      # read file
      config = ""
      with open('config.dev.json') as json_file:
        config = json.load(json_file)

      # check config data
      if not config:
        print("[ERROR] No have value on config file, "+config)
        sys.exit()
      
      # read data file
      r = open("data/rss_kr.txt", mode='r', encoding='utf-8')
      for x in r.readlines():
        if not x.startswith("http"):
          print("[INFO][PASS] "+x)
          continue
        else:
          # add schedule
          target, interval, last = x.split(",")

          # defined data
          key = hashlib.md5(target.encode('utf-8')).hexdigest()
          if not last.replace("\n", "").strip():
            last = 0
          self.jobs_list[key] = { "target" : target, "last" : last, "key" : key, "interval" : interval }

          # just start once
          Thread(target=self.NewsParser, args=(target, last, key)).start()

          # logging
          print("[INFO][RUN] "+x)
            
    except Exception as e:
      print("[RUN][ERROR] ", e)

    while 1:
      if not self.q.empty():
        pass
        # pprint(self.q.get())
      time.sleep(1)
      pass

if __name__ == "__main__":
    start = time.time()
    r_service = RssWatcher(debug = True)
    r_service.run()
    print("time: {0}".format(time.time() - start))
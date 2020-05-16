#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : hdh0926@naver.com

import datetime
import time
import feedparser
from pprint import pprint
from Protocol import news, news_collection
from threading import Thread
import json, sys

# start schedule
# 스케줄 종류에는 여러가지가 있는데 대표적으로 BlockingScheduler, BackgroundScheduler 입니다
# BlockingScheduler 는 단일수행에, BackgroundScheduler은 다수 수행에 사용됩니다.
# 여기서는 BackgroundScheduler 를 사용하겠습니다.
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import hashlib, queue

class RssWatcher(object):
  # define
  debug = False
  sched = BackgroundScheduler()
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
      print(e)
      return 0

  def run(self, target, last, key):
    start = time.time()
    rss = feedparser.parse(target)
    last_time = last.strip()
    print("insert", last_time)
    if not last_time:
      last_time = 0
    if self.jobs_list[key]["last"]:
      last_time = self.jobs_list[key]["last"]
      print("update", last_time, key)

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
          a = self.LastParser(row)
          print(a, "asdasda")
          if last_time > a:
            continue
      # last action
      print(newsList[len(newsList) - 1].published)
      self.jobs_list[key]["last"] = newsList[len(newsList) - 1].published
      print("[+] Last : {0}, Count : {1}".format(self.jobs_list[key]["last"], str(len(newsList))))
      print("[+] Runtime : {0}".format(str(time.time() - start)))
      # pprint(self.jobs_list[key])
      self.q.put({ "newsList" : newsList, "target" : target, "key" : key })
    except Exception as e:
      print(e)
  
  def runner(self):
    try:
      # read file
      with open('config.dev.json') as json_file:
        config = json.load(json_file)

      # check config data
      if not config:
        print("[ERROR] No have value on config file, "+config)
        sys.exit()
      
      # start schedule on background
      self.sched.start()

      # read data file
      r = open("data/rss_kr.txt", mode='r', encoding='utf-8')
      for x in r.readlines():
        if not x.startswith("http"):
          if self.debug:
            print("[DEBUG][PASS] "+x)
          continue
        else:
          # add schedule
          target, interval, last = x.split(",")
          key = hashlib.md5(target.encode('utf-8')).hexdigest()
          params = { "target" : target, "last" : last, "key" : key }
          self.sched.add_job(self.run, 'interval', seconds=int(interval), id=key, kwargs=params)
          self.jobs_list[key] = params
          print(self.jobs_list[key])

          # logging
          if self.debug:
            print("[INFO][RUN] "+x)
      # start wait
      # self.th_start()
      # self.th_wait()
    except Exception as e:
      print("[ERROR] unable to start thread", e)
    while self.sched.running:
      print("run main")
      if not self.q.empty:
        pprint(self.q.get())
      time.sleep(1)
      pass

if __name__ == "__main__":
    start = time.time()
    r_service = RssWatcher(debug = True)
    r_service.runner()
    print("time: {0}".format(time.time() - start))
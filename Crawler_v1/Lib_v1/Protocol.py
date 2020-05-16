#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : hdh0926@naver.com
# protocol defined by class
import time

class news():
    title      = ""    # title on news
    content    = ""    # content on news
    time       = ""    # target rss url(xml link)
    is_up      = False # preflight later ai check value or build up, default is false
    status     = ""    # content is positive or negative status
    published  = ""

    def __init__(self, title = "", content = "", published = ""):
        self.title = title
        self.content = content
        self.time = time.time()
        self.published  = published

class news_collection():
    target     = "" # target
    last       = "" # news target
    news_list  = [] # cloned news list

    def __init__(self, target = "", last = "", targt = ""):
        self.target = target
        self.last = last
        self.targt  = targt

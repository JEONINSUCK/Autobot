from Lib_v1 import * # import lib_V1
import json, logging
import __main__ as main
import sys, os, datetime, time


# logging level rule accroding debug mode
# debug > info > waring > error > critical

class CoreRssService():
    debug = False
    LOG = ""
    th_list = []

    def __init__(self, debug = False, config = ""):
        try:
            logfile = main.__file__
            super().__init__()

            self.setLogger('/logs/{logfile}.log', debug)
            self.debug = debug
            logging.info('[+] init done', logfile)
        except Exception as e:
            print(e)
    
    def setLogger(self, filename, debug = False):
        try:
            if(filename):
                raise TypeError
                sys.exit()
            if os.path.isfile(filename) != True:
                
                LOG = logging.getLogger(filename)
                LOG.setLevel(logging.DEBUG if debug else logging.INFO)

                # create file handler which logs even debug messages
                fh = logging.FileHandler(filename)
                fh.setLevel(logging.DEBUG)

                # create console handler with a higher log level
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)

                # create formatter and add it to the handlers
                formatter = logging.Formatter('-->%(asctime)s - %(name)s:%(levelname)s - %(message)s')
                fh.setFormatter(formatter)
                ch.setFormatter(formatter)

                # add the handlers to the logger
                LOG.addHandler(fh)
                LOG.addHandler(ch)
            else:
                LOG = logging.getLogger()
        except Exception as e:
            print(e)


    def run(self):
        # preflight check config file
        start = time.time()
        config = ""
        
        
        # read file
        with open('config.dev.json') as json_file:
            config = json.load(json_file)

        if(config == ""):
            print("[-] not found config file")
            sys.exit()

        # therad start and manager

        # read data file
        r = open("data/rss_kr.txt", mode='r', encoding='utf-8')
        print(r.readlines())
        for x in r.readlines():
            if(x.startswith("#")):
                print("[DEBUG]"+x)
            else:
                target, interval = x.split(",")
                r_service = RssWatcher(target = target, interval = interval, debug = True)
                # r_service.runner()
                r_service.wait()
                

        

        
        logging.info("run time: {0}".format(time.time() - start))


    



if __name__ == "__main__":
    try:
        service = CoreRssService(debug = True)
        service.run()
        
    except Exception as e:
        print(e)
    pass
    
    
    
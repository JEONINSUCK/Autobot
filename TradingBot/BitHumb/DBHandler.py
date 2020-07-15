import pymysql
from sqlalchemy import create_engine

from OpenAPI import *
from UserAPI import *
import pandas

class DBHandler():
    def __init__(self, debug=0):
        self.debug = debug

    def 
    
with open(Path().KeyPath(), "r") as f:
        buf = f.read().split()
        connect = buf[1]
        secret = buf[3]

bit = Bithumb(connect, secret)

data = bit.GetCandleStick()

print(data)
engine = create_engine('mysql+pymysql://root:root@localhost/test')

data.to_sql("candle", con=engine,if_exists='append')
import UserAPI
import DBHandler
import threading
import time
from enum import Enum
from pandas import DataFrame


class Candle(Enum):
    date = 0
    ticktype = 1
    time = 2
    openprice = 3
    closeprice = 4
    lowprice = 5
    highprice = 6
    symbol = 7

COINTYPE = "BTC"
TICKTYPE = "30M"
DBHOST = "localhost"
DBUSER = 'root'
DBPASSWORD = 'root'
DBNAME = 'test'
CANTABLE = "candle_test"
TRANTABLE = "trans_test"
MATABLE = "ma_test"
DBCOLUMN = "*"

def GetMA(data):
    """
    Store the MA(moving average) data
    """
    try:
        pass
    except Exception as e:
        return e

def StoreMA(num):
    """
    Return the MA(Moving average) data
    """
    try:
        dbhand = DBHandler.DBHandler(host=DBHOST, user=DBUSER, password=DBPASSWORD, db=DBNAME)
        date = time.localtime()
        date = "%02d%02d%02d" %(date.tm_year, date.tm_mon, date.tm_mday)
        options = "where date={0}\
                        order by time desc\
                        limit {1}".format(date, num)
        candle_datas = dbhand.DbGet(select=DBCOLUMN, ffrom=CANTABLE, options=options)
        if candle_datas == -1:
            return candle_datas
        if candle_datas == 0:
            return candle_datas
        standard_time = candle_datas[0][Candle.time.value]
        ma_value = 0
        for candle_data in candle_datas:
            ma_value += int(candle_data[Candle.closeprice.value])
        ma_value = ma_value / num
        df = DataFrame(data=[[date, standard_time, ma_value, num]], columns=['date', 'time', 'maValue', 'maNum'])
        df = df.set_index('date')
        res = dbhand.DbSend(df, MATABLE)
        if res == -1: 
            print("table is not exist")
        return res
    except Exception as e:
        return e

def StoreCandle(con,sec):
    """
    Store the candle stick data into database
    """
    try:
        dbhand = DBHandler.DBHandler(host=DBHOST, user=DBUSER, password=DBPASSWORD, db=DBNAME)
        cbit = UserAPI.Bithumb(con, sec)
        res = cbit.CandleObsStart(order_currency=COINTYPE, tickTypes=TICKTYPE)
        while True:
            data = cbit.NowCandleStick()
            if isinstance(data, int):
                print("observer is not runing")
                break
            print(data)
            res = dbhand.DbSend(data, CANTABLE)
            if res == -1: 
                print("table is not exist")
                break
    except Exception as e:
        return e
    finally:
        cbit.CandleObsStop()

def StoreTrans(con,sec):
    """
    Store the transaciton data into the database
    """
    try:
        dbhand = DBHandler.DBHandler(host=DBHOST, user=DBUSER, password=DBPASSWORD, db=DBNAME)
        tbit = UserAPI.Bithumb(con, sec)
        res = tbit.TransObsStart(order_currency=COINTYPE)
        while True:
            data = tbit.NowTransaction()
            if isinstance(data, int):
                print("observer is not runing")
                break
            print(data)
            res = dbhand.DbSend(data, TRANTABLE)
            if res == -1: 
                print("table is not exist")
                break
    except Exception as e:
        return e
    finally:
        tbit.TransObsStop()

def GetKey():
    """
    Get the connect key & secret key
    """
    try:
        with open(UserAPI.path().KeyPath(), "r") as f:
            buf = f.read().split()
        return (buf[1], buf[3])
    except Exception as e:
        return e

if __name__ == "__main__":
    try:
        conkey, seckey = GetKey()
        bithumb = UserAPI.Bithumb(conkey, seckey)
        

        # candle_th = threading.Thread(target=StoreCandle, args=(conkey,seckey))
        # candle_th.start()
        # trans_th = threading.Thread(target=StoreTrans, args=(conkey,seckey))
        # trans_th.start()

        # candle_th.join()
        # trans_th.join()

        print(StoreMA(num=20))
    except Exception as e:
        print(e)
    
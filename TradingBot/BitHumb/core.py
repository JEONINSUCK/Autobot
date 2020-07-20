import UserAPI
import DBHandler
import threading

def StoreCandle(con,sec):
    try:
        dbhand2 = DBHandler.DBHandler(host="localhost", user='root', password='root', db='test')
        cbit = UserAPI.Bithumb(con, sec)
        res = cbit.CandleObsStart(order_currency="BTC", tickTypes="30M")
        while True:
            data = cbit.NowCandleStick()
            if isinstance(data, int):
                print("observer is not runing")
                break
            print(data)
            res = dbhand2.Hander(data, "candle_test")
            if res == -1: 
                print("table is not exist")
                break
    except Exception as e:
        return e
    finally:
        cbit.CandleObsStop()

def StoreTrans(con,sec):
    try:
        dbhand1 = DBHandler.DBHandler(host="localhost", user='root', password='root', db='test')
        tbit = UserAPI.Bithumb(con, sec)
        res = tbit.TransObsStart(order_currency="BTC")
        while True:
            data = tbit.NowTransaction()
            if isinstance(data, int):
                print("observer is not runing")
                break
            print(data)
            res = dbhand1.Hander(data, "trans_test")
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
        

        candle_th = threading.Thread(target=StoreCandle, args=(conkey,seckey))
        candle_th.start()
        trans_th = threading.Thread(target=StoreTrans, args=(conkey,seckey))
        trans_th.start()

        candle_th.join()
        trans_th.join()
    except Exception as e:
        print(e)
    
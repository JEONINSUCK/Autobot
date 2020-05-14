# from TradingBot.BitHumb.OpenAPI import *
from OpenAPI import *
import datetime

class Bithumb():
    def __init__(self, con_key, secr_key):
        self.pri_api = Private(con_key, secr_key)
        self.pblc_api = Public()

    def get_ticker(self, order_currency="BTG", payment_currency="KRW"):
        try:
            pars_data = {}
            resp = self.pblc_api.Ticker(order_currency=order_currency, payment_currency=payment_currency)
            if(resp['status'] != "0000"):
                return resp['message']
            resp = resp['data']
            pars_data.update(
                            {"권종": order_currency,
                            "시가": resp['opening_price'],
                            "현재가": resp['closing_price'],
                            "시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
            return pars_data
        except Exception as e:
            return(e)
    

if __name__ == "__main__":
    start = time.time()
    with open(Path().KeyPath(), "r") as f:
        buf = f.read().split()
        connect = buf[1]
        secret = buf[3]

    test = Bithumb(connect, secret)
    print(test.get_ticker())

    print("\ntime: {} 초".format(time.time() - start))
    # print(time.gmtime(time.time()))
    
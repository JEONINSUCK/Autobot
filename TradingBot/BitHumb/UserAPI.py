# from TradingBot.BitHumb.OpenAPI import *
from OpenAPI import *
import datetime

class Bithumb():
    def __init__(self, con_key, secr_key):
        self.pri_api = Private(con_key, secr_key)
        self.pblc_api = Public()
        self.order_id_list = []

    
    def GetPrice(self, order_currency="BTG", payment_currency="KRW"):
        """
        Get the coin price

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            pars_data = {}
            resp = self.pblc_api.Ticker(order_currency=order_currency, payment_currency=payment_currency)

            if 'message' in resp:
                return resp["message"]
            resp = resp['data']

            if order_currency is "ALL":
                del resp['date']
                for key in resp:
                    pars_data.update(
                                    {key: {
                                    "시가": float(resp[key]['opening_price']),
                                    "현재가": float(resp[key]['closing_price']),
                                    "시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    }})
                return pars_data
            else:
                pars_data.update(
                                {order_currency: {
                                "시가": float(resp['opening_price']),
                                "현재가": float(resp['closing_price']),
                                "시간": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }})
                return pars_data
        except Exception as e:
            return(e)
    
    
    def GetTicker(self, payment_currency="KRW"):
        """
        Get the kind of coin

        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            resp = self.pblc_api.Ticker(order_currency="ALL", payment_currency=payment_currency)
            resp = resp['data']
            del resp['date']
            return resp.keys()
        except Exception as e:
            return e

    def OrderBuy(self, units, price, type=BUY, order_currency="BTG", payment_currency="KRW"):
        """
        Order to buy the coin

        * Param units: coin quantity
        * Param price: coin price
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            resp = self.pri_api.Place(units=units, price=price, type=type, order_currency=order_currency, payment_currency=payment_currency)
            if 'message' in resp:
                return resp["message"]
            self.order_id_list.append(resp["order_id"])
            return {order_currency: {"order_id": resp['order_id']}}
        except  Exception as e:
            return e

    def OrderSell(self, units, price, type=SELL, order_currency="BTG", payment_currency="KRW"):
        """
        Order to sell the coin

        * Param units: coin quantity
        * Param price: coin price
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            resp = self.pri_api.Place(units=units, price=price, type=type, order_currency=order_currency, payment_currency=payment_currency)
            if 'message' in resp:
                return resp["message"]
            return {order_currency: {"order_id": resp['order_id']}}
        except  Exception as e:
            return e

    def OrderCancel(self, type, order_id, order_currency="BTG", payment_currency="KRW"):
        """
        Cancel the watting order

        * Param type: SELL, BUY
        * Param order_id: your order number
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            resp = self.pri_api.Cancel(type=type, order_id=order_id, order_currency=order_currency, payment_currency=payment_currency)
            if "message" in resp:
                return resp['message']
            return resp
        except Exception as e:
            return e

    
    def GetOrderID(self):
        """
        Get the order id list

        * return type: list
        """
        try:
            resp = self.pri_api.Order(type=None, order_id=None)
            if "message" in resp:
                return resp['message']
            resp = resp['data']
            return resp
        except Exception as e:
            return e

if __name__ == "__main__":
    start = time.time()
    with open(Path().KeyPath(), "r") as f:
        buf = f.read().split()
        connect = buf[1]
        secret = buf[3]

    test = Bithumb(connect, secret)
    # print(test.GetPrice())
    # print(test.GetTicker())
    # print(test.OrderBuy(units=0.2, price=10800))
    # print(test.OrderSell(units=1, price=10800))
    # print(test.GetOrderID())
    # print(test.OrderCancel(type=BUY, order_id=))
    print(test.GetOrderID())



    print("\ntime: {} 초".format(time.time() - start))
    # print(time.gmtime(time.time()))
    
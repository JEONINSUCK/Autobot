# from TradingBot.BitHumb.OpenAPI import *
from OpenAPI import *
import datetime

class Bithumb():
    def __init__(self, con_key, secr_key):
        # self.pri_api = Private(con_key, secr_key)
        self.con_key = con_key
        self.secr_key = secr_key
        self.order_id_dict = {"buy": [], "sell": []}

    
    def GetPrice(self, order_currency="BTG", payment_currency="KRW"):
        """
        Get the coin price

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        """
        try:
            pars_data = {}
            resp = Public().Ticker(
                                order_currency=order_currency, 
                                payment_currency=payment_currency)

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
            resp = Public().Ticker(
                                order_currency="ALL", 
                                payment_currency=payment_currency)
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
            resp = Private(self.con_key, self.secr_key).Place(
                                                            units=units, 
                                                            price=price, 
                                                            type=type, 
                                                            order_currency=order_currency, 
                                                            payment_currency=payment_currency)
            if 'message' in resp:
                return resp["message"]
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
            resp = Private(self.con_key, self.secr_key).Place(
                                                            units=units, 
                                                            price=price, 
                                                            type=type, 
                                                            order_currency=order_currency, 
                                                            payment_currency=payment_currency)
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
            resp = Private(self.con_key, self.secr_key).Cancel(
                                                            type=type, 
                                                            order_id=order_id, 
                                                            order_currency=order_currency, 
                                                            payment_currency=payment_currency)
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
            resp = Private(self.con_key, self.secr_key).Order(
                                                            type=None, 
                                                            order_id=None)
            if "message" in resp:
                return resp['message']
            resp = resp['data']
            for res in resp:
                if res['type'] == BUY:
                    self.order_id_dict["buy"].append(res['order_id'])
                elif res['type'] == SELL:
                    self.order_id_dict["sell"].append(res['order_id'])
            return self.order_id_dict
        except Exception as e:
            return e

    def CancelAll(self):
        """
        Cancel all of the order

        * Param order_id_dict: return value of GetOrderId() method
        * return type: str(message)
        """
        try:
            resp = self.GetOrderID()
            for res in resp:
                for orderid in resp[res]:
                    if res == "buy":
                        state_code = self.OrderCancel(type=BUY, order_id=orderid)['status']
                    elif res == "sell":
                        state_code = self.OrderCancel(type=SELL, order_id=orderid)['status']
                    if state_code != "0000": 
                        return state_code
                    print("{} was canceled".format(orderid))
            return 0
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
    print(test.CancelAll())
    



    print("\ntime: {} 초".format(time.time() - start))
    # print(time.gmtime(time.time()))
    
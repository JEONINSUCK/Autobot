import requests
import time
import pybithumb
from xcoin_api_client import *

DEFUALTPATH = "https://api.bithumb.com"
TICKERPATH = "/public/ticker"
ORDERBOOKPATH = "/public/orderbook"
TRANSHISPATH = "/public/transaction_history"
BALANCEPATH = "/info/balance"
BTCIPATH = "/public/btci"

class Public():
    def __init__(self, debug=0):
        self.debug = debug
        # self.connect_key = connect_key
        # self.secret_key = secret_key

    def Ticker(self, order_currency="ALL", payment_currency="KRW"):
        """
        Get current price of the coin
        docs: https://apidocs.bithumb.com/docs/ticker

        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        * return unit: 원(KRW)
        * return exam:
        {
        "status": "0000",
        "data": {
            "opening_price": "504000",
            "closing_price": "505000",
            "min_price": "504000",
            "max_price": "516000",
            "units_traded": "14.71960286",
            "acc_trade_value": "16878100",
            "prev_closing_price": "503000",
            "units_traded_24H": "1471960286",
            "acc_trade_value_24H": "16878100",
            "fluctate_24H": "1000",
            "fluctate_rate_24H": 0.19,
            "date": "1417141032622"
    }
}
        """
        try:
            url = DEFUALTPATH + TICKERPATH + "/{0}_{1}".format(order_currency, payment_currency)
            req = requests.get(url)
            return req.json()['data']
        except Exception as e:
            return -1
    
    def OrderBook(self, order_currency="ALL", payment_currency="KRW", count=10):
        """
        Get current information of order 
        docs: https://apidocs.bithumb.com/docs/order_book

        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        * return unit: 원(KRW)
        * return exam:
        {
        "status"    : "0000",
        "data"      : {
        "timestamp"         : 1417142049868,
        "order_currency"    : "BTC",
        "payment_currency"  : "KRW",
        "bids": [
            {
                "quantity"  : "6.1189306",
                "price"     : "504000"
            },
            {
                "quantity"  : "10.35117828",
                "price"     : "503000"
            }
        ],
        "asks": [
            {
                "quantity"  : "2.67575",
                "price"     : "506000"
            },
            {
                "quantity"  : "3.54343",
                "price"     : "507000"    }
}
        
        """
        try:
            url = DEFUALTPATH + ORDERBOOKPATH + "/{0}_{1}?count={2}".format(order_currency, payment_currency,count)
            req = requests.get(url)
            return req.json()['data']
        except Exception as e:
            return -1

    def TransHistory(self, order_currency="ALL", payment_currency="KRW", count=10):
        """
        Get coin transaction history
        docs: https://apidocs.bithumb.com/docs/transaction_history

        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        * return unit: 원(KRW)
        * return exam:
        {
    "status"    : "0000",
    "data"      : [
        {
            "transaction_date"  : "2018-04-10 17:47:46",
            "type"              : "bid",
            "units_traded"      : "1.0",
            "price"             : "6779000",
            "total"             : "6779000"
        },
        {
            "transaction_date"  : "2018-04-10 17:43:38",
            "type"              : "bid",
            "units_traded"      : "0.1",
            "price"             : "6779000",
            "total"             : "677900"
        },
        {
            "transaction_date"  : "2018-04-10 14:13:25",
            "type"              : "ask",
            "units_traded"      : "0.0001",
            "price"             : "7575000",
            "total"             : "758"
        }
    ]
}
        """
        try:
            url = DEFUALTPATH + TRANSHISPATH + "/{0}_{1}?count={2}".format(order_currency, payment_currency,count)
            req = requests.get(url)
            return req.json()['data']
        except Exception as e:
            return -1

    def BTCI(self):
        """
        Get Bithumb index(BTMI,BTAI)
        : It is an index that shows the overall flow of the market.
        docs: https://apidocs.bithumb.com/docs/btci

        * return type: dict
        * return unit: None
        * return exam:
        {
    "status": "0000",
    "data": {
        "btai" : {
                    "market_index " : "1000",
                    "width"  : "0",
                    "rate"   : "0",
                  },
        "btmi" : {
                    "market_index " : "1000",
                    "width"  : "0",
                    "rate"   : "0",
                  },
        "date" : "1542002781568"
    }
}
        """
        try:
            url = DEFUALTPATH + BTCIPATH
            req = requests.get(url)
            return req.json()['data']
        except Exception as e:
            return -1

        
    
    


if __name__ == "__main__":
    start = time.time()
    connect = "1168d95f1a7c1d1166e421f7b31d3f8f"
    secret = "1c9aaede2ab3ba4ce6b51cb8e4894dea"
    
    # print(Public().Ticker("BTC"))
    # print(Public().OrderBook("BTC"))
    # print(Public().TransHistory("BTC"))
    # print(Public().BTCI())
    
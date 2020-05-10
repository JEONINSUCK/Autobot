import requests
import time
import os
import pybithumb
from xcoin_api_client import *

DEFUALTCOIN = "BTG"
DEFUALTCOUNT = 5
BUY = "bid"
SELL = "ask"

DEFUALTPATH = "https://api.bithumb.com"
TICKERPATH = "/public/ticker"
ORDERBOOKPATH = "/public/orderbook"
TRANSHISPATH = "/public/transaction_history"
BALANCEPATH = "/info/balance"
BTCIPATH = "/public/btci"
ACCOUNTPATH = "/info/account"
ORDERPATH = "/info/orders"
PLACEPATH = "/trade/place"


class Public():
    def __init__(self, debug=0):
        self.debug = debug

    def Ticker(self, order_currency=DEFUALTCOIN, payment_currency="KRW"):
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
    
    def OrderBook(self, order_currency=DEFUALTCOIN, payment_currency="KRW", count=10):
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

    def TransHistory(self, order_currency=DEFUALTCOIN, payment_currency="KRW", count=10):
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

class Path():
    def __init__(self):
        self.top_path = os.getcwd()
        self.default_path = __file__
        self.key_path = "/key.lock"

    """
    Find the key.lock path

    * return type: str
    * return 
    """
    def KeyPath(self):
        dirpath = self.GetDir(self.default_path)
        if(self.CheckFile(dirpath + self.key_path)):
            return dirpath + self.key_path
    
    # Confirm it is a directory
    def CheckDir(self, path):
        return os.path.isdir(path)

    # Filter File
    def GetDir(self, path):
        return os.path.dirname(path)

    # Get the under directroy list
    def GetDirList(self, path):
        return os.listdir(path)    
    
    # Check the file whether existence and not existence
    def CheckFile(self, path):
        return os.path.exists(path)

class Private():
    def __init__(self, connect, secret, debug=0):
        self.debug = debug
        self.connect = connect
        self.secret = secret
        self.xcoin = XCoinAPI(self.connect, self.secret)

    """
    Get my account & coin trade fee
    docs: https://apidocs.bithumb.com/docs/account

    * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
    * param payment_currency: KRW
    * return type: dict
    """
    def Account(self, order_currency=DEFUALTCOIN, payment_currency="KRW"):
        try:
            rgParams = { 
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
                         }
            req = self.xcoin.xcoinApiCall(ACCOUNTPATH, rgParams)
            return req
        except Exception as e:
            return e
    
    """
    Get my asset
    docs: https://apidocs.bithumb.com/docs/balance

    * param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
    * return type: dict
    """
    def Balance(self, currency=DEFUALTCOIN):
        try:
            rgParams = { 
                        "currency": currency
                         }
            req = self.xcoin.xcoinApiCall(BALANCEPATH, rgParams)
            return req
        except Exception as e:
            return e

    def Place(self,units, price, type, order_currency=DEFUALTCOIN, payment_currency="KRW"):
        try:
            rgParms = {
                        "order_currency": order_currency,
                        "payment_currency": payment_currency,
                        "units": float(units),
                        "price": int(price),
                        "type": type
            }
            req = self.xcoin.xcoinApiCall(PLACEPATH, rgParms)
            return req
        except Exception as e:
            return e

    def Order(self, type, order_id, count=DEFUALTCOUNT, after=None, order_currency=DEFUALTCOIN, payment_currency="KRW"):
        try:
            rgParms = {
                        # "order_id": order_id,
                        # "type" : type,
                        # "count": count,
                        # "after": after,
                        "order_currency": order_currency,
                        # "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(ORDERPATH, rgParms)
            return req
        except Exception as e:
            return e
        
if __name__ == "__main__":
    start = time.time()

    with open(Path().KeyPath(), "r") as f:
        buf = f.read().split()
        connect = buf[1]
        secret = buf[3]

    pri_test = Private(connect, secret)
    # print(pri_test.Place(units=1, price=10820, type=BUY))
    print(pri_test.Order(type=BUY,order_id="C0111000000012701182"))

    # print(Path().KeyPath())
    
    # print(Public().Ticker("BTC"))
    # print(Public().OrderBook("BTC"))
    # print(Public().TransHistory("BTC"))
    # print(Public().BTCI())
    
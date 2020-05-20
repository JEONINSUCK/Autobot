import requests
import time
import os
import pybithumb
from xcoin_api_client import *

DEFAULTCOIN = "BTG"
DEFAULTPAYMENT = "KRW"
DEFAULTINTERVAL = "1m"
DEFAULTCOUNT = 100
BUY = "bid"
SELL = "ask"

DEFAULTPATH = "https://api.bithumb.com"
TICKERPATH = "/public/ticker"
ORDERBOOKPATH = "/public/orderbook"
TRANSHISPATH = "/public/transaction_history"
BALANCEPATH = "/info/balance"
BTCIPATH = "/public/btci"
ACCOUNTPATH = "/info/account"
ORDERPATH = "/info/orders"
ORDERDETAILPATH = "/info/order_detail"
TRANSPATH = "/info/user_transactions"
PLACEPATH = "/trade/place"
CANCELPATH = "/trade/cancel"
MARKETBUYPATH = "/trade/market_buy"
MARKETSELLPATH = "/trade/market_sell"
CANDLESTICKPATH = "/public/candlestick"


class Public():
    def __init__(self, debug=0):
        self.debug = debug

    def Ticker(self, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
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
            url = DEFAULTPATH + TICKERPATH + "/{0}_{1}".format(order_currency, payment_currency)
            req = requests.get(url)
            return req.json()
        except Exception as e:
            return e
    
    def OrderBook(self, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT, count=10):
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
            url = DEFAULTPATH + ORDERBOOKPATH + "/{0}_{1}?count={2}".format(order_currency, payment_currency,count)
            req = requests.get(url)
            return req.json()
        except Exception as e:
            return e

    def TransHistory(self, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT, count=10):
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
            url = DEFAULTPATH + TRANSHISPATH + "/{0}_{1}?count={2}".format(order_currency, payment_currency,count)
            req = requests.get(url)
            return req.json()
        except Exception as e:
            return e

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
            url = DEFAULTTPATH + BTCIPATH
            req = requests.get(url)
            return req.json()
        except Exception as e:
            return e

    def CandleStick(self, chart_instervals=DEFAULTINTERVAL, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Get the candle stick
        docs: https://apidocs.bithumb.com/docs/candlestick

        * Param chart_intervals: 1m(dafault), 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        """
        try:
            url = DEFAULTPATH + CANDLESTICKPATH + "/{0}_{1}/{2}".format(order_currency, payment_currency,chart_instervals)
            req = requests.get(url)
            return req.json()
        except Exception as e:
            return e

class Path():
    def __init__(self):
        self.top_path = os.getcwd()
        self.default_path = __file__
        self.key_path = "/key.lock"

    
    def KeyPath(self):
        """
        Find the key.lock path

        * return type: str
        * return 
        """
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


    def Account(self, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Get my account & coin trade fee
        docs: https://apidocs.bithumb.com/docs/account

        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParams = { 
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
                         }
            req = self.xcoin.xcoinApiCall(ACCOUNTPATH, rgParams)
            return req
        except Exception as e:
            return e
    

    def Balance(self, currency=DEFAULTCOIN):
        """
        Get my asset
        docs: https://apidocs.bithumb.com/docs/balance

        * param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * return type: dict
        """
        try:
            rgParams = { 
                        "currency": currency
                         }
            req = self.xcoin.xcoinApiCall(BALANCEPATH, rgParams)
            return req
        except Exception as e:
            return e

   
    def Place(self,units, price, type, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Order to sell or buy the coin
        docs: https://apidocs.bithumb.com/docs/place

        * Param units: coin quantity
        * Param price: coin price
        * param type: BUY, SELL
        * param currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * return type: dict
        """
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
    
    
    def Order(self, type, order_id, count=DEFAULTCOUNT, after=None, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Look up the watting transaction history
        docs: https://apidocs.bithumb.com/docs/orders

        * Param type: BUY, SELL
        * Param order_id: your order number
        * Param count: searching count
        * Param after: searching after date
        * param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        # "order_id": order_id,
                        # "type" : type,
                        "count": count,
                        # "after": after,
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(ORDERPATH, rgParms)
            return req
        except Exception as e:
            return e
    
    
    def OrderDetail(self, order_id, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Look up the traded trasaction history
        docs: https://apidocs.bithumb.com/docs/orders_detail

        * Param order_id: your order number
        * Param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        "order_id": order_id,
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(ORDERDETAILPATH, rgParms)
            return req
        except Exception as e:
            return e
    
    def Transaction(self, offset=0, count=20, searchGb=0, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Get the list of completed trade
        docs: https://apidocs.bithumb.com/docs/transactions

        * Param count: 1~50 (the number of list)
        * Param searchGb: 0 : 전체, 1 : 매수 완료, 2 : 매도 완료, 3 : 출금 중 4 : 입금, 5 : 출금, 9 : KRW 입금 중
        * Param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        "offset": offset,
                        "count": count,
                        "searchGb": searchGb,
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(TRANSPATH, rgParms)
            return req
        except Exception as e:
            return e
        pass

    def Cancel(self, type, order_id, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Cancel the watting order
        docs: https://apidocs.bithumb.com/docs/cancel

        * Param type: BUY, SELL
        * Param order_id: your order number
        * Param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        "type": type,
                        "order_id": order_id,
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(CANCELPATH, rgParms)
            return req
        except Exception as e:
            return e
    
    
    def MarketPriceBuy(self, units, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Buy the coin as market price
        docs: https://apidocs.bithumb.com/docs/market_buy

        * Param units: coin quantity
        * Param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        "units": float(units),
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(MARKETBUYPATH, rgParms)
            return req
        except Exception as e:
            return e

    
    def MarketPriceSell(self, units, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Sell the coin as market price
        docs: https://apidocs.bithumb.com/docs/market_sell

        * Param units: coin quantity
        * Param order_currency: BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/BTG/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW
        * return type: dict
        """
        try:
            rgParms = {
                        "units": float(units),
                        "order_currency": order_currency,
                        "payment_currency": payment_currency
            }
            req = self.xcoin.xcoinApiCall(MARKETSELLPATH, rgParms)
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
    # print(pri_test.Balance())
    # print(pri_test.Account())
    # print(pri_test.Place(units=1, price=10800, type=BUY))
    # print(pri_test.Order(type=SELL,order_id="C0111000000012844333")) 
    # print(pri_test.OrderDetail(order_id="C0111000000012849231"))
    # print(pri_test.Cancel(type=SELL, order_id="C0111000000012844333"))
    # print(pri_test.MarketPriceSell(units=0.8))
    # print(pri_test.MarketPrice
    # Buy(units=0.8))
    # print(pri_test.Transaction())

    # print(Path().KeyPath())
    
    # print(Public().Ticker("BTG"))
    # print(Public().OrderBook("BTG"))
    # print(Public().TransHistory("BTC"))
    # print(Public().BTCI())
    print(Public().CandleStick())
    
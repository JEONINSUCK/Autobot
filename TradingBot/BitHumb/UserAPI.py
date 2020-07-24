# from TradingBot.BitHumb.OpenAPI import *
from OpenAPI import *
from DBHandler import *
from datetime import datetime
from pandas import DataFrame
from pandas import to_datetime

class Bithumb():
    def __init__(self, con_key, secr_key):
        # self.pri_api = Private(con_key, secr_key)
        self.con_key = con_key
        self.secr_key = secr_key
        self.order_id_dict = {"buy": [], "sell": []}

        self.info = LiveInfo()


    def GetPrice(self, order_currency="BTG", payment_currency="KRW"):
        """
        Get the coin price

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {
                                        "시가": value,
                                        "현재가": value,
                                        "시간": value }})
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
                                    "시간": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                    }})
                return pars_data
            else:
                pars_data.update(
                                {order_currency: {
                                "시가": float(resp['opening_price']),
                                "현재가": float(resp['closing_price']),
                                "시간": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                }})
                return pars_data
        except Exception as e:
            return(e)
    
    
    def GetTicker(self, payment_currency="KRW"):
        """
        Get the kind of coin

        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {value, value, ...}
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

    def DesignBuy(self, units, price, type=BUY, order_currency="BTG", payment_currency="KRW"):
        """
        Reservate to buy the coin

        * Param units: coin quantity
        * Param price: coin price
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {order_id: value}}
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

    def DesignSell(self, units, price, type=SELL, order_currency="BTG", payment_currency="KRW"):
        """
        Reservate to sell the coin

        * Param units: coin quantity
        * Param price: coin price
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {order_id: value}}
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

        * return type: dict
        * return value: {'buy': [], 'sell': []}
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

    def GetOrderDetail(self, order_id, order_currency="BTG", payment_currency="KRW"):
        """
        Get the information of the order detaily

        * Param order_id: your order number
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {
                                            "매수/매도": value,
                                            "주문금액": value,
                                            "주문수량": value,
                                            "주문상태": value,
                                            "취소날짜": value,
                                            "주문시간": value }})
        """
        try:
            pars_data = {}
            resp = Private(self.con_key, self.secr_key).OrderDetail(
                                                                    order_id=order_id,
                                                                    order_currency=order_currency, 
                                                                    payment_currency=payment_currency)
            if 'message' in resp:
                return resp['message']
            resp = resp['data']
            if(resp['type'] == "bid"):
                ordertype = "매수"
            else:
                ordertype = "매도"
            pars_data.update({order_currency: {
                                            "매수/매도": ordertype,
                                            "주문금액": resp['order_price'],
                                            "주문수량": resp['order_qty'],
                                            "주문상태": resp['order_status'],
                                            "취소날짜": resp['cancel_date'],
                                            "주문시간": resp['order_date']}
                                            })
            return pars_data
        except Exception as e:
            return e

    def GetTransHis(self, offset=0, count=20, searchGb=0, order_currency="BTG", payment_currency="KRW"):
        """
        Get the transaction history

        * Param count: 20(Default) 1-50 (the number of lists)
        * Param searchGb: 0(Defualt) : 전체, 1 : 매수 완료, 2 : 매도 완료, 3 : 출금 중 4 : 입금, 5 : 출금, 9 : KRW 입금 중
        * Param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * Param payment_currency: KRW(Default)
        * return type: dict
        * return value: 'transfer_date':{
                                            "거래구분": value,
                                            "거래코인": value,
                                            "거래수량": value,
                                            "1개당금액": value,
                                            "거래금액": value,
                                            "거래수수료": value,
                                            "잔여수량": value,
                                            "잔여금액": value 
        """
        try:
            pars_data = {order_currency: {}}
            resp = Private(self.con_key, self.secr_key).Transaction(
                                                                offset=offset, 
                                                                count=count, 
                                                                searchGb=searchGb, 
                                                                order_currency=order_currency, 
                                                                payment_currency=payment_currency)
            if 'message' in resp:
                return resp['message']
            resp = resp['data']
            
            for res in resp:
                if res['search'] == "1":
                    search_type = "구매완료"
                elif res['search'] == "2":
                    search_type = "판매완료"
                elif res['search'] == "3":
                    search_type = "출금중"
                elif res['search'] == "4":
                    search_type = "입금"
                elif res['search'] == "5":
                    search_type = "출금"
                elif res['search'] == "9":
                    search_type = "KRW입금중"

                pars_data[order_currency].update({
                                res['transfer_date']:{
                                                    "거래구분": search_type,
                                                    "거래코인": res['order_currency'],
                                                    "거래수량": res['units'],
                                                    "1개당금액": res['price'],
                                                    "거래금액": res['amount'],
                                                    "거래수수료": res['units'],
                                                    "잔여수량": res['order_balance'],
                                                    "잔여금액": res['payment_balance']                            
                 }})
            return pars_data
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

    def GetBalance(self, currency):
        """
        Get my asset

        * param currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * return type: dict
        * return value: {currency: {
                                    "보유금액": value,
                                    "예약금액": value,
                                    "사용가능금액": value,
                                    "보유코인": value,
                                    "판매가능코인": value,
                                    "판매예약수량": value
        }}
        """
        try:
            pars_data = {}
            resp = Private(self.con_key, self.secr_key).Balance(
                                                                currency=currency)
            if 'message' in resp:
                return resp['message']
            resp = resp['data']
            pars_data.update({currency: 
                            {"보유금액": resp['total_krw'],
                            "예약금액": resp['in_use_krw'],
                            "사용가능금액": resp['available_krw'],
                            "보유코인": resp["total_"+currency.lower()],
                            "판매가능코인": resp['available_'+currency.lower()],
                            "판매예약수량": resp['in_use_'+currency.lower()]}
            })
            return pars_data
        except Exception as e:
            return e

    def GetTradeFee(self, order_currency="BTG", payment_currency="KRW"):
        """
        Get the trade fee

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: { order_currency: {"거래수수료": value}}
        """
        try:
            resp = Private(self.con_key, self.secr_key).Account(
                                                            order_currency=order_currency,
                                                            payment_currency=payment_currency)
            if 'message' in resp:
                return resp['message']
            resp = resp['data']
            return { order_currency: {"거래수수료": resp['trade_fee']}}
        except Exception as e:
            return e
    
    def MarketBuy(self, units, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Buy the coin at market price

        * Param units: coin quantity
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {"order_id": value}}
        """
        try:
            resp = Private(self.con_key, self.secr_key).MarketPriceBuy(
                                                                    units=units,
                                                                    order_currency=order_currency,
                                                                    payment_currency=payment_currency)
            if 'message' in resp:
                return resp['message']
            return {order_currency: {"order_id": resp['order_id']}}
        except Exception as e:
            return e

    def MarketSell(self, units, order_currency=DEFAULTCOIN, payment_currency=DEFAULTPAYMENT):
        """
        Sell the coin at market price

        * Param units: coin quantity
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: dict
        * return value: {order_currency: {"order_id": value}}
        """
        try:
            resp = Private(self.con_key, self.secr_key).MarketPriceSell(
                                                                    units=units,
                                                                    order_currency=order_currency,
                                                                    payment_currency=payment_currency)
            if 'message' in resp:
                return resp['message']
            return {order_currency: {"order_id": resp['order_id']}}
        except Exception as e:
            return e

    def GetCandleStick(self, chart_instervals="1m", order_currency="BTG", payment_currency="KRW"):
        """
        Get the candle stick

        * Param chart_instervals: 1m(dafault), 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: Dataframe
        * return value: columns[time, open, close, high, low, volume], index[time]
        """
        try:
            pars_data = {}
            resp = Public().CandleStick(
                                        chart_instervals=chart_instervals,
                                        order_currency=order_currency,
                                        payment_currency=payment_currency
            )
            if 'message' in resp:
                return resp['message']

            resp = resp['data']
            df = DataFrame(data=resp, columns=['time', 'open', 'close', 'high', 'low', 'volume'])
            df = df.set_index('time')
            df.index = to_datetime(df.index, unit='ms')
            return df.astype(float)
        except Exception as e:
            return e

    def GetVolumes(self, count=20, order_currency="BTG", payment_currency="KRW"):
        """
        Get current transaction history

        * Param count: Get the count
        return type: Dataframe
        return value: columns[type, units_traded, price, total], index[transaction_date]
        """
        try:
            resp = Public().TransHistory(
                                        count=count,
                                        order_currency=order_currency,
                                        payment_currency=payment_currency
            )
            if 'message' in resp:
                return resp['message']

            resp = resp['data']
            df = DataFrame(data=resp)
            df = df.set_index('transaction_date')
            return df
        except Exception as e:
            return e

    def GetMAL(self, number, chart_instervals="1m", order_currency="BTG", payment_currency="KRW"):
        """
        Get the MAL(Moving Everage Line)

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * param payment_currency: KRW(Default)
        * return type: Dataframe
        * return value:
        """
        try:
            MAL_list = []
            resp = self.GetCandleStick(
                                    chart_instervals=chart_instervals,
                                    order_currency=order_currency,
                                    payment_currency=payment_currency
            )

            index = resp.index[number-1::]
            for i in range(len(resp)-number):
                summ = 0
                for j in range(number):
                    summ += resp.iloc[i+j].loc['close']
                MAL = summ / number
                MAL_list.append(MAL)
                # print("{} -> {}".format(index[i],MAL))

            df = DataFrame(data=MAL_list, index=index[:len(MAL_list):], columns=['MA'])
            return df
        except Exception as e:
            return e

    def NowCandleStick(self):
        """
        Get the current candle stick

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * return type: Dataframe
        * return value: columns['value', 'volume', 'sellVolume', 'buyVolume', 'prevClosePrice', 'chgRate', 'chgAmt', 'volumePower']
                        index ['data']
        """
        try:
            rm_keys = ['value', 'volume', 'sellVolume', 'buyVolume', 'prevClosePrice', 'chgRate', 'chgAmt', 'volumePower']
            while True:
                resp = self.info.GetCandleData()
                if resp == -1:
                    return resp
                if resp == -2: 
                    continue
                resp = resp['content']
                for rm_key in rm_keys: del resp[rm_key]
                df = DataFrame(data=[resp])
                df = df.set_index('date')
                return df
        except Exception as e:
            return e
    
    def NowTransaction(self):
        """
        Get the current transaction

        * param order_currency: BTG(Default)/BTC/ETH/DASH/LTC/ETC/XRP/BCH/XMR/ZEC/QTUM/EOS/ICX/VEN/TRX/ELF/MITH/MCO/OMG/KNC
        * return type: Dataframe
        * return value: columns['buySellGb', 'contPrice', 'contQty', 'contAmt', 'symbol']
                        index ['contDtm']
        """
        try:
            while True:
                resp = self.info.GetTransData()
                if resp == -1:
                    return resp
                if resp == -2: 
                    continue
                resp = resp['content']['list']
                for res in resp: del res['updn']
                df = DataFrame(data=resp)
                df = df.set_index('contDtm')
                return df
        except Exception as e:
            return e
    
    def TransObsStart(self, order_currency="BTG"):
        """
        Start Transaction observer thread
        """
        try:
            self.info.trans_run = 1
            th =  threading.Thread(target=self.info.TransThread, args=(order_currency+"_KRW",))
            th.start()
        except Exception as e:
            return e
    
    def TransObsStop(self):
        """
        Stope Transaction observer thread
        """
        try:
            self.info.TransThreadStop()
        except Exception as e:
            return e

    def CandleObsStart(self, tickTypes, order_currency="BTG"):
        """
        Start candlestick observer thread
        """
        try:
            self.info.candle_run = 1
            th =  threading.Thread(target=self.info.CandleThread, args=(order_currency+"_KRW",tickTypes))
            th.start()
            return th
        except Exception as e:
            return e
    
    def CandleObsStop(self):
        """
        Stop candlestick observer thread
        """
        try:
            self.info.CandleThreadStop()
        except Exception as e:
            return e

    # def GetMA(self, ma):
    #     """
    #     Return the MA(Moving average) data
    #     """
    #     try:
            
    #     except Exception as e:
    #         return e

class path(Path):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    start = time.time()
    with open(path().KeyPath(), "r") as f:
        buf = f.read().split()
        connect = buf[1]
        secret = buf[3]

    test = Bithumb(connect, secret)
    # print(test.GetPrice())
    # print(test.GetTicker())
    # print(test.DesignBuy(units=0.1, price=10800))
    # print(test.DesignSell(units=0.1, price=11000))
    # print(test.GetOrderID())
    # print(test.OrderCancel(type=BUY, order_id=))
    # print(test.CancelAll())
    # print(test.GetBalance(currency="BTG"))
    # print(test.GetTradeFee(order_currency="BTG"))
    # print(test.GetOrderDetail(test.GetOrderID()['buy'][0]))
    # print(test.GetTransHis())
    # print(test.MarketBuy(units=0.1))
    # print(test.MarketSell(units=0.6))
    # print(test.GetCandleStick(chart_instervals="1m"))
    # print(test.GetVolumes())
    # print(test.GetMAL(number=5))

    # test.CandleObsStart(order_currency="BTC", tickTypes="30M")
    # while True:
    #     data = test.NowCandleStick()
    #     if isinstance(data, int):
    #         break
    #     print(test.NowCandleStick())
        # test.CandleObsStop()
 
    
    # test.TransObsStart(order_currency="BTC")
    # while True:
    #     data = test.NowTransaction()
    #     if isinstance(data, int) == True:
    #         print("int")
    #         break
    #     print(data)
    #     test.TransObsStop()

    # a = dateti
    # e.fromtimestamp(time.time())
    
    # print(time.time() * 1000)
    # b = round(time.time() * 1000)
    # print(datetime.fromtimestamp(b/1000))
    # # print(datetime.strftime("%Y-%m-%d %H:%M:%S"))

    print("\ntime: {} 초".format(time.time() - start))
    # print(time.gmtime(time.time()))
    
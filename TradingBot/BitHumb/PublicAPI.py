import requests

DEFUALTPATH = "https://api.bithumb.com"
TICKERPATH = "/public/ticker"
BALANCEPATH = "/info/balance"

class Public():
    def __init__(self, connect_key, secret_key, debug=0):
        self.debug = debug
        self.connect_key = connect_key
        self.secret_key = secret_key

    def Ticker(self, order_currency, payment_currency="KRW"):
        url = DEFUALTPATH + TICKERPATH + "/{0}_{1}".format(order_currency, payment_currency)
        req = requests.get(url)
        return req.content.decode()

    def SignSet(self, path, nonce, *kwargs):
        query_string = path + chr(0)
    
    def Balance(self):
        url = DEFUALTPATH + BALANCEPATH
        data = {"apiKey": self.connect_key,
                "secretKey": self.secret_key
                }
        req = requests.post(url, data)
        print(req)
        return req.text
        
    
    


if __name__ == "__main__":
    connect = "1168d95f1a7c1d1166e421f7b31d3f8f"
    secret = "1c9aaede2ab3ba4ce6b51cb8e4894dea"
    test = Public(connect, secret, debug=1)
    print(test.Balance())
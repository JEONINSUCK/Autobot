import os
import uuid
import jwt
from urllib.parse import urlencode
import requests

DEFAULTPATH = "https://api.upbit.com/"
ACCOUNTPATH = "v1/accounts/"

class Exchange():
    def __init__(self,secret, access, debug=0):
        self.debug = debug
        self.access_key = access
        self.secret_key = secret

    def LookUp(self):
        try:
            url = DEFAULTPATH + ACCOUNTPATH
            header = self.HeaderSet()
            res = requests.get(url, headers=header)
            print(res.json())
        except Exception as e:
            print(e)

    def HeaderSet(self):
        payload = {'access_key': self.access_key,
                        'nonce': str(uuid.uuid4())
                        }
        
        jwt_token = jwt.encode(payload, self.secret_key).decode('utf-8')
        auth_token = 'Bearer {}'.format(jwt_token)
        header = {"Authorization": auth_token}
        return header

if __name__ == "__main__":
    access  = "UAid1P5ICY7ELWx0c9lBYeQCLkbCquFkaNCxLn8g"
    secret = "ulRrMuojx08hw3469xvIXR456rzrcxdqGZbzpxt1"
    test = Exchange(secret=secret, access=access, debug=1)
    test.LookUp()
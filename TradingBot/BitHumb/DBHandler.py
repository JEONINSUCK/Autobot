import pymysql
from sqlalchemy import create_engine
from sqlalchemy import exc
from OpenAPI import *
from UserAPI import *
import pandas

class DBHandler():
    def __init__(self, host, user, password, db, debug=0):
        self.debug = debug
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def DbSend(self, dataframe, table):
        """
        Store the data into the DB

        * return value: 0 = complete
                        -1 = "table is not exist"
        """
        try:
            if self.TableCheck(table=table):
                engine = create_engine("mysql+pymysql://{0}:{1}@{2}/{3}".format(self.user, self.password, self.host, self.db))
                dataframe.to_sql(table, con=engine, if_exists="append")
                return 0
            return -1
        except exc.OperationalError as e:
            return e
        except Exception as e:
            return e

    def DbGet(self, select, ffrom, options=None):
        """
        Get the data into the DB

        * return value: 0 = no data about query
        """
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
            with con.cursor() as cur:
                if options == None:
                    query = "SELECT {0} \
                        FROM {1}".format(select, ffrom)
                else:
                    query = "SELECT {0} \
                            FROM {1}\
                            {2}".format(select, ffrom, options)
                if cur.execute(query) == 0:
                    return -1
                return cur.fetchall()

        except Exception as e:
            return e

    def TableCheck(self, table):
        """
        Table exists check
        """
        try:
            con = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db)
            with con.cursor() as cur:
                query = "SELECT * \
                        FROM INFORMATION_SCHEMA.TABLES\
                        WHERE TABLE_TYPE = 'BASE TABLE'\
                        AND TABLE_NAME = '{}'".format(table)
                if cur.execute(query) != 1:
                    return False
                return True
        except Exception as e:
            return e

if __name__ == "__main__":
    try:
        with open(Path().KeyPath(), "r") as f:
                buf = f.read().split()
                connect = buf[1]
                secret = buf[3]

        bit = Bithumb(connect, secret)
        dbhand = DBHandler(host="localhost", user='root', password='root', db='test')

        print(dbhand.DbGet(select="*", ffrom="candle_test", options="where date=20200720 and time<=165000 limit 5"))
        # # res = bit.CandleObsStart(order_currency="BTC", tickTypes="30M")
        # res = bit.TransObsStart(order_currency="BTC")
        # while True:
        #     data = bit.NowTransaction()
        #     if isinstance(data, int):
        #         print("observer is not runing")
        #         break
        #     print(data)
        #     res = dbhand.DbSend(data, "trans_test")
        #     if res == -1: 
        #         print("table is not exist")
        #         break
        
    except Exception as e:
        print(e)
    # finally:
    #     bit.TransObsStop()
    # pass
    
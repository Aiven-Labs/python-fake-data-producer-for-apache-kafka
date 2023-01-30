from faker.providers import BaseProvider
import random
import time
from yahoo_fin import stock_info as si

StockNames = ["BTC-USD", "ETH-USD", "BNB-USD", "ADA-USD", "DOGE-USD"]


class RealStockProvider(BaseProvider):
    def stock_name(self):
        return random.choice(StockNames)

    def stock_value(self, stockname):
        nextval = si.get_live_price(stockname)
        return nextval

    def produce_msg(self):
        stockname = self.stock_name()
        ts = time.time()
        message = {
            "stock_name": stockname,
            "stock_value": self.stock_value(stockname),
            "timestamp": int(ts * 1000),
        }
        key = {"stock_name": stockname}
        return message, key

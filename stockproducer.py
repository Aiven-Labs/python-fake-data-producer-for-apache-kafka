from faker.providers import BaseProvider
import random
import time


StockNames = [
    "Deja Brew",
    "Jurassic Pork",
    "Lawn & Order",
    "Pita Pan",
    "Bread Pitt",
    "Indiana Jeans",
    "Thai Tanic",
]
StockCurrentValues = [10.0, 20.1, 20.2, 12.1, 25.1, 25.1, 27.5]
StockUpProb = [0.5, 0.6, 0.7, 0.8, 0.9, 0.4, 0.3]
ShuffleProb = 0.2
ChangeAmount = 0.8


class StockProvider(BaseProvider):
    def stock_name(self):
        return random.choice(StockNames)

    def stock_value(self, stockname):
        indexStock = StockNames.index(stockname)
        currentval = StockCurrentValues[indexStock]
        goesup = 1
        if random.random() > StockUpProb[indexStock]:
            goesup = -1
        nextval = currentval + random.random() * ChangeAmount * goesup
        StockCurrentValues[indexStock] = nextval

        return nextval

    def reshuffle_probs(self, stockname):
        indexStock = StockNames.index(stockname)
        StockUpProb[indexStock] = random.random()

    def produce_msg(self):
        stockname = self.stock_name()
        ts = time.time()
        if random.random() > ShuffleProb:
            self.reshuffle_probs(stockname)
        message = {
            "stock_name": stockname,
            "stock_value": self.stock_value(stockname),
            "timestamp": int(ts * 1000),
        }
        key = {"user": "all_users"}
        return message, key

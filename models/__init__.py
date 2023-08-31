import os

from mysql import connector
from dotenv import load_dotenv
from arbitrage_trading.utils import create_xlsx

load_dotenv()


class Database:
    def __init__(self):
        self.db = connector.connect(host=os.environ.get("DB_HOST"), user=os.environ.get("DB_USER"),
                                    passwd=os.environ.get("DB_PASSWORD"), db=os.environ.get("DB_NAME"))

    def get_all_distinct_assets(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT DISTINCT harmonized_symbol from price;")

            high_stake = []
            data = []
            symbols = cursor.fetchall()

            for row in symbols:
                cursor.execute(f"select * from price where harmonized_symbol='{row[0]}' order by ask desc")
                basket = cursor.fetchall()
                if basket.__len__() >= 2:
                    profit = round(float(basket[0][6]) - float(basket[-1][5]), 2)
                    win_percent = round(profit * 100 / float(basket[0][6]), 2)
                    if win_percent > 1:
                        high_stake.append(f"{win_percent}% - Buy {basket[-1][2]} on {basket[-1][1]} at {basket[-1][6]} and Sell on {basket[0][1]} at {basket[0][5]}")
                        data += ([("Buy", basket[-1][2], basket[-1][1], basket[-1][6], f"{win_percent}%", profit, "Sell", basket[0][5], basket[0][1])])

            heads = ["Action", "symbol", "exchange", "ask price", "win percent", "expected profit", "arbitrage",
                     "bid price", "arbitrage exchange"]
            create_xlsx("arbitrage", heads, data)

            self.db.close()
        except Exception as e:
            print("Exception ", e)

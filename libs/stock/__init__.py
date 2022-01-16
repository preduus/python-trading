import json
import os.path

import pandas


class Stock:

    stock: list = []

    def __init__(self):
        self.generate_stock_data()

    def set_stock_data(self, stock_data):
        self.stock = stock_data

    def stock_dataframe(self):
        df = pandas.DataFrame(self.stock)
        df.rename(columns={"max": "high", "min": "low"}, inplace=True)
        return df

    def generate_stock_data(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(f"{dirr}/data.json", "r") as f:
            self.stock = json.loads(f.read())

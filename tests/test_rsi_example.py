import unittest

import pandas

from examples.rsi import RsiExample


class TestRsiStrategy(unittest.TestCase):

    def setUp(self) -> None:
        self.strategy = RsiExample()

    def test_get_stock_data(self):
        self.assertIsInstance(self.strategy.get_stock_data(), list, "Stock data type list. ok!")
        self.assertTrue(len(self.strategy.get_stock_data()) > 0, "Stock data is not empty. ok!")

    def test_create_dataframe(self):
        self.strategy.create_dataframe()
        self.assertIsInstance(self.strategy.dataframe, pandas.DataFrame, "DataFrame initialization. ok!")
        self.assertTrue(len(self.strategy.dataframe.index) > 0, "DataFrame data is not empty. ok!")

    def test_strategy(self):
        self.assertIsInstance(self.strategy.strategy(), tuple, "Strategy classmethod returns correct type. ok!")


if __name__ == "__main__":
    unittest.main()

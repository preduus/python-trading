import pandas
from typing import Union

from libs.stock import Stock
from libs.indicators import Indicators
from . import ExamplesInterface

from .common.trigger import get_entry_momment


class ChineseExample(Stock, ExamplesInterface):
    dataframe: pandas.DataFrame
    market_orders_stock_details: list = []

    def __init__(self, stock_data: Union[list, None] = None):
        super().__init__()

        """ Set custom stock data """
        if stock_data is not None:
            self.set_stock_data(stock_data)

        self.create_dataframe()
        self.indicators = Indicators(self.dataframe)

    def get_stock_data(self) -> list:
        return self.stock

    def create_dataframe(self):
        self.dataframe = self.stock_dataframe()

    def strategy(self, condition_type: Union[str, None] = None) -> tuple:
        ssma_3 = self.indicators.ssma(3)
        ssma_50 = self.indicators.ssma(50)
        dev, dev_color = self.indicators.deviation(20)

        """ Strategy conditions """
        strategy_buy_conditions = (ssma_3.iloc[-1] > ssma_50.iloc[-1] and ssma_3.iloc[-2] < ssma_50.iloc[
            -2] and dev[0] > 0 and dev[0] > dev[1])
        strategy_sell_conditions = (ssma_3.iloc[-1] < ssma_50.iloc[-1] and ssma_3.iloc[-2] > ssma_50.iloc[
            -2] and dev[0] < 0 and dev[0] < dev[1])

        entry_signal, entry_direction = get_entry_momment(strategy_buy_conditions, strategy_sell_conditions,
                                                          condition_type)

        if entry_signal:
            self.market_orders_stock_details.append({
                "direction": entry_direction,
                "indicators": [
                    {"name": "SSMA 3 Periods", "value": ssma_3.iloc[-1]},
                    {"name": "SSMA 3 Periods [Closed]", "value": ssma_3.iloc[-2]},
                    {"name": "SSMA 50 Periods", "value": ssma_50.iloc[-1]},
                    {"name": "SSMA 50 Periods [Closed]", "value": ssma_50.iloc[-2]},
                    {"name": "MA Deviation", "value": dev},
                    {"name": "MA Deviation Color", "value": dev_color},
                ],
                "candle": self.dataframe.iloc[-1]
            })

        return entry_signal, entry_direction

    def market_order_stock_details(self) -> dict:
        return self.market_orders_stock_details[-1]

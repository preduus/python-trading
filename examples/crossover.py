import pandas
from typing import Union

from libs.stock import Stock
from libs.indicators import Indicators
from . import ExamplesInterface

from .common.trigger import get_entry_momment


class CrossoverExample(Stock, ExamplesInterface):
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
        crossover, (fast_ma, slow_ma) = self.indicators.crossover(fast_ma_period=7, slow_ma_period=20)

        """ Strategy conditions """
        strategy_buy_conditions = (crossover == "buy")
        strategy_sell_conditions = (crossover == "sell")

        entry_signal, entry_direction = get_entry_momment(strategy_buy_conditions, strategy_sell_conditions,
                                                          condition_type)

        if entry_signal:
            self.market_orders_stock_details.append({
                "direction": entry_direction,
                "indicators": [
                    {"name": "Fast MA 7 Periods", "value": fast_ma.iloc[-1]},
                    {"name": "Fast MA 7 Periods [Closed]", "value": fast_ma.iloc[-2]},
                    {"name": "Slow MA 20 Periods", "value": fast_ma.iloc[-1]},
                    {"name": "Slow MA 20 Periods [Closed]", "value": fast_ma.iloc[-2]}
                ],
                "candle": self.dataframe.iloc[-1]
            })

        return entry_signal, entry_direction

    def market_order_stock_details(self) -> dict:
        return self.market_orders_stock_details[-1]

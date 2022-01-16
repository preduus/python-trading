import pandas
from typing import Union

from libs.stock import Stock
from libs.indicators import Indicators
from . import ExamplesInterface

from .common.trigger import get_entry_momment


class RsiExample(Stock, ExamplesInterface):
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
        fast_rsi = self.indicators.rsi(1)
        slow_rsi = self.indicators.rsi(20)

        """ define RSI limits """
        fast_overbought, slow_overbought = (100, 75)
        fast_oversold, slow_oversold = (5, 25)

        """ Strategy conditions """
        strategy_buy_conditions = (0 < slow_rsi.iloc[-1] < slow_oversold and fast_rsi.iloc[-1] >= fast_overbought)
        strategy_sell_conditions = (0 > slow_rsi.iloc[-1] > slow_overbought and fast_rsi.iloc[-1] <= fast_oversold)

        entry_signal, entry_direction = get_entry_momment(strategy_buy_conditions, strategy_sell_conditions,
                                                          condition_type)

        if entry_signal:
            self.market_orders_stock_details.append({
                "direction": entry_direction,
                "indicators": [
                    {"name": "Fast RSI 3 Periods", "value": fast_rsi.iloc[-1]},
                    {"name": "Fast RSI 3 Periods [Closed]", "value": fast_rsi.iloc[-2]},
                    {"name": "Slow RSI 20 Periods", "value": slow_rsi.iloc[-1]},
                    {"name": "Slow RSI 20 Periods [Closed]", "value": slow_rsi.iloc[-2]}
                ],
                "candle": self.dataframe.iloc[-1]
            })

        return entry_signal, entry_direction

    def market_order_stock_details(self) -> dict:
        return self.market_orders_stock_details[-1]

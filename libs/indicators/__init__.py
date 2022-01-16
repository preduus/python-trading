""" Technical Analysis Library """
from typing import Union, Tuple

import pandas
from finta import TA
from pandas import Series


class Indicators:
    dataframe: pandas.DataFrame

    def __init__(self, dataframe: pandas.DataFrame) -> None:
        self.dataframe = dataframe

    def rsi(self, period: int) -> pandas.Series:
        return TA.RSI(self.dataframe, period=period)

    def sma(self, period: int) -> pandas.Series:
        return TA.SMA(self.dataframe, period=period)

    def ssma(self, period: int) -> pandas.Series:
        return TA.SSMA(self.dataframe, period=period)

    def ema(self, period: int) -> pandas.Series:
        return TA.EMA(self.dataframe, period=period)

    def deviation(self, period: int = 20) -> tuple:
        ssma = TA.SSMA(self.dataframe, period=period)
        """ calculate deviation information """
        deviation_means = [self.dataframe.iloc[-i]['close'] - ssma.iloc[-i] for i in range(1, 3)]
        deviation_colors = ["green" if self.dataframe.iloc[-i]['close'] - ssma.iloc[-i] >= (
                    self.dataframe.iloc[-(i + 1)]["close"] - ssma.iloc[-(i + 1)]) else "red" for i in range(1, 3)]

        return deviation_means, deviation_colors

    def crossover(self, fast_ma_period: int, slow_ma_period: int, fast_ma_type: str = "ema", slow_ma_type: str = "ssma",
                  fma_price_index: str = "close", sma_price_index: str = "close") -> Tuple[Union[str, bool],
                                                                                           Tuple[Series, Series]]:
        fast_ma: pandas.Series = self.get_indicator(fast_ma_type, fast_ma_period, fma_price_index)
        slow_ma: pandas.Series = self.get_indicator(slow_ma_type, slow_ma_period, sma_price_index)

        crossover_buy_conditions: bool = (fast_ma.iloc[-1] > slow_ma.iloc[-1] and fast_ma.iloc[-2] < slow_ma.iloc[-2])
        crossover_sell_conditions: bool = (fast_ma.iloc[-1] > slow_ma.iloc[-1] and fast_ma.iloc[-2] < slow_ma.iloc[-2])
        crossover_direction: Union[str, bool] = "buy" if crossover_buy_conditions else \
            "sell" if crossover_sell_conditions else False

        return crossover_direction, (fast_ma, slow_ma)

    def get_indicator(self, indicator_name: str, period: int = 14, price_index: str = "close") -> pandas.Series:
        if not hasattr(TA, indicator_name.upper()):
            raise Exception("Exception: Invalid Indicator")

        return getattr(TA, indicator_name.upper())(self.dataframe, period, column=price_index)

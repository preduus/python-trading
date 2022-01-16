from typing import Union


def get_candle_type(close_price: float, open_price: float) -> Union[str, None]:
    return "buy" if close_price > open_price else "sell" if close_price < open_price else None

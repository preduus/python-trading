

def get_entry_momment(buy_cond: bool, sell_cond: bool, cond_type: str = None) -> tuple:
    entry_signal = (buy_cond or sell_cond)
    entry_signal_direction = "buy" if buy_cond else "sell" if sell_cond else None

    """ filter market actions """
    if cond_type is not None:
        if cond_type == "buy" and buy_cond:
            return entry_signal, entry_signal_direction
        elif cond_type == "sell" and sell_cond:
            return entry_signal, entry_signal_direction

    return entry_signal, entry_signal_direction

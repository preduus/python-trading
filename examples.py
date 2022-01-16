from tabulate import tabulate

from examples import Examples, ExamplesInterface
from examples.common.candle import get_candle_type
from libs.stock import Stock


class Runner(Stock):
    def __init__(self):
        super().__init__()
        self.examples = Examples()

    def simulate_real_market_sync(self):

        for example in self.examples.get_all():
            print(f'Running {example["name"]} Example ...')

            diagnostic = {
                "Orders": 0,
                "Winners": 0,
                "Losers": 0
            }
            for stock_price_index in range(5, len(self.stock)):
                stock_mocked_data = self.stock[:stock_price_index]

                example_class: ExamplesInterface = example["class"](stock_mocked_data)
                entry_signal, entry_direction = example_class.strategy()

                if entry_signal:
                    market_order_details = example_class.market_order_stock_details()

                    """ Compute order """
                    diagnostic["Orders"] += 1

                    """ Mock order result """
                    closed_signal_candle = self.stock[stock_price_index+1]

                    if entry_direction == get_candle_type(closed_signal_candle["close"], closed_signal_candle["open"]):
                        diagnostic["Winners"] += 1
                    else:
                        diagnostic["Losers"] += 1

            diagnostic["Avg"] = "{0} %".format(round(100 * float(diagnostic["Winners"]) / float(diagnostic["Orders"])))
            print(tabulate({h: [d] for h, d in diagnostic.items()}, headers="keys"))
            print("\n")


if __name__ == "__main__":
    runner = Runner()
    runner.simulate_real_market_sync()

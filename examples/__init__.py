import os
import glob
import importlib
from typing import Union

import pandas


class ExamplesInterface:

    dataframe: pandas.DataFrame
    market_orders_stock_details: list = []

    def __init__(self, stock_data: Union[list, None] = None):
        pass

    def get_stock_data(self) -> list:
        pass

    def create_dataframe(self):
        pass

    def strategy(self, condition_type: Union[str, None] = None) -> tuple:
        pass

    def market_order_stock_details(self) -> dict:
        pass


class Examples:

    examples_modules: list = []

    def __init__(self):
        self.load_examples_modules()

    def load_examples_modules(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        examples_modules_names = [os.path.basename(f)[:-3] for f in glob.glob(f"{dirr}/*.py") if "__init__" not in f]
        for emn in examples_modules_names:
            __, class_module = self.load_module_class(emn)
            if not __:
                continue

            self.examples_modules.append({
                "name": emn.title(),
                "class": class_module
            })

    def load_module_class(self, example_module_name: str) -> tuple:
        module = importlib.import_module(f"examples.{example_module_name}")
        example_class_name = f"{example_module_name.title()}Example"

        if not hasattr(module, example_class_name):
            return False, object

        c = getattr(module, example_class_name)
        return True, c

    def get_all(self) -> list:
        return self.examples_modules

    def get_example(self, example_module_name: str) -> Union[dict, bool]:
        filter_examples_modules = [em for em in self.examples_modules if em["name"].lower() == example_module_name.lower()]
        if not filter_examples_modules:
            return False
        return filter_examples_modules[0]

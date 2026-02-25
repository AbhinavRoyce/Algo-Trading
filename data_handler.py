import MetaTrader5 as mt5
import pandas as pd
import logging
from datetime import datetime

class DataHandler:
    def __init__(self, symbol="XAUUSD", timeframe=mt5.TIMEFRAME_M5, bars=500):
        self.symbol = symbol
        self.timeframe = timeframe
        self.bars = bars

    def initialize(self):
        if not mt5.initialize():
            logging.error("MT5 Initialization Failed")
            raise ConnectionError("MT5 not initialized")

        logging.info("MT5 Initialized")

    def shutdown(self):
        mt5.shutdown()
        logging.info("MT5 Shutdown")

    def get_data(self):
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.bars)

        if rates is None:
            logging.error("Failed to retrieve data")
            return None

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)

        return df

    def get_account_info(self):
        return mt5.account_info()

    def get_symbol_info(self):
        return mt5.symbol_info(self.symbol)
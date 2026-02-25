import MetaTrader5 as mt5
import logging

class ExecutionEngine:

    def __init__(self, symbol="XAUUSD"):
        self.symbol = symbol

    def place_trade(self, direction, lot, sl, tp):
        price = mt5.symbol_info_tick(self.symbol).ask if direction == "buy" else mt5.symbol_info_tick(self.symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY if direction == "buy" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 10,
            "magic": 123456,
            "comment": "StructureBot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Trade Failed: {result.retcode}")
        else:
            logging.info(f"Trade Executed: {direction} {lot} lots")

        return result
import talib
import numpy as np

class MarketStructureStrategy:

    def __init__(self):
        self.trades_today = 0
        self.max_trades = 3

    def calculate_ema(self, df):
        df['ema50'] = talib.EMA(df['close'], timeperiod=50)
        df['ema_slope'] = df['ema50'].diff()
        return df

    def generate_signal(self, df, trend, bos):
        if self.trades_today >= self.max_trades:
            return None

        ema_slope = df['ema_slope'].iloc[-1]

        if trend == "bullish" and bos == "bullish_bos" and ema_slope > 0:
            return "buy"

        if trend == "bearish" and bos == "bearish_bos" and ema_slope < 0:
            return "sell"

        
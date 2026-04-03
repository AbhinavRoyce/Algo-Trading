import numpy as np
import pandas as pd

class StructureDetector:

    def __init__(self, window=5):
        self.window = window

    def detect_swings(self, df):
        df['swing_high'] = df['high'][
            (df['high'] == df['high'].rolling(self.window, center=True).max())
        ]
        df['swing_low'] = df['low'][
            (df['low'] == df['low'].rolling(self.window, center=True).min())
        ]
        return df

    def classify_structure(self, df):
        swings = df.dropna(subset=['swing_high', 'swing_low'], how='all')

        swings['structure'] = None

        last_high = None
        last_low = None

        for i in swings.index:
            if not pd.isna(swings.loc[i, 'swing_high']):
                if last_high and swings.loc[i, 'swing_high'] > last_high:
                    swings.loc[i, 'structure'] = 'HH'
                else:
                    swings.loc[i, 'structure'] = 'LH'
                last_high = swings.loc[i, 'swing_high']

            if not pd.isna(swings.loc[i, 'swing_low']):
                if last_low and swings.loc[i, 'swing_low'] > last_low:
                    swings.loc[i, 'structure'] = 'HL'
                else:
                    swings.loc[i, 'structure'] = 'LL'
                last_low = swings.loc[i, 'swing_low']

        return swings

    def identify_trend(self, swings):
        recent = swings['structure'].dropna().tail(4).tolist()

        if 'HH' in recent and 'HL' in recent:
            return "bullish"
        if 'LH' in recent and 'LL' in recent:
            return "bearish"
        return "range"

    def detect_bos(self, df, swings):
        last_swing_high = swings['swing_high'].dropna().iloc[-1] if not swings['swing_high'].dropna().empty else None
        last_swing_low = swings['swing_low'].dropna().iloc[-1] if not swings['swing_low'].dropna().empty else None

        current_price = df['close'].iloc[-1]

        if last_swing_high and current_price > last_swing_high:
            return "bullish_bos"

        if last_swing_low and current_price < last_swing_low:
            return "bearish_bos"

        return 
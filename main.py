import logging
from data_handler import DataHandler
from structure_detector import StructureDetector
from strategy import MarketStructureStrategy
from risk_manager import RiskManager
from execution_engine import ExecutionEngine

logging.basicConfig(level=logging.INFO, filename="trading.log")

def backtest(df, strategy):
    wins = 0
    losses = 0

    for i in range(100, len(df)):
        subset = df.iloc[:i]
        signal = strategy.generate_signal(subset, "bullish", "bullish_bos")

        if signal:
            if df['close'].iloc[i] > df['close'].iloc[i-1]:
                wins += 1
            else:
                losses += 1

    total = wins + losses
    win_rate = wins / total if total else 0

    print("Total Trades:", total)
    print("Win Rate:", round(win_rate * 100, 2), "%")

def run():
    data_handler = DataHandler()
    structure = StructureDetector()
    strategy = MarketStructureStrategy()
    risk = RiskManager()
    executor = ExecutionEngine()

    data_handler.initialize()
    df = data_handler.get_data()

    df = structure.detect_swings(df)
    swings = structure.classify_structure(df)
    trend = structure.identify_trend(swings)
    bos = structure.detect_bos(df, swings)

    df = strategy.calculate_ema(df)
    signal = strategy.generate_signal(df, trend, bos)

    if signal:
        account = data_handler.get_account_info()
        balance = 

        entry_price = df['close'].iloc[-1]
        structure_price = swings['swing_low'].dropna().iloc[-1] if signal == "buy" else swings['swing_high'].dropna().iloc[-1]

        sl, tp = risk.calculate_sl_tp(entry_price, structure_price, signal)

        stop_loss_points = abs(entry_price - sl)
        lot = risk.calculate_position_size(balance, stop_loss_points, 10)

        executor.place_trade(signal, lot, sl, tp)

    data_handler.shutdown()

if __name__ == "__main__":
    run()
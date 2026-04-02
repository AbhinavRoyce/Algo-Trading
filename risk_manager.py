class RiskManager:

    def __init__(self, risk_percent=1):
        self.risk_percent = risk_percent

    def calculate_position_size(self, account_balance, stop_loss_points, tick_value):
        risk_amount = account_balance * (self.risk_percent / 100)
        lot_size = risk_amount / (stop_loss_points * tick_value)
        return round(lot_size, 2)

    def calculate_sl_tp(self, entry_price, structure_price, direction):
        if direction == "buy":
            sl = structure_price
            tp = entry_price + 2 * (entry_price - sl)
        else:
            sl = structure_price
            tp = entry_price - 2 * (sl - entry_price)

        
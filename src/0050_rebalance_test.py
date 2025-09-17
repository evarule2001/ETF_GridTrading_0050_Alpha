import pandas as pd
import os
import logging
from datetime import datetime

# === 檔案路徑 ===
DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "0050_twse.csv")
TRADE_FILE = os.path.join(DATA_DIR, "rebalance_trades_manual.csv")
SIGNAL_FILE = os.path.join(DATA_DIR, "rebalance_signals.csv")
LOG_FILE = os.path.join("log", "log_trade_msg.log")

# === 策略參數 ===
target_ratio = 0.9
rebalance_band = 0.01

# === Logging 設定 ===
for h in logging.root.handlers[:]:
    logging.root.removeHandler(h)
log_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8-sig")
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
)


# === 載入最新狀態 ===
def load_data():
    df = pd.read_csv(CSV_FILE, encoding="utf-8-sig", parse_dates=["日期"]).sort_values(
        "日期"
    )
    latest_price = df.iloc[-1]["收盤價"]

    trades = pd.read_csv(
        TRADE_FILE, encoding="utf-8-sig", parse_dates=["Date"]
    ).sort_values("Date")
    last_record = trades.iloc[-1]
    cash = last_record["Cash_After"]
    holdings = last_record["Holdings_After"]
    total_value = last_record["TotalValue_After"]

    return latest_price, holdings, cash, total_value


# === 再平衡策略 ===
def rebalance_decision(price, holdings, cash, total_value):
    current_ratio = (holdings * price) / total_value if total_value > 0 else 0
    action, shares = "HOLD", 0

    if current_ratio < target_ratio - rebalance_band and cash >= price:
        buy_amount = int((target_ratio * total_value - holdings * price) // price)
        if buy_amount > 0:
            action, shares = "BUY", buy_amount

    elif current_ratio > target_ratio + rebalance_band and holdings > 0:
        sell_amount = int((holdings * price - target_ratio * total_value) // price)
        if sell_amount > 0:
            action, shares = "SELL", sell_amount

    return action, shares, total_value, current_ratio


# === 計算下一步可能動作 ===
def next_signal(price, holdings, cash, total_value):
    # 下一次買入
    next_buy_price = round(price * (1 - rebalance_band), 2)
    buy_amount = int(
        (target_ratio * total_value - holdings * next_buy_price) // next_buy_price
    )
    buy_amount = max(buy_amount, 0)

    # 下一次賣出
    next_sell_price = round(price * (1 + rebalance_band), 2)
    sell_amount = int(
        (holdings * next_sell_price - target_ratio * total_value) // next_sell_price
    )
    sell_amount = max(sell_amount, 0)

    return next_buy_price, buy_amount, next_sell_price, sell_amount


# === 主程式 ===
if __name__ == "__main__":
    latest_price, holdings, cash, total_value = load_data()
    action, shares, total_value, ratio = rebalance_decision(
        latest_price, holdings, cash, total_value
    )
    next_buy_price, next_buy_shares, next_sell_price, next_sell_shares = next_signal(
        latest_price, holdings, cash, total_value
    )

    msg = f"價格 {latest_price:.2f}, 總資產 {total_value:.2f}, 持倉比例 {ratio:.2%}, 建議動作: {action} {shares} 股"
    print(msg)
    logging.info(msg)

    # 寫入 signal csv
    os.makedirs(DATA_DIR, exist_ok=True)
    signal_row = {
        "Date": datetime.today().strftime("%Y/%m/%d"),
        "CurrentPrice": latest_price,
        "TotalValue": total_value,
        "Holdings": holdings,
        "Cash": cash,
        "CurrentRatio": ratio,
        "Action": action,
        "Shares": shares,
        "TargetRatio": target_ratio,
        "Band": rebalance_band,
        "Next_Buy_Price": next_buy_price,
        "Next_Buy_Shares": next_buy_shares,
        "Next_Sell_Price": next_sell_price,
        "Next_Sell_Shares": next_sell_shares,
    }
    if os.path.exists(SIGNAL_FILE):
        signals = pd.read_csv(SIGNAL_FILE, encoding="utf-8-sig")
        signals = pd.concat([signals, pd.DataFrame([signal_row])], ignore_index=True)
    else:
        signals = pd.DataFrame([signal_row])

    signals.to_csv(SIGNAL_FILE, index=False, encoding="utf-8-sig")
    print(f"✅ 今日訊號已存到 {SIGNAL_FILE}")

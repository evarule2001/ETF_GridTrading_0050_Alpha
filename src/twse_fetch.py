import requests
import pandas as pd
import os
import logging
from datetime import datetime


# 📁 路徑設定
DATA_DIR = "data"
DATA_DIR2 = "logs"
CSV_FILE = os.path.join(DATA_DIR, "0050_twse.csv")
LOG_FILE = os.path.join(DATA_DIR2, "update.log")

# 📝 設定 logging（避免亂碼，用 utf-8-sig）
log_handler = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8-sig")
logging.basicConfig(
    handlers=[log_handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# 🧮 取得 API 所需日期（當月第一天，西元年月日）
def get_twse_date():
    today = datetime.today()
    return f"{today.year}{today.month:02d}01"  # 例如 20250901


# 📦 抓取 TWSE 資料
def fetch_twse_data(date_str):
    url = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date_str}&stockNo=0050"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        if "data" not in data or not data["data"]:
            logging.warning("TWSE 回傳資料為空")
            return None
        return data["data"]
    except Exception as e:
        logging.error(f"抓取 TWSE 資料失敗：{e}")
        return None


# 🧼 清洗資料（民國日期 → 西元日期）
def clean_data(raw_data):
    columns = [
        "日期",
        "成交股數",
        "成交金額",
        "開盤價",
        "最高價",
        "最低價",
        "收盤價",
        "漲跌價差",
        "成交筆數",
    ]
    df = pd.DataFrame(raw_data, columns=columns)

    # 民國 → 西元
    df["日期"] = df["日期"].apply(
        lambda x: str(int(x.split("/")[0]) + 1911)
        + "/"
        + x.split("/")[1]
        + "/"
        + x.split("/")[2]
    )
    df["日期"] = pd.to_datetime(df["日期"], format="%Y/%m/%d")

    # 數值欄位清理
    for col in columns[1:]:
        df[col] = df[col].astype(str).str.replace(",", "").astype(float)

    return df


# 🧠 主流程
def update_twse():
    os.makedirs(DATA_DIR, exist_ok=True)
    date_str = get_twse_date()
    raw_data = fetch_twse_data(date_str)
    if raw_data is None:
        logging.warning("未取得新資料，跳過更新")
        return

    df_new = clean_data(raw_data)

    if os.path.exists(CSV_FILE):
        df_old = pd.read_csv(CSV_FILE, encoding="utf-8-sig", parse_dates=["日期"])
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=["日期"], inplace=True)
        df_combined.sort_values("日期", inplace=True)
        df_combined.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        logging.info(f"✅ 已更新，總共有 {len(df_combined)} 筆資料")
    else:
        df_new.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        logging.info("📁 初次建立 CSV 檔案")


# 🚀 執行
if __name__ == "__main__":
    update_twse()

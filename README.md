# ETF GridTrading 0050 Alpha

本專案實作 **ETF 0050 網格 & 再平衡策略**，目前為手動交易模擬版本。  
目標是透過自動抓取市場資料，結合手動交易紀錄，計算再平衡建議，並輸出交易訊號。

---
ETF_GridTrading_0050_Alpha/
│── data/ # 存放市場歷史資料、手動交易紀錄、策略輸出
│ ├── 0050_twse.csv
│ ├── rebalance_trades_manual.csv
│ └── rebalance_signals.csv
│
│── log/ # 紀錄日誌
│ ├── log_0050data_retrieve.log
│ └── log_trade_msg.log
│
│── src/ # 程式碼
│ ├── data_fetch.py # 抓取 0050 每日行情資料
│ └── rebalance.py # 再平衡策略，根據交易紀錄計算訊號
│
│── .gitignore
│── requirements.txt
│── README.md
---

## 🚀 使用方式

### 1. 建立虛擬環境並安裝套件
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux

pip install -r requirements.txt

2. 更新每日行情資料
python src/data_fetch.py

3. 執行再平衡策略
python src/rebalance.py

專案功能

 自動抓取 0050.tw 日行情資料

 手動交易紀錄輸入

 再平衡策略計算

 產出每日訊號 (建議買/賣價與數量)

 自動下單（未來規劃）

 📊 範例：交易紀錄格式

手動交易紀錄 (rebalance_trades_manual.csv)：

Date	Action	Shares	Price	Cash_After	Holdings_After	TotalValue_After
2025/09/14	Buy	8888	56	502276	497728	1000000
2025/09/15	Invest	0	0	702276	497728	1200000

小建議：

如果你只想要「手動安裝過的主要套件」而不是整個環境，可以用：

pip list --format=freeze > requirements.txt


未來新環境只要執行：

pip install -r requirements.txt
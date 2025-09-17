@echo off
cd C:\Users\TedLi\Documents\Learning_VSCODE\ETF_GridTrading_0050_Alpha

REM 使用虛擬環境內的 Python
C:\Users\TedLi\Documents\Learning_VSCODE\ETF_GridTrading_0050_Alpha\.venv\Scripts\python.exe src\twse_fetch.py
C:\Users\TedLi\Documents\Learning_VSCODE\ETF_GridTrading_0050_Alpha\.venv\Scripts\python.exe src\0050_rebalance_test.py

pause

# 台指選擇權買方損益計算器 (TXO)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

專為台灣投資人設計的 **台指選擇權 (TXO)** 買方損益計算工具  
同時支援 **月選擇權** 與 **週選擇權**，一鍵計算成本、平衡點、損益與視覺化曲線。

## ✨ 功能亮點
- ✅ 買 Call / 買 Put 皆支援
- ✅ 月選 + 週選同時對比
- ✅ 互動模式 + 命令列快速模式
- ✅ 自動繪製損益曲線圖（儲存為高解析 PNG）
- ✅ 契約乘數自動乘 50 元

## 🚀 安裝與執行

```bash
# Clone 下載
git clone https://github.com/你的帳號/taiex-txo-calculator.git
cd taiex-txo-calculator

# 安裝繪圖套件（選裝）
pip install -r requirements.txt

# 執行
python main.py

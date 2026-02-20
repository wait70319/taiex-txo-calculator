
#### 2. `main.py`
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台指選擇權買方損益計算器 (TXO)
支援月選擇權與週選擇權同時計算
"""

import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

MULTIPLIER = 50  # 台指選擇權契約乘數 NT$50/點

def calculate_pl(settlement: float, strike: float, premium: float, lots: int, opt_type: str) -> float:
    """計算單筆損益"""
    if opt_type.lower() in ['call', 'c']:
        intrinsic = max(settlement - strike, 0)
    else:
        intrinsic = max(strike - settlement, 0)
    return (intrinsic - premium) * MULTIPLIER * lots

def get_balance_point(strike: float, premium: float, opt_type: str) -> float:
    """取得盈虧平衡點"""
    if opt_type.lower() in ['call', 'c']:
        return strike + premium
    else:
        return strike - premium

def plot_profit_curve(strike: float, prem_month: float, prem_week: float, lots: int, opt_type: str, filename="txo_profit_curve.png"):
    """繪製損益曲線圖"""
    prices = np.arange(strike - 800, strike + 801, 10)
    
    pl_month = [calculate_pl(p, strike, prem_month, lots, opt_type) for p in prices]
    pl_week = [calculate_pl(p, strike, prem_week, lots, opt_type) for p in prices]
    
    plt.figure(figsize=(12, 7))
    plt.plot(prices, pl_month, label=f'月選擇權 ({prem_month}點)', linewidth=2.5, color='blue')
    plt.plot(prices, pl_week, label=f'週選擇權 ({prem_week}點)', linewidth=2.5, color='red')
    
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.7)
    plt.axvline(x=strike, color='gray', linestyle=':', alpha=0.8, label=f'履約價 {strike}')
    
    plt.title(f'台指選擇權買{opt_type.upper()} 損益曲線圖\n履約價 {strike:,.0f} 點 | {lots}口', fontsize=14, pad=20)
    plt.xlabel('到期結算指數 (點)', fontsize=12)
    plt.ylabel('損益 (新台幣 元)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"\n✅ 損益曲線圖已儲存為：{filename}")
    # plt.show()  # 想跳出視窗看圖就取消註解

def interactive_mode():
    """互動式輸入模式"""
    print("=== 台指選擇權買方損益計算器 ===")
    print("契約乘數：NT$50 / 點\n")
    
    while True:
        opt_type = input("買 Call 還是買 Put？ (c/p)：").strip().lower()
        if opt_type in ['c', 'p']:
            break
        print("請輸入 c 或 p！")
    
    strike = float(input("履約價 (點)："))
    prem_month = float(input("月選擇權成交價 (點)："))
    prem_week = float(input("週選擇權成交價 (點)："))
    lots = int(input("交易口數 [預設1]：") or 1)
    
    opt_name = "Call" if opt_type == 'c' else "Put"
    
    print("\n" + "="*60)
    print(f"交易設定：買{opt_name} | 履約價 {strike:,.0f} | {lots}口")
    print("="*60)
    print(f"月選擇權總成本：{prem_month * MULTIPLIER * lots:,.0f} 元 ({prem_month}點)")
    print(f"週選擇權總成本：{prem_week * MULTIPLIER * lots:,.0f} 元 ({prem_week}點)")
    print(f"月選盈虧平衡點：{get_balance_point(strike, prem_month, opt_type):,.2f} 點")
    print(f"週選盈虧平衡點：{get_balance_point(strike, prem_week, opt_type):,.2f} 點")
    
    while True:
        s = input("\n輸入到期結算指數 (輸入 q 結束)：").strip()
        if s.lower() in ['q', 'quit', '']:
            break
        try:
            settlement = float(s)
            pl_m = calculate_pl(settlement, strike, prem_month, lots, opt_type)
            pl_w = calculate_pl(settlement, strike, prem_week, lots, opt_type)
            print(f"結算 {settlement:,.2f} → 月選 {pl_m:+,.0f} 元 | 週選 {pl_w:+,.0f} 元")
        except ValueError:
            print("請輸入數字或 q 結束")
    
    if input("\n是否產生損益曲線圖？ (y/n)：").strip().lower() == 'y':
        plot_profit_curve(strike, prem_month, prem_week, lots, opt_type)

def main():
    parser = argparse.ArgumentParser(description="台指選擇權買方損益計算器")
    parser.add_argument('-t', '--type', choices=['call', 'put', 'c', 'p'], help='買Call還是買Put')
    parser.add_argument('-k', '--strike', type=float, help='履約價')
    parser.add_argument('-m', '--month', type=float, help='月選擇權成交價')
    parser.add_argument('-w', '--week', type=float, help='週選擇權成交價')
    parser.add_argument('-l', '--lots', type=int, default=1, help='口數')
    parser.add_argument('--plot', action='store_true', help='產生損益曲線圖')
    
    args = parser.parse_args()
    
    # 沒有給參數 → 進入互動模式
    if args.strike is None:
        interactive_mode()
    else:
        opt_type = args.type[0].lower() if args.type else 'c'
        opt_type = 'c' if opt_type in ['c', 'call'] else 'p'
        
        print(f"\n=== 台指買{opt_type.upper()} 損益計算 ===")
        print(f"履約價：{args.strike:,.0f} 點 | 口數：{args.lots}")
        print(f"月選價：{args.month} 點 | 週選價：{args.week} 點")
        
        be_m = get_balance_point(args.strike, args.month, opt_type)
        be_w = get_balance_point(args.strike, args.week, opt_type)
        print(f"月選平衡點：{be_m:,.2f} 點")
        print(f"週選平衡點：{be_w:,.2f} 點")
        
        if args.plot:
            plot_profit_curve(args.strike, args.month, args.week, args.lots, opt_type)

if __name__ == "__main__":
    main()

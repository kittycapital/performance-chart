#!/usr/bin/env python3
"""
자산 성과 데이터 수집 스크립트
- ETF: yfinance (무료)
- 암호화폐: CoinGecko API (무료)
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'yfinance', '--break-system-packages', '-q'])
    import yfinance as yf

# ============================================
# 자산 정의
# ============================================

ASSETS = {
    # ETFs (yfinance)
    "SPY": {"name": "S&P 500", "type": "etf", "color": "#3b82f6"},
    "QQQ": {"name": "Nasdaq 100", "type": "etf", "color": "#8b5cf6"},
    "IWM": {"name": "Russell 2000", "type": "etf", "color": "#06b6d4"},
    "DIA": {"name": "Dow Jones", "type": "etf", "color": "#f59e0b"},
    "GLD": {"name": "Gold", "type": "etf", "color": "#eab308"},
    "EWY": {"name": "Korea (EWY)", "type": "etf", "color": "#ef4444"},
    "USO": {"name": "Oil (USO)", "type": "etf", "color": "#84cc16"},
    
    # Crypto ETFs (yfinance)
    "IBIT": {"name": "Bitcoin (IBIT)", "type": "etf", "color": "#f7931a"},
    "ETHA": {"name": "Ethereum (ETHA)", "type": "etf", "color": "#627eea"},
    "SOLZ": {"name": "Solana (SOLZ)", "type": "etf", "color": "#00ffa3"},
}

COINGECKO_API = "https://api.coingecko.com/api/v3"


def get_date_ranges():
    """기간별 시작 날짜 계산"""
    today = datetime.now()
    
    return {
        "1W": today - timedelta(days=7),
        "1M": today - timedelta(days=30),
        "3M": today - timedelta(days=90),
        "12M": today - timedelta(days=365),
        "YTD": datetime(today.year, 1, 1),
    }


def fetch_etf_data(symbol, days=400):
    """yfinance로 ETF 데이터 가져오기"""
    print(f"  📈 {symbol} 데이터 수집 중...")
    
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        hist = ticker.history(start=start_date, end=end_date)
        
        if hist.empty:
            print(f"  ⚠️ {symbol} 데이터 없음")
            return None
        
        # 날짜와 종가만 추출
        data = []
        for date, row in hist.iterrows():
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "price": round(row["Close"], 2)
            })
        
        print(f"  ✅ {symbol}: {len(data)}일 데이터")
        return data
        
    except Exception as e:
        print(f"  ❌ {symbol} 오류: {e}")
        return None


def fetch_crypto_data(coin_id, days=400):
    """CoinGecko로 암호화폐 데이터 가져오기"""
    print(f"  🪙 {coin_id} 데이터 수집 중...")
    
    try:
        url = f"{COINGECKO_API}/coins/{coin_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        data = []
        for timestamp, price in result["prices"]:
            date = datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")
            data.append({
                "date": date,
                "price": round(price, 2)
            })
        
        # 중복 날짜 제거 (마지막 값 유지)
        seen = {}
        for item in data:
            seen[item["date"]] = item["price"]
        
        data = [{"date": d, "price": p} for d, p in seen.items()]
        data.sort(key=lambda x: x["date"])
        
        print(f"  ✅ {coin_id}: {len(data)}일 데이터")
        return data
        
    except Exception as e:
        print(f"  ❌ {coin_id} 오류: {e}")
        return None


def calculate_performance(prices, start_date):
    """특정 날짜부터의 수익률 계산"""
    start_str = start_date.strftime("%Y-%m-%d")
    
    # 시작 날짜에 가장 가까운 데이터 찾기
    start_price = None
    for p in prices:
        if p["date"] >= start_str:
            start_price = p["price"]
            break
    
    if not start_price or not prices:
        return None
    
    end_price = prices[-1]["price"]
    return round((end_price - start_price) / start_price * 100, 2)


def main():
    print("=" * 50)
    print("🚀 자산 성과 데이터 수집 시작")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    date_ranges = get_date_ranges()
    all_data = {}
    
    # 모든 ETF 데이터 수집
    print("\n📊 ETF 데이터 수집")
    for symbol, info in ASSETS.items():
        prices = fetch_etf_data(symbol)
        if prices:
            all_data[symbol] = {
                "name": info["name"],
                "color": info["color"],
                "prices": prices,
                "performance": {}
            }
            
            # 기간별 수익률 계산
            for period, start_date in date_ranges.items():
                perf = calculate_performance(prices, start_date)
                all_data[symbol]["performance"][period] = perf
    
    # 결과 저장
    output = {
        "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "assets": all_data
    }
    
    output_path = Path(__file__).parent.parent / "data" / "performance.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print(f"✅ 완료! {len(all_data)}개 자산 저장됨")
    print(f"📁 {output_path}")
    print("=" * 50)
    
    # YTD 성과 출력
    print("\n📊 YTD 성과:")
    for symbol, data in sorted(all_data.items(), key=lambda x: x[1]["performance"].get("YTD", 0) or 0, reverse=True):
        perf = data["performance"].get("YTD", "N/A")
        if perf is not None:
            sign = "+" if perf >= 0 else ""
            print(f"  {symbol:5} {data['name']:20} {sign}{perf}%")


if __name__ == "__main__":
    main()

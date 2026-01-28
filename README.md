# 📊 자산 성과 비교 차트

10개 자산의 기간별 수익률을 비교하는 차트입니다.

## 📈 포함 자산

| 심볼 | 자산 | 유형 |
|------|------|------|
| SPY | S&P 500 | ETF |
| QQQ | Nasdaq 100 | ETF |
| IWM | Russell 2000 | ETF |
| DIA | Dow Jones | ETF |
| GLD | Gold | ETF |
| EWY | Korea | ETF |
| USO | Oil | ETF |
| BTC | Bitcoin | Crypto |
| ETH | Ethereum | Crypto |
| SOL | Solana | Crypto |

## 🗓️ 기간 옵션

- 1주 (1W)
- 1개월 (1M)
- 3개월 (3M)
- 1년 (12M)
- 연초대비 (YTD) - 기본값

## 🚀 배포 방법

### GitHub Pages

1. 이 저장소를 Fork 또는 Clone
2. Settings → Pages → Source: `main` branch
3. 자동으로 매일 업데이트됨

### imweb

GitHub Pages URL을 iframe으로 삽입:

```html
<iframe 
  src="https://your-username.github.io/performance-chart/" 
  width="100%" 
  height="700px" 
  style="border: none; border-radius: 12px;"
></iframe>
```

## 📡 데이터 소스

- **ETF**: Yahoo Finance (yfinance)
- **암호화폐**: CoinGecko API

모두 무료입니다.

## ⚙️ 자동 업데이트

GitHub Actions가 매일 UTC 14:00 (한국시간 23:00)에 자동 실행됩니다.

수동 실행: Actions → "자산 성과 데이터 업데이트" → Run workflow

## 📁 구조

```
performance-chart/
├── index.html              # 메인 페이지
├── data/
│   └── performance.json    # 가격 데이터
├── scripts/
│   ├── fetch_data.py       # 데이터 수집
│   └── generate_html.py    # HTML 생성
└── .github/workflows/
    └── update-data.yml     # 자동 업데이트
```

## 📄 라이선스

MIT License

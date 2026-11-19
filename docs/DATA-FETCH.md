# 시세 데이터 받기 (크롬 연결 대화에서)

1. 크롬 새 탭에서 `https://query1.finance.yahoo.com/v8/finance/chart/%5EIXIC?range=5d&interval=1d` 를 연다(같은 출처라 fetch 가능).
2. javascript_tool 로 아래 종목의 1년 일봉을 받는다:
   `^IXIC ^GSPC ^DJI SOXX QQQ SPY ^VIX ^TNX DX-Y.NYB KRW=X CL=F ^SOX` + 그날 다루는 종목(예: NVDA SNDK MU).
   `/v8/finance/chart/{심볼}?range=1y&interval=1d` → `chart.result[0].indicators.quote[0]` (open/high/low/close/volume).
   200일선은 `range=2y` 로 따로 받는다.
3. 도구 출력은 약 1,000자에서 잘리므로, 결과를 window 변수에 담아 1,000자씩 나눠 읽는다.
4. 형식
   - `data/summary.txt`: `SYM|date,close,prev,chg,open,high,low,ma20,ma50,ma200,ma20p,ma50p,ma200p,hi52,hi52d,lo52,lo52d,rsi,vol,vol20,volr,res20,sup20,res60,sup60,w1,m1,m3`
     지수(^IXIC·^GSPC·^DJI)의 마지막 날 거래량은 야후가 덜 집계해 쓰지 않는다 → 거래량은 QQQ·SPY 로 본다.
   - `data/raw_series.txt`: `D|MMDD…` 120거래일 · `SYM|종가(배율 정수)|거래량(10만 주)|MA20|MA50|MA200`(MA 는 3일 간격 40점, 인덱스 2,5,8…)
     배율: ^IXIC 1, ^GSPC 10, SOXX 100.
5. `python3 scripts/chart_analysis.py data/raw_series.txt data/summary.txt > data/charts.json`
6. 탭 닫기.

공포·탐욕: `https://production.dataviz.cnn.io/index/fearandgreed/graphdata/<최근 날짜>` 탭에서 `fear_and_greed.score`, `put_call_options` 마지막 값.

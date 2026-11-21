"""제3호(2026-11-21 토, 미국 11/20 금 장) 초안 — build_issue1.py 틀을 돌린 뒤 글·일정·의견을 11/20 장 기준으로 바꾼다.
숫자는 data/*(CNBC 일봉, 11/20 종가)와 아래 출처의 확인값만 쓴다. 샌디스크는 11/20부터 8:1 액면분할 반영가."""
import json

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1346.06"), ("D = '2026-11-19'", "D = '2026-11-21'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-20 16:00 ET 종가'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-21 08:00 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 3, 'weekday': '토'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-20(금) 뉴욕장'"),
       ("'ma200':1284.66", "'ma200':160.73"),  # 샌디스크 8:1 분할 반영(tickers_mini 값)
       ("for c in JL['cards']:", "for c in [x for x in JL['cards'] if not x.get('quietCard')]:"),
       # 회사 이름의 '&amp;' 속 ';' 때문에 쪼개지지 않도록(11/20 수집분부터)
       ("open('data/sp500_top100.txt',encoding='utf-8').read().strip().split(';')", "TOP100")]
for a, b in REP:
    assert a in src, a
    src = src.replace(a, b)
src = src[:src.rindex('json.dump(')]
import re, html
TOP100 = [html.unescape(x) for x in re.split(r';(?=[A-Z][A-Z.]*,[\d.]+,-?[\d.]+,)', open('data/sp500_top100.txt', encoding='utf-8').read().strip())]
ns = {'TOP100': TOP100}
exec(compile(src, 'build_issue1.py', 'exec'), ns)
issue, f, summ, Y, FX, TD = ns['issue'], ns['f'], ns['summ'], ns['Y'], ns['FX'], ns['TD']
N, row, CLOSE = ns['N'], ns['row'], ns['CLOSE']
won = lambda usd: (lambda v: f"약 {v/10000:.1f}만 원".replace('.0만', '만') if v < 1e5 else f"약 {round(v/1e4)}만 원")(usd * FX)

# ── 출처 ─────────────────────────────────────────────
AP = 'https://www.wtae.com/article/sp-500-sinks-nasdaq-composite-goes-negative-nov-20/74494971'
RTR = 'https://wmbdradio.com/2026/11/20/exclusive-us-secs-nvidia-probe-is-examining-potential-accounting-issues-sources-say/'
FOOL_NV = 'https://www.fool.com/investing/2026/11/20/nvidia-stock-plunge-wipes-out-nearly-usd500-billion-in-one-day-as-sec-reportedly-probes-its-accounting/'
TKEY = 'https://www.tradingkey.com/analysis/stocks/us-stocks/262316111-nasdaq-falls-ai-stock-selloff-nvidia-sec-probe-tradingkey'
AVGO_SA = 'https://stockanalysis.com/news/broadcom-falls-google-tpu-cut-mediatek/'
AVGO_WS = 'https://247wallst.com/investing/2026/11/20/broadcom-stock-plunges-12-and-loses-191-billion-after-a-report-that-google-cut-its-plans-for-broadcom-ai-chips/'
MU_WS = 'https://247wallst.com/investing/2026/11/20/micron-stock-plunges-13-as-barrons-calls-memory-stocks-agonizingly-cheap-western-digital-sandisk-and-seagate-sink-in-ai-chip-selloff/'
SNDK_WS = 'https://247wallst.com/investing/2026/11/20/sandisk-tumbles-8-as-trendforce-turns-bearish-on-2027-nand-prices-micron-falls-5-sk-hynix-slides-4/'
SPLIT = 'https://stock3.com/news/sandisk-aktiensplit-81-das-aendert-sich-am-20-november-im-depot-17399975'
ANT_YH = 'https://finance.yahoo.com/markets/stocks/articles/anthropic-stock-came-within-5-211710460.html'
SAXO = 'https://www.home.saxo/content/articles/options/anthropic-ipo-when-can-you-trade-ant-options-and-what-to-expect-when-you-can-20112026'
COOK = 'https://www.investing.com/news/economy-news/feds-cook-says-rate-hikes-needed-to-lower-high-inflation-5042321'
FW99 = 'https://financefeeds.com/gold-price-near-3560-after-hitting-14-month-low-as-fed-hike-odds-reach-99'
UM = 'https://www.kitco.com/news/article/2026-11-20/gold-price-trades-near-3568oz-after-final-consumer-sentiment-rises-515'
NQ = 'https://www.newsquawk.com/headlines/us-market-wrap-aggressive-equity-sell-off-sees-spx-enter-correction-and-ndx-test-bear-market'
CAPP = 'https://cappnotes.substack.com/p/closing-look-friday-november-20-2026'
MSCR = 'https://www.marketscreener.com/news/wall-st-ends-sharply-lower-on-ai-selloff-s-p-500-dow-in-correction-ce785ed3dd80f527'
FGU = 'https://www.tokenpost.com/news/investing/62212'
FG = 'https://edition.cnn.com/markets/fear-and-greed'
ZS = 'https://www.investing.com/news/stock-market-news/crowdstrike-in-talks-to-acquire-zscaler-sources-say-5042720'
BTC = 'https://bitcoinmagazine.com/markets/bitcoin-price-slips-58300-nasdaq'
TRUMP = 'https://www.investing.com/news/world-news/trump-says-us-to-penalize-firms-building-data-centers-abroad-5042390'
HUANG = 'https://gvwire.com/2026/11/20/former-nvidia-ceo-huang-agreed-to-testify-at-public-us-senate-hearing-senators-aide-says/'
STL = 'https://www.stocktitan.net/articles/stock-market-today-live-november-20-2026'
INTU_TV = 'https://www.tradingview.com/news/invezz:6d543feea094b:0-intuit-stock-falls-9-on-fy27-revenue-forecast-cut-mailchimp-sale-analysts-cut-pts/'
INTU_AOL = 'https://www.aol.com/articles/intuit-stock-falls-weaker-outlook-160641000.html'
CBS = 'https://www.cbsnews.com/news/why-stocks-are-falling-ai-fears/'
FORT = 'https://fortune.com/2026/11/20/sp-500-correction-panic-selling-ai-selloff-nasdaq-2026-gains-bnp-paribas/'
AJ = 'https://aljazeera.com/economy/2026/11/20/asias-stock-markets-dive-as-anthropic-debut-fails-to-allay-ai-bubble-fears'
LAMONT = 'https://fortune.com/2026/11/18/ai-bubble-owen-lamont-70-percent-four-horsemen-stock-issuance-anthropic-ipo'
RBC_MU = 'https://www.tradingpedia.com/2026/11/20/micron-slides-below-key-averages-despite-1500-target/'
NQ13 = 'https://www.newsquawk.com/headlines/us-broker-moves-panw-upgraded-at-keybanc-avgo-downgraded-at-rothschild-redburn'
MSTR_BZ = 'https://www.benzinga.com/trading-ideas/movers/26/11/63486747/strategy-stock-slides-to-52-week-low-as-bitcoin-dips-below-60000'
AMD_HB = 'https://www.openingbelldailynews.com/p/amd-stock-short-seller-nov-20-2026'
FJ = 'https://features.financialjuice.com/2026/11/20/week-ahead-economic-indicators-23rd-27th-november-us/'
CMC = 'https://www.cmcmarkets.com/en-ie/news-and-analysis/the-week-ahead-global-pmis-us-pce-dell-earnings'
NQW = 'https://www.newsquawk.com/headlines/week-in-focus--november-23rd-27th-highlights-include-us-pce-flash-pmis-aussie-cpi-and-ecb-minutes'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
JL_U = 'https://stock.jintar.co.kr/'
FGv = {'v': 14, 'w': 37}  # CNN 2026-11-20 장중(11:55 ET) 보도값, 3/30 이후 최저

g = lambda t: f(t, 'chg') if t in summ else TD[t][5]
q_ = {q['t']: q for q in issue['quotes']['list']}
qc = lambda t: q_[t]['ch']

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스',
 'title': "엔비디아 -14% '회계 조사' 보도에 나스닥 -5.3%, S&P 500은 조정 진입",
 'img': 'img/2026-11-21-top.jpg',
 'points': [
  {'t': f"로이터가 '미 증권거래위원회(SEC)가 엔비디아의 회계 문제 가능성을 들여다보고 있다'고 보도하자 엔비디아는 {g('NVDA'):+.2f}%, 125.53달러({won(125.53)})로 마감했습니다. SEC와 엔비디아는 답하지 않았습니다.", 'src': RTR},
  {'t': '하루 새 시가총액 약 4,910억 달러(약 661조 원)가 증발했고, 10/6 최고 종가 239.24달러(약 32만 원)보다 47.5% 낮아졌습니다.', 'src': FOOL_NV},
  {'t': f"나스닥은 {f('^IXIC','chg'):+.2f}%로 올해 오른 몫을 모두 내줬고, S&P 500은 {f('^GSPC','chg'):+.2f}%로 7일 연속 내려 고점 대비 10% 넘게 빠진 '조정'에 들어갔습니다. 다우도 조정 구간입니다.", 'src': AP},
  {'t': f"필라델피아 반도체 지수는 {f('^SOX','chg'):+.2f}%로 30종목이 모두 내렸습니다. 마이크론 {g('MU'):+.2f}%, AMD {g('AMD'):+.2f}%, 브로드컴 {g('AVGO'):+.2f}%입니다.", 'src': TKEY},
  {'t': f"이번 주 S&P 500은 {f('^GSPC','w1'):+.1f}%, 나스닥은 {f('^IXIC','w1'):+.1f}%로 2025년 4월 이후 가장 나쁜 한 주였습니다.", 'src': MSCR},
  {'t': '쿡 연준 이사는 같은 날 물가가 내려간다는 증거가 거의 없다며 금리를 더 올려야 한다고 말했습니다. 12월 인상 확률은 약 99%로 반영됐습니다.', 'src': COOK},
 ],
 'risks': [
  {'t': f"CNN 공포·탐욕 지수는 장중 {FGv['v']}로 3월 30일 이후 가장 낮았습니다. 1주 전은 {FGv['w']}였습니다. 겁에 질린 매도가 한쪽으로 몰렸다는 뜻이기도 합니다.", 'src': FGU},
  {'t': f"S&P 500 RSI는 {float(summ['^GSPC']['rsi']):.0f}, 나스닥은 {float(summ['^IXIC']['rsi']):.0f}로 30 아래 과매도입니다. 로이터 보도처럼 조사가 곧 잘못을 뜻하지는 않고, 많은 조사가 제재 없이 끝납니다.", 'src': RTR},
 ],
 'why': '엔비디아 회계 의혹과 브로드컴 주문 축소 보도가 하루에 겹치며, 쌓여 있던 AI 투자 의심이 한꺼번에 가격에 찍혔습니다. 금리 인상 경고까지 더해져 피할 곳이 거의 없던 하루입니다.',
 'watch': [
  '엔비디아가 SEC 조사 보도에 공식 입장을 내는지 (보도 시점 응답 없음)',
  f"월요일 S&P 500이 20일 저점 6,883 아래로 내려가 8일째 하락하는지",
  '수요일 밤 10월 PCE 물가·3분기 GDP 수정치 (추수감사절 전날)',
 ],
 'src': [{'t': '로이터(WMBD 전재)', 'u': RTR}, {'t': 'AP', 'u': AP}, {'t': 'Motley Fool', 'u': FOOL_NV}, {'t': 'TradingKey', 'u': TKEY}, {'t': 'MarketScreener', 'u': MSCR}, {'t': 'Investing.com', 'u': COOK}],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': 'S&P 500은 265포인트, 나스닥은 1,261포인트 빠졌습니다. S&P 500 종목 중 오른 곳은 123개, 내린 곳은 376개였고 세 지수 모두 하루 저점 근처에서 끝났습니다.',
 'src': AP,
}

# ── 참고 지표 ─────────────────────────────────────────
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'close') / (1 + f('^TNX', 'chg') / 100), 2)
issue['indicators'] = [
 {'name': '공포·탐욕 지수', 'v': FGv['v'], 'd': 0, 'label': '극단적 공포', 'src': FGU},
 {'name': 'VIX', 'v': f('^VIX', 'close'), 'd': 2, 'chg': f('^VIX', 'chg'), 'src': Y('%5EVIX')},
 {'name': '미 국채 10년', 'v': f('^TNX', 'close'), 'd': 2, 'suf': '%', 'chg': TNX_CH, 'chgsuf': '%p', 'src': Y('%5ETNX')},
 {'name': '달러인덱스', 'v': f('DX-Y.NYB', 'close'), 'd': 2, 'chg': f('DX-Y.NYB', 'chg'), 'src': Y('DX-Y.NYB')},
 {'name': 'WTI 유가', 'v': f('CL=F', 'close'), 'd': 2, 'chg': f('CL=F', 'chg'), 'src': Y('CL%3DF')},
 {'name': '금', 'v': f('GC=F', 'close'), 'd': 1, 'chg': f('GC=F', 'chg'), 'src': Y('GC%3DF')},
 {'name': '원/달러', 'v': FX, 'd': 2, 'chg': f('KRW=X', 'chg'), 'src': Y('KRW%3DX')},
]
issue['gauges'] = [x for x in issue.get('gauges', []) if x['name'] in ('공포·탐욕 지수', 'VIX 변동성')]
for x in issue['gauges']:
    if x['name'] == '공포·탐욕 지수':
        x['v'] = N(FGv['v'], FGU, '2026-11-20 11:55 ET 장중 보도'); x['note'] = f"1주 전 {FGv['w']} · 3월 30일 이후 최저 (CNN, 25 아래는 극단적 공포)"
    if x['name'] == 'VIX 변동성':
        x['note'] = f"장중 40.03까지 · 50일 평균 {float(summ['^VIX']['ma50']):.1f}의 약 두 배"
issue['macro'] = []

# ── 간밤 뉴스 ─────────────────────────────────────────
issue['news'] = [
 {'tag': '규제', 'img': 'img/2026-11-21-nvda.jpg', 'title': "엔비디아 -14%, 'SEC가 회계 들여다본다' 보도",
  'line': f"로이터는 SEC 조사 담당자들이 엔비디아의 회계 문제 가능성을 살핀다고 전했고, 엔비디아는 {g('NVDA'):+.2f}%로 이번 주에만 {f('NVDA','w1'):.1f}% 빠졌습니다.",
  'src': [{'t': '로이터(WMBD 전재)', 'u': RTR}, {'t': 'Motley Fool', 'u': FOOL_NV}]},
 {'tag': '시장', 'img': 'img/2026-11-21-spx.jpg', 'title': 'S&P 500·다우 조정 진입, 나스닥은 올해 상승분 반납',
  'line': f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 7일 연속 내렸고 2020년 이후 가장 긴 하락입니다. 7,000선 아래로 내려간 것은 4월 이후 처음입니다.",
  'src': [{'t': 'AP', 'u': AP}, {'t': 'MarketScreener', 'u': MSCR}]},
 {'tag': '반도체', 'img': 'img/2026-11-21-chip.jpg', 'title': "반도체 지수 -10.7%, 브로드컴은 '구글 주문 축소' 보도",
  'line': f"밍치궈 애널리스트가 구글이 2027년 TPU 주문을 약 20% 줄였다고 전하자 브로드컴은 {g('AVGO'):+.2f}%였습니다. 구글·브로드컴은 확인하지 않았습니다.",
  'src': [{'t': 'StockAnalysis', 'u': AVGO_SA}, {'t': '24/7 Wall St.', 'u': AVGO_WS}, {'t': 'TradingKey', 'u': TKEY}]},
 {'tag': '메모리', 'img': 'img/2026-11-21-memory.jpg', 'title': '샌디스크 분할 첫날 -16%, 마이크론 -13.9%',
  'line': f"트렌드포스가 내년 1분기 낸드 계약 가격이 0~5% 내린다고 전망한 뒤 메모리주가 함께 밀렸습니다. 샌디스크는 8:1 분할 첫날 79.24달러({won(79.24)})입니다.",
  'src': [{'t': '24/7 Wall St.', 'u': SNDK_WS}, {'t': '24/7 Wall St.', 'u': MU_WS}, {'t': 'stock3', 'u': SPLIT}]},
 {'tag': '상장', 'img': 'img/2026-11-21-ipo.jpg', 'title': '앤트로픽 둘째 날 -9.1%, 공모가 턱밑까지',
  'line': f"장중 83.05달러({won(83.05)})까지 내려 공모가 83달러에 5센트 차로 다가갔다가 88.30달러({won(88.30)})에 마감했습니다.",
  'src': [{'t': 'AP', 'u': AP}, {'t': 'Yahoo Finance', 'u': ANT_YH}]},
 {'tag': '연준', 'img': 'img/2026-11-21-fed.jpg', 'title': "쿡 연준 이사 '금리 더 올려야', 소비심리는 51.5",
  'line': '쿡 이사는 지금 금리로는 물가를 잡기 부족하다고 했습니다. 미시간대 소비자심리 확정치는 51.5였고 1년 뒤 물가 전망은 3.7%로 10월 4.7%보다 낮아졌습니다.',
  'src': [{'t': 'Investing.com', 'u': COOK}, {'t': 'Kitco', 'u': UM}]},
 {'tag': '인수', 'img': 'img/2026-11-21-cyber.jpg', 'title': '장 마감 뒤 크라우드스트라이크, 지스케일러 인수 협상 보도',
  'line': '지스케일러는 시간외에서 약 17% 오르고 크라우드스트라이크는 약 8% 내렸습니다. 지스케일러 시가총액은 약 335억 달러(약 45조 원)이고 조건은 나오지 않았습니다.',
  'src': [{'t': 'Investing.com(로이터)', 'u': ZS}]},
 {'tag': '자산', 'img': 'img/2026-11-21-gold.jpg', 'title': '비트코인 6만 달러(약 8,080만 원) 아래, 금은 -4%',
  'line': f"비트코인은 약 5만 8,300달러({won(58300)})로 11월에만 약 25% 빠졌습니다. 금 선물은 {f('GC=F','chg'):.2f}% 내린 3,539달러({won(3539)})입니다.",
  'src': [{'t': 'Bitcoin Magazine', 'u': BTC}, {'t': '야후 파이낸스', 'u': Y('GC%3DF')}]},
 {'tag': '방어주', 'img': 'img/2026-11-21-health.jpg', 'title': '하락장 속 유나이티드헬스 +2.8%, 월마트 +1.5%',
  'line': f"TD 코웬이 유나이티드헬스를 매수로 올렸고(목표 455달러, {won(455)}), 헬스케어·필수소비재로 돈이 옮겨 갔습니다. 상위 100개 중 오른 종목은 11개뿐이었습니다.",
  'src': [{'t': 'Stock Titan', 'u': STL}, {'t': 'MarketScreener', 'u': MSCR}]},
]
for n in issue['news']:
    n['body'] = n['line']

issue['movers'] = [
 {'ticker': t, 'name': nm, 'close': N(TD[t][4], Y(t), CLOSE), 'chg_pct': N(TD[t][5], Y(t), CLOSE), 'won': won(TD[t][4]), 'why': why}
 for t, nm, why in [('NVDA', '엔비디아', 'SEC 회계 조사 보도, 하루 시총 약 661조 원 증발'), ('AVGO', '브로드컴', '구글 TPU 주문 약 20% 축소 보도(확인 안 됨)'),
                    ('MU', '마이크론', '낸드 가격 하락 전망·메모리 동반 급락'), ('UNH', '유나이티드헬스', 'TD 코웬 매수 상향, 방어주로 돈 이동')]]

# ── 다음 거래일 일정 (한국 시간, 다음 주 11/23~11/27) ─────────
issue['schedule'] = [
 {'kst': '11/23(월) 23:30', 'type': '개장', 'name': '뉴욕 정규장 개장 · S&P 500 8일째 하락하나', 'star': 5, 'why': '7일 연속 하락에 공포·탐욕 지수 14까지 내려간 뒤 첫 거래일입니다. 엔비디아 입장 발표 여부가 먼저입니다.', 'src': AP},
 {'kst': '11/23(월) 23:45', 'type': '지표', 'name': '11월 S&P 글로벌 제조업·서비스업 PMI 속보치', 'star': 3, 'why': '경기가 버티는지 보는 첫 숫자. 강하면 금리 인상 걱정이 커질 수 있습니다.', 'src': FJ},
 {'kst': '11/24(화) 06:00', 'type': '연준', 'name': '윌리엄스 뉴욕 연은 총재 연설', 'star': 3, 'why': '지난주 "극적인 조치는 필요 없다"고 했던 인물. 12월 0.5%p 인상론에 선을 긋는지 봅니다.', 'src': FJ},
 {'kst': '11/25(수) 00:00', 'type': '지표', 'name': '11월 컨퍼런스보드 소비자신뢰지수', 'star': 3, 'why': '연말 쇼핑을 앞둔 소비자 체감. 이전 91.7.', 'src': FJ},
 {'kst': '11/25(수) 장 후', 'type': '실적', 'name': '델 테크놀로지스 3분기 실적', 'star': 4, 'why': 'AI 서버 주문이 꺾였는지 보여줄 첫 대형 실적. 옵션 시장은 ±12~17% 움직임을 예상합니다.', 'src': CMC},
 {'kst': '11/25(수) 22:30', 'type': '지표', 'name': '10월 PCE 물가 · 3분기 GDP 수정치 · 내구재 · 실업수당', 'star': 5, 'why': '연준이 가장 중시하는 물가. 근원 PCE 예상 전년 대비 3.2%(이전 3.1%). 12월 인상 폭을 가를 숫자입니다.', 'src': NQW},
 {'kst': '11/26(목) 밤', 'type': '휴장', 'name': '추수감사절 휴장 · 27일(금) 03:00 KST 조기 폐장', 'star': 2, 'why': '거래일이 짧아 거래량이 줄고 움직임이 커질 수 있습니다.', 'src': NYSE},
]
issue['schedule_note'] = '토요일이라 오늘 밤은 미국 장이 없습니다. 월요일 06:00에 주말 요약 호가 나갑니다. 시각은 한국 시간이며 발표 기관 일정에 따라 바뀔 수 있습니다.'
issue['calendar'] = {
 'today': '2026-11-21',
 'days': [
  {'d': '2026-11-16', 'ev': [{'k': '연준', 't': '워시 의장 연설'}]},
  {'d': '2026-11-17', 'ev': [{'k': '실적', 't': '엔비디아', 'when': '장 후'}]},
  {'d': '2026-11-18', 'ev': [{'k': '연준', 't': 'FOMC 의사록'}, {'k': '실적', 't': '팔로알토', 'when': '장 후'}]},
  {'d': '2026-11-19', 'ev': [{'k': '상장', 't': '앤트로픽 +17%'}, {'k': '실적', 't': '월마트·인튜이트'}]},
  {'d': '2026-11-20', 'ev': [{'k': '급락', 't': '엔비디아 -14% · S&P 조정', 'hl': True}, {'k': '연준', 't': '쿡 "더 올려야"'}]},
  {'d': '2026-11-23', 'ev': [{'k': '지표', 't': 'PMI 속보치'}, {'k': '실적', 't': 'HPE·줌', 'when': '장 후'}]},
  {'d': '2026-11-24', 'ev': [{'k': '지표', 't': '소비자신뢰'}, {'k': '실적', 't': '델', 'when': '장 후', 'hl': True}]},
  {'d': '2026-11-25', 'ev': [{'k': '지표', 't': 'PCE 물가·GDP', 'hl': True}, {'k': '연준', 't': '베이지북'}]},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장'}]},
  {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}]},
 ],
 'src': [{'t': 'FinancialJuice 주간 일정', 'u': FJ}, {'t': 'Newsquawk 주간', 'u': NQW}, {'t': 'CMC Markets', 'u': CMC}, {'t': 'NYSE 휴장일', 'u': NYSE}],
}
issue['earnings'] = [
 {'date': '11/19(목)', 'time': '장 마감 후', 'company': '인튜이트', 'ticker': 'INTU', 'done': True},
 {'date': '11/23(월)', 'time': '장 마감 후', 'company': 'HPE', 'ticker': 'HPE', 'done': False},
 {'date': '11/23(월)', 'time': '장 마감 후', 'company': '줌', 'ticker': 'ZM', 'done': False},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '델 테크놀로지스', 'ticker': 'DELL', 'done': False},
]

# ── 차트 분석 (어제 → 최근 대비 → 앞으로) ───────────────
pct = lambda a, b: (a / b - 1) * 100
CH = {
 '^IXIC': ('-5.28%, 시가부터 밀려 하루 저점 근처에서 마감', [
   ('어제', f"나스닥은 {f('^IXIC','chg'):+.2f}%로 22,618에 끝났습니다. 23,593에서 시작해 반등 없이 22,513까지 밀렸고, 엔비디아({g('NVDA'):+.2f}%)·브로드컴({g('AVGO'):+.2f}%)·마이크론({g('MU'):+.2f}%)이 끌어내렸습니다."),
   ('최근 대비', f"1주 {f('^IXIC','w1'):+.1f}%, 1달 {f('^IXIC','m1'):+.1f}%, 고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%로 약세장 기준(-20%)에 가까워졌습니다. QQQ 거래량은 20일 평균의 {f('QQQ','volr'):.2f}배였습니다."),
   ('앞으로', f"RSI {f('^IXIC','rsi'):.0f}로 과매도라 기술적 반등이 나올 수 있는 자리지만, 200일선 25,157은 {pct(25157.47, f('^IXIC','close')):+.1f}% 위에 있습니다. 어제 저점 22,513을 지키는지가 먼저입니다.")]),
 '^GSPC': ('7일 연속 하락, 7,000선 아래로 내려온 하루', [
   ('어제', f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 6,910에 마감했습니다. 하루 고가 7,199에서 저가 6,883까지 밀렸고, 4월 이후 처음 7,000 아래로 내려왔습니다."),
   ('최근 대비', f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%입니다. 고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%로 조정에 들어갔고, SPY 거래량은 평균의 {f('SPY','volr'):.2f}배로 크게 늘었습니다."),
   ('앞으로', f"200일선 7,349는 {pct(7348.58, f('^GSPC','close')):+.1f}% 위로 멀어졌습니다. RSI {f('^GSPC','rsi'):.0f}의 과매도에서 어제 저점 6,883을 지키면 바닥 다지기, 깨지면 하락이 더 길어진다는 신호로 볼 수 있습니다.")]),
 'SOXX': ('-10.55%, 고점 대비 -44% 약세장', [
   ('어제', f"반도체 ETF는 {f('SOXX','chg'):+.2f}%로 123.40달러({won(123.40)})에 끝났습니다. 135.08달러({won(135.08)})에서 시작해 122.20달러({won(122.20)})까지 밀린 거의 일직선 하락입니다."),
   ('최근 대비', f"1주 {f('SOXX','w1'):+.1f}%, 1달 {f('SOXX','m1'):+.1f}%이고, 거래량은 평균의 {f('SOXX','volr'):.2f}배로 최근 6개월 중 가장 많았습니다."),
   ('앞으로', f"200일선 160.97달러({won(160.97)})는 {pct(160.97, f('SOXX','close')):+.1f}% 위로 멀고, RSI {f('SOXX','rsi'):.0f}로 과매도입니다. 어제 저점 122.20달러({won(122.20)})를 지키며 거래량이 붙는 반등이 나오는지가 먼저입니다.")]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = f"세 지수 모두 **20·50·200일선 아래**, **하루 저점 근처**에서 마감했습니다. S&P 500은 **고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%로 조정**, 반도체 ETF는 **-44%로 약세장**입니다."

# ── 트리맵 해설 ───────────────────────────────────────
for i in issue['treemap']['items']:
    if i.get('d'): i['ch'] = i['d']['ch']
tmi = issue['treemap']['items']; ups = sum(1 for i in tmi if i['ch'] > 0)
secw = {}
for i in tmi:
    a = secw.setdefault(i['s'], [0, 0]); a[0] += i['w']; a[1] += i['w'] * i['ch']
sw = {k: round(b / a, 1) for k, (a, b) in secw.items()}
gt = lambda t: next(i for i in tmi if i['t'] == t)['ch']
issue['treemap']['asof'] = CLOSE
issue['treemap']['comment'] = {
 'h': f"100개 중 {ups}개만 상승 — 반도체가 무너지고 헬스케어·필수소비재만 버틴 날",
 't': (f"어제는 상위 100개 중 {ups}개만 올랐습니다. 엔비디아({gt('NVDA')}%)·마이크론({gt('MU')}%)·AMD({gt('AMD')}%)·브로드컴({gt('AVGO')}%)이 10% 넘게 빠졌고, 오라클({gt('ORCL')}%)·테슬라({gt('TSLA')}%)·메타({gt('META')}%)도 크게 밀렸습니다. "
       f"오른 곳은 유나이티드헬스(+{gt('UNH')}%)·월마트(+{gt('WMT')}%)·존슨앤드존슨(+{gt('JNJ')}%)·펩시코(+{gt('PEP')}%) 같은 방어주였습니다. "
       f"업종별로는 정보기술 {sw['정보기술']}%가 가장 크게 밀렸고, 필수소비재({sw['필수소비재']:+}%)·헬스케어({sw['헬스케어']:+}%)·에너지({sw['에너지']:+}%)는 거의 흔들리지 않았습니다."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'AP', 'u': AP}, {'t': '야후 파이낸스', 'u': 'https://finance.yahoo.com'}]}

# ── 롱/숏 한마디 (11/18~11/20 실제 발언) ─────────────────
issue['street']['camps'] = {'long': [
 {'who': '댄 아이브스', 'role': '기술주 애널리스트 (11/20)', 'sil': 'glasses', 'say': '이번 급락 때 파는 건 잘못된 선택이라고 봐요.', 'src': CBS},
 {'who': '크리스 라킨', 'role': 'E*Trade (모건스탠리)', 'sil': 'suit_g', 'say': '이번 움직임은 심리에 크게 휘둘린 것 같아요.', 'src': FORT},
 {'who': '빈키 차다', 'role': '도이체방크 전략가', 'sil': 'firm', 'say': '시장이 아주 많이 팔린 상태(과매도)예요.', 'src': FORT},
 {'who': '척 칼슨', 'role': '호라이즌 인베스트먼트', 'sil': 'suit', 'say': '엔비디아는 실적에서 할 일을 다 했어요.', 'src': MSCR},
], 'short': [
 {'who': '리사 쿡', 'role': '연준 이사 (11/20)', 'sil': 'woman', 'say': '물가가 내려간다는 증거가 거의 없어요. 금리를 더 올려야 해요.', 'src': COOK},
 {'who': '카를로스 카사노바', 'role': '유니온 방케르 프리베', 'sil': 'suit', 'say': 'AI 투자 논리에 대한 믿음이 무너지고 있어요.', 'src': AJ},
 {'who': '애덤 크리사풀리', 'role': '바이탈 널리지', 'sil': 'glasses', 'say': '반도체엔 새 수출 규제 충격이 훨씬 클 수 있어요.', 'src': CBS},
 {'who': '오언 라몬트', 'role': '시장 연구자 (11/18)', 'sil': 'hood', 'say': '우리가 이미 AI 거품 안에 있을 확률은 70%예요.', 'src': LAMONT},
]}
issue['street']['title'] = '최근 눈에 띈 증권사 의견'
issue['street']['headline'] = '방어주는 올리고, 실적 실망 인튜이트·브로드컴은 목표를 내렸다'
issue['street']['summary'] = '급락장 속에서도 등급을 올린 곳은 유나이티드헬스·휴매나 같은 건강보험주였습니다. 실적 전망을 낮춘 인튜이트는 여러 곳이 목표주가를 내렸고, 브로드컴도 이번 주 하향이 이어졌습니다.'
issue['street']['summary_src'] = STL
issue['street']['rows'] = [
 {'stock': '유나이티드헬스', 'firm': 'TD 코웬', 'rating': '보유 → 매수', 'to': f"455달러({won(455)})", 'date': '11/20', 'dir': 1, 'src': STL, 't': 'UNH'},
 {'stock': '휴매나', 'firm': 'TD 코웬', 'rating': '매수 (상향)', 'to': f"485달러({won(485)})", 'date': '11/20', 'dir': 1, 'src': STL},
 {'stock': '인튜이트', 'firm': '제프리스', 'rating': '매수 유지 (목표 하향)', 'to': f"445달러({won(445)}, 이전 500달러)", 'date': '11/20', 'dir': -1, 'src': INTU_TV},
 {'stock': '인튜이트', 'firm': '바클레이스', 'rating': '비중확대 유지 (목표 하향)', 'to': f"385달러({won(385)}, 이전 408달러)", 'date': '11/20', 'dir': -1, 'src': INTU_TV},
 {'stock': '인튜이트', 'firm': 'UBS', 'rating': '중립 유지 (목표 하향)', 'to': f"315달러({won(315)}, 이전 360달러)", 'date': '11/20', 'dir': -1, 'src': INTU_TV},
 {'stock': '브로드컴', 'firm': '골드만삭스', 'rating': '매수 유지 (목표 하향)', 'to': f"460달러({won(460)}, 이전 540달러)", 'date': '11/18', 'dir': -1, 'src': AVGO_WS, 't': 'AVGO'},
 {'stock': '마이크론', 'firm': 'RBC', 'rating': '시장수익률 상회 유지', 'to': f"1,500달러({won(1500)})", 'date': '11/18', 'dir': 0, 'src': RBC_MU, 't': 'MU'},
 {'stock': '브로드컴', 'firm': '로스차일드 레드번', 'rating': '매수 → 중립', 'to': f"398달러({won(398)})", 'date': '11/13', 'dir': -1, 'src': NQ13, 't': 'AVGO'},
]
for r in issue['street']['rows']:
    t = r.pop('t', None); d_ = TD.get(t) if t else None
    if d_:
        tv = float(r['to'].split('달러')[0].replace(',', ''))
        r['c'] = d_[4]; r['rx'] = d_[5]; r['gap'] = round((tv / d_[4] - 1) * 100)

# ── 내 종목 분석 ──────────────────────────────────────
WHY3 = {'NVDA': 'SEC 회계 조사 보도에 -14%', 'AMD': '반도체 동반 급락, 전날 헌터브룩 공매도 보고서 여파', 'MU': '낸드 가격 하락 전망·메모리 급락',
        'SNDK': '8:1 분할 첫날, 낸드 가격 하락 전망에 -16%', 'AVGO': '구글 TPU 주문 축소 보도', 'UNH': 'TD 코웬 매수 상향', 'WMT': '전망 상향 뒤 방어주로 돈 이동',
        'SOXL': '반도체 -10.55%를 3배로 -31.8%', 'MSTR': '비트코인 6만 달러(약 8,080만 원) 붕괴', 'HOOD': '비트코인·위험자산 약세', 'COIN': '비트코인 6만 달러(약 8,080만 원) 붕괴',
        'CRWD': '장 마감 뒤 지스케일러 인수 협상 보도에 시간외 약 -8%'}
TN3 = {
 'SOXL': {'y': [(f"반도체 ETF {f('SOXX','chg'):+.2f}%를 3배로 받아 하루 {qc('SOXL'):+.2f}%, 1주 {q_['SOXL']['w1']:+}%", Y('SOXL')), ('수리수리진타리 ⑨ 카드: 11/20 시가 42.35달러(약 5.7만 원) 기준 손절선 33.88달러(약 4.6만 원) 아래로 마감', 'https://stock.jintar.co.kr/c/9/')],
          't': [('수요일 밤 PCE 물가·목요일 휴장으로 짧은 한 주', NQW)]},
 'NVDA': {'y': [('로이터: SEC가 회계 문제 가능성 조사 → -14.01%, 시총 약 4,910억 달러(약 661조 원) 증발', RTR), ('젠슨 황 전 CEO, 상원 공개 청문회 출석에 동의', HUANG)], 't': [('트럼프, 해외 데이터센터 짓는 기업에 세금 경고', TRUMP)]},
 'AMD': {'y': [('반도체 30종목 동반 하락, 전날 헌터브룩 공매도 보고서(AMD는 반박) 이후 이틀째 급락', AMD_HB)], 't': []},
 'MU': {'y': [("트렌드포스, 내년 1분기 낸드 계약가 0~5% 하락 전망 · 배런스 '메모리주 지독하게 싸다'", MU_WS)], 't': []},
 'SNDK': {'y': [('8:1 액면분할 첫 거래일(이전 종가 94.39달러, 약 12.7만 원으로 환산)', SPLIT), ('트렌드포스 2027년 낸드 가격 하락 전망에 메모리 급락', SNDK_WS)], 't': []},
 'SNXX': {'y': [('기초자산 샌디스크 -16%를 2배로 반영', SNDK_WS)], 't': []},
 'AVGO': {'y': [('밍치궈: 구글이 2027년 TPU 8i 주문 약 100만 개(약 20%) 줄여 미디어텍 쪽으로(확인 안 됨)', AVGO_SA)], 't': []},
 'UNH': {'y': [('TD 코웬, 보유 → 매수 · 목표 455달러(약 61만 원)', STL)], 't': []},
 'WMT': {'y': [('연간 전망 상향 뒤 방어주로 돈 이동, 하락장 속 +1.5%', MSCR)], 't': []},
 'CRWD': {'y': [('장 마감 뒤 지스케일러 인수 협상 보도 → 시간외 약 -8%', ZS)], 't': []},
 'MSTR': {'y': [('비트코인 6만 달러(약 8,080만 원) 아래로, 52주 최저', MSTR_BZ)], 't': []},
 'QQQ': {'y': [(f"나스닥100 -5.61%, 고점 대비 약 -20%", TKEY)], 't': [('수리수리진타리 ① 급락 초입 신호(B+) 진행 중', 'https://stock.jintar.co.kr/c/1/')]},
}
REASON = {
 'NVDA': 'SEC가 회계 문제 가능성을 조사한다는 로이터 보도에 하루 14% 빠졌습니다. 회사와 SEC는 보도에 답하지 않았습니다.',
 'AMD': '전날 헌터브룩 공매도 보고서에 이어 반도체 전체 급락에 휩쓸려 이틀 새 20% 가까이 밀렸습니다.',
 'MU': '트렌드포스의 낸드 가격 하락 전망과 AI 반도체 급락이 겹쳐 하루 13.9% 빠졌습니다.',
 'SNDK': '8:1 액면분할 첫날(분할 반영 이전 종가 94.39달러, 약 12.7만 원) 16% 넘게 빠졌습니다. 낸드 가격이 내년 1분기부터 내린다는 트렌드포스 전망이 부담입니다.',
 'AVGO': '구글이 TPU 주문을 줄였다는 밍치궈의 보도(확인 안 됨)로 하루 12% 넘게 빠졌습니다.',
 'SOXL': '반도체 지수를 하루 3배로 따라가는 상품이라 어제 하루에만 31.8% 빠졌습니다. 같은 폭으로 오르내려도 원금이 깎이는 구조입니다.',
 'UNH': '급락장에서 TD 코웬의 매수 상향과 방어주 선호로 2.8% 올랐습니다.',
 'WMT': '전망 상향과 방어주 선호로 하락장 속에서도 1.5% 올랐습니다.',
 'CRWD': '정규장 -5.76%에 이어, 장 마감 뒤 지스케일러 인수 협상 보도로 시간외에서 약 8% 더 내렸습니다.',
 'TSLA': '위험자산 회피 속에 7.6% 내렸습니다.',
 'MSTR': '비트코인이 6만 달러(약 8,080만 원) 아래로 내려가며 52주 최저로 밀렸습니다.',
 'QQQ': '나스닥100 ETF는 하루 5.67% 빠져 고점 대비 약 20%에 다가갔습니다.',
}
HL3 = {
 'SOXL': '하루 -31.8%, 3배 상품의 가장 아픈 얼굴',
 'NVDA': 'SEC 회계 조사 보도에 -14%, 고점 대비 거의 반 토막',
 'AMD': '공매도 보고서 다음 날 반도체 폭락까지, 이틀 새 -20%',
 'SNDK': '분할 첫날 -16%, 낸드 가격 하락 전망이 발목',
 'SNXX': '샌디스크 -16%를 2배로, 하루 -31.5%',
 'MU': '낸드 가격 하락 전망에 -13.9%',
 'AVGO': '구글 주문 축소 보도에 -12%',
 'TSM': '반도체 동반 급락 -9.5%',
 'ARM': '하루 -14%, 반도체 중 가장 크게 밀린 축',
 'QQQ': '하루 -5.7%, 고점 대비 약세장 문턱',
 'SOXX': '하루 -10.6%, 6개월 중 가장 많은 거래량',
 'UNH': '하락장 속 +2.8%, 매수 상향',
 'WMT': '하락장 속 +1.5%, 방어주 역할',
 'CRWD': '정규장 -5.8% 뒤 시간외 인수 협상 보도',
 'MSTR': '비트코인 약 8,080만 원(6만 달러) 붕괴에 52주 최저',
 'TSLA': '-7.6%, 위험자산 회피',
}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY3.get(t, '')
    n = TN3.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = (REASON[t] + ' ' if t in REASON else '') + ns['auto_ai'](q)
    q['h'] = HL3.get(t) or ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE

# ── 수리수리진타리 (stock.jintar.co.kr, 11/21 05:40 KST 슬롯) ──
JL = json.load(open('data/jintari_latest.json', encoding='utf-8'))
usd = lambda s: float(s.replace('$', '').replace(',', ''))
cards = []
c1 = next(x for x in JL['cards'] if x['n'] == 'QQQ')
qq = q_['QQQ']['c']; s1, t1, st1 = usd(c1['pxSig']), usd(c1['tgt']), usd(c1['stop'])
cards.append({'g': c1['g'], 't': 'QQQ', 'kn': c1['kn'], 's': c1['s'], 'ln': c1.get('ln', []),
  'rows': [('신호 기준가', f"{s1}달러({won(s1)}) · 11/19 발동"),
           ('어제 종가', f"{qq}달러({won(qq)}) · 기준가 대비 {(qq/s1-1)*100:+.1f}%"),
           ('익절 · 손절', f"+20%({t1}달러, {won(t1)}) · −15%({st1}달러, {won(st1)})"),
           ('보유 기간', '최대 40거래일, 40일째 종가에 정리')],
  'h': 'S&P 500이 60일 고점보다 8% 넘게 빠지면 켜지는 ① 급락 초입 카드',
  'why': '11/19 S&P 500이 60일 고점보다 8.1% 낮아져 ① 급락 초입 신호가 켜졌습니다. 2014~2026년 23번 중 40거래일 뒤 평균 +7.1%, 74%가 올랐다는 기록입니다. 다만 신호 뒤에도 하루 5% 넘게 더 빠졌고, 손절선은 기준가의 −15%로 넓게 잡혀 있습니다.',
  'img': 'https://stock.jintar.co.kr/c/1.jpg', 'u': 'https://stock.jintar.co.kr/c/1/'})
c9 = next(x for x in JL['cards'] if x['n'] == 'SOXL')
o9, st9, t9, s9 = 42.35, usd(c9['stop']), usd(c9['tgt']), usd(c9['pxSig'])
cl9 = q_['SOXL']['c']
cards.append({'g': c9['g'], 't': 'SOXL', 'kn': c9['kn'], 's': c9['s'], 'ln': c9.get('ln', []),
  'rows': [('신호 기준가', f"{s9}달러({won(s9)}) · 11/19 종가"),
           ('어제 시가 → 종가', f"{o9}달러({won(o9)}) → {cl9}달러({won(cl9)}), 시가 대비 {(cl9/o9-1)*100:.1f}%"),
           ('익절 · 손절', f"+40%({t9}달러, {won(t9)}) · −20%({st9}달러, {won(st9)})"),
           ('결과', f"종가가 손절선 {st9}달러({won(st9)}) 아래 — 규칙상 손절 구간")],
  'h': f"시가 대비 {(cl9/o9-1)*100:.0f}% — 손절선을 뚫은 ⑨ 카드",
  'why': f"11/19 반도체 ETF가 20일 최고 종가보다 20.7% 낮아져 ⑨ 신호가 다시 켜졌고, 카드는 11/20 시가 {o9}달러({won(o9)})를 기준으로 잡았습니다. 그날 반도체가 10% 넘게 빠지며 SOXL은 {cl9}달러({won(cl9)})로 끝나 −20% 손절선({st9}달러, {won(st9)})을 넘어섰습니다. 11/18 카드의 손절선(43.23달러, {won(43.23)})도 11/20 시가에서 이미 아래로 열렸습니다. 레버리지 상품은 손절 규칙을 미리 정해 두는 이유를 보여준 하루입니다.",
  'img': 'https://stock.jintar.co.kr/c/9.jpg', 'u': 'https://stock.jintar.co.kr/c/9/'})
issue['jintari'] = {'cards': cards, 'cash': [],
 'note': '발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다.',
 'u': JL_U, 'asof': '2026-11-20 장 종료 기준 · 카드 갱신 11/21 05:40 KST'}

# ── v11: 1면 두 건 + 사람들 반응, 간밤 뉴스에서 1면 두 건 빼기 (발행인 11/21) ──
SA='https://stockanalysis.com/news/broadcom-falls-google-tpu-cut-mediatek/'
W247='https://247wallst.com/investing/2026/11/20/broadcom-stock-plunges-12-and-loses-191-billion-after-a-report-that-google-cut-its-plans-for-broadcom-ai-chips/'
W247b='https://247wallst.com/investing/2026/11/20/broadcom-plunges-11-as-google-reportedly-shifts-tpu-orders-to-mediatek-overshadowing-goldmans-460-target-marvell-sinks-10/'
INV='https://invezz.com/news/2026/11/20/why-broadcom-shares-are-down-over-11-on-friday/'
TIP='https://tipranks.com/news/google-cuts-broadcom-ai-chip-orders-by-20-avgo-stock-sinks'
MB='https://www.marketbeat.com/instant-alerts/price-broadcom-nasdaq-avgo-stock-falls-124-heres-what-happened-2026-11-20/'
BG='https://finance.biggo.com/news/dd24faec-557c-44e9-bf10-6089d4d44839'
EXP='https://explainx.ai/blog/google-broadcom-tpu-8i-million-unit-cut-2027-claimed-vs-verified-2026'
KUO='https://x.com/mingchikuo/status/2123792271195918462'
ST_NV='https://stocktwits.com/news-articles/markets/equity/nvda-stock-clocks-worst-week-in-18-years-as-sec-reportedly-probes-its-accounting-practices/cNbSDIWR91Q'
YH_NV='https://finance.yahoo.com/markets/stocks/articles/nvda-stock-down-40-october-041800878.html'
YH_POLL='https://finance.yahoo.com/markets/stocks/articles/nvda-stock-heads-worst-week-032900844.html'
IBT='https://www.ibtimes.co.uk/nvidia-reddit-meme-executive-scandals-stock-gains-1831263'
GEN='https://stocktwits.com/news-articles/markets/equity/gary-gensler-says-key-question-in-nvidia-probe-is-whether-huang-misled-shareholders-sees-ai-repricing-ahead/cNGrO6sR9ev'
DCD='https://www.datacenterdynamics.com/en/news/nvidia-says-its-not-like-enron-in-leaked-memo-to-financial-analysts/'
issue['top']['react'] = [
 {'p': '스톡트윗', 't': '그날 하루도 개인 투자자 분위기는 여전히 "매우 낙관" — 글 수는 "매우 많음"으로 폭발', 'u': ST_NV},
 {'p': '스톡트윗', 't': '"이 가격이면 코로나 이후 가장 쉬운 돈벌이"라며 줍줍을 외치는 글', 'u': YH_NV},
 {'p': '스톡트윗', 't': '지난주 투표에선 10명 중 6명꼴이 "떨어질 때 산다", 4명은 "일단 피한다"', 'u': YH_POLL},
 {'p': '스톡트윗', 't': '엔비디아 앞날을 두고 개인들끼리도 의견이 크게 갈리는 중', 'u': YH_POLL},
 {'p': '레딧', 't': '창업자 스캔들 뒤 오히려 주가가 더 올랐던 베이조스·게이츠 사례를 붙인 "그냥 사" 밈', 'u': IBT},
 {'p': 'TV', 't': '크레이머: 엔비디아가 시장 전체에 그늘을 드리우고 다른 종목까지 물들인다', 'u': YH_NV},
 {'p': 'TV', 't': '크레이머: 황의 복귀설이 오히려 회사를 더 가라앉히고 있다', 'u': YH_NV},
 {'p': '전문가', 't': '전 SEC 위원장 겐슬러: 핵심은 투자자를 오도했느냐, 시장은 이미 "중대한 일"로 본다', 'u': GEN},
 {'p': '회사', 't': '엔비디아는 예전부터 "엔론·월드컴 같은 회계 사기와 다르다"고 반박해 왔다', 'u': DCD},
]
F_ = TD['AVGO'] if 'AVGO' in TD else None
issue['top2'] = {
 'kicker': '두 번째 큰 뉴스',
 'title': "브로드컴 -12%, '구글이 AI칩 주문 20% 줄였다' 설문 한 장에 휘청",
 'img': 'img/2026-11-21-top2.jpg',
 'points': [
  {'t': "TF인터내셔널 궈밍치 애널리스트가 X에 '구글이 2027년 브로드컴 설계 TPU 8i 출하를 약 100만 개, 20%가량 줄였다'는 업계 설문 결과를 올렸습니다. 대신 미디어텍이 설계한 TPU 8t를 늘릴 계획이라고 했습니다.", 'src': SA},
  {'t': f"브로드컴은 {F_[5]:+.2f}%, {F_[4]}달러({won(F_[4])})로 마감했습니다. 거래량은 평소의 약 2배였습니다.", 'src': MB},
  {'t': '목요일 종가 이후 시가총액 약 1,910억 달러(약 257조 원)가 증발했고, 최고가보다 36% 낮아졌습니다.', 'src': W247},
  {'t': '구글과 브로드컴은 이 내용을 확인하지 않았습니다. 같은 날 골드만삭스는 12개월 주가 전망을 540달러(약 73만 원)에서 460달러(약 62만 원)로 낮췄습니다.', 'src': INV},
  {'t': '맞춤형 AI칩을 설계하는 마벨도 -10%로 같이 밀렸습니다.', 'src': W247b},
 ],
 'risks': [
  {'t': '팁랭크스는 구글이 AI 투자를 줄이는 게 아니라 연산 자원을 다시 나누는 것이라고 봤습니다.', 'src': TIP},
  {'t': '반도체 전체가 무너진 날이라 이 보도만의 영향으로 보기는 어렵다는 분석도 있습니다.', 'src': BG},
 ],
 'why': '엔비디아 다음 AI 반도체 대장으로 꼽히던 브로드컴이 최대 고객 구글의 주문 축소설에 흔들렸습니다. 맞춤형 AI칩 이야기가 꺾이는지가 관건입니다.',
 'watch': ['구글·브로드컴이 공식 입장을 내는지', '12월 9일 브로드컴 실적 발표에서 2027년 AI 매출 전망', '미디어텍·마벨 등 맞춤칩 경쟁사 주가 흐름'],
 'src': [{'t': 'StockAnalysis', 'u': SA}, {'t': '24/7 Wall St.', 'u': W247}, {'t': 'Invezz', 'u': INV}, {'t': '궈밍치 X', 'u': KUO}],
 'react': [
  {'p': 'X', 't': '궈밍치 본인: 구글이 최첨단 모델 개발에 연산을 먼저 몰아주려는 조정일 뿐', 'u': KUO},
  {'p': 'X', 't': '"추론칩을 줄이는 건 말이 된다"며 구글 결정에 수긍하는 답글', 'u': KUO},
  {'p': '분석', 't': '"브로드컴은 양쪽에서 맞고 있다" — 주문 축소설에 AI 반도체 몸값 낮추기까지 겹쳤다는 매도 의견', 'u': INV},
  {'p': '분석', 't': '"구글 발표는 없고 설문뿐" — 확인된 사실이 아니라 분위기라는 지적', 'u': EXP},
  {'p': '분석', 't': 'AI 투자를 줄이는 게 아니라 배분을 바꾸는 것이라는 해석', 'u': TIP},
  {'p': '분석', 't': '반도체 전체 투매 날이라 이 보도 탓만 하긴 어렵다는 시각', 'u': BG},
  {'p': '시장', 't': '골드만의 460달러(약 62만 원) 주가 전망이 그나마 반론으로 거론됨', 'u': MB},
  {'p': '시장', 't': '이득은 미디어텍, 매도는 마벨 등 다른 맞춤칩 설계사로 번졌다는 반응', 'u': W247b},
  {'p': '시장', 't': '결국 12월 9일 실적에서 확인하자며 관망하는 분위기', 'u': W247},
 ],
}
issue['news'] = [n for n in issue['news'] if n['img'] not in ('img/2026-11-21-nvda.jpg', 'img/2026-11-21-chip.jpg')]

issue['site_v'] = 11
issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 CNBC·야후 파이낸스 일봉(11/20 종가) 기준이며, 증권사·전문가 의견은 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

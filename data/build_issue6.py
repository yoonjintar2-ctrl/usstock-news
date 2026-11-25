"""제6호(2026-11-26 목, 미국 11/25 수 장) — build_issue3.py 와 같이 build_issue1.py 틀을 돌린 뒤 글·일정·의견을 11/25 장 기준으로 바꾼다.
숫자는 data/*(CNBC 일봉, 11/25 종가)와 아래 출처의 확인값만 쓴다. 샌디스크는 8:1 액면분할 반영가."""
import json

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1344.26"), ("D = '2026-11-19'", "D = '2026-11-26'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-25 16:00 ET 종가'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-26 06:40 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 6, 'weekday': '목'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-25(수) 뉴욕장'"),
       ("'ma200':1284.66", "'ma200':160.84"),  # 샌디스크 8:1 분할 반영(tickers_mini 값)
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


jo = lambda usd_e8: f"약 {usd_e8 * 1e8 * FX / 1e12:,.0f}조 원"   # 억 달러 → 조 원
eok = lambda usd_e8: f"약 {usd_e8 * 1e8 * FX / 1e8:,.0f}억 원"   # 억 달러 → 억 원


# ── 출처 (11/25 장) ─────────────────────────────────────
YLIVE = 'https://finance.yahoo.com/markets/live/stock-market-today-wednesday-november-25-dow-sp-500-nasdaq-pce-inflation-data-091428237.html'
KIP = 'https://www.kiplinger.com/investing/stocks/stocks-rally-off-lows-despite-inflation-and-ai-gloom-stock-market-today'
KITCO = 'https://www.kitco.com/news/off-the-wire/2026-11-25/nasdaq-sinks-about-4-ai-rout-fresh-trump-tariffs-spook-wall-st'
STL = 'https://www.stocktitan.net/articles/stock-market-today-live-november-25-2026'
INV_RB = 'https://ca.investing.com/news/stock-market-news/wall-street-rebounds-amid-fragile-sentiment-as-nasdaq-recovers-from-steep-morning-drop-93CH-4981517'
TIPR = 'https://www.tipranks.com/news/stocks-finish-mostly-lower-ahead-of-u-s-thanksgiving'
ST_N100 = 'https://stocktwits.com/news-articles/markets/equity/nasdaq-100-flirts-with-bear-market-territory-drops-20-from-october-highs/cNbHVpRR9mM'
ST_DOW = 'https://stocktwits.com/news-articles/markets/equity/dow-craters-over-1000-points-nasdaq-slips-4-as-ai-trade-unravels-investors-digest-pce-inflation-fresh-tariff-proposal/cNbHjJvR9mj'
FOOL_NV = 'https://www.fool.com/investing/2026/11/25/why-nvidia-stock-is-falling-again/'
DISR = 'https://www.disruptionbanking.com/2026/11/25/why-are-ai-credit-default-swaps-hitting-record-spreads/'
Y_CRWV = 'https://finance.yahoo.com/technology/ai/articles/coreweave-nvidia-credit-risk-hit-164402586.html'
SA_NV = 'https://stockanalysis.com/news/nvidia-gives-back-half-huang-rally/'
NAT_HU = 'https://www.thenationalnews.com/future/technology/2026/11/25/jensen-huang-testimony-dates-congress-nvidia/'
TECHT = 'https://www.techtimes.com/articles/331408/20261124/nvidias-jensen-huang-face-lawmakers-public-hearings-following-his-reinstatement-ceo.htm'
ST_ELE = 'https://stocktwits.com/news-articles/markets/equity/mohamed-el-erian-is-buying-the-tech-dip-very-slowly-says-nvidia-is-too-big-to-wobble/cNbHNilR9mp'
Y_MEM = 'https://finance.yahoo.com/markets/stocks/articles/mu-skhy-sndk-stocks-focus-082710611.html'
ST_DIP = 'https://stocktwits.com/news-articles/markets/equity/nvda-dip-buyers-still-fighting-break-even-after-huang-return-analyst-says/cNbHEckR9lm'
X_HEDG = 'https://247wallst.com/cards/xpost-01m89km0ncjhxgb172yg75d7zw'
ROIC_GS = 'https://www.roic.ai/news/goldman-strategist-warns-its-too-early-to-buy-the-ai-selloff-as-markets-remain-fragile-11-25-2026'
ROIC_BT = 'https://www.roic.ai/news/btigs-krinsky-says-use-rallies-above-7300-to-cut-ai-and-tech-exposure-11-25-2026'
LB_BANK = 'https://longbridge.com/en/news/306802027'
LB_BOND = 'https://longbridge.com/en/news/306824440'
FOOL_SNDK = 'https://www.fool.com/investing/2026/11/25/why-sandisk-stock-just-dropped-again/'
PARA_SNDK = 'https://parameter.io/sandisk-sndk-stock-falls-8-after-trendforce-trims-nand-price-outlook/'
Y_MU7 = 'https://finance.yahoo.com/markets/stocks/articles/micron-falls-7-weaker-dram-141311449.html'
# 물가·관세
Y_PCE = 'https://finance.yahoo.com/economy/policy/article/feds-favored-inflation-gauge-heats-up-solidifying-a-rate-hike-in-december-with-more-likely-next-year-135510084.html'
SA_PCE = 'https://stockanalysis.com/news/us-pce-inflation-october-2026/'
DUKE = 'https://duke.fm/2026/11/25/us-inflation-rises-further-in-october-2/'
CRISK = 'https://calculatedrisk.substack.com/p/new-home-sales-increase-to-701000'
BEIGE = 'https://www.investing.com/news/economy-news/fed-beige-book-shows-slight-growth-sticky-inflation-ahead-of-dec-meeting-5051430'
BEIGE2 = 'https://gsmglobalnews.com/article/d20261125-beige1.html'
FW_PM = 'https://predictionmarketspicks.com/articles/fed-hike-odds-october-pce-gdp-december-2026-kalshi-polymarket-futures'
FW_AM = 'https://marketspeaker.com/briefs/december-fed-rate-hike-odds-98-percent-cme-fedwatch'
USTR = 'https://ustr.gov/about/policy-offices/press-office/press-releases/2026/november/ustr-makes-determinations-and-proposes-actions-14-section-301-investigations-relating-structural'
Y_TAR = 'https://finance.yahoo.com/markets/article/us-announces-new-tariffs-of-up-to-20-on-china-the-eu-and-12-other-nations-131802359.html'
KT_TAR = 'https://www.koreatimes.co.kr/world/20261126/us-proposes-tariffs-over-excess-production-retains-15-cap-for-korea-japan-eu'
RSM = 'https://realeconomy.rsmus.com/inflation-rises-and-income-is-stout-as-u-s-imposes-new-tariffs/'
INVN = 'https://www.investmentnews.com/equities/pce-inflation-gauge-still-running-hot-as-december-rate-hike-looms/269173'
X_BESP = 'https://247wallst.com/cards/xpost-01m89nbay65fxr3t4wwdd6xy1p'
X_HEDG2 = 'https://247wallst.com/cards/xpost-01m89g6kktekms4fjnv7rb8408'
ST_YARD = 'https://stocktwits.com/news-articles/markets/equity/fed-december-rate-hike-oil-prices-nvidia-rally-inflation/cNbuClGR9l5'
CN_MFA = 'https://www.newsminimalist.com/articles/china-rejects-us-tariffs-on-false-overcapacity-premise-90c3bc22'
FALK = 'https://falkenstein.substack.com/p/tariffs-a-tech-bear-market-and-a'
FG17 = 'https://longbridge.com/en/news/306739800'
# 종목
HPQ_K = KIP
HPQ_PR = 'https://www.stocktitan.net/news/HPQ/hp-inc-reports-fiscal-2026-full-year-and-fourth-quarter-results-uf92ayljaqtq.html'
HPQ_W = 'https://247wallst.com/investing/2026/11/25/hp-earnings-memory-went-from-15-to-40-of-a-pcs-parts-cost-in-a-year/'
DE_SEC = 'https://www.sec.gov/Archives/edgar/data/0000315189/000110465926131741/de-ex99d1.htm'
DE_INV = 'https://www.investing.com/news/transcripts/earnings-call-transcript-deere-q4-2026-revenue-beats-as-eps-misses-forecast-93CH-5051213'
NTNX_P = 'https://parameter.io/nutanix-ntnx-stock-drops-17-as-ceo-exit-and-flat-guidance-overshadow-earnings-beat/'
NTNX_F = 'https://www.fool.com/investing/2026/11/25/why-nutanix-plunged-today/'
ORCL_F = 'https://www.fool.com/investing/2026/11/25/why-oracle-stock-slumped-today/'
ORCL_U = 'https://unusualwhales.com/news/oracle-stock-falls-new-52-week-low-2026-11-25'
META_J = 'https://journalarta.com/en/2026/11/26/meta-platforms-shares-rise-2-5-as-ai-loan-and-amazon-talks-draw-focus/'
ADI_W = 'https://247wallst.com/investing/2026/11/25/analog-devices-stock-just-had-its-worst-day-since-1998/'
ADI_TR = 'https://www.investing.com/news/analyst-ratings/truist-cuts-analog-devices-stock-price-target-to-323-on-cyclical-peak-signals-93CH-5050894'
ADI_BS = 'https://www.investing.com/news/analyst-ratings/analog-devices-stock-price-target-lowered-to-410-by-bernstein-socgen-on-multiple-reset-93CH-5050373'
ADI_MS = 'https://www.marketbeat.com/instant-alerts/analyst-analog-devices-nasdaq-adi-price-target-cut-to-40300-by-analysts-at-morgan-stanley-2026-11-25/'
ASTS_W = 'https://247wallst.com/investing/2026/11/25/ast-spacemobile-surges-9-erasing-early-losses-as-space-stocks-diverge-spacex-eases-rocket-lab-holds-steady/'
ASTS_ST = 'https://stocktwits.com/news-articles/markets/equity/asts-stock-bulls-director-dip-buy-bet-on-launch-fueled-comeback/cNbHb6dR9lO'
ANT_W = 'https://247wallst.com/investing/2026/11/25/anthropics-sharp-reversal-up-4-ant-stock-reclaims-83-ipo-price-after-early-8-drop-coreweave-slides-2-iren-holds-steady/'
ANT_TT = 'https://www.techtimes.com/articles/331481/20261125/anthropic-stock-falls-below-83-ipo-price-after-morgan-stanley-ended-price-support-early.htm'
ANT_AR = 'https://fourweekmba.com/ai-arete-starts-anthropic-at-300-3-7x-tuesdays-81-91-close/'
ABC = 'https://abcnews.com/Business/stocks-tumble-tech-sell-off-resumes-nvidia-falls/story?id=138442070'
GOLD_Y = 'https://finance.yahoo.com/markets/commodities/articles/gold-price-today-november-25-110850194.html'
GOLD_LB = 'https://longbridge.com/en/news/306811592'
BTC_F = 'https://fortune.com/article/price-of-bitcoin-11-25-2026/'
HPQ_BC = 'https://rallies.ai/news/hp-inc-barclays-raises-target-price-to-24-from-23-0253852642e53caf'
EXPE = 'https://skift.com/2026/11/25/expedia-to-buy-kiwi-com-extending-its-acquisition-spree-into-flights/'
# 의견·일정
BNNB = 'https://www.bnnbloomberg.ca/markets/2026/11/25/mike-vinokurs-top-picks-for-nov-25-2026/'
IRISH = 'https://www.irishtimes.com/business/2026/11/25/us-stocks-sell-off-deepens-as-ai-trade-cracks/'
OINV = 'https://en.oninvest.com/article/a-rather-fragile-market-goldman-strategist-calls-buying-ai-stocks-premature'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
LPB = 'https://leprivatebanker.com/2026/11/25/nasdaq-futures-sink-up-to-3-as-chip-rout-deepens-ahead-of-pce-data-and-a-holiday-shortened-week/'
ADOBE = 'https://news.adobe.com/news/2026/09/adobe-us-holiday-shopping-season-to-hit-record'
BLS = 'https://www.bls.gov/schedule/2026/12_sched_list.htm'
FORBES_HU = 'https://www.forbes.com/sites/saradorn/2026/11/17/huang-agrees-to-testify-before-congress-on-dec-1/'
MRVL_IR = 'https://investor.marvell.com/news-events/press-releases/detail/1041/marvell-technology-inc-announces-conference-call-to-review-third-quarter-of-fiscal-year-2027-financial-results'
CRM_IR = 'https://investor.salesforce.com/news/news-details/2026/Salesforce-Announces-Date-of-Third-Quarter-Fiscal-2027-Earnings-Release-and-Webcast/default.aspx'
EW = 'https://www.earningswhispers.com/calweek/20261130'
CONT = 'https://continuumeconomics.com/a/13d43c4f/preview-due-december-4-us-november-employment-non-farm-payrolls-slower-but-far-from-weak'
BLACKOUT = 'https://propdatalab.com/fomc-blackout-period-calendar-fed-speeches/'
JL_U = 'https://stock.jintar.co.kr/'

q_ = {q['t']: q for q in issue['quotes']['list']}
g = lambda t: f(t, 'chg') if t in summ else (TD[t][5] if t in TD else q_[t]['ch'])
qc = lambda t: q_[t]['ch']
SOX = f('^SOX', 'chg')
pct = lambda a, b: (a / b - 1) * 100
lowp = lambda s: pct(f(s, 'low'), f(s, 'prev'))
tdlow = lambda t: pct(TD[t][3], TD[t][4] / (1 + TD[t][5] / 100))

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스',
 'title': f"AI 신용 공포에 반도체 장중 {lowp('^SOX'):.0f}%…마감 땐 {SOX:+.2f}%로 대부분 되돌려",
 'img': 'img/2026-11-26-top.jpg',
 'points': [
  {'t': f"장 초반 나스닥은 4% 넘게, 다우는 1,000포인트 넘게 빠졌고 나스닥100은 10월 고점보다 20% 가까이 낮아져 약세장 문턱까지 갔습니다. 마감은 나스닥 {f('^IXIC','chg'):+.2f}%, S&P 500 {f('^GSPC','chg'):+.2f}%, 다우 {f('^DJI','chg'):+.2f}%였습니다.", 'src': KITCO},
  {'t': f"필라델피아 반도체 지수는 장중 {f('^SOX','low'):,.0f}(전날보다 {lowp('^SOX'):.1f}%)까지 밀렸다가 {f('^SOX','close'):,.2f}({SOX:+.2f}%)로 끝났습니다. VIX도 장중 {f('^VIX','high'):.2f}까지 올랐다가 {f('^VIX','close'):.2f}로 내려왔습니다.", 'src': INV_RB},
  {'t': "불씨는 신용시장이었습니다. S&P 글로벌 집계로 코어위브 5년 신용부도스와프(CDS)가 1,314bp로 사상 최고가 됐고, 오라클·알파벳·엔비디아 CDS도 기록을 새로 썼습니다. AI 투자를 빚으로 대는 구조에 대한 걱정입니다.", 'src': FOOL_NV},
  {'t': f"엔비디아는 장중 {TD['NVDA'][3]}달러({tdlow('NVDA'):.1f}%)까지 내렸다가 {TD['NVDA'][4]}달러({won(TD['NVDA'][4])}), {g('NVDA'):+.2f}%로 마감했습니다. 이틀 사이 월요일 +31.5% 상승분의 절반 넘게를 돌려줬습니다.", 'src': SA_NV},
  {'t': "장중 나스닥100 하락분의 60% 넘게가 엔비디아·마이크론·인텔·AMD·램리서치·어플라이드머티어리얼즈 6개 반도체주에서 나왔습니다(블룸버그 집계).", 'src': ST_N100},
 ],
 'risks': [
  {'t': "바닥에서 사려는 돈이 들어오며 소재·에너지·부동산이 1% 넘게 올랐고 다우는 플러스로 끝났습니다. 다만 나스닥 신저가 종목이 465개로 신고가(34개)보다 훨씬 많아 '불안한 반등'이라는 평가입니다.", 'src': INV_RB},
  {'t': "모하메드 엘에리언은 '길게 보면 기회'라며 기술주를 아주 천천히 사고 있다고 했고, 소시에테제네랄은 VIX가 30을 넘은 뒤 S&P 500이 12개월 동안 평균 22% 올랐다는 과거 통계를 냈습니다.", 'src': ST_ELE},
 ],
 'why': '주가보다 먼저 회사채·CDS 같은 신용시장이 AI 투자에 경고를 보냈다는 점이 새롭습니다. 주가는 하루 만에 대부분 되돌렸지만, 빚으로 지은 데이터센터의 돈줄이 흔들리면 칩 주문도 흔들릴 수 있다는 걱정이 남았습니다.',
 'watch': [
  '코어위브·오라클 CDS가 더 오르는지(신용시장 신호)',
  '12/1(미국) 황 CEO 하원 비공개 면담 · 12/3 상원 은행위 공개 청문회',
  f"반도체 ETF(SOXX)가 어제 장중 저점 {f('SOXX','low')}달러({won(f('SOXX','low'))})를 지키는지",
 ],
 'src': [{'t': 'Kitco(로이터)', 'u': KITCO}, {'t': 'Investing.com 마감', 'u': INV_RB}, {'t': 'Motley Fool(엔비디아·CDS)', 'u': FOOL_NV}, {'t': 'StockAnalysis', 'u': SA_NV}, {'t': 'Stocktwits(나스닥100)', 'u': ST_N100}, {'t': '야후 파이낸스 실시간', 'u': YLIVE}],
 'react': [
  {'p': '스톡트윗', 't': "엔비디아 게시판 분위기가 '매우 낙관'에서 '낙관'으로 한 단계 식고 글 수도 줄었음(11:40 ET)", 'u': ST_ELE},
  {'p': '스톡트윗', 't': "마이크론·샌디스크 게시판은 트렌드포스 하향에도 '낙관' 유지, 요즘 시장은 실적대로 안 움직인다는 푸념도", 'u': Y_MEM},
  {'p': '스톡트윗', 't': "AI 칩 고객이 빚을 내 사는 것이라 수요가 아니라 '신용 사슬'이라는 경고 글", 'u': ST_DIP},
  {'p': 'X', 't': '헤지아이: 나스닥100이 고점 대비 -19.5%, 약세장 직전이라고 알림(09:58 ET)', 'u': X_HEDG},
  {'p': 'X', 't': '로스 거버(거버 가와사키): 지금 공포는 지나치다며 일축', 'u': ST_N100},
  {'p': 'TV', 't': "CNBC 엘에리언: 기술주를 아주 천천히 산다, 엔비디아는 '흔들리기엔 너무 크다'", 'u': ST_ELE},
  {'p': 'TV', 't': 'CNBC 리즈 앤 손더스(슈왑): AI 매도는 황 뉴스 전부터 시작됐다, 지배구조 문제만이 아니다', 'u': STL},
  {'p': '전문가', 't': '노무라 맥엘리곳: 분위기가 나쁘고, 월요일 황 복귀로 바뀐 건 별로 없다', 'u': YLIVE},
  {'p': '전문가', 't': '골드만 뮐러글리스만: AI 매도를 사기엔 이르다, 시장이 깨지기 쉬운 상태', 'u': ROIC_GS},
  {'p': '분석', 't': 'BTIG 크린스키: S&P 7,250~7,350까지 반등을 보지만 7,300 위에선 AI 비중을 줄이라고', 'u': ROIC_BT},
  {'p': '시장', 't': "올스프링 클레그: AI 회사채가 '블랙프라이데이 세일', 싼 건지 떨어지는 칼인지 묻는다", 'u': Y_CRWV},
  {'p': '분석', 't': "인터랙티브브로커스 소스닉: 엔비디아를 받치는 '정치적 풋'은 수명이 짧다", 'u': SA_NV},
 ],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': f"다우는 장 초반 1,100포인트 가까이 빠졌다가 오름세로 돌아 {f('^DJI','close'):,.0f}에 끝났습니다. 나스닥은 장중 {lowp('^IXIC'):.1f}%에서 {f('^IXIC','chg'):+.2f}%까지, 반도체 지수는 {lowp('^SOX'):.1f}%에서 {SOX:+.2f}%까지 되돌렸습니다.",
 'src': TIPR,
}

# ── 참고 지표 ─────────────────────────────────────────
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'prev'), 2)
issue['indicators'] = [
 {'name': '12월 금리 인상 확률', 'v': 95.8, 'd': 1, 'suf': '%', 'src': FW_PM},
 {'name': 'VIX', 'v': f('^VIX', 'close'), 'd': 2, 'chg': f('^VIX', 'chg'), 'src': Y('%5EVIX')},
 {'name': '미 국채 10년', 'v': f('^TNX', 'close'), 'd': 2, 'suf': '%', 'chg': TNX_CH, 'chgsuf': '%p', 'src': Y('%5ETNX')},
 {'name': '달러인덱스', 'v': f('DX-Y.NYB', 'close'), 'd': 2, 'chg': f('DX-Y.NYB', 'chg'), 'src': Y('DX-Y.NYB')},
 {'name': 'WTI 유가', 'v': f('CL=F', 'close'), 'd': 2, 'chg': f('CL=F', 'chg'), 'src': Y('CL%3DF')},
 {'name': '금', 'v': f('GC=F', 'close'), 'd': 1, 'chg': f('GC=F', 'chg'), 'src': Y('GC%3DF')},
 {'name': '원/달러', 'v': FX, 'd': 2, 'chg': f('KRW=X', 'chg'), 'src': Y('KRW%3DX')},
]
issue['gauges'] = [x for x in issue.get('gauges', []) if x['name'] == 'VIX 변동성']
for x in issue['gauges']:
    x['note'] = f"하루 {f('^VIX','chg'):+.1f}% · 장중 {f('^VIX','high'):.2f}까지 올랐다 내려옴 · CNN 공포·탐욕 지수 17(극단적 공포, 11/24 마감 기준)"
issue['macro'] = []

# ── 간밤 뉴스 (1면 두 건 제외) ────────────────────────
issue['news'] = [
 {'tag': '메모리', 'img': 'img/2026-11-26-memory.jpg', 'title': f"트렌드포스, 내년 메모리 값 전망 낮춰…샌디스크 {g('SNDK'):.2f}%, 마이크론 {g('MU'):.2f}%",
  'line': f"중국 클라우드 회사들이 2027년 서버 메모리 주문을 줄여 내년 D램 계약가 상승 폭이 좁아지고, 내년 1분기 낸드 계약가는 보합~5% 하락으로 봤습니다. 샌디스크는 {TD['SNDK'][4] if 'SNDK' in TD else q_['SNDK']['c']}달러로 끝났고 에버코어는 적정 주가를 200→175달러({won(175)})로 낮췄습니다.",
  'src': [{'t': 'Motley Fool(샌디스크)', 'u': FOOL_SNDK}, {'t': 'Parameter(에버코어)', 'u': PARA_SNDK}, {'t': '야후 파이낸스(트렌드포스)', 'u': Y_MEM}]},
 {'tag': '실적', 'img': 'img/2026-11-26-earn.jpg', 'title': f"HP +11.4% S&P 500 1위, 디어 {TD['DE'][5]:+.2f}%, 뉴타닉스 약 -18%",
  'line': f"HP는 분기 매출 160억 달러({jo(160)}), 조정 주당순이익 0.83달러(예상 약 0.74달러)로 예상을 넘었고 메모리·저장장치가 PC 부품값의 약 40%가 됐다고 밝혔습니다. 디어는 주당순이익이 3.89달러로 예상에 못 미쳤지만 매출 121.2억 달러({jo(121.2)})가 예상을 넘어 반등했고, 뉴타닉스는 CEO 사임 예고에 급락했습니다.",
  'src': [{'t': 'Kiplinger(HP)', 'u': HPQ_K}, {'t': 'HP 실적 발표', 'u': HPQ_PR}, {'t': '디어 실적(SEC)', 'u': DE_SEC}, {'t': 'Parameter(뉴타닉스)', 'u': NTNX_P}]},
 {'tag': '신용', 'img': 'img/2026-11-26-orcl.jpg', 'title': f"오라클 {g('ORCL'):.2f}%, 52주 신저가…CDS 약 360bp 사상 최고",
  'line': f"오라클 5년 CDS는 11/24 약 360bp로 2025년 중반 35bp의 10배가 됐습니다. 잉여현금흐름이 마이너스이고, 주가 {TD['ORCL'][4]}달러({won(TD['ORCL'][4])})는 11/2 유상증자 가격 116달러보다 낮습니다.",
  'src': [{'t': 'Motley Fool(오라클)', 'u': ORCL_F}, {'t': 'Unusual Whales', 'u': ORCL_U}]},
 {'tag': '빅테크', 'img': 'img/2026-11-26-bigtech.jpg', 'title': f"메타 {g('META'):+.2f}%, 아마존 {g('AMZN'):+.2f}%…빅테크 엇갈림",
  'line': f"메타와 아마존이 메타의 AI 쇼핑 에이전트 'Muse' 차단을 풀기 위한 협상을 한다는 포춘 보도가 나왔습니다(두 회사 모두 확인 안 함). 아마존은 장중 약 5%까지 밀렸고 알파벳 {g('GOOGL'):+.2f}%, 마이크로소프트 {g('MSFT'):+.2f}%였습니다.",
  'src': [{'t': 'JournalArta(메타)', 'u': META_J}, {'t': 'Kitco(로이터)', 'u': KITCO}]},
 {'tag': '상장', 'img': 'img/2026-11-26-ipo.jpg', 'title': f'앤트로픽, 장중 -9%에서 반등해 공모가 83달러({won(83)}) 언저리',
  'line': f"장중 약 75.6달러까지 밀렸다가 약 82.8달러({won(82.8)}), +1.1% 안팎으로 끝났습니다. 모건스탠리가 주가 안정 매수를 일찍 끝낸 것이 부담으로 거론됐고, 아레테는 '매수'·적정 주가 300달러({won(300)})로 분석을 시작했습니다.",
  'src': [{'t': 'ABC 뉴스', 'u': ABC}, {'t': '24/7 Wall St.', 'u': ANT_W}, {'t': 'TechTimes', 'u': ANT_TT}, {'t': 'FourWeekMBA(아레테)', 'u': ANT_AR}]},
 {'tag': '반등', 'img': 'img/2026-11-26-rebound.jpg', 'title': f"ADI {g('ADI'):+.2f}% 반등, AST 스페이스모바일 {qc('ASTS'):+.2f}%",
  'line': f"전날 1998년 이후 최악(-17.37%)이었던 아날로그디바이스가 일부 되돌렸지만 트루이스트·모건스탠리 등은 적정 주가를 낮췄습니다. AST 스페이스모바일은 52주 신저가에서 이사의 약 103만 달러({eok(0.0103)}) 자사주 매입 공시 뒤 반등했습니다.",
  'src': [{'t': '24/7 Wall St.(ADI)', 'u': ADI_W}, {'t': 'Investing.com(트루이스트)', 'u': ADI_TR}, {'t': '24/7 Wall St.(ASTS)', 'u': ASTS_W}, {'t': 'Stocktwits(ASTS)', 'u': ASTS_ST}]},
 {'tag': '자산', 'img': 'img/2026-11-26-gold.jpg', 'title': f"금 장중 {f('GC=F','low'):,.0f}달러({won(f('GC=F','low'))}) 1년여 최저 뒤 반등, 비트코인 5.9만 달러 안팎({won(59000)})",
  'line': f"뜨거운 물가로 금리 인상 전망이 굳자 금 선물은 장중 {f('GC=F','low'):,.1f}달러({won(f('GC=F','low'))})까지 밀렸다가 {f('GC=F','close'):,.1f}달러로 끝났습니다(선물 마지막 체결가). 비트코인은 ETF 자금 유출 속에 5만 8~9천 달러대({won(59000)} 안팎)였습니다.",
  'src': [{'t': '야후 파이낸스(금)', 'u': GOLD_Y}, {'t': 'Longbridge(금 선물)', 'u': GOLD_LB}, {'t': 'Fortune(비트코인)', 'u': BTC_F}]},
]
for n in issue['news']:
    n['body'] = n['line']

issue['movers'] = [
 {'ticker': t, 'name': nm, 'close': N(TD[t][4], Y(t), CLOSE), 'chg_pct': N(TD[t][5], Y(t), CLOSE), 'won': won(TD[t][4]), 'why': why}
 for t, nm, why in [('ADI', '아날로그디바이스', '전날 -17% 뒤 반등, 적정 주가는 줄줄이 하향'), ('DE', '디어', '이익은 못 미쳤지만 매출 예상 상회·바닥론'),
                    ('META', '메타', '아마존과 AI 쇼핑 에이전트 협상 보도'), ('LRCX', '램리서치', '반도체 장비 급락, 장중 -12%대'),
                    ('ORCL', '오라클', 'CDS 사상 최고·52주 신저가'), ('MU', '마이크론', '트렌드포스 내년 D램 전망 하향')]]

# ── 오늘 밤·다음 주 일정 (한국 시간) ─────────────────────
issue['schedule'] = [
 {'kst': '11/26(목) 밤', 'type': '휴장', 'name': '추수감사절 미국 증시 휴장', 'star': 2, 'why': '오늘 밤은 미국 증시가 쉬어 11/27(금) 호는 쉽니다.', 'src': NYSE},
 {'kst': '11/28(토) 03:00', 'type': '단축', 'name': '금요일 조기 폐장(미 동부 13:00) · 블랙프라이데이', 'star': 2, 'why': f"어도비 예상 블랙프라이데이 온라인 판매 129억 달러({jo(129)}, +9.2%). 거래가 얇아 움직임이 커질 수 있습니다.", 'src': ADOBE},
 {'kst': '11/30(월) 밤', 'type': '소비', 'name': '사이버먼데이', 'star': 2, 'why': f"어도비 예상 온라인 판매 151억 달러({jo(151)}, +6.2%), 올해 가장 큰 온라인 쇼핑일.", 'src': ADOBE},
 {'kst': '12/2(수) 00:00', 'type': '지표', 'name': '11월 ISM 제조업 · 10월 JOLTS 구인', 'star': 3, 'why': '연준이 말을 아끼는 기간(11/28~12/10)이라 지표 하나하나가 더 크게 읽힙니다.', 'src': BLS},
 {'kst': '12/1(화)~12/2(수)', 'type': '의회', 'name': '황 엔비디아 CEO 하원 3개 위원회 비공개 면담', 'star': 4, 'why': '복귀 뒤 첫 의회 일정. 12/2에는 엔비디아 법무 책임자도 나옵니다.', 'src': FORBES_HU},
 {'kst': '12/2(수) 06:30', 'type': '실적', 'name': '마벨 실적 (장 후)', 'star': 3, 'why': 'AI 맞춤 칩·광통신 주문이 꺾였는지 봅니다. 같은 날 옥타·몽고DB·넷앱도 발표.', 'src': MRVL_IR},
 {'kst': '12/3(목) 07:00', 'type': '실적', 'name': '세일즈포스 · 스노우플레이크 실적 (장 후)', 'star': 3, 'why': 'AI가 소프트웨어 매출을 갉아먹는지, 키우는지 가늠합니다.', 'src': CRM_IR},
 {'kst': '12/3(목) 밤~', 'type': '의회', 'name': '황 CEO 상원 은행위 공개 청문회(수출 통제)', 'star': 4, 'why': '중국 관련 의혹과 수출 통제가 쟁점입니다.', 'src': TECHT},
 {'kst': '12/4(금) 22:30', 'type': '지표', 'name': '11월 고용보고서', 'star': 5, 'why': '예상: 일자리 +9.5만 개, 실업률 4.1%, 시간당 임금 전년 대비 2.9%(컨티뉴엄 이코노믹스).', 'src': CONT},
 {'kst': '12/10(목) 04:00', 'type': '연준', 'name': '12월 FOMC 결정 · 점도표', 'star': 5, 'why': '0.25%p 인상이 거의 확실시되며, 내년 추가 인상 횟수가 관건입니다.', 'src': BLACKOUT},
]
issue['schedule_note'] = '시각은 한국 시간이며 발표 기관·회사 일정에 따라 바뀔 수 있습니다. 예상치는 집계 기관마다 조금씩 다릅니다.'
issue['calendar'] = {
 'today': '2026-11-26',
 'days': [
  {'d': '2026-11-23', 'ev': [{'k': '급등', 't': '황 복귀 · 엔비디아 +31%'}, {'k': '인수', 't': 'CRWD→ZS 인수'}]},
  {'d': '2026-11-24', 'ev': [{'k': '급락', 't': '반도체 -7.9%'}, {'k': '실적', 't': '델·워크데이·HP', 'when': '장 후'}]},
  {'d': '2026-11-25', 'ev': [{'k': '급락', 't': '장중 반도체 -8% → -0.7%', 'hl': True}, {'k': '지표', 't': 'PCE 3.8%·GDP 4.3%', 'hl': True}, {'k': '관세', 't': '14개 경제권 관세 제안'}]},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장'}]},
  {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}, {'k': '소비', 't': '블랙프라이데이'}]},
  {'d': '2026-11-30', 'ev': [{'k': '소비', 't': '사이버먼데이'}]},
  {'d': '2026-12-01', 'ev': [{'k': '의회', 't': '황 하원 비공개 면담', 'hl': True}, {'k': '지표', 't': 'ISM 제조업·JOLTS'}, {'k': '실적', 't': '마벨', 'when': '장 후'}]},
  {'d': '2026-12-02', 'ev': [{'k': '실적', 't': '세일즈포스·스노우플레이크', 'when': '장 후'}]},
  {'d': '2026-12-03', 'ev': [{'k': '의회', 't': '황 상원 공개 청문회', 'hl': True}, {'k': '지표', 't': 'ISM 서비스업'}]},
  {'d': '2026-12-04', 'ev': [{'k': '지표', 't': '11월 고용보고서', 'hl': True}]},
 ],
 'src': [{'t': 'NYSE 휴장일', 'u': NYSE}, {'t': 'BLS 12월 일정', 'u': BLS}, {'t': 'Forbes(황 의회)', 'u': FORBES_HU}, {'t': 'TechTimes(상원 청문회)', 'u': TECHT}, {'t': 'Earnings Whispers', 'u': EW}]}
issue['earnings'] = [
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '델 테크놀로지스', 'ticker': 'DELL', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': 'HP', 'ticker': 'HPQ', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '뉴타닉스', 'ticker': 'NTNX', 'done': True},
 {'date': '11/25(수)', 'time': '장 시작 전', 'company': '디어', 'ticker': 'DE', 'done': True},
 {'date': '12/1(화)', 'time': '장 마감 후', 'company': '마벨', 'ticker': 'MRVL', 'done': False},
 {'date': '12/1(화)', 'time': '장 마감 후', 'company': '옥타', 'ticker': 'OKTA', 'done': False},
 {'date': '12/2(수)', 'time': '장 마감 후', 'company': '세일즈포스', 'ticker': 'CRM', 'done': False},
 {'date': '12/2(수)', 'time': '장 마감 후', 'company': '스노우플레이크', 'ticker': 'SNOW', 'done': False},
 {'date': '12/3(목)', 'time': '장 시작 전', 'company': '달러제너럴', 'ticker': 'DG', 'done': False},
]

# ── 차트 분석 (어제 → 최근 대비 → 앞으로) ───────────────
m = lambda s, k: f(s, k)
CH = {
 '^IXIC': (f"{f('^IXIC','chg'):+.2f}%, 장중 {lowp('^IXIC'):.1f}%에서 끌어올린 긴 아래꼬리 양봉", [
   ('어제', f"나스닥은 {m('^IXIC','open'):,.0f}에서 출발해 {m('^IXIC','low'):,.0f}까지 밀렸다가 {f('^IXIC','close'):,.0f}({f('^IXIC','chg'):+.2f}%)로 끝났습니다. 시가보다 높게 끝난 양봉이라 장중 매수세가 강했습니다."),
   ('최근 대비', f"1주 {f('^IXIC','w1'):+.1f}%, 1달 {f('^IXIC','m1'):+.1f}%, 고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%입니다. QQQ 거래량은 20일 평균의 {f('QQQ','volr'):.2f}배로 평소보다 많았습니다."),
   ('앞으로', f"20일선 {m('^IXIC','ma20'):,.0f}이 {pct(m('^IXIC','ma20'), f('^IXIC','close')):+.1f}% 위, 200일선 {m('^IXIC','ma200'):,.0f}이 {pct(m('^IXIC','ma200'), f('^IXIC','close')):+.1f}% 위입니다. RSI는 {f('^IXIC','rsi'):.0f}, 아래로는 최근 20일 저점 {m('^IXIC','sup20'):,.0f}이 기준입니다.")]),
 '^GSPC': (f"{f('^GSPC','chg'):+.2f}%, 장중 7,000선 아래 찍고 회복", [
   ('어제', f"S&P 500은 장중 {m('^GSPC','low'):,.0f}까지 내려갔다가 {f('^GSPC','close'):,.0f}({f('^GSPC','chg'):+.2f}%)로 마감했습니다. 시가 {m('^GSPC','open'):,.0f}보다 높게 끝난 양봉입니다."),
   ('최근 대비', f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%, 고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%입니다. SPY 거래량은 평균의 {f('SPY','volr'):.2f}배였습니다."),
   ('앞으로', f"200일선 {m('^GSPC','ma200'):,.0f}은 {pct(m('^GSPC','ma200'), f('^GSPC','close')):+.1f}% 위, 20일선 {m('^GSPC','ma20'):,.0f}은 {pct(m('^GSPC','ma20'), f('^GSPC','close')):+.1f}% 위입니다. 아래 기준선은 최근 20일 저점 {m('^GSPC','sup20'):,.0f}입니다.")]),
 'SOXX': (f"{f('SOXX','chg'):+.2f}%, 장중 저점에서 8% 넘게 되올라", [
   ('어제', f"반도체 ETF는 {m('SOXX','open')}달러에서 시작해 {m('SOXX','low')}달러({won(m('SOXX','low'))})까지 밀렸다가 {f('SOXX','close')}달러({f('SOXX','chg'):+.2f}%)로 끝났습니다. 저점 대비 {pct(f('SOXX','close'), m('SOXX','low')):+.1f}%입니다."),
   ('최근 대비', f"1주 {f('SOXX','w1'):+.1f}%, 1달 {f('SOXX','m1'):+.1f}%, 고점 대비 {pct(f('SOXX','close'), f('SOXX','hi52')):.1f}%입니다. 거래량은 평균의 {f('SOXX','volr'):.2f}배였습니다."),
   ('앞으로', f"20일선 {m('SOXX','ma20')}달러({won(m('SOXX','ma20'))})가 {pct(m('SOXX','ma20'), f('SOXX','close')):+.1f}% 위, 200일선 {m('SOXX','ma200')}달러는 {pct(m('SOXX','ma200'), f('SOXX','close')):+.1f}% 위입니다. 어제 장중 저점 {m('SOXX','low')}달러({won(m('SOXX','low'))})가 새 20일 저점이 됐습니다.")]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = f"세 지수 모두 **20·50·200일선 아래**지만, 어제는 셋 다 **긴 아래꼬리 양봉**이었습니다. 반도체 ETF는 장중 저점에서 **{pct(f('SOXX','close'), m('SOXX','low')):+.1f}%** 되올랐고, 나스닥은 **고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%**입니다."

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
SWTXT = ' · '.join(f"{k} {v:+}%" for k, v in sorted(sw.items(), key=lambda x: x[1]))
issue['treemap']['comment'] = {
 'h': f"100개 중 {ups}개 상승 — 장중엔 다 빠졌다가 반도체·AI만 약하게 끝난 날",
 't': (f"장중엔 거의 모두 빠졌지만 마감 때는 상위 100개 중 {ups}개가 올랐습니다. 가장 크게 내린 곳은 램리서치({gt('LRCX')}%)·오라클({gt('ORCL')}%)·마이크론({gt('MU')}%)·엔비디아({gt('NVDA')}%)·아마존({gt('AMZN')}%)으로 반도체·AI 쪽이었습니다. "
       f"반대로 아날로그디바이스({gt('ADI'):+}%)·디어({gt('DE'):+}%)·메타({gt('META'):+}%)가 크게 올랐습니다. "
       f"업종 가중 평균: {SWTXT}."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'Investing.com 마감', 'u': INV_RB}, {'t': 'StockTitan', 'u': STL}]}

# ── 롱/숏 한마디 (11/25 실제 발언) ─────────────────────
issue['street']['camps'] = {'long': [
 {'who': '모하메드 엘에리언', 'role': '알리안츠 수석 경제고문 (CNBC)', 'sil': 'glasses', 'say': '길게 보면 이건 기회가 될 거예요.', 'src': ST_ELE},
 {'who': '더그 비스', 'role': '웰스파고 투자연구소 전략가', 'sil': 'suit', 'say': 'AI는 여러 해 이어질 투자 사이클로 봐요.', 'src': KIP},
 {'who': '마이크 비노커', 'role': '프로펠러스 웰스 운용역 (BNN)', 'sil': 'suit_g', 'say': '지금 조정은 오히려 건설적인 흐름이라고 봐요.', 'src': BNNB},
 {'who': '로스 거버', 'role': '거버 가와사키 공동창업자 (X)', 'sil': 'firm', 'say': '이런 공포는 너무 지나쳐요.', 'src': ST_N100},
], 'short': [
 {'who': '웨이 리', 'role': 'BNP파리바 멀티에셋 투자 총괄', 'sil': 'woman', 'say': '지금은 저가 매수할 때가 아니에요. 거시 위험이 너무 커요.', 'src': IRISH},
 {'who': '크리스티안 뮐러글리스만', 'role': '골드만삭스 자산배분 리서치', 'sil': 'glasses', 'say': '시장이 꽤 깨지기 쉬운 상태예요.', 'src': OINV},
 {'who': '찰리 맥엘리곳', 'role': '노무라 크로스에셋 전략가', 'sil': 'hood', 'say': '그냥 분위기가 안 좋아요.', 'src': YLIVE},
 {'who': '조지프 브루수엘라스', 'role': 'RSM 수석 이코노미스트', 'sil': 'suit', 'say': '수요는 뜨겁고 물가는 빨라지고 있어요.', 'src': RSM},
]}
issue['street']['title'] = '최근 눈에 띈 증권사 의견'
issue['street']['headline'] = f'ADI·뉴타닉스 적정 주가 줄하향, 앤트로픽엔 첫 300달러({won(300)})'
issue['street']['summary'] = f'전날 급락한 아날로그디바이스에 적정 주가 하향이 이어졌고, 뉴타닉스는 BofA가 투자의견을 내렸습니다. 트렌드포스 하향 뒤 에버코어는 샌디스크 적정 주가를 낮췄고, 아레테는 앤트로픽 분석을 300달러({won(300)})로 시작했습니다.'
issue['street']['summary_src'] = ADI_TR
issue['street']['rows'] = [
 {'stock': '아날로그디바이스', 'firm': '트루이스트', 'rating': '보유 유지', 'to': f"405→323달러({won(323)})", 'date': '11/25', 'dir': -1, 'src': ADI_TR, 't': 'ADI'},
 {'stock': '아날로그디바이스', 'firm': '번스타인 SG', 'rating': '시장수익률 상회 유지', 'to': f"465→410달러({won(410)})", 'date': '11/25', 'dir': -1, 'src': ADI_BS, 't': 'ADI'},
 {'stock': '아날로그디바이스', 'firm': '모건스탠리', 'rating': '비중 확대 유지', 'to': f"458→403달러({won(403)})", 'date': '11/25', 'dir': -1, 'src': ADI_MS, 't': 'ADI'},
 {'stock': '샌디스크', 'firm': '에버코어 ISI', 'rating': '시장수익률 상회 유지', 'to': f"200→175달러({won(175)})", 'date': '11/25', 'dir': -1, 'src': PARA_SNDK},
 {'stock': '뉴타닉스', 'firm': 'BofA', 'rating': '매수 → 중립', 'to': f"62달러({won(62)})", 'date': '11/25', 'dir': -1, 'src': NTNX_P},
 {'stock': '뉴타닉스', 'firm': '파이퍼샌들러', 'rating': '비중 확대 유지', 'to': f"75→67달러({won(67)})", 'date': '11/25', 'dir': -1, 'src': NTNX_P},
 {'stock': '앤트로픽', 'firm': '아레테', 'rating': '신규 매수', 'to': f"300달러({won(300)})", 'date': '11/25', 'dir': 1, 'src': ANT_AR},
 {'stock': 'HP', 'firm': '바클레이즈', 'rating': '적정 주가 상향', 'to': f"23→24달러({won(24)})", 'date': '11/25', 'dir': 1, 'src': HPQ_BC},
]
for r in issue['street']['rows']:
    t = r.pop('t', None); d_ = TD.get(t) if t else None
    if d_:
        tv = float(r['to'].split('달러')[0].replace(',', '').split('→')[-1])
        r['c'] = d_[4]; r['rx'] = d_[5]; r['gap'] = round((tv / d_[4] - 1) * 100)

# ── 내 종목 분석 ──────────────────────────────────────
WHY6 = {'NVDA': '장중 -9% 뒤 -3.9%로 마감, AI 신용 걱정', 'MU': '트렌드포스 내년 D램 전망 하향', 'SNDK': '낸드 계약가 전망 하향·에버코어 적정 주가 하향',
        'SNXX': '샌디스크 -5.6%를 2배로', 'SOXL': '장중 반도체 -8%, 마감 -0.65%를 3배로', 'SOXX': '장중 -8% 뒤 대부분 회복', 'AMD': '장중 -10% 뒤 -1.75%로 회복',
        'TSM': '반도체 동반 약세', 'QQQ': '나스닥100 장중 약세장 문턱', 'TQQQ': '나스닥100 하락을 3배로', 'ORCL': 'CDS 사상 최고·52주 신저가',
        'META': '아마존과 AI 쇼핑 에이전트 협상 보도', 'AMZN': '빅테크 약세, 장중 -5%', 'GOOGL': 'AI 신용 걱정(알파벳 CDS 최고)',
        'ASTS': '52주 신저가에서 이사 자사주 매입 뒤 반등', 'IONQ': '고변동주 반등', 'MSTR': f'비트코인 5.9만 달러({won(59000)}) 안팎', 'DIS': '방어주로 돈 이동, 52주 신고가',
        'WDC': '저장장치 약세', 'STX': '저장장치 약세', 'AVGO': '장중 -6% 뒤 보합 마감'}
TN6 = {
 'NVDA': {'y': [(f"장중 {TD['NVDA'][3]}달러까지 밀렸다가 {TD['NVDA'][4]}달러({won(TD['NVDA'][4])}) 마감", FOOL_NV), ('엔비디아 CDS도 사상 최고(ICE)', Y_CRWV)],
          't': [('12/1 하원 비공개 면담 · 12/3 상원 공개 청문회', NAT_HU)]},
 'MU': {'y': [('트렌드포스, 내년 D램 계약가 상승 폭 전망 낮춤', Y_MU7)], 't': []},
 'SNDK': {'y': [('트렌드포스 1분기 낸드 계약가 보합~-5% 전망', PARA_SNDK), (f'에버코어 적정 주가 200→175달러({won(175)})', PARA_SNDK)], 't': []},
 'SNXX': {'y': [('기초자산 샌디스크 하락을 2배로 반영', FOOL_SNDK)], 't': []},
 'SOXL': {'y': [(f"반도체 지수 장중 {lowp('^SOX'):.1f}% → 마감 {SOX:+.2f}%", INV_RB)], 't': [('목요일 휴장 · 금요일 조기 폐장', NYSE)]},
 'ORCL': {'y': [('5년 CDS 약 360bp 사상 최고 · 52주 신저가', ORCL_F)], 't': []},
 'META': {'y': [('아마존과 Muse 차단 해제 협상 보도(포춘)', META_J)], 't': []},
 'ASTS': {'y': [(f'이사 약 103만 달러({eok(0.0103)}) 자사주 매입 공시', ASTS_ST)], 't': []},
 'QQQ': {'y': [('나스닥100 장중 고점 대비 약 -20% 근접', ST_N100)], 't': [('12/4 고용보고서 · 12/9 FOMC', BLS)]},
}
REASON = {
 'NVDA': f"장중 9% 넘게 빠졌다가 {g('NVDA'):+.2f}%로 줄였습니다. 이틀 새 월요일 상승분의 절반 넘게를 돌려줬고, 다음 주 의회 일정이 남아 있습니다.",
 'MU': '트렌드포스가 중국 클라우드 주문 감소로 내년 D램 값 상승 폭이 좁아진다고 보자 장중 11%까지 빠졌다가 4.5%로 줄였습니다.',
 'SNDK': '낸드 계약가가 내년 1분기 보합~5% 하락할 수 있다는 전망에 5.6% 내렸습니다. 한 달 새 절반 넘게 빠진 상태입니다.',
 'SOXL': '반도체 지수를 하루 3배로 따라가는 상품이라 장중 낙폭이 컸지만, 마감은 -1.8%로 줄었습니다.',
 'QQQ': '나스닥100 ETF는 장중 4% 넘게 빠졌다가 -0.65%로 끝났습니다.',
}
HL6 = {'NVDA': '장중 -9.1% → -3.9%', 'SOXL': '장중 급락 뒤 -1.8%', 'MU': '트렌드포스 하향에 -4.5%', 'SNDK': '낸드 전망 하향 -5.6%',
       'SNXX': '샌디스크 -5.6%를 2배로 -11.5%', 'AMD': '장중 -10% → -1.8%', 'ORCL': 'CDS 최고, -5.1%', 'META': '+3.4%, 아마존 협상 보도',
       'ASTS': '+10.3% 반등', 'QQQ': '장중 -4%대 → -0.65%'}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY6.get(t, '')
    n = TN6.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = (REASON[t] + ' ' if t in REASON else '') + ns['auto_ai'](q)
    q['h'] = HL6.get(t) or ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE
issue['quotes']['default'] = ['NVDA']

# ── 수리수리진타리 (c/latest.json — 이번 실행은 stock 저장소에 접근하지 못해 11/25 05:20 KST 판 그대로) ──
JL = json.load(open('data/jintari_latest.json', encoding='utf-8'))
usd = lambda s: float(s.replace('$', '').replace(',', ''))
cards = []; seen = set()
WHYJ = {'①': '11/19 S&P 500이 60일 고점보다 8.1% 낮아져 켜진 ① 급락 초입 카드입니다. 2014~2026년 23번 중 40거래일 뒤 평균 +7.1%, 74%가 올랐다는 기록입니다.',
        '⑤': '금리·금·은이 함께 급락하고 S&P 500도 내린 날(11/20) 켜진 ⑤ 카드입니다. 과거 UGL 20거래일 뒤 평균 +7.0%, 77%가 올랐다는 기록입니다.',
        '⑨': '반도체 ETF가 최근 20일 최고 종가보다 19.4% 낮아져 다시 켜진 ⑨ 카드입니다. 나스닥 선물이 싸게 거래돼 한 단계 낮춘 B+ 등급이고, 이런 때는 반등이 약했다는 기록도 함께 적혀 있습니다.'}
IMG = {'①': 1, '⑤': 5, '⑨': 9}
for c in JL['cards']:
    key = c['n'] + c['s'].split(' · ')[0]
    if key in seen or '단타' in c['s']: continue
    seen.add(key)
    s0, tg, st = usd(c['pxSig']), usd(c['tgt']), usd(c['stop'])
    now = q_[c['n']]['c'] if c['n'] in q_ else usd(c['now'])
    nlab = '어제 종가' if c['n'] in q_ else f"카드 시세({JL['time']} KST)"
    no = c['s'][0]; num = IMG.get(no, 1)
    hold = c['hold'].split(' · ')[0]
    cards.append({'g': c['g'], 't': c['n'], 'kn': c['kn'], 's': c['s'], 'ln': c.get('ln', []),
      'rows': [('신호 기준가', f"{s0}달러({won(s0)})"),
               (nlab, f"{now}달러({won(now)}) · 기준가 대비 {(now/s0-1)*100:+.1f}%"),
               ('익절 · 손절', f"{c['tp']}({tg}달러, {won(tg)}) · {c['sp']}({st}달러, {won(st)})"),
               ('보유 기간', hold)],
      'h': f"{c['s']} — 기준가 대비 {(now/s0-1)*100:+.1f}%",
      'why': WHYJ.get(no, '') + ' 과거 기록일 뿐 미래를 보장하지 않습니다.',
      'img': f'https://stock.jintar.co.kr/c/{num}.jpg', 'u': f'https://stock.jintar.co.kr/c/{num}/'})
issue['jintari'] = {'cards': cards, 'cash': [],
 'note': '발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다.',
 'u': JL_U, 'asof': f"2026-11-25 장 종료 가격 · 카드 내용은 {JL['time']} KST 판(오늘 판은 받지 못함)"}

# ── 1면 두 번째 기사 ─────────────────────────────────
issue['top2'] = {
 'kicker': '두 번째 큰 뉴스 · 물가·성장·관세',
 'title': '근원 PCE 3.3%·GDP 4.3%로 예상 웃돌아…관세 최대 35% 예고, 12월 인상 확률 약 95%',
 'img': 'img/2026-11-26-top2.jpg',
 'points': [
  {'t': '10월 PCE 물가는 전년 대비 3.8%로 예상과 같았지만(9월 3.6%), 연준이 중시하는 근원 PCE는 3.3%로 예상 3.2%를 넘어 2023년 11월 이후 가장 높았습니다. 전월 대비는 둘 다 0.3%였습니다.', 'src': Y_PCE},
  {'t': '3분기 GDP 수정치는 연율 4.3%로 속보치 3.4%와 예상 3.5%를 크게 넘었습니다. 실업수당 청구는 18.9만 건(예상 20만), 10월 신규주택판매는 70.1만 채(예상 66만)였습니다.', 'src': DUKE},
  {'t': '미 무역대표부(USTR)는 14개 경제권에 301조 관세를 제안했습니다. 중국 최대 20%, 베트남 최대 35%, 인도 최대 25%이고 한국·일본·EU·대만은 15% 상한을 유지했습니다. 반도체·자동차·철강은 빠졌고 의견 접수는 2027년 1/5까지입니다.', 'src': USTR},
  {'t': '12월 FOMC 0.25%p 인상 확률은 발표 전 97.8%에서 오후 약 95.8%로 조금 내려왔습니다(CME 선물 기준 계산). 기준금리는 지금 3.75~4.00%입니다.', 'src': FW_PM},
  {'t': '연준 베이지북은 12개 지역 중 8곳이 소폭~완만하게 성장했고 물가는 완만히 올랐다고 했습니다. 에너지·운송·보험·관세 비용 압박을 꼽았고, AI 데이터센터 투자는 강했습니다.', 'src': BEIGE},
 ],
 'risks': [
  {'t': f"뜨거운 물가에도 미 국채 10년 금리는 {f('^TNX','close'):.2f}%로 {TNX_CH:+.2f}%p 내렸습니다. 주식이 급락하자 돈이 채권으로 몰렸습니다.", 'src': LB_BOND},
  {'t': '실질 소비는 거의 제자리(예상 +0.1%)였고 베이지북도 소비가 보합이라고 해, 수요 과열만 있는 것은 아니라는 신호도 있습니다.', 'src': SA_PCE},
 ],
 'why': '연준이 12월 인상에 이어 내년 추가 인상까지 열어둘 근거가 쌓였습니다. 새 관세는 빨라야 1월부터지만 2027년 물가를 더 밀어올릴 수 있어, AI 신용 걱정과 금리 부담이 동시에 주식을 누르는 구도입니다.',
 'watch': ['12/4(금) 11월 고용보고서(예상 +9.5만 개, 실업률 4.1%)', '12/8~9 FOMC 점도표의 내년 인상 횟수', '1/10 미·중 관세 휴전 만료 · 1/5 관세 의견 마감'],
 'src': [{'t': '야후 파이낸스(PCE)', 'u': Y_PCE}, {'t': 'StockAnalysis(PCE)', 'u': SA_PCE}, {'t': '로이터(Duke.fm)', 'u': DUKE}, {'t': 'USTR 발표', 'u': USTR}, {'t': 'Investing.com(베이지북)', 'u': BEIGE}, {'t': '코리아타임스(한국 15%)', 'u': KT_TAR}],
 'react': [
  {'p': 'X', 't': '비스포크: 월 0.3%씩 끈적한 PCE라 연준이 내릴 핑계가 없다, 금리 민감주가 대가를 치른다', 'u': X_BESP},
  {'p': 'X', 't': '헤지아이: GDP 4.3%는 2분기의 거의 두 배, 매파에게 기름을 붓는 숫자', 'u': X_HEDG2},
  {'p': '스톡트윗', 't': 'SPY·다우 게시판은 비관, 나스닥이 4% 빠지는데도 QQQ는 낙관 — 기술주 저가 매수 심리', 'u': ST_DOW},
  {'p': '전문가', 't': 'FWDBONDS 럽키: 수요를 식히려면 연준이 인상 속도를 높여야 한다', 'u': DUKE},
  {'p': '전문가', 't': 'RSM 브루수엘라스: 12월 인상은 끝난 이야기, 3월도 예상하고 관세가 2027년 물가를 높인다', 'u': RSM},
  {'p': '전문가', 't': '노스라이트 자카렐리: 물가는 너무 높지만 관세발 주식 불안이 쉬어갈 여지를 줄 수도', 'u': INVN},
  {'p': '전문가', 't': '야데니: 0.25%p는 확실, 오히려 0.5%p를 해야 한다는 쪽(11/24)', 'u': ST_YARD},
  {'p': '분석', 't': '도이치방크는 12·1·3월 세 번 연속 인상, 골드만은 GDP 수정치를 연착륙 신호로 해석', 'u': LB_BANK},
  {'p': '분석', 't': '레이먼드 제임스 밀스: 새 관세는 대법원 판결 이전 구조를 되돌리는 성격', 'u': Y_TAR},
  {'p': '정부', 't': "중국 외교부: 과잉생산이라는 전제가 '거짓'이라고 반박, 보복 언급은 없음", 'u': CN_MFA},
  {'p': '시장', 't': '팔켄슈타인 마켓: 외환시장은 관세·PCE 둘 다 무시했고 채권만 강세', 'u': FALK},
 ],
}

issue['site_v'] = 11
issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 CNBC 일봉(11/25 종가) 기준이며, 장중 수치·증권사·전문가 의견은 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

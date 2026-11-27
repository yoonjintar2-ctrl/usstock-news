"""제8호(2026-11-28 토, 미국 11/27 금 블랙프라이데이 조기 폐장) — build_issue6.py 와 같은 방식. 숫자는 data/*(CNBC 일봉)와 아래 출처의 확인값만."""
import json

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1333.09"), ("D = '2026-11-19'", "D = '2026-11-28'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-27 13:00 ET 종가(조기 폐장)'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-28 06:30 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 8, 'weekday': '토'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-27(금) 뉴욕장 · 블랙프라이데이 조기 폐장'"),
       ("'ma200':1284.66", "'ma200':160.90"),  # 샌디스크 8:1 분할 반영(tickers_mini 값)
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


D = '2026-11-28'
# ── 출처 (11/27 금 조기 폐장) ─────────────────────────────
STL = 'https://www.stocktitan.net/articles/stock-market-today-live-november-27-2026'
SA_WK = 'https://stockanalysis.com/news/sp-500-caps-best-week-in-over-a-year/'
TK = 'https://www.tradingkey.com/analysis/stocks/us-stocks/262325775-nasdaq-leads-black-friday-rally-dow-posts-best-week-since-2022-tradingkey'
KUC = 'https://www.kucoin.com/news/flash/nasdaq-100-rises-2-to-session-high-on-november-27-2026'
GURU = 'https://gurufocus.com/news/9228874/nvda-leads-stocks-rally-as-dow-and-sp-500-post-best-weekly-gains-in-years'
WISE = 'https://wisevoter.com/world/us/2026/11/27/stocks-best-week-since-april-tech-rally'
STLN = 'https://www.stl.news/us-stock-market-today-november-27-2026/'
W_SNDK = 'https://247wallst.com/investing/2026/11/27/sandisk-surges-16-as-memory-stocks-extend-their-rebound-can-sndk-stock-blast-through-100-before-2026-ends/'
TIP_SNDK = 'https://www.tipranks.com/news/sandisk-stock-sndk-soars-to-lead-a-rally-in-memory-and-storage-stocks-on-black-friday'
INV_SNDK = 'https://www.investing.com/news/stock-market-news/why-is-sandisk-stock-rallying-today-93CH-5053600'
CB_SNDK = 'https://cryptobriefing.com/sandisk-stock-surges-oversold-bounce/'
TV_SNDK = 'https://www.tradingview.com/news/benzinga:0c8e25b38094b:0-sandisk-stock-jumps-double-digits-as-memory-names-roar-back/'
BG_SNDK = 'https://finance.biggo.com/news/b23e9b57-9b30-403b-9a7e-4fca339a86c3'
CP_SNDK = 'https://coinpaper.com/39526/sandisk-outperforms-nvidia-as-investors-return-to-battered-memory-chip-stocks'
CNBC_CN = 'https://www.cnbc.com/2026/11/27/china-chip-stocks-beijing-market-support.html'
MLQ_CN = 'https://mlq.ai/news/chinas-chip-stocks-post-record-176-one-day-gain-on-state-support-pledge/'
CHIP_CN = 'https://chipdispatch.com/articles/chinese-chip-stocks-post-record-17-6-gain-on-state-support-pledge'
FX_LSCC = 'https://api.finexus.net/api/news/earnings/130006/html'
FX_FUT = 'https://api.finexus.net/api/news/events/e0fbb820-e69c-4351-bab1-46f25cdc6e2b/html'
ANT_SA = 'https://stockanalysis.com/news/anthropic-jumps-11-percent-back-above-ipo-price/'
ANT_RO = 'https://rollingout.com/2026/11/27/anthropic-stock-jumps-bigger-test/'
ANT_INV = 'https://invezz.com/sg/news/2026/11/27/nasdaq-dow-rise-over-500-pts-as-anthropic-pops-11percent-to-lead-ai-rebound/'
SMH = 'https://tickeron.com/blogs/why-is-vaneck-semiconductor-etf-smh-etf-up-2-08-today-48461/'
ADOBE = 'https://news.adobe.com/news/2026/09/adobe-us-holiday-shopping-season-to-hit-record'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
BLS = 'https://www.bls.gov/schedule/2026/12_sched_list.htm'
FORBES_HU = 'https://www.forbes.com/sites/saradorn/2026/11/17/huang-agrees-to-testify-before-congress-on-dec-1/'
TECHT = 'https://www.techtimes.com/articles/331408/20261124/nvidias-jensen-huang-face-lawmakers-public-hearings-following-his-reinstatement-ceo.htm'
MRVL_IR = 'https://investor.marvell.com/news-events/press-releases/detail/1041/marvell-technology-inc-announces-conference-call-to-review-third-quarter-of-fiscal-year-2027-financial-results'
CRM_IR = 'https://investor.salesforce.com/news/news-details/2026/Salesforce-Announces-Date-of-Third-Quarter-Fiscal-2027-Earnings-Release-and-Webcast/default.aspx'
EW = 'https://www.earningswhispers.com/calweek/20261130'
CONT = 'https://continuumeconomics.com/a/13d43c4f/preview-due-december-4-us-november-employment-non-farm-payrolls-slower-but-far-from-weak'
BLACKOUT = 'https://propdatalab.com/fomc-blackout-period-calendar-fed-speeches/'
JL_U = 'https://stock.jintar.co.kr/'

q_ = {q['t']: q for q in issue['quotes']['list']}
g = lambda t: f(t, 'chg') if t in summ else (TD[t][5] if t in TD else q_[t]['ch'])
cl = lambda t: f(t, 'close') if t in summ else (TD[t][4] if t in TD else q_[t]['c'])
SOX = f('^SOX', 'chg')
pct = lambda a, b: (a / b - 1) * 100

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스 · 메모리 반등',
 'title': f"샌디스크 {g('SNDK'):+.1f}%, 마이크론 {g('MU'):+.1f}%…블랙프라이데이 짧은 장, 반도체 지수 {SOX:+.1f}%",
 'img': f'img/{D}-top.jpg',
 'points': [
  {'t': f"미국 증시는 미 동부 13:00에 일찍 닫은 짧은 장에서 크게 올랐습니다. 나스닥 {f('^IXIC','chg'):+.2f}%, S&P 500 {f('^GSPC','chg'):+.2f}%, 다우 {f('^DJI','chg'):+.2f}%였습니다.", 'src': STL},
  {'t': f"필라델피아 반도체 지수는 {f('^SOX','close'):,.0f}로 {SOX:+.2f}% 올라 이날 가장 강한 업종이었습니다.", 'src': Y('%5ESOX')},
  {'t': f"샌디스크는 {cl('SNDK')}달러({won(cl('SNDK'))})로 {g('SNDK'):+.2f}% 올라 메모리·저장장치 반등을 이끌었다고 보도됐습니다. 씨게이트 {g('STX'):+.1f}%, 웨스턴디지털 {g('WDC'):+.1f}%, 마이크론 {g('MU'):+.1f}%도 함께 올랐습니다.", 'src': TIP_SNDK},
  {'t': "샌디스크는 고점에서 75% 가까이 빠진 뒤라 '지나치게 팔린 데서 나온 반등'이라는 해석이 많았습니다.", 'src': CB_SNDK},
  {'t': "추수감사절 휴장 중 중국 반도체주가 정부 지원 신호로 사상 최대 폭 올랐고, 이 흐름이 세계 반도체주 반등으로 번졌다고 전해졌습니다.", 'src': FX_LSCC},
 ],
 'risks': [
  {'t': f"샌디스크는 반등에도 52주 고점보다 {abs(pct(f('SNDK','close'), f('SNDK','hi52'))):.0f}% 낮고, 200일선({f('SNDK','ma200'):.0f}달러, {won(f('SNDK','ma200'))})보다 한참 아래입니다. 이틀 전엔 트렌드포스가 내년 낸드 값 전망을 낮췄습니다.", 'src': W_SNDK},
  {'t': f"조기 폐장이라 거래가 얇았습니다. 나스닥 종합 거래량은 20일 평균의 약 {f('^IXIC','volr'):.2f}배에 그쳐, 다음 주 정규 거래에서 다시 확인이 필요합니다.", 'src': Y('%5EIXIC')},
 ],
 'why': '한 달 새 절반 넘게 빠졌던 메모리주가 하루 만에 크게 튄 날입니다. 낸드 값 걱정은 그대로라 바닥을 확인했다고 보긴 이르지만, 팔 사람은 다 팔았다는 신호인지 다음 주 거래량과 함께 봐야 합니다.',
 'watch': [f"샌디스크가 100달러({won(100)}) 위로 다시 올라서는지", '12/1(화) 마벨 실적 · 12/1~3 황 엔비디아 CEO 의회 일정', f"반도체 ETF(SOXX)가 20일선 {f('SOXX','ma20'):.0f}달러({won(f('SOXX','ma20'))})를 되찾는지"],
 'src': [{'t': 'StockTitan 마감', 'u': STL}, {'t': 'TipRanks(샌디스크)', 'u': TIP_SNDK}, {'t': '24/7 Wall St.(샌디스크)', 'u': W_SNDK}, {'t': 'CryptoBriefing', 'u': CB_SNDK}, {'t': 'Investing.com', 'u': INV_SNDK}],
 'react': [
  {'p': '분석', 't': '샌디스크가 메모리·저장장치 랠리의 선봉이었다는 평가', 'u': TIP_SNDK},
  {'p': '분석', 't': f'연말 전에 100달러({won(100)})를 다시 뚫을 수 있을지 묻는 시각', 'u': W_SNDK},
  {'p': '분석', 't': '75% 급락 뒤 나온 과매도 반등이라는 해석', 'u': CB_SNDK},
  {'p': '시장', 't': "메모리주가 '돌아왔다'며 두 자릿수 급등을 반기는 분위기", 'u': TV_SNDK},
  {'p': '시장', 't': '추수감사절 직전 매도를 되돌린 반등이라는 평', 'u': BG_SNDK},
  {'p': '분석', 't': '샌디스크가 엔비디아보다 더 올라, 두들겨 맞은 메모리주로 돈이 돌아왔다는 해석', 'u': CP_SNDK},
  {'p': '시장', 't': '왜 오르는지 묻는 투자자가 많아 원인 정리 기사가 따로 나옴', 'u': INV_SNDK},
  {'p': '분석', 't': '반도체 ETF도 함께 올라 업종 전체 반등이라는 시각', 'u': SMH},
  {'p': '시장', 't': '선물부터 AI·기술주가 반등을 이끌었다는 장 전 분위기', 'u': FX_FUT},
 ],
}
issue['top2'] = {
 'kicker': '두 번째 큰 뉴스 · 주간 성적표',
 'title': f"S&P 500 1년 반 만에 가장 좋은 한 주…앤트로픽 약 +11%로 공모가 위로",
 'img': f'img/{D}-top2.jpg',
 'points': [
  {'t': 'S&P 500은 이번 주 2025년 4월 이후 가장 좋은 한 주를 보냈고, 다우도 2022년 10월 이후 가장 큰 주간 상승이었다고 보도됐습니다.', 'src': SA_WK},
  {'t': f"앤트로픽은 약 11% 올라 91.88달러({won(91.88)})로 공모가 83달러({won(83)}) 위로 돌아왔고, AI주 반등의 앞줄에 섰습니다.", 'src': ANT_SA},
  {'t': f"다우는 짧은 장에서 약 590포인트 올라 {f('^DJI','close'):,.0f}에 끝났습니다.", 'src': TK},
  {'t': f"공포 지표 VIX는 {f('^VIX','close'):.2f}로 {f('^VIX','chg'):+.1f}% 내려왔습니다.", 'src': Y('%5EVIX')},
 ],
 'risks': [
  {'t': '나스닥은 이번 달 7개월 연속 상승이 끊길 처지라는 분석이 나와, 한 주 반등만으로 흐름이 바뀌었다고 보긴 이릅니다.', 'src': 'https://finviz.com/news/241089/nasdaq-set-to-snap-monthly-win-streak-amid-tech-volatility'},
  {'t': '앤트로픽은 앞으로 더 큰 시험(첫 실적·보호예수 해제 등)이 남아 있다는 지적이 있습니다.', 'src': ANT_RO},
 ],
 'why': '지난주 AI 신용 공포로 크게 흔들린 뒤, 한 주 만에 상당 부분을 되찾았습니다. 다음 주 고용보고서와 12월 FOMC를 앞두고 이 반등이 버티는지가 연말 분위기를 가를 수 있습니다.',
 'watch': ['12/4(금) 11월 고용보고서', '12/10(목) FOMC 결정 · 점도표', f'앤트로픽이 공모가 83달러({won(83)}) 위를 지키는지'],
 'src': [{'t': 'StockAnalysis(주간)', 'u': SA_WK}, {'t': 'StockAnalysis(앤트로픽)', 'u': ANT_SA}, {'t': 'TradingKey', 'u': TK}, {'t': 'GuruFocus', 'u': GURU}],
 'react': [
  {'p': '분석', 't': '반도체가 이끈 금요일 랠리로 S&P 500이 1년여 만의 최고 주간을 마쳤다는 평', 'u': SA_WK},
  {'p': '분석', 't': '엔비디아가 랠리를 이끌며 다우·S&P가 몇 년 만의 주간 상승을 냈다는 시각', 'u': GURU},
  {'p': '시장', 't': '기술주 랠리로 4월 이후 최고의 한 주라는 분위기', 'u': WISE},
  {'p': '시장', 't': '앤트로픽이 11% 뛰며 AI 반등을 이끌었다는 반응', 'u': ANT_INV},
  {'p': '분석', 't': '앤트로픽 반등은 반갑지만 더 큰 시험이 남았다는 신중론', 'u': ANT_RO},
  {'p': '시장', 't': '나스닥100이 장중 2% 넘게 올라 고점에서 거래됐다는 속보', 'u': KUC},
  {'p': '분석', 't': '블랙프라이데이에 세 지수 모두 강하게 올랐다는 정리', 'u': STLN},
  {'p': '분석', 't': '나스닥은 그래도 월간 연승이 끊길 수 있다는 경계', 'u': 'https://finviz.com/news/241089/nasdaq-set-to-snap-monthly-win-streak-amid-tech-volatility'},
 ],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': f"블랙프라이데이라 미 동부 13:00(한국 03:00)에 일찍 닫았습니다. 반도체 지수가 {SOX:+.2f}%로 가장 강했고 러셀 2000도 {f('^RUT','chg'):+.2f}% 올랐습니다.",
 'src': STL,
}
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'prev'), 2)
issue['indicators'] = [
 {'name': 'VIX', 'v': f('^VIX', 'close'), 'd': 2, 'chg': f('^VIX', 'chg'), 'src': Y('%5EVIX')},
 {'name': '미 국채 10년', 'v': f('^TNX', 'close'), 'd': 2, 'suf': '%', 'chg': TNX_CH, 'chgsuf': '%p', 'src': Y('%5ETNX')},
 {'name': '달러인덱스', 'v': f('DX-Y.NYB', 'close'), 'd': 2, 'chg': f('DX-Y.NYB', 'chg'), 'src': Y('DX-Y.NYB')},
 {'name': 'WTI 유가', 'v': f('CL=F', 'close'), 'd': 2, 'chg': f('CL=F', 'chg'), 'src': Y('CL%3DF')},
 {'name': '금', 'v': f('GC=F', 'close'), 'd': 1, 'chg': f('GC=F', 'chg'), 'src': Y('GC%3DF')},
 {'name': '원/달러', 'v': FX, 'd': 2, 'chg': f('KRW=X', 'chg'), 'src': Y('KRW%3DX')},
]
issue['gauges'] = [x for x in issue.get('gauges', []) if x['name'] == 'VIX 변동성']
for x in issue['gauges']:
    x['note'] = f"하루 {f('^VIX','chg'):+.1f}% · 1주 {f('^VIX','w1'):+.1f}%"
issue['macro'] = []

# ── 간밤 뉴스 (1면 두 건 제외) ────────────────────────
issue['news'] = [
 {'tag': '중국', 'img': f'img/{D}-china.jpg', 'title': '중국 반도체주 하루 +17.6% 사상 최대…베이징 증시 지원 신호',
  'line': '미국이 쉬던 목요일, 중국 정부가 증시를 넓게 받치겠다는 신호를 보내자 중국 반도체주가 하루 기준 사상 가장 크게 올랐다고 보도됐습니다. 미국 반도체주 반등의 불씨로 꼽혔습니다.',
  'src': [{'t': 'CNBC', 'u': CNBC_CN}, {'t': 'MLQ', 'u': MLQ_CN}, {'t': 'Chip Dispatch', 'u': CHIP_CN}]},
 {'tag': '대형주', 'img': f'img/{D}-big.jpg', 'title': f"테슬라 {g('TSLA'):+.1f}%, 팔란티어 {g('PLTR'):+.1f}%, 델 {g('DELL'):+.1f}%",
  'line': f"AI·기술주가 고르게 올랐습니다. 아마존 {g('AMZN'):+.1f}%, 메타 {g('META'):+.1f}%, 브로드컴 {g('AVGO'):+.1f}%, 마벨 {g('MRVL'):+.1f}%였고, 엔비디아는 {g('NVDA'):+.2f}%로 상대적으로 덜 올랐습니다.",
  'src': [{'t': 'StockTitan 마감', 'u': STL}, {'t': '야후 파이낸스', 'u': Y('TSLA')}]},
 {'tag': '자산', 'img': f'img/{D}-gold.jpg', 'title': f"금 {g('GC=F'):+.1f}% 반등, {f('GC=F','close'):,.0f}달러({won(f('GC=F','close'))})",
  'line': f"금 선물은 {f('GC=F','close'):,.1f}달러({won(f('GC=F','close'))})로 올랐습니다(선물 마지막 체결가). 10년 국채 금리는 {f('^TNX','close'):.2f}%로 {TNX_CH:+.2f}%p, 달러인덱스는 {f('DX-Y.NYB','chg'):+.2f}%였습니다.",
  'src': [{'t': '야후 파이낸스(금)', 'u': Y('GC%3DF')}, {'t': '야후 파이낸스(10년물)', 'u': Y('%5ETNX')}]},
 {'tag': '하락', 'img': f'img/{D}-health.jpg', 'title': f"버텍스 {g('VRTX'):+.1f}%, 상위 100개 중 가장 크게 내려",
  'line': '대부분 오른 날 버텍스 파마슈티컬스가 크게 내렸습니다. 크리네틱스 인수와 자금 조달 계획을 시장이 소화하는 중이라는 보도가 있었지만, 이날 하락의 직접적인 이유는 확인 중입니다.',
  'src': [{'t': 'Quiver Quant', 'u': 'https://www.quiverquant.com/news/Vertex+shares+fall+as+investors+digest+Crinetics+acquisition+and+related+financing+plans'}, {'t': '야후 파이낸스', 'u': Y('VRTX')}]},
]
for n in issue['news']:
    n['body'] = n['line']

def mv(t, nm, why):
    return {'ticker': t, 'name': nm, 'close': N(cl(t), Y(t), CLOSE), 'chg_pct': N(g(t), Y(t), CLOSE), 'won': won(cl(t)), 'why': why}
issue['movers'] = [mv('STX', '씨게이트', '메모리·저장장치 동반 반등'), mv('MU', '마이크론', '메모리 반등'), mv('MRVL', '마벨', '반도체 반등 · 12/1 실적'),
                   mv('DELL', '델', 'AI 서버주 반등'), mv('TSLA', '테슬라', '기술주 동반 상승'), mv('VRTX', '버텍스', '상위 100개 중 최대 하락')]

# ── 일정 ────────────────────────────────────────────
issue['schedule'] = [
 {'kst': '11/30(월) 밤', 'type': '소비', 'name': '사이버먼데이', 'star': 2, 'why': f"어도비는 올해 연말 온라인 쇼핑이 2,751억 달러({jo(2751)}, +6.7%)로 사상 최대가 될 것으로 내다봤습니다.", 'src': ADOBE},
 {'kst': '12/2(수) 00:00', 'type': '지표', 'name': '11월 ISM 제조업 · 10월 JOLTS 구인', 'star': 3, 'why': '연준이 말을 아끼는 기간이라 지표 하나하나가 더 크게 읽힙니다.', 'src': BLS},
 {'kst': '12/1(화)~12/2(수)', 'type': '의회', 'name': '황 엔비디아 CEO 하원 비공개 면담', 'star': 4, 'why': '복귀 뒤 첫 의회 일정입니다.', 'src': FORBES_HU},
 {'kst': '12/2(수) 06:30', 'type': '실적', 'name': '마벨 실적 (장 후)', 'star': 3, 'why': 'AI 맞춤 칩·광통신 주문을 봅니다.', 'src': MRVL_IR},
 {'kst': '12/3(목) 07:00', 'type': '실적', 'name': '세일즈포스 · 스노우플레이크 실적 (장 후)', 'star': 3, 'why': 'AI가 소프트웨어 매출을 키우는지 가늠합니다.', 'src': CRM_IR},
 {'kst': '12/3(목) 밤~', 'type': '의회', 'name': '황 CEO 상원 은행위 공개 청문회', 'star': 4, 'why': '수출 통제가 쟁점입니다.', 'src': TECHT},
 {'kst': '12/4(금) 22:30', 'type': '지표', 'name': '11월 고용보고서', 'star': 5, 'why': '예상: 일자리 +9.5만 개, 실업률 4.1%(컨티뉴엄 이코노믹스).', 'src': CONT},
 {'kst': '12/10(목) 04:00', 'type': '연준', 'name': '12월 FOMC 결정 · 점도표', 'star': 5, 'why': '0.25%p 인상 여부와 내년 경로가 관건입니다.', 'src': BLACKOUT},
]
issue['schedule_note'] = '시각은 한국 시간이며 발표 기관·회사 일정에 따라 바뀔 수 있습니다.'
issue['calendar'] = {
 'today': D,
 'days': [
  {'d': '2026-11-24', 'ev': [{'k': '급락', 't': '반도체 -7.9%'}]},
  {'d': '2026-11-25', 'ev': [{'k': '급락', 't': '장중 반도체 -8% → -0.7%'}, {'k': '지표', 't': 'PCE 3.8%·GDP 4.3%'}]},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장'}]},
  {'d': '2026-11-27', 'ev': [{'k': '급등', 't': f"반도체 {SOX:+.1f}% · 샌디스크 {g('SNDK'):+.0f}%", 'hl': True}, {'k': '단축', 't': '조기 폐장'}]},
  {'d': '2026-11-30', 'ev': [{'k': '소비', 't': '사이버먼데이'}]},
  {'d': '2026-12-01', 'ev': [{'k': '의회', 't': '황 하원 비공개 면담', 'hl': True}, {'k': '지표', 't': 'ISM 제조업·JOLTS'}, {'k': '실적', 't': '마벨', 'when': '장 후'}]},
  {'d': '2026-12-02', 'ev': [{'k': '실적', 't': '세일즈포스·스노우플레이크', 'when': '장 후'}]},
  {'d': '2026-12-03', 'ev': [{'k': '의회', 't': '황 상원 공개 청문회', 'hl': True}]},
  {'d': '2026-12-04', 'ev': [{'k': '지표', 't': '11월 고용보고서', 'hl': True}]},
  {'d': '2026-12-09', 'ev': [{'k': '연준', 't': 'FOMC 결정', 'hl': True}]},
 ],
 'src': [{'t': 'NYSE 휴장일', 'u': NYSE}, {'t': 'BLS 12월 일정', 'u': BLS}, {'t': 'Forbes(황 의회)', 'u': FORBES_HU}, {'t': 'Earnings Whispers', 'u': EW}]}
issue['earnings'] = [
 {'date': '12/1(화)', 'time': '장 마감 후', 'company': '마벨', 'ticker': 'MRVL', 'done': False},
 {'date': '12/1(화)', 'time': '장 마감 후', 'company': '옥타', 'ticker': 'OKTA', 'done': False},
 {'date': '12/2(수)', 'time': '장 마감 후', 'company': '세일즈포스', 'ticker': 'CRM', 'done': False},
 {'date': '12/2(수)', 'time': '장 마감 후', 'company': '스노우플레이크', 'ticker': 'SNOW', 'done': False},
 {'date': '12/3(목)', 'time': '장 시작 전', 'company': '달러제너럴', 'ticker': 'DG', 'done': False},
]

# ── 차트 분석 ────────────────────────────────────────
m = lambda s, k: f(s, k)
def ch3(s, nm, unit=''):
    W = (lambda v: f'({won(v)})') if unit else (lambda v: '')
    return [
     ('어제', f"{nm}는 {m(s,'open'):,.2f}{unit}{W(m(s,'open'))}에서 시작해 {f(s,'close'):,.2f}{unit}{W(f(s,'close'))}({f(s,'chg'):+.2f}%)로 끝났습니다. 짧은 장이었고 거래량은 평소보다 적었습니다."),
     ('최근 대비', f"1주 {f(s,'w1'):+.1f}%, 1달 {f(s,'m1'):+.1f}%, 52주 고점 대비 {pct(f(s,'close'), f(s,'hi52')):.1f}%입니다."),
     ('앞으로', f"20일선 {m(s,'ma20'):,.2f}{unit}{W(m(s,'ma20'))}{'은' if not unit else '는'} {pct(m(s,'ma20'), f(s,'close')):+.1f}% 위, 200일선 {m(s,'ma200'):,.2f}{unit}{W(m(s,'ma200'))}{'은' if not unit else '는'} {pct(m(s,'ma200'), f(s,'close')):+.1f}% 위입니다. RSI는 {f(s,'rsi'):.0f}입니다.")]
CH = {'^IXIC': (f"{f('^IXIC','chg'):+.2f}%, 짧은 장 강한 양봉", ch3('^IXIC', '나스닥')),
      '^GSPC': (f"{f('^GSPC','chg'):+.2f}%, 200일선 위로 복귀 시도", ch3('^GSPC', 'S&P 500')),
      'SOXX': (f"{f('SOXX','chg'):+.2f}%, 반도체 가장 강해", ch3('SOXX', '반도체 ETF', '달러'))}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = f"세 지수 모두 강하게 올랐지만 아직 **20·50일선 아래**입니다. S&P 500은 200일선({m('^GSPC','ma200'):,.0f})을 **{pct(f('^GSPC','close'), m('^GSPC','ma200')):+.1f}%** 웃돌았고, 반도체 ETF는 **고점 대비 {pct(f('SOXX','close'), f('SOXX','hi52')):.1f}%**입니다."

# ── 트리맵 ──────────────────────────────────────────
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
 'h': f"100개 중 {ups}개 상승 — 반도체·저장장치가 앞장선 날",
 't': (f"상위 100개 중 {ups}개가 올랐습니다. 가장 크게 오른 곳은 씨게이트({gt('STX'):+}%)·마이크론({gt('MU'):+}%)·마벨({gt('MRVL'):+}%)·델({gt('DELL'):+}%)로 반도체·저장장치·AI 서버였습니다. "
       f"반대로 버텍스({gt('VRTX'):+}%)가 가장 크게 내렸습니다. 업종 가중 평균: {SWTXT}."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'StockTitan', 'u': STL}]}

# 롱숏·증권사 의견: 11/27 짧은 장에서 확인된 발언·의견을 찾지 못해 칸을 숨긴다(지어내지 않음)
issue.pop('street', None)

# ── 내 종목 ─────────────────────────────────────────
WHY8 = {'NVDA': '반도체 반등 속 상대적으로 덜 오름', 'MU': '메모리 반등', 'SNDK': '메모리·저장장치 반등 선봉', 'SNXX': '샌디스크 상승을 2배로',
        'SOXL': '반도체 지수 상승을 3배로', 'SOXX': '반도체 가장 강한 업종', 'AMD': '반도체 반등', 'QQQ': '나스닥100 반등', 'TQQQ': '나스닥100 상승을 3배로',
        'TSLA': '기술주 동반 상승', 'STX': '저장장치 반등', 'WDC': '저장장치 반등', 'INTC': '반도체 반등', 'ARM': '반도체 반등'}
REASON = {'SNDK': f"고점에서 크게 빠진 뒤 {g('SNDK'):+.1f}% 튀었습니다. 지나치게 팔린 데서 나온 반등이라는 해석이 많았습니다.",
          'NVDA': f"반도체 지수가 {SOX:+.1f}% 오른 날 {g('NVDA'):+.2f}%에 그쳤습니다. 다음 주 의회 일정이 남아 있습니다."}
TN8 = {'SNDK': {'y': [('메모리·저장장치 랠리 선봉(TipRanks)', TIP_SNDK), ('75% 급락 뒤 과매도 반등', CB_SNDK)], 't': []},
       'NVDA': {'y': [], 't': [('12/1 하원 비공개 면담 · 12/3 상원 공개 청문회', FORBES_HU)]}}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY8.get(t, '')
    n = TN8.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = (REASON[t] + ' ' if t in REASON else '') + ns['auto_ai'](q)
    q['h'] = ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE
issue['quotes']['default'] = ['SNDK']

# ── 진타리 ──────────────────────────────────────────
JL = json.load(open('data/jintari_latest.json', encoding='utf-8'))
usd = lambda s: float(s.replace('$', '').replace(',', ''))
cards = []
for c in JL['cards']:
    if '단타' in c['s'] or c.get('quietCard'): continue
    s0, tg, st = usd(c['pxSig']), usd(c['tgt']), usd(c['stop'])
    now = q_[c['n']]['c'] if c['n'] in q_ else usd(c['now'])
    nlab = '어제 종가' if c['n'] in q_ else f"카드 시세({JL['time']} KST)"
    no = c['s'][0]; num = {'①': 1, '⑤': 5, '⑨': 9}.get(no, 1)
    cards.append({'g': c['g'], 't': c['n'], 'kn': c['kn'], 's': c['s'], 'ln': c.get('ln', []),
      'rows': [('신호 기준가', f"{s0}달러({won(s0)})"), (nlab, f"{now}달러({won(now)}) · 기준가 대비 {(now/s0-1)*100:+.1f}%"),
               ('익절 · 손절', f"{c['tp']}({tg}달러, {won(tg)}) · {c['sp']}({st}달러, {won(st)})"), ('보유 기간', c['hold'].split(' · ')[0])],
      'h': f"{c['s']} — 기준가 대비 {(now/s0-1)*100:+.1f}%",
      'why': '11/25 반도체 ETF가 최근 20일 최고 종가보다 26.4% 낮아져 켜진 ⑨ 카드입니다. 나스닥 선물이 싸게 거래돼 한 단계 낮춘 B+ 등급입니다. 과거 기록일 뿐 미래를 보장하지 않습니다.',
      'img': f'https://stock.jintar.co.kr/c/{num}.jpg', 'u': f'https://stock.jintar.co.kr/c/{num}/'})
issue['jintari'] = {'cards': cards, 'cash': [], 'note': '발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다.',
                    'u': JL_U, 'asof': f"2026-11-27 장 종료 가격 · 카드 내용은 {JL['time']} KST 판"}

issue['site_v'] = 11
issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 CNBC 일봉(11/27 조기 폐장 종가) 기준이며, 그 밖의 내용은 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

"""창간호(2026-11-19) 초안 조립 — 숫자는 data/summary.txt(야후 일봉)·data/charts.json·웹 검색 확인값만 쓴다."""
import json

FX = 1330.28
D = '2026-11-19'
Y = lambda s: f'https://finance.yahoo.com/quote/{s}/history'
CLOSE = '2026-11-18 16:00 ET 종가'
LIVE = '2026-11-19 11:20 KST 시세'

summ = {}
head, *rows = open('data/summary.txt', encoding='utf-8').read().strip().split('\n')
keys = head.split('|')[1].split(',')
for r in rows:
    s, v = r.split('|'); summ[s] = dict(zip(keys, v.split(',')))
f = lambda s, k: float(summ[s][k])
N = lambda v, src, asof: {'v': v, 'src': src, 'asof': asof}


def row(name, sym, asof=CLOSE, unit=''):
    return {'name': name, 'unit': unit, 'close': N(f(sym, 'close'), Y(sym.replace('^', '%5E')), asof),
            'chg_pct': N(f(sym, 'chg'), Y(sym.replace('^', '%5E')), asof)}


AP = 'https://wtop.com/national/2026/11/how-major-us-stock-indexes-fared-wednesday-11-18-2026'
CNBC_IPO = 'https://www.cnbc.com/2026/11/18/anthropic-ipo-ai-offering-price.html'
CNBC_LIVE = 'https://cnbc.com/2026/11/18/stock-market-today-live-updates.html'
NV_PR = 'https://www.globenewswire.com/news-release/2026/11/17/3405200/0/en/nvidia-announces-financial-results-for-third-quarter-fiscal-2027.html'
NV_TK = 'https://www.tradingkey.com/analysis/stocks/us-stocks/262309793-nvidia-earnings-report-q3-rubin-ramp-data-center-growth-revenue-guidance-gross-margin-tradingkey'
FED_MIN = 'https://www.investmentnews.com/equities/the-fed-came-close-to-an-october-rate-hike-fomc-minutes-show/269079'
FED_INV = 'https://ca.investing.com/news/economy-news/couple-of-policymakers-see-more-than-a-25-bp-rate-hike-in-december--fed-minutes-4967731'
FED_YH = 'https://finance.yahoo.com/economy/policy/articles/fed-officials-expect-further-interest-195844967.html'
SED = 'https://en.sedaily.com/society/2026/11/19/us-dec-rate-hike-odds-at-957-percent-as-fed-resists-bigger'
BABY = 'https://babypips.com/news/daily-financial-forex-market-recap-2026-11-18'
CAPP = 'https://cappnotes.substack.com/p/closing-look-wednesday-november-18'
MEM = 'https://247wallst.com/investing/2026/11/17/sandisk-and-micron-fall-4-as-gf-securities-cuts-nand-price-forecast-and-warns-of-a-glut-sk-hynix-dips/'
GOLD = 'https://fxstreet.com/news/gold-falls-to-14-month-low-below-3-750-on-hawkish-fed-rhetoric-202611182327'
TV_ANT = 'https://www.tradingview.com/symbols/NASDAQ-ANT/'
FG = 'https://edition.cnn.com/markets/fear-and-greed'
PT_TR = 'https://www.tipranks.com/news/nvidia-stock-price-forecast-analysts-cut-targets-despite-strong-q3'
PT_BZ = 'https://www.benzinga.com/quote/NVDA/price-targets'
PT_MS = 'https://www.dailypolitical.com/2026/11/18/nvidia-nasdaqnvda-stock-gets-price-target-reduction-from-morgan-stanley.html'
PT_JPM = 'https://www.aol.com/articles/strong-nvidia-earnings-being-clouded-161240000.html'
PT_BOFA = 'https://247wallst.com/cards/nvda-xpost-01m7qfdn0mz79tzg8n52bd1d1g'
PT_MED = 'https://fourweekmba.com/ai-nvidias-q3-drew-5-target-cuts-2-raises-median-is-222-50/'
PT_BERN = 'https://www.kiplinger.com/news/live/nvidia-earnings-live-updates-and-commentary-november-2026'
WK = 'https://www.heygotrade.com/en/news/weekly-economic-outlook-2026-11-16/'
WMT = 'https://admiralmarkets.com/analytics/traders-blog/walmart-earnings-preview-q3-fiscal-2027'
FV = 'https://finviz.com/calendar/economic'
SCHWAB = 'https://www.schwab.com/learn/story/stock-market-update-open'
TVIX = 'https://www.cboe.com/tradable_products/vix/'

charts = json.load(open('data/charts.json', encoding='utf-8'))

issue = {
 'date': D, 'no': 1, 'weekday': '목',
 'session': '2026-11-18(수) 뉴욕장',
 'publisher': '샌디스크 올인',
 'lead': '엔비디아 호실적에도 S&P 500은 5일 연속 하락. 연준 의사록이 12월 금리 인상에 무게를 실었고, 오늘 밤 앤트로픽이 사상 최대 공모로 나스닥에 상장합니다.',
 'fx': {'usdkrw': N(FX, Y('KRW%3DX'), LIVE)},

 # ── 1면: 지금 가장 중요한 뉴스 ───────────────────────────
 'top': {
  'kicker': '지금 가장 중요한 뉴스',
  'title': '역대 최대 IPO 앤트로픽, 오늘 밤 나스닥 첫 거래',
  'img': 'img/2026-11-19-ipo.jpg',
  'short': {'id': 'N87Ld5PFYkM', 'title': '앤트로픽 상장하면 사야 돼요? 공모가 $70~78, 가능성 vs 위험'},
  'figures': [
   {'n': '83달러', 'won': '약 11만 원', 't': '최종 공모가 · 희망 범위 70~78달러(약 9만 3천~10만 4천 원) 위', 'src': CNBC_IPO},
   {'n': '813억 달러', 'won': '약 108조 원', 't': '조달 금액 · 역대 최대 IPO', 'src': CNBC_IPO},
   {'n': '약 7배', 'won': '', 't': '공모 물량 대비 주문', 'src': TV_ANT},
   {'n': '+1%', 'won': '', 't': '전날 밤 나스닥100 선물', 'src': CNBC_LIVE},
  ],
  'why': 'AI 대장주들이 흔들리는 가운데 나오는 역대 최대 공모입니다. 첫날 성적이 AI 투자 심리의 온도계가 됩니다.',
  'watch': [
   '첫 거래 가격이 공모가 83달러(약 11만 원)를 지키는지',
   '전날 밤 나스닥100 선물 +1%가 정규장까지 이어지는지',
   '엔비디아·반도체로 매수세가 번지는지, 거꾸로 돈이 빠져나가는지',
  ],
  'src': [{'t': 'CNBC', 'u': CNBC_IPO}, {'t': 'TradingView', 'u': TV_ANT}],
 },

 # ── 밤사이 미장 ───────────────────────────────────────────
 'market': {
  'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'),
           {'name': '러셀 2000', 'unit': '', 'close': N(2714.31, AP, CLOSE), 'chg_pct': N(0.46, AP, CLOSE)}],
  'note': 'S&P 500은 6월 이후 가장 긴 5일 연속 하락. 다우는 건강보험주 급락에 1.1% 내렸고, 나스닥은 0.4% 올라 하락을 멈췄습니다.',
  'src': AP,
 },

 # ── 참고 지표 ─────────────────────────────────────────────
 'gauges': [
  {'name': '공포·탐욕 지수', 'v': N(24.6, FG, '2026-11-18 장 마감'), 'scale': [0, 100], 'label': '극단적 공포', 'ends': ['0 극단적 공포', '100 극단적 탐욕'],
   'note': '1주 전 35.9 · 1달 전 18.2 (CNN, 25 아래는 극단적 공포)'},
  {'name': '12월 금리 인상 확률', 'v': N(95.7, SED, '2026-11-19 CME FedWatch'), 'scale': [0, 100], 'label': '0.25%p 인상', 'ends': ['0%', '100%'],
   'note': '0.5%p 인상 4.3% · 현재 기준금리 3.75~4.00%'},
  {'name': 'VIX 변동성', 'v': N(f('^VIX', 'close'), Y('%5EVIX'), CLOSE), 'chg': N(f('^VIX', 'chg'), Y('%5EVIX'), CLOSE), 'scale': [10, 40], 'label': '20 위 = 불안', 'ends': ['10 안정', '40 공포'],
   'note': f"50일 평균 {float(summ['^VIX']['ma50']):.1f}보다 높음"},
  {'name': '풋/콜 비율', 'v': N(0.88, FG, '2026-11-18 5일 평균'), 'scale': [0.5, 1.2], 'label': '풋 쪽으로 기움', 'ends': ['◀ 콜 우세 (오른다에 베팅)', '풋 우세 (내린다에 대비) ▶'], 'mid': '1.0 = 풋·콜 같음',
   'note': '풋(하락에 거는 옵션) ÷ 콜(상승에 거는 옵션) 거래량'},
 ],
 'macro': [
  {'name': '미 국채 10년', 'close': N(f('^TNX', 'close'), Y('%5ETNX'), CLOSE), 'chg_pct': N(round(f('^TNX','close')-f('^TNX','close')/(1+f('^TNX','chg')/100),2), Y('%5ETNX'), CLOSE), 'unit': '%', 'note': '유가 하락에 소폭 내림'},
  {'name': '달러인덱스', 'close': N(f('DX-Y.NYB', 'close'), Y('DX-Y.NYB'), LIVE), 'chg_pct': N(f('DX-Y.NYB', 'chg'), Y('DX-Y.NYB'), LIVE), 'unit': '', 'note': '52주 최고(103.91) 근처'},
  {'name': 'WTI 유가', 'close': N(f('CL=F', 'close'), Y('CL%3DF'), LIVE), 'chg_pct': N(f('CL=F', 'chg'), Y('CL%3DF'), LIVE), 'unit': '달러', 'note': '배럴당 82.36달러(약 11만 원)'},
  {'name': '원/달러', 'close': N(FX, Y('KRW%3DX'), LIVE), 'chg_pct': N(f('KRW=X', 'chg'), Y('KRW%3DX'), LIVE), 'unit': '원', 'note': ''},
 ],

 # ── 차트 분석 ─────────────────────────────────────────────
 'charts': charts,
 'chart_summary': '세 지수 모두 **20·50·200일선 아래**. S&P 500은 **200일선(7,347)까지 0.3%** 남았고, 나스닥·SOXX 반등은 **거래량이 평균보다 적었습니다**.',

 # ── 간밤 핵심 뉴스 ─────────────────────────────────────────
 'news': [
  {'tag': '실적', 'img': 'img/2026-11-19-nvda.jpg', 'title': '엔비디아, 실적은 이겼는데 주가는 5일 연속 하락',
   'body': '3분기 매출 1,158억 달러(약 154조 원, +103%)에 다음 분기 1,300억 달러(약 173조 원)를 제시했습니다. 장 초반 올랐다가 2.9% 내린 150.96달러(약 20만 원)로 마감했습니다.',
   'src': [{'t': 'NVIDIA 발표', 'u': NV_PR}, {'t': 'AP', 'u': AP}]},
  {'tag': '연준', 'img': 'img/2026-11-19-fed.jpg', 'title': '연준 의사록 "10월 동결은 아슬아슬했다"',
   'body': '대부분 위원이 추가 인상을 예상했고, 일부는 0.5%p 인상도 거론했습니다. 12월 0.25%p 인상 확률은 약 95%입니다.',
   'src': [{'t': 'InvestmentNews', 'u': FED_MIN}, {'t': 'Investing.com', 'u': FED_INV}]},
  {'tag': '보안', 'img': 'img/2026-11-19-cyber.jpg', 'title': '사이버보안주 급등, 팔로알토 +9.9%',
   'body': f"정부가 자바의 치명적 취약점을 경고하자 보안주가 올랐습니다. 크라우드스트라이크 {f('CRWD','chg') if 'CRWD' in summ else 7.95:+.2f}%, 팔로알토는 장 마감 뒤 실적도 예상을 넘었습니다.",
   'src': [{'t': 'Capp Notes', 'u': CAPP}, {'t': '야후 파이낸스', 'u': Y('PANW')}]},
  {'tag': '업종', 'img': 'img/2026-11-19-health.jpg', 'title': '건강보험주 급락, 다우 1.1% 하락',
   'body': '메디케어 어드밴티지 감사 강화 규정안 영향으로 유나이티드헬스가 다우를 가장 많이 끌어내렸습니다.',
   'src': [{'t': 'Capp Notes', 'u': CAPP}]},
  {'tag': '메모리', 'img': 'img/2026-11-19-memory.jpg', 'title': '샌디스크·마이크론 약세 이어져',
   'body': f"샌디스크 {f('SNDK','chg'):+.2f}%, 마이크론 {f('MU','chg'):+.2f}%. 중국 GF증권이 2027년 낸드 공급 과잉을 전망한 뒤 매도가 이어졌고, 샌디스크는 3개월 동안 {abs(f('SNDK','m3')):.0f}% 빠졌습니다.",
   'src': [{'t': '24/7 Wall St.', 'u': MEM}, {'t': '야후 파이낸스', 'u': Y('SNDK')}]},
  {'tag': '원자재', 'img': 'img/2026-11-19-gold_oil.jpg', 'title': '금값 14개월 최저, 유가도 하락',
   'body': '금리 인상 신호에 금은 온스당 3,750달러(약 499만 원) 아래로 내려갔고, 유가 하락에 국채 금리도 조금 내렸습니다.',
   'src': [{'t': 'FXStreet', 'u': GOLD}, {'t': 'AP', 'u': AP}]},
 ],

 # ── 특징주 ─────────────────────────────────────────────────
 'movers': [
  {'ticker': 'NVDA', 'name': '엔비디아', 'close': N(f('NVDA', 'close'), Y('NVDA'), CLOSE), 'chg_pct': N(f('NVDA', 'chg'), Y('NVDA'), CLOSE), 'won': '약 20만 원', 'why': '실적 발표 뒤 상승분을 반납하고 5일 연속 하락'},
  {'ticker': 'SNDK', 'name': '샌디스크', 'close': N(f('SNDK', 'close'), Y('SNDK'), CLOSE), 'chg_pct': N(f('SNDK', 'chg'), Y('SNDK'), CLOSE), 'won': '약 103만 원', 'why': '낸드 공급 과잉 우려 지속, 52주 고점 대비 -67%'},
  {'ticker': 'MU', 'name': '마이크론', 'close': N(f('MU', 'close'), Y('MU'), CLOSE), 'chg_pct': N(f('MU', 'chg'), Y('MU'), CLOSE), 'won': '약 94만 원', 'why': '메모리 업종 동반 약세'},
  {'ticker': 'SOXX', 'name': '반도체 ETF', 'close': N(f('SOXX', 'close'), Y('SOXX'), CLOSE), 'chg_pct': N(f('SOXX', 'chg'), Y('SOXX'), CLOSE), 'won': '약 19만 원', 'why': 'AMD·브로드컴 강세로 소폭 반등'},
 ],

 # ── 월가·연준 한마디 ─────────────────────────────────────
 'street': {
  'title': '엔비디아 실적 뒤 증권사 반응',
  'summary': '실적 뒤 목표주가 24개의 중간값은 222.50달러(약 30만 원)입니다. 이전 목표를 밝힌 7곳 중 5곳이 낮췄고 2곳은 올렸습니다. 숫자보다 CEO 공백과 중국 리스크를 더 크게 본 결과입니다.',
  'summary_src': PT_MED,
  'rows': [
   {'firm': '레이먼드 제임스', 'rating': '', 'from': '515달러', 'to': '350달러(약 47만 원)', 'dir': -1, 'src': PT_TR},
   {'firm': '파이퍼 샌들러', 'rating': '비중확대 유지', 'from': '300달러', 'to': '230달러(약 31만 원)', 'dir': -1, 'src': PT_TR},
   {'firm': '모건스탠리', 'rating': '', 'from': '267달러', 'to': '260달러(약 35만 원)', 'dir': -1, 'src': PT_MS},
   {'firm': '에버코어 ISI', 'rating': '중립 유지', 'from': '186달러', 'to': '184달러(약 24만 원)', 'dir': -1, 'src': PT_BZ},
   {'firm': 'JP모건', 'rating': '비중확대 유지', 'from': '215달러', 'to': '230달러(약 31만 원)', 'dir': 1, 'src': PT_JPM},
   {'firm': '웨드부시', 'rating': '시장수익률 상회', 'from': '275달러', 'to': '293달러(약 39만 원)', 'dir': 1, 'src': PT_BZ},
   {'firm': 'BofA', 'rating': '매수', 'from': '—', 'to': '280달러(약 37만 원)', 'dir': 0, 'src': PT_BOFA},
  ],
  'voices': [
   {'who': '월러 연준 이사', 'say': '물가가 잘못된 방향으로 가고 있어 12월 0.5%p 인상도 필요할 수 있다고 말했습니다.', 'src': BABY},
   {'who': '윌리엄스 뉴욕 연은 총재', 'say': '지금은 극적인 조치가 필요한 상황은 아니라고 선을 그었습니다.', 'src': SED},
   {'who': '번스타인(지난주)', 'say': '엔비디아를 시장수익률로 내리고 목표를 400달러에서 200달러(약 27만 원)로 절반 낮췄습니다.', 'src': PT_BERN},
  ],
 },

 # ── 오늘 밤 일정 (한국 시간) ────────────────────────────
 'schedule': [
  {'kst': '장 전', 'type': '실적', 'name': '월마트 3분기 실적 (예상 주당 0.64달러, 약 850원)', 'why': '미국 소비가 버티는지 보는 대표 실적. 연말 쇼핑 시즌 전망이 핵심입니다.', 'star': 3, 'src': WMT},
  {'kst': '장 전', 'type': '실적', 'name': '알리바바 · 넷이즈 실적', 'why': '중국 소비와 AI 투자 분위기. 중국 주식(ADR) 흐름을 가릅니다.', 'star': 2, 'src': SCHWAB},
  {'kst': '22:00', 'type': '실적', 'name': '월마트 컨퍼런스콜', 'why': '관세와 가격 인상, 소비자 지갑 사정에 대한 언급을 봅니다.', 'star': 2, 'src': WMT},
  {'kst': '22:30', 'type': '지표', 'name': '신규 실업수당 청구 (예상 19.6만, 이전 20만)', 'why': '예상보다 낮으면 고용이 탄탄하다는 뜻이라 12월 금리 인상 압력이 커집니다.', 'star': 3, 'src': FV},
  {'kst': '22:30', 'type': '지표', 'name': '11월 필라델피아 연준 제조업지수 (예상 19.2, 이전 20.9)', 'why': '제조업 경기와 함께 가격 항목으로 물가 압력을 봅니다.', 'star': 2, 'src': FV},
  {'kst': '23:30', 'type': '개장', 'name': '뉴욕 정규장 개장 · 앤트로픽(ANT) 첫 거래', 'why': '첫 거래가 공모가 83달러(약 11만 원) 위인지, AI주로 돈이 몰리는지 빠지는지.', 'star': 3, 'src': CNBC_IPO},
  {'kst': '00:00', 'type': '지표', 'name': '10월 경기선행지수', 'why': '경기 둔화 신호를 보는 지표. 시장 영향은 작은 편입니다.', 'star': 1, 'src': SCHWAB},
  {'kst': '06:00 뒤', 'type': '실적', 'name': '인튜이트 · 로스스토어 실적 (장 마감 후)', 'why': 'AI 소프트웨어(인튜이트)와 할인 소매(로스) 실적, 시간외 반응.', 'star': 2, 'src': WK},
  {'kst': '내일', 'type': '지표', 'name': '미시간대 소비자심리 확정치 · 리사 쿡 연준 이사 연설', 'why': '소비자 기대 인플레이션과 연준 인사 발언으로 금리 경로 단서를 봅니다.', 'star': 2, 'src': WK},
 ],
 'schedule_note': '미국 서머타임 종료로 정규장은 한국 시간 23:30~06:00입니다. 시각은 발표 기관 일정 기준이며 바뀔 수 있습니다.',

 'calendar': {
  'today': '2026-11-19',
  'days': [
   {'d': '2026-11-16', 'ev': [{'k': '연준', 't': '워시 의장 연설'}]},
   {'d': '2026-11-17', 'ev': [{'k': '실적', 't': '엔비디아', 'hl': True, 'when': '장 후'}]},
   {'d': '2026-11-18', 'ev': [{'k': '연준', 't': 'FOMC 의사록', 'hl': True}, {'k': '실적', 't': '팔로알토', 'when': '장 후'}]},
   {'d': '2026-11-19', 'ev': [{'k': '상장', 't': '앤트로픽(ANT)', 'hl': True}, {'k': '실적', 't': '월마트·알리바바', 'when': '장 전'}, {'k': '지표', 't': '실업수당·필라델피아'}, {'k': '실적', 't': '인튜이트·로스', 'when': '장 후'}]},
   {'d': '2026-11-20', 'ev': [{'k': '지표', 't': '미시간대 소비자심리'}, {'k': '연준', 't': '쿡 이사 연설'}]},
   {'d': '2026-11-23', 'ev': []}, {'d': '2026-11-24', 'ev': []}, {'d': '2026-11-25', 'ev': []},
   {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장', 'hl': True}]},
   {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}]},
  ],
  'src': [{'t': 'HeyGoTrade 주간 일정', 'u': WK}, {'t': 'Kiplinger', 'u': 'https://www.kiplinger.com/investing/economy/this-weeks-economic-calendar'}, {'t': 'NYSE 휴장일', 'u': 'https://www.nyse.com/markets/hours-calendars'}],
 },

 # ── 이번 주 실적 달력 ───────────────────────────────────
 'earnings': [
  {'date': '11/17(화)', 'time': '장 마감 후', 'company': '엔비디아', 'ticker': 'NVDA', 'done': True},
  {'date': '11/18(수)', 'time': '장 마감 후', 'company': '팔로알토 네트웍스', 'ticker': 'PANW', 'done': True},
  {'date': '11/19(목)', 'time': '장 전', 'company': '월마트', 'ticker': 'WMT', 'done': False},
  {'date': '11/19(목)', 'time': '장 전', 'company': '알리바바', 'ticker': 'BABA', 'done': False},
  {'date': '11/19(목)', 'time': '장 마감 후', 'company': '인튜이트', 'ticker': 'INTU', 'done': False},
  {'date': '11/19(목)', 'time': '장 마감 후', 'company': '로스스토어', 'ticker': 'ROST', 'done': False},
 ],

 # ── 발행인 칼럼 (두 번째 쇼츠) ───────────────────────────
 'column': {
  'title': '젠슨 황 없는 엔비디아, 숫자보다 무거운 물음표',
  'short': {'id': 'VCv3p1YwE_c', 'title': '엔비디아 고점 -35%, 이번 주가 AI 운명 가른다?'},
  'body': f"매출은 1년 새 두 배가 됐는데 주가는 52주 고점보다 {abs((f('NVDA','close')/f('NVDA','hi52')-1)*100):.0f}% 낮습니다. 시장은 지금 실적보다 '누가 이끄느냐'를 더 따지고 있습니다. 후임 CEO가 정해지는 날이 반도체 업종의 다음 분기점이 될 수 있습니다.",
  'src': [{'t': 'NVIDIA 8-K', 'u': 'https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvda-20261111.htm'}],
 },

 'term': {'word': '200일 이동평균선', 'body': '최근 200거래일(약 10개월) 종가의 평균입니다. 장기 추세를 가르는 기준으로 쓰여, 지수가 이 선 아래로 내려가면 "장기 추세가 꺾였다"는 말이 나옵니다. 오늘 S&P 500은 이 선보다 0.3% 아래에 있습니다.'},
 'disclaimer': '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 야후 파이낸스 일봉 기준이며, 증권사 전망치는 보도된 내용을 옮긴 것입니다.',
}


# ── 특징주 검색용 시세(인기 종목) ───────────────────────────
KO = {'AAPL':'애플','ADBE':'어도비','AMD':'AMD','AMZN':'아마존','ARM':'ARM','ASML':'ASML','ASTS':'AST 스페이스모바일','AVGO':'브로드컴','BA':'보잉','BAC':'뱅크오브아메리카',
 'BRK-B':'버크셔 해서웨이','COIN':'코인베이스','COST':'코스트코','CRM':'세일즈포스','CRWD':'크라우드스트라이크','CVX':'셰브론','DIS':'디즈니','GLD':'금 ETF(GLD)',
 'GOOGL':'알파벳(구글)','HOOD':'로빈후드','IBIT':'비트코인 ETF(IBIT)','INTC':'인텔','IONQ':'아이온큐','JNJ':'존슨앤드존슨','JPM':'JP모건','KO':'코카콜라','LLY':'일라이 릴리',
 'MA':'마스터카드','MCD':'맥도날드','META':'메타','MSFT':'마이크로소프트','MSTR':'스트래티지','MU':'마이크론','NFLX':'넷플릭스','NKE':'나이키','NOW':'서비스나우',
 'NVDA':'엔비디아','OKLO':'오클로','ORCL':'오라클','PANW':'팔로알토 네트웍스','PEP':'펩시코','PFE':'화이자','PLTR':'팔란티어','QCOM':'퀄컴','QQQ':'나스닥100 ETF(QQQ)',
 'RIVN':'리비안','RKLB':'로켓랩','SBUX':'스타벅스','SCHD':'배당 ETF(SCHD)','SHOP':'쇼피파이','SMCI':'슈퍼마이크로','SNDK':'샌디스크','SNOW':'스노우플레이크','SOFI':'소파이',
 'SOXL':'반도체 3배(SOXL)','SOXX':'반도체 ETF(SOXX)','SPY':'S&P500 ETF(SPY)','STX':'씨게이트','TLT':'美 장기채 ETF(TLT)','TQQQ':'나스닥 3배(TQQQ)','TSLA':'테슬라',
 'TSM':'TSMC','UBER':'우버','UNH':'유나이티드헬스','V':'비자','VOO':'S&P500 ETF(VOO)','WDC':'웨스턴디지털','WMT':'월마트','XOM':'엑손모빌'}
WHY = {m['ticker']: m['why'] for m in issue['movers']}
WHY.update({'UNH': '메디케어 어드밴티지 감사 강화 규정안에 급락, 다우 하락 1위 요인', 'PANW': '자바 취약점 경고에 보안주 강세, 장 마감 뒤 실적 예상 상회',
            'CRWD': '보안주 동반 강세', 'AMD': 'AI 칩주 가운데 강세', 'AVGO': 'AI 칩주 가운데 강세'})
quotes = []
for ln in open('data/movers_raw.txt', encoding='utf-8'):
    t, d, c, ch, w1, m1, hi, a50, a200, rsi = ln.strip().split(',')
    quotes.append({'t': t, 'n': KO.get(t, t), 'c': float(c), 'won': round(float(c) * FX), 'ch': float(ch), 'w1': float(w1), 'm1': float(m1),
                   'hi': float(hi), 'a50': a50 == '1', 'a200': a200 == '1', 'rsi': int(rsi), 'why': WHY.get(t, '')})
issue['quotes'] = {'asof': CLOSE, 'src': 'https://finance.yahoo.com', 'fx': FX,
                   'default': ['NVDA', 'SNDK', 'MU', 'UNH', 'PANW', 'AMD'], 'list': quotes}

# ── v3: 일정(시각·별 5개·상세) ───────────────────────────
WMT_IR='https://finviz.com/news/421667/walmart-to-host-third-quarter-earnings-conference-call-november-19-2026'
BABA_IR='https://investingnews.com/alibaba-group-will-announce-september-quarter-2026-results-on-november-19-2026/'
BABA_EW='https://beta.earningswhispers.com/go/w/BABA'
issue['schedule']=[
 {'kst':'19:30','type':'실적','name':'알리바바 9월 분기 실적 발표','star':3,'why':'중국 소비와 클라우드·AI 투자 흐름. 중국 주식(ADR) 분위기를 가릅니다. 컨퍼런스콜은 21:00.','src':BABA_IR},
 {'kst':'21:00','type':'실적','name':'월마트 3분기 실적 발표','star':5,'why':'미국 소비가 버티는지 보는 대표 실적. 주당 예상 0.64달러(약 850원), 연말 쇼핑 시즌 전망이 핵심입니다. 컨퍼런스콜은 22:00.','src':WMT_IR},
 {'kst':'22:30','type':'지표','name':'신규 실업수당 청구 (예상 19.6만)','star':4,'why':'예상보다 낮으면 고용이 탄탄하다는 뜻이라 12월 금리 인상 압력이 커집니다. 이전 20만.','src':FV},
 {'kst':'22:30','type':'지표','name':'11월 필라델피아 연준 제조업지수','star':3,'why':'제조업 경기와 함께 가격 항목으로 물가 압력을 봅니다. 예상 19.2, 이전 20.9.','src':FV},
 {'kst':'23:30','type':'개장','name':'뉴욕 정규장 개장 · 앤트로픽(ANT) 첫 거래','star':5,'why':'첫 거래가 공모가 83달러(약 11만 원) 위인지, AI주로 돈이 몰리는지 빠지는지. IPO 첫 거래는 보통 개장 뒤 몇 시간 안에 시작됩니다.','src':CNBC_IPO},
 {'kst':'00:00','type':'지표','name':'10월 경기선행지수','star':2,'why':'경기 둔화 신호를 보는 지표. 시장 영향은 작은 편입니다.','src':SCHWAB},
 {'kst':'06:00~','type':'실적','name':'인튜이트 · 로스스토어 실적 (장 마감 후)','star':3,'why':'AI 소프트웨어(인튜이트)와 할인 소매(로스) 실적. 시간외 반응을 봅니다.','src':WK},
 {'kst':'내일','type':'지표','name':'미시간대 소비자심리 확정치 · 쿡 연준 이사 연설','star':3,'why':'소비자 기대 인플레이션과 연준 인사 발언으로 금리 경로 단서를 봅니다.','src':WK},
]
# ── v3: 참고 지표(이름·수치만) ───────────────────────────
issue['indicators']=[
 {'name':'공포·탐욕 지수','v':24.6,'d':1,'label':'극단적 공포','src':FG},
 {'name':'12월 금리 인상 확률','v':95.7,'d':1,'suf':'%','src':SED},
 {'name':'VIX','v':f('^VIX','close'),'d':2,'chg':f('^VIX','chg'),'src':Y('%5EVIX')},
 {'name':'풋/콜 비율','v':0.88,'d':2,'src':FG},
 {'name':'미 국채 10년','v':f('^TNX','close'),'d':2,'suf':'%','chg':round(f('^TNX','close')-f('^TNX','close')/(1+f('^TNX','chg')/100),2),'chgsuf':'%p','src':Y('%5ETNX')},
 {'name':'달러인덱스','v':f('DX-Y.NYB','close'),'d':2,'chg':f('DX-Y.NYB','chg'),'src':Y('DX-Y.NYB')},
 {'name':'WTI 유가','v':f('CL=F','close'),'d':2,'chg':f('CL=F','chg'),'src':Y('CL%3DF')},
 {'name':'원/달러','v':FX,'d':2,'chg':f('KRW=X','chg'),'src':Y('KRW%3DX')},
]
# ── v3: 캔들 데이터 ─────────────────────────────────────
C3=json.load(open('data/idx_candles.json',encoding='utf-8'))['idx']
TITLE={'^IXIC':'나스닥 차트 분석','^GSPC':'S&P 500 차트 분석','SOXX':'반도체(SOXX) 차트 분석'}
DATES=open('data/raw_series.txt',encoding='utf-8').readline().split('|')[1].split()
for c in issue['charts']:
    c['title']=TITLE[c['sym']]; c['candle']=C3[c['sym']]; c['candle']['dates']=['2026-'+d[:2]+'-'+d[2:] for d in DATES]
    c.pop('series',None); c.pop('points',None)
# ── v3: S&P 500 트리맵(시총 비중 상위 100) ───────────────
SEC={'정보기술':'AAPL MSFT NVDA AVGO AMD MU CSCO PLTR ORCL INTC AMAT TXN LRCX ANET CRWD IBM DELL KLAC APH ADI QCOM CRM ACN MRVL APP STX PANW',
 '커뮤니케이션':'GOOGL GOOG META NFLX DIS VZ TMUS T','경기소비재':'AMZN TSLA HD MCD TJX LOW SBUX','필수소비재':'WMT COST KO PG PM PEP MO',
 '헬스케어':'LLY JNJ ABBV UNH MRK TMO AMGN GILD ABT DHR PFE ISRG VRTX MDT MCK BMY SYK','금융':'BRK.B JPM V MA BAC MS GS WFC AXP C BLK SCHW CB PGR SPGI',
 '에너지':'XOM CVX COP','산업재':'GE RTX CAT GEV UNP DE LMT ETN BA ADP PH UBER','소재':'LIN','유틸리티':'NEE','부동산':'WELL PLD'}
S2={t:k for k,v in SEC.items() for t in v.split()}
tm=[]
for it in open('data/sp500_top100.txt',encoding='utf-8').read().strip().split(';'):
    t,w,ch,nm=it.split(',',3); tm.append({'t':t,'w':float(w),'ch':float(ch),'s':S2.get(t,'기타')})
issue['treemap']={'items':tm,'asof':CLOSE,'src':'https://www.slickcharts.com/sp500','note':'S&P 500 시가총액 비중 상위 100개 종목 · 크기=지수 비중, 색=전일 등락'}
# ── v3: 종목별 미니 차트·이슈 ───────────────────────────
MINI=json.load(open('data/tickers_mini.json',encoding='utf-8'))
INTC_A='https://www.finanzen.at/nachrichten/aktien/why-intel-stock-just-dropped-16071647'
INTC_B='https://www.trefis.com/stock/intc/articles/625805/why-did-intel-stock-fall-7/2026-11-17'
SPX_A='https://marketchameleon.com/Overview/SPCX/'
SPX_B='https://www.heygotrade.com/en/news/spacex-spcx-stock-news-november-13-2026/'
SPX_C='https://fourweekmba.com/spacex-stock/'
TN={
 'NVDA':{'y':[('3분기 매출 1,158억 달러(약 154조 원, +103%), 다음 분기 1,300억 달러(약 173조 원) 제시에도 5일 연속 하락',NV_PR),('증권사 7곳 중 5곳이 전망치를 낮춤',PT_MED)],'t':[('앤트로픽 상장 첫날 AI주 수급 흐름',CNBC_IPO)]},
 'SNDK':{'y':[('GF증권 2027년 낸드 공급 과잉 전망 뒤 매도 지속, 3개월 -52%',MEM)],'t':[]},
 'SNXX':{'y':[('기초자산 샌디스크 약세(낸드 공급 과잉 우려)를 2배로 반영',MEM)],'t':[]},
 'MU':{'y':[('낸드 가격 전망 하향에 메모리 업종 동반 약세',MEM)],'t':[]},
 'UNH':{'y':[('메디케어 어드밴티지 감사 강화 규정안에 -10.21%, 다우 하락 1위 요인',CAPP)],'t':[]},
 'PANW':{'y':[('정부의 자바 치명적 취약점 경고로 보안주 강세, 장 마감 뒤 실적도 예상 상회',CAPP)],'t':[]},
 'CRWD':{'y':[('자바 취약점 경고로 보안주 동반 강세',CAPP)],'t':[]},
 'WMT':{'y':[],'t':[('21:00 3분기 실적 발표 · 22:00 컨퍼런스콜 (예상 주당 0.64달러, 약 850원)',WMT_IR)]},
 'INTC':{'y':[('엔비디아가 보유한 인텔 지분을 매도한다는 소식에 11/17 장중 -2.3%, 11월 들어 약 18% 하락',INTC_A),('11/16 공시 관련 주주 집단소송 제기',INTC_B)],'t':[]},
 'SPCX':{'y':[('11/14 스타십 우주선 첫 발사대 포획 성공(부스터는 추락)',SPX_A),('테슬라와 합병 협상 보도(11/12)',SPX_B)],'t':[('12월 8일 보호예수 해제 예정',SPX_C)]},
 'SOXX':{'y':[('AMD·브로드컴 강세로 소폭 반등했지만 거래량은 평균 아래',Y('SOXX'))],'t':[]},
 'SOXL':{'y':[('반도체 지수 3배 · 고점 대비 -84%, 변동성 매우 큼',Y('SOXL'))],'t':[]},
 'GLD':{'y':[('금리 인상 신호에 금 14개월 최저',GOLD)],'t':[]},
 'XOM':{'y':[('유가 하락에 에너지주 약세',AP)],'t':[]},
 'CVX':{'y':[('유가 하락에 에너지주 약세',AP)],'t':[]},
}
KO.update({'SPCX':'스페이스X','SNXX':'샌디스크 2배(SNXX)'})
for q in issue['quotes']['list']:
    m=MINI.get(q['t'])
    if m: q['mini']={'mn':m[0],'mx':m[1],'b':m[2],'res':m[3],'sup':m[4],'ma5':m[5],'ma20':m[6],'ma50':m[7],'ma200':m[8],'vr':m[9]}
    n=TN.get(q['t'],{'y':[],'t':[]}); q['news']={'y':[{'t':a,'u':b} for a,b in n['y']],'t':[{'t':a,'u':b} for a,b in n['t']]}
    q['n']=KO.get(q['t'],q['n'])
issue['quotes']['default']=['NVDA']
issue['site_v']=8
issue['top']['img']='img/2026-11-19-ipo.jpg'

# ── v4: AI 종합 의견 ───────────────────────────────────
AI={
 'NVDA':'실적은 시장 예상보다 좋았지만 주가는 CEO 공백과 AI 투자 자금 조달 우려에 눌려 5일째 밀렸습니다. 모든 이동평균선 아래에 있고 RSI 21로 과매도 구간이라 기술적 반등 여지는 있지만, 후임 CEO가 정해지기 전까지는 반등이 나와도 힘이 약할 수 있습니다. 오늘 밤 앤트로픽 첫 거래로 AI 수요 심리가 살아나는지가 첫 시험대입니다.',
 'INTC':'11월 들어 약 18% 빠지며 20·50·200일선을 모두 내줬습니다. 엔비디아의 지분 매도 소식과 주주 소송이 겹쳐 단기 수급이 무거운 상태이고, RSI 29로 과매도에 들어왔습니다. 51.51달러(약 6만 9천 원)가 최근 20일 저점이라 이 자리를 지키는지가 단기 관전 포인트이고, 파운드리 고객 확보 같은 자체 재료가 나와야 추세가 바뀔 수 있습니다.',
 'SPCX':'상장 이후 고점보다 36% 낮지만 최근 한 주는 +2.7%로 나스닥보다 강했습니다. 20·50일선 근처에서 방향을 고르는 중이고, 스타십 포획 성공과 테슬라 합병설이 버팀목입니다. 12월 8일 보호예수 해제로 풀리는 물량이 다음 큰 변수입니다.',
 'SNDK':'3개월 새 52% 빠진 메모리 대표 약세주입니다. 낸드 공급 과잉 전망이 나온 뒤 매도가 이어져 모든 이동평균선 아래에 있고, 20일 저점 749달러(약 100만 원) 부근에서 버티는 중입니다. 낸드 가격 지표가 바닥을 확인해 줘야 추세 전환을 말할 수 있는 구간입니다.',
 'SNXX':'샌디스크 2배 상품이라 기초자산 하락이 두 배로 반영돼 고점 대비 -94%까지 밀렸습니다. 변동성이 매우 커 같은 반등에도 원금 회복이 어렵다는 레버리지 상품의 특성을 염두에 둬야 합니다.',
 'MU':'고점 대비 -44%로 메모리 업종 조정을 그대로 받았습니다. 650달러(약 86만 원)대가 20일 저점이고, 이동평균선은 모두 위에 있어 저항이 겹겹입니다. 업종 전체의 가격 지표 회복을 기다리는 흐름입니다.',
 'SOXL':'반도체 지수의 3배 상품으로 고점 대비 -84%입니다. SOXX가 200일선을 11% 아래에서 돌고 있어 반도체 지수가 200일선을 되찾기 전까지는 반등이 나와도 변동성이 클 수 있습니다.',
 'SOXX':'반도체 ETF는 10/30 200일선을 이탈한 뒤 고점 대비 -35%까지 내려왔습니다. 어제는 AMD·브로드컴 강세로 소폭 올랐지만 거래량이 평균보다 적었습니다. 위로는 200일선 160.77, 아래로는 20일 저점 130.75가 기준선입니다.',
 'QQQ':'나스닥100 ETF는 200일선을 약 3% 아래에서 돌고 있습니다. 앤트로픽 상장과 12월 금리 결정이 단기 방향을 정할 변수이고, 646달러(약 86만 원) 20일 저점을 지키는지가 기술적 관전 포인트입니다.',
 'TSLA':'50·200일선 위를 지키는 몇 안 되는 대형 기술주입니다(20일선은 살짝 아래). 1달 수익률 +2.7%로 시장보다 강했고, 스페이스X와의 합병설이 재료로 거론됩니다. 20일 범위 상단인 414달러(약 55만 원)를 넘는지가 다음 관전 포인트입니다.',
 'UNH':'메디케어 어드밴티지 감사 강화 규정안에 하루 10% 급락해 모든 이동평균선 아래로 내려갔습니다. 거래량이 평균의 3.5배로 실린 하락이라 단기 충격이 큰 편이고, 규정안의 최종 내용이 나오기 전까지는 불확실성이 남습니다.',
 'PANW':'자바 취약점 경고와 장 마감 뒤 실적 호조가 겹쳐 하루 9.9% 올랐고, 200일선 위를 지키고 있습니다. 거래량이 평균의 2.7배로 실린 상승이라 시간외 실적 반응이 이어지는지가 관건입니다.',
 'CRWD':'보안주 강세에 하루 7.95% 올랐고 200일선 위에 있습니다. 거래량도 평균보다 많았습니다. 20일 범위 상단 272달러(약 36만 원)가 다음 저항입니다.',
 'AMD':'AI 칩주 가운데 어제 5.3% 오르며 엔비디아와 반대로 움직였습니다. 20·200일선 위를 지키고 있어 중기 추세는 살아 있지만, 50일선(555달러, 약 74만 원) 아래라 그 저항을 넘는지 확인이 필요합니다.',
 'AVGO':'어제 3.6% 올라 20·50일선을 회복했습니다. 다만 200일선(367달러, 약 49만 원)은 아직 위에 있어 그 자리를 넘는지가 추세 전환의 기준입니다.',
 'WMT':'오늘 밤 21:00 실적 발표를 앞두고 있습니다. 주가는 이동평균선 위에서 안정적이고 1달 +8%로 방어주 역할을 해 왔습니다. 연말 쇼핑 시즌 전망이 핵심 변수입니다.',
 'PLTR':'고점 대비 -26%로 조정 중이지만 200일선 위는 지키고 있습니다. 20일선 아래라 단기 흐름은 약하고, AI 소프트웨어 투자 심리에 따라 움직일 가능성이 큽니다.',
 'AAPL':'모든 이동평균선 위에서 고점에 가까운(-2.3%) 몇 안 되는 빅테크입니다. 시장 하락 때 방어주처럼 움직이고 있어 기술주 약세장에서 상대적으로 강한 흐름입니다.',
 'GOOGL':'1달 -17%로 50·200일선을 모두 내줬습니다. 기술주 전반의 조정을 받는 중이고, 200일선(337달러, 약 45만 원)을 되찾는지가 중기 기준입니다.',
 'MSFT':'200일선 위는 지키고 있지만 20·50일선 아래라 단기 약세입니다. 고점 대비 -9%로 빅테크 가운데 낙폭은 작은 편입니다.',
 'META':'1달 -11%로 이동평균선을 모두 내줬고 거래량은 평균보다 적었습니다. AI 투자 비용 부담 논쟁의 영향을 받는 흐름입니다.',
 'AMZN':'어제 3.8% 올라 이동평균선을 모두 회복했습니다. 기술주 가운데 강한 편이고, 20일 범위 상단 275달러(약 37만 원)를 넘는지가 다음 관전 포인트입니다.',
}
def auto_ai(q):
    m=q.get('mini') or {}; c=q['c']; parts=[]
    mas=[(m.get('ma20'),'20일선'),(m.get('ma50'),'50일선'),(m.get('ma200'),'200일선')]
    below=[n for v,n in mas if v and c<v]; above=[n for v,n in mas if v and c>=v]
    if mas and not above: parts.append(f"{q['n']}은(는) 20·50·200일선 아래에 있어 단기·중기 흐름이 모두 약합니다.")
    elif not below: parts.append(f"{q['n']}은(는) 주요 이동평균선 위에서 추세를 유지하고 있습니다.")
    else: parts.append(f"{q['n']}은(는) {'·'.join(above)} 위, {'·'.join(below)} 아래에서 방향을 고르는 중입니다.")
    parts.append(f"고점 대비 {q['hi']}%, 최근 1달 {q['m1']:+}%이고 RSI는 {q['rsi']}입니다."+(' 과매도 구간이라 기술적 반등이 나올 수 있지만 추세 전환 신호는 아닙니다.' if q['rsi']<30 else ' 과열 구간이라 단기 숨 고르기가 나올 수 있습니다.' if q['rsi']>70 else ''))
    if m.get('sup') and m.get('res'): parts.append(f"최근 20일 범위는 {m['sup']}~{m['res']} 사이로, 이 범위를 벗어나는 방향이 다음 흐름을 정할 가능성이 큽니다.")
    return ' '.join(parts)
for q in issue['quotes']['list']:
    q['ai']=AI.get(q['t']) or auto_ai(q)
# ── v4: 인플루언서 의견 ───────────────────────────────
issue['street']['influencers']=[
 {'who':'마이클 버리 (빅쇼트)','say':'젠슨 황 사태보다 AI 투자 자금을 어떻게 조달하느냐가 엔비디아의 더 큰 문제라고 봅니다. 빅테크의 AI 지출 약정이 3조 달러(약 4,000조 원)를 넘는다고 추정했습니다.','src':'https://finance.yahoo.com/technology/ai/articles/michael-burry-says-nvidia-biggest-173049740.html'},
 {'who':'캐시 우드 (ARK 인베스트)','say':'앤트로픽이 2조 달러(약 2,660조 원) 가까운 기업가치도 정당화할 수 있다고 말했습니다. ARK는 11/9 엔비디아를 사들였다가 실적 발표 전에 일부를 판 것으로 공시됐습니다.','src':'https://finance.yahoo.com/markets/article/why-the-anthropic-ipo-could-be-a-trap-for-investors-135504884.html','src2':'https://finance.yahoo.com/markets/crypto/articles/why-did-cathie-wood-sell-050000758.html'},
 {'who':'짐 크레이머 (CNBC)','say':'앤트로픽 상장 없이는 AI 관련주가 제대로 회복하기 어렵다고 말했습니다. 엔비디아는 일주일 전보다 매력이 떨어졌다고 평가했습니다.','src':'https://finbold.com/jim-cramer-calls-this-ai-company-the-most-consequential-deal-of-our-time/','src2':'https://247wallst.com/cards/the-call-that-matters-for-anyone-long-ai-hardware-cramer-is-amd-podcast-episode-01m71syszzacafye5y3hrz3y10'},
 {'who':'일론 머스크','say':'젠슨 황 없는 엔비디아는 핵심 계약을 잃을 것이라고 말했습니다.','src':'https://www.ytn.co.kr/_ln/0102_202611160649379740'},
 {'who':'전인구 (유튜버)','say':'최근 발언은 확인된 출처를 찾지 못해 싣지 않았습니다. 샌디스크 올인이 그의 전망 적중률을 데이터로 따져 본 쇼츠(적중률 47%)로 대신합니다.','src':'https://www.youtube.com/shorts/p29QHMLDHvo'},
]

# ── v6: 1면 핵심 문장 · 차트 한 줄 요약 · 트리맵 해설/종목 팝업 · 롱/숏 카드 · 샌디스크 일봉 ──
TC='https://techcrunch.com/2026/11/18/anthropic-reportedly-prices-ipo-at-83-a-share-above-projected-range/'
FOOL='https://www.fool.com/investing/2026/11/18/anthropic-priced-its-ipo-at-usd83-here-s-what-i-d-pay-for-the-stock/'
BPN='https://www.babypips.com/news/headline-anthropic-ipo-what-could-mean-nasdaq-2026-11-16'
STT='https://www.stocktitan.net/articles/anthropic-ipo-live-ant-first-trading-day-2026'
BMF='https://www.buildmvpfast.com/blog/anthropic-ipo-price-range-run-rate-claude-builders-2026'
issue['top'].pop('figures',None)
issue['top']['points']=[
 {'t':'공모가를 83달러(약 11만 원)로 정했습니다. 희망 범위 70~78달러(약 9만 3천~10만 4천 원)보다 높습니다.','src':CNBC_IPO},
 {'t':'공모 주식을 8.25억 주에서 9.8억 주로 늘려 813억 달러(약 108조 원)를 모았습니다. 스페이스X의 750억 달러(약 100조 원)를 넘는 역대 최대입니다.','src':TC},
 {'t':'주문은 공모 물량의 약 7배가 몰렸고, 희석 기준 기업가치는 약 1.5조 달러(약 2,000조 원)입니다.','src':TV_ANT},
 {'t':'올해 1~9월 매출은 332억 달러(약 44조 원)로 1년 전보다 1,200% 늘었습니다. 기업가치는 연환산 매출의 약 18배입니다.','src':FOOL},
 {'t':'나스닥 새 규칙대로면 15거래일 만에 나스닥100에 들어갈 수 있어, 지수를 따라가는 자금이 사들일 수 있습니다.','src':BPN},
]
issue['top']['risks']=[
 {'t':'AMD·브로드컴·구글 등 7개 기업이 공모가로 260억 달러(약 35조 원)어치를 따로 사는데, 이 물량은 매도 제한(보호예수)이 없습니다.','src':BMF},
 {'t':'6월 스페이스X는 첫날 19% 올랐지만 한 달 뒤 공모가 아래로 내려갔습니다. 첫날 성적이 그 뒤를 보장하지는 않습니다.','src':BPN},
]
issue['top']['why']='AI 대장주가 흔들리는 가운데 나온 역대 최대 공모입니다. 첫날 주가가 AI 투자 심리의 온도계가 됩니다.'
issue['top']['watch']=[
 '첫 거래 가격이 공모가 83달러(약 11만 원) 위에서 시작하는지 (첫 체결은 개장 몇 시간 뒤일 수 있음)',
 '엔비디아·반도체로 매수세가 번지는지, 거꾸로 돈이 빠져나가는지',
 '큰 공모 물량을 소화하느라 다른 기술주가 눌리는지',
]
issue['top']['src']=[{'t':'CNBC','u':CNBC_IPO},{'t':'TechCrunch','u':TC},{'t':'TradingView','u':TV_ANT},{'t':'Motley Fool','u':FOOL},{'t':'BabyPips','u':BPN},{'t':'Stock Titan','u':STT}]
# 차트 위 한 줄 요약(데이터로 문장 생성)
import re as _re
def lv(c,v): return f"{v:,.2f}" if c.get('unit')=='달러' else f"{round(v):,}"
for c in issue['charts']:
    vr=next((float(m.group(1)) for t in c.get('tags',[]) for m in [_re.search(r'거래량 ([\d.]+)배',t['t'])] if m),None)
    ch=c['chg_pct']['v']; up,dn=c['watch']['up'],c['watch']['down']; s=[]
    if vr is not None:
        if vr<0.95: s.append(f"어제 거래량은 최근 20거래일 평균의 {vr}배로 적은 편이라, {abs(ch):.2f}% {'반등' if ch>0 else '하락'}에 힘이 실리지는 않았습니다.")
        elif vr<1.15: s.append(f"어제 거래량은 최근 20거래일 평균({vr}배) 수준이었고, 지수는 {ch:+.2f}% 움직였습니다.")
        else: s.append(f"어제 거래량이 최근 20거래일 평균의 {vr}배로 늘어난 {'상승' if ch>0 else '하락'}이었습니다.")
    if abs(up['gap'])<=1.5 and abs(dn['gap'])<=1.5:
        s.append(f"바로 위 {up['name']}({lv(c,up['v'])}, {up['gap']:+}%)과 바로 아래 {dn['name']}({lv(c,dn['v'])}, {dn['gap']}%) 사이에 끼어 있어, 어느 쪽을 먼저 깨느냐가 다음 방향을 정합니다.")
    elif abs(dn['gap'])<abs(up['gap']):
        s.append(f"위의 {up['name']}({lv(c,up['v'])})까지는 {up['gap']:+}%로 멀고, 먼저 {dn['name']} {lv(c,dn['v'])}({dn['gap']}%) 지지를 시험하는 자리입니다.")
    else:
        s.append(f"{up['name']} {lv(c,up['v'])}({up['gap']:+}%) 돌파를 시험하는 자리이고, 밀리면 {dn['name']} {lv(c,dn['v'])}({dn['gap']}%)가 받침입니다.")
    c['brief']=' '.join(s)
    # 어제 캔들 모양으로 한 줄 제목
    r=summ[c['sym']]; o,h,l,cl=(float(r[k]) for k in ('open','high','low','close'))
    rg=h-l or 1; lw=(min(o,cl)-l)/rg; uw=(h-max(o,cl))/rg; bd=abs(cl-o)/rg
    near=abs(l/dn['v']-1)*100<=0.6
    if lw>=0.45: shape='장중 밀렸다가 긴 아래꼬리를 달고 되돌린 하루'
    elif uw>=0.45: shape='장중 올랐다가 긴 위꼬리를 남기고 밀린 하루'
    elif bd>=0.6: shape='큰 '+('양봉으로 밀고 올라간' if cl>o else '음봉으로 밀려 내려간')+' 하루'
    else: shape='작은 몸통으로 방향을 못 정한 하루'
    tail=(f", {dn['name']} 바로 위까지 밀려 지지를 시험" if near else (', 저점을 테스트하며 버티는 구간' if lw>=0.45 else ''))
    c['headline']=shape+tail+(' · 거래량은 적음' if vr is not None and vr<0.95 else '')
# 트리맵: 종목 팝업 데이터 + 해설
TD=json.load(open('data/tm_daily.json',encoding='utf-8'))
NM={x.split(',')[0]:x.split(',',3)[3] for x in open('data/sp500_top100.txt',encoding='utf-8').read().strip().split(';')}
for it in issue['treemap']['items']:
    r=TD.get(it['t'].replace('.','-'))
    it['n']=KO.get(it['t'],NM.get(it['t'],it['t']))
    if r and r!='ERR': it['d']={'o':r[1],'h':r[2],'l':r[3],'c':r[4],'ch':r[5],'v':r[6],'vr':r[7],'w1':r[8],'m1':r[9],'ma20':r[10],'ma50':r[11],'hi':r[12],'lo':r[13]}
tmi=issue['treemap']['items']; ups=sum(1 for i in tmi if i['ch']>0)
secw={}
for i in tmi: a=secw.setdefault(i['s'],[0,0]); a[0]+=i['w']; a[1]+=i['w']*i['ch']
sw={k:round(b/a,1) for k,(a,b) in secw.items()}
g=lambda t:next(i for i in tmi if i['t']==t)
issue['treemap']['comment']={'h':f"100개 중 {ups}개만 상승, 보안주·AMD만 웃고 헬스케어·에너지는 밀린 하루",'t':(f"어제는 상위 100개 중 {ups}개만 올라, S&P 500 하락폭({f('^GSPC','chg'):+.2f}%)보다 체감이 더 나빴습니다. "
 f"기술주는 한 방향이 아니었습니다. 실적을 낸 엔비디아는 {g('NVDA')['ch']}%였지만, 정부의 자바 취약점 경고에 팔로알토(+{g('PANW')['ch']}%)·크라우드스트라이크(+{g('CRWD')['ch']}%) 같은 보안주가 뛰었고 AMD도 +{g('AMD')['ch']}%였습니다. "
 f"가장 약한 곳은 헬스케어(비중 가중 {sw['헬스케어']}%)로, 메디케어 감사 강화안에 유나이티드헬스가 {g('UNH')['ch']}% 빠졌습니다. 유가 하락에 에너지({sw['에너지']}%)도 밀렸고, 필수소비재도 {sw['필수소비재']}%라 방어주로 돈이 몰린 날은 아니었습니다. "
 f"한 달로 넓혀 보면 인텔 {TD['INTC'][9]}%, 마이크론 {TD['MU'][9]}% 등 반도체·메모리가 가장 약합니다."),
 'src':[{'t':'slickcharts','u':'https://www.slickcharts.com/sp500'},{'t':'CappNotes 마감 정리','u':CAPP},{'t':'AP','u':AP},{'t':'야후 파이낸스','u':'https://finance.yahoo.com'}]}
# 롱/숏 한마디 카드 (말풍선 = 실제 발언·보도를 쉬운 말로 줄인 것)
issue['street']['camps']={'long':[
 {'who':'캐시 우드','role':'ARK 인베스트','sil':'woman','say':'앤트로픽은 2조 달러(약 2,660조 원)짜리 회사도 될 수 있어요.','src':'https://finance.yahoo.com/markets/article/why-the-anthropic-ipo-could-be-a-trap-for-investors-135504884.html'},
 {'who':'짐 크레이머','role':'CNBC 진행자','sil':'mic','say':'앤트로픽 상장이 AI주 회복의 열쇠예요.','src':'https://finbold.com/jim-cramer-calls-this-ai-company-the-most-consequential-deal-of-our-time/'},
 {'who':'JP모건','role':'증권사','sil':'firm','say':'엔비디아 실적은 탄탄해요. 목표주가를 215달러에서 230달러(약 31만 원)로 올렸어요.','src':PT_JPM},
 {'who':'윌리엄스','role':'뉴욕 연은 총재','sil':'suit_g','say':'지금 금리를 확 올릴 만큼 급한 상황은 아니에요.','src':SED},
],'short':[
 {'who':'월러','role':'연준 이사','sil':'suit','say':'물가가 거꾸로 가요. 12월엔 0.5%p 올려야 할 수도 있어요.','src':BABY},
 {'who':'번스타인','role':'증권사 (지난주)','sil':'firm','say':'엔비디아 목표주가를 400달러에서 200달러(약 27만 원)로 반 토막 냈어요.','src':PT_BERN},
 {'who':'마이클 버리','role':'빅쇼트 투자자','sil':'hood','say':'진짜 문제는 AI에 쓸 돈을 어디서 구하느냐예요.','src':'https://finance.yahoo.com/technology/ai/articles/michael-burry-says-nvidia-biggest-173049740.html'},
 {'who':'일론 머스크','role':'테슬라 CEO','sil':'tee','say':'젠슨 황 없는 엔비디아는 큰 계약을 놓칠 거예요.','src':'https://www.ytn.co.kr/_ln/0102_202611160649379740'},
]}
issue['street'].pop('voices',None); issue['street'].pop('influencers',None)
# 샌디스크: 야후 일봉이 2개뿐이라 1시간봉을 일봉으로 묶어 미니 차트 생성
import base64
SD=json.load(open('data/sndk_daily.json',encoding='utf-8')); last=SD[-22:]
mn=min(r[3] for r in last); mx=max(r[2] for r in last)
pk=bytes(max(0,min(255,round((v-mn)/(mx-mn)*255))) for r in last for v in r[1:5])
cl=[r[4] for r in SD]; vo=[r[5] for r in SD]; avg=lambda a:sum(a)/len(a)
for q in issue['quotes']['list']:
    if q['t']=='SNDK':
        q['mini']={'mn':mn,'mx':mx,'b':base64.b64encode(pk).decode(),'res':round(max(r[2] for r in SD[-20:]),2),'sup':round(min(r[3] for r in SD[-20:]),2),
                   'ma5':round(avg(cl[-5:]),2),'ma20':round(avg(cl[-20:]),2),'ma50':round(avg(cl[-50:]),2),'ma200':1284.66,'vr':round(vo[-1]/avg(vo[-21:-1]),2),'note':'1시간봉을 묶은 일봉'}
# ── v7: 리드 문구 삭제 · 뉴스 한 줄 요약 · 증권사 의견(종목 무관, 이슈 순) · 내 종목 기본 SOXL ──
issue['lead']=''
LINES=['매출 1,158억 달러(약 154조 원, +103%)로 예상을 넘었지만 주가는 2.9% 내려 150.96달러(약 20만 원)에 마감했습니다.',
 '위원 대부분이 추가 인상을 예상했고, 12월 0.25%p 인상 확률은 약 95%입니다.',
 '정부의 자바 취약점 경고에 보안주가 오르고, 팔로알토는 장 마감 뒤 실적도 예상을 넘었습니다.',
 '메디케어 감사 강화 규정안에 유나이티드헬스가 10% 넘게 빠져 다우를 끌어내렸습니다.',
 f"낸드 공급 과잉 전망 뒤 매도가 이어져 샌디스크는 3개월 새 {abs(f('SNDK','m3')):.0f}% 빠졌습니다.",
 '금리 인상 신호에 금은 온스당 3,750달러(약 499만 원) 아래로, 유가도 함께 내렸습니다.']
for n,l in zip(issue['news'],LINES): n['line']=l
NQ17='https://www.newsquawk.com/headlines/us-broker-moves-csco-upgraded-at-hsbc-pep-downgraded-at-bernstein'
NQ13='https://www.newsquawk.com/headlines/us-broker-moves-panw-upgraded-at-keybanc-avgo-downgraded-at-rothschild-redburn'
NQ09='https://www.newsquawk.com/headlines/us-broker-moves-amd-upgraded-at-oppenheimer-dkng-downgraded-at-numerous-brokerages'
issue['street']['title']='최근 눈에 띈 증권사 의견'
issue['street']['summary']='최근 2주 사이 등급을 올린 곳은 시스코·팔로알토·AMD처럼 AI 인프라와 보안 쪽이 많았습니다. 반대로 브로드컴과 펩시코는 낮춘 의견이 나왔습니다. 이슈가 크거나 시장에 미친 영향이 큰 순서입니다.'
issue['street']['summary_src']=NQ17
issue['street']['rows']=[
 {'stock':'시스코','firm':'HSBC · DZ은행','rating':'보유 → 매수','to':'133달러(약 17.7만 원)','date':'11/17','dir':1,'src':NQ17},
 {'stock':'팔로알토','firm':'키뱅크','rating':'중립 → 비중확대','to':'380달러(약 50.5만 원)','date':'11/13','dir':1,'src':NQ13},
 {'stock':'AMD','firm':'오펜하이머','rating':'시장수익률 → 시장수익률 상회','to':'600달러(약 79.8만 원)','date':'11/9','dir':1,'src':NQ09},
 {'stock':'엔비디아','firm':'BofA','rating':'매수 유지 (실적 뒤)','to':'280달러(약 37.2만 원)','date':'11/18','dir':0,'src':PT_BOFA},
 {'stock':'브로드컴','firm':'로스차일드 레드번','rating':'매수 → 중립','to':'398달러(약 52.9만 원)','date':'11/13','dir':-1,'src':NQ13},
 {'stock':'뉴코어','firm':'모건스탠리','rating':'중립 → 비중확대','to':'310달러(약 41.2만 원)','date':'11/17','dir':1,'src':NQ17},
 {'stock':'메드트로닉','firm':'파이퍼 샌들러','rating':'중립 → 비중확대','to':'120달러(약 16만 원)','date':'11/17','dir':1,'src':NQ17},
 {'stock':'펩시코','firm':'번스타인','rating':'시장수익률 → 시장수익률 하회','to':'128달러(약 17만 원)','date':'11/17','dir':-1,'src':NQ17},
]
issue['quotes']['default']=['SOXL']
for q in issue['quotes']['list']:
    if q['t']=='SOXL':
        q['news']={'y':[{'t':'SOXX가 20일 최고 종가보다 18.5% 낮아져 수리수리진타리 ⑨ 반도체 급락 반등 신호(B+)가 켜짐','u':'https://stock.jintar.co.kr/c/9/'},{'t':'AMD +5.31%·브로드컴 +3.64%가 받쳤지만 엔비디아 -2.89%','u':Y('SOXX')}],
                   't':[{'t':'23:30 앤트로픽(ANT) 첫 거래 — AI 반도체로 돈이 몰리는지 빠지는지','u':CNBC_IPO}]}
        q['ai']=f"반도체 지수를 하루 3배로 따라가는 상품이라 고점 대비 {q['hi']}%, 최근 1주 {q['w1']:+}%·1달 {q['m1']:+}%로 크게 밀렸습니다. 모든 이동평균선 아래라 추세는 아직 약하지만, RSI {q['rsi']}로 과매도에 가까워졌고 어제는 거래량이 평소 수준인 채 소폭 올랐습니다. 반도체 ETF(SOXX)가 200일선을 약 11% 아래에서 돌고 있어 반등이 나와도 흔들림이 클 수 있고, 3배 상품은 같은 폭으로 오르내려도 원금이 깎이는 구조라 보유 기간을 짧게 정해 두는 편이 안전합니다."

issue.pop('column',None); issue.pop('term',None)
# ── v8: 차트 분석 = 어제 이슈 → 최근 대비 → 앞으로 ──
CH={
 '^IXIC':('엔비디아가 밀려도 5일 만에 반등, 긴 아래꼬리로 저점 방어',[
   ('어제',f"나스닥은 {f('^IXIC','chg'):+.2f}%로 5거래일 만에 올랐습니다. 실적을 낸 엔비디아는 -2.89%였지만 아마존(+3.82%)·AMD(+5.31%)·브로드컴(+3.64%)이 받쳤고, 장중 24,268까지 밀렸다가 되돌렸습니다."),
   ('최근 대비',f"1주 {f('^IXIC','w1'):+.1f}%, 1달 {f('^IXIC','m1'):+.1f}% 빠진 데 비하면 작은 반등입니다. 거래량도 20일 평균의 0.87배로 적었고, 지수는 20·50·200일선 아래에 있습니다."),
   ('앞으로','오늘 밤 앤트로픽 첫 거래가 AI 심리를 살리면 200일선 25,152(+3.0%) 회복을 시도할 수 있고, 반대라면 20일 저점 23,989(-1.8%) 시험이 먼저 나올 수 있습니다.')]),
 '^GSPC':('5일 연속 하락, 200일선 바로 아래서 버티는 중',[
   ('어제',f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 5일 연속 내렸습니다. 6월 이후 가장 긴 하락입니다. 유나이티드헬스(-10.21%)와 에너지주가 끌어내렸고, 보안주·아마존은 버텼습니다."),
   ('최근 대비',f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%입니다. 거래량은 평소 수준(1.03배)이라 한꺼번에 던지기보다 천천히 밀리는 모습이고, 200일선 7,347 바로 아래(-0.3%)에서 끝났습니다."),
   ('앞으로','20일 저점 7,288(-0.5%)과 200일선 사이가 1%도 안 됩니다. 200일선을 되찾으면 하락이 멈췄다는 신호, 7,288 아래로 내려가면 조정이 더 이어진다는 신호로 볼 수 있습니다.')]),
 'SOXX':('이틀째 소폭 반등, 아직은 바닥 다지기',[
   ('어제',f"반도체 ETF는 {f('SOXX','chg'):+.2f}%로 이틀째 조금 올랐습니다. AMD·브로드컴 강세가 엔비디아(-2.89%)·마이크론(-1.00%) 약세를 상쇄했습니다."),
   ('최근 대비',f"그래도 1주 {f('SOXX','w1'):+.1f}%, 1달 {f('SOXX','m1'):+.1f}%로 세 지수 중 가장 약하고 고점 대비 -35%입니다. 거래량은 평균의 0.82배라 반등에 매수세가 크게 붙지 않았습니다."),
   ('앞으로','200일선 160.77까지는 +13%로 멀어 당장은 바닥을 다지는 구간입니다. 20일 저점 130.75(-7.8%)를 지키면서 거래량이 붙는 반등이 나오는지가 먼저입니다.')]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'],c['an']=CH[c['sym']]
# ── v6: 수리수리진타리 오늘의 카드 (stock.jintar.co.kr · 11/18 장 종료 기준 신호) ──
JL=json.load(open('data/jintari_latest.json',encoding='utf-8'))
w=lambda usd:(lambda v:f"약 {v/10000:.1f}만 원".replace('.0만','만') if v<100000 else f"약 {round(v/10000)}만 원")(usd*FX)
usd=lambda s:float(s.replace('$','').replace(',',''))
JC=[]
for c in JL['cards']:
    slug=c['s'][0]; num={'①':'1','②':'2','③':'3','④':'4','⑤':'5','⑥':'6','⑦':'7','⑧':'8','⑨':'9'}.get(slug,'')
    JC.append({'g':c['g'],'t':c['n'],'kn':c['kn'],'s':c['s'],'ln':c.get('ln',[]),
     'rows':[('신호 기준가',f"{usd(c['pxSig'])}달러({w(usd(c['pxSig']))}) · 11/18 종가"),
             ('살 수 있는 가격',f"{usd(c['buy'])}달러({w(usd(c['buy']))}) 안쪽"),
             ('익절 · 손절',f"+40%({usd(c['tgt'])}달러, {w(usd(c['tgt']))}) · −20%({usd(c['stop'])}달러, {w(usd(c['stop']))})"),
             ('보유 기간','최대 15거래일, 15일째 종가에 정리')],
     'why':'11/18 반도체 ETF(SOXX)가 20일 최고 종가보다 18.5% 낮아져 ⑨ 반도체 급락 반등 신호가 켜졌습니다. 2012~26년 이런 날 들어간 경우 아무 날보다 성과가 좋았고 승률은 57~67%였습니다. 다만 나스닥 선물이 평소보다 싸게 거래되고 있어(헤지 매도가 많음) 등급을 한 단계 낮춘 B+입니다.',
     'img':f'https://stock.jintar.co.kr/c/{num}.jpg' if num else '','u':f'https://stock.jintar.co.kr/c/{num}/' if num else 'https://stock.jintar.co.kr/'})
issue['jintari']={'cards':JC,'cash':[{'t':x['n'],'kn':x['kn'],'s':x['s']} for x in JL.get('cond',[])],
 'note':'발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다.','u':'https://stock.jintar.co.kr/','asof':'2026-11-18 장 종료 기준 신호'}

# ── v9: 종목별 큰 한 줄 의견 ──
HL={
 'SOXL':'한 주 만에 25% 빠진 3배 상품, 반등 신호는 켜졌지만 흔들림도 3배',
 'NVDA':'실적은 이겼는데 5일째 하락, CEO 공백이 숫자를 누르는 중',
 'SNDK':'3개월 새 반 토막, 20일 저점 749달러(약 100만 원) 지키는지가 먼저',
 'SNXX':'샌디스크 하락을 2배로 맞은 상품, 원금 회복이 가장 어려운 구간',
 'MU':'메모리 조정 한가운데, 650달러(약 86만 원)대 바닥을 시험하는 중',
 'TSLA':'대형 기술주 중 드물게 50·200일선 위, 시장보다 강한 흐름',
 'INTC':'11월에만 18% 하락, 지분 매도·소송이 겹친 무거운 수급',
 'SPCX':'고점 대비 -36%지만 이번 주는 나스닥보다 강세, 12월 보호예수 해제가 변수',
 'PLTR':'200일선은 지키지만 20일선 아래, 단기 힘이 빠진 상태',
 'QQQ':'200일선 3% 아래, 앤트로픽 첫날이 방향을 가를 자리',
 'SOXX':'이틀째 소폭 반등, 아직은 바닥 다지기',
 'UNH':'규정안 하나에 하루 -10%, 평소 3.5배 거래량이 실린 충격',
 'PANW':'취약점 경고와 실적 호조가 겹친 +9.9%, 시간외 반응이 관건',
 'CRWD':'보안주 강세 타고 +8%, 200일선 위로 올라선 흐름',
 'AMD':'엔비디아와 반대로 +5.3%, AI 칩 안에서도 갈린 하루',
 'AVGO':'+3.6%로 20·50일선 회복, 200일선이 다음 고비',
 'WMT':'1달 +8% 방어주, 오늘 밤 실적이 연말 소비를 보여줄 차례',
 'AAPL':'고점 2% 아래, 기술주 약세장 속 피난처 역할',
 'GOOGL':'1달 -17%로 이평선 모두 이탈, 200일선 회복이 먼저',
 'MSFT':'200일선은 지키는 중, 빅테크 중 낙폭이 작은 편',
 'META':'1달 -11%, AI 비용 논쟁에 거래량도 줄어든 약세',
 'AMZN':'+3.8%로 이평선 모두 회복, 기술주 중 가장 강한 하루',
}
def auto_h(q):
    m=q.get('mini') or {}; c=q['c']
    below=sum(1 for k in ('ma20','ma50','ma200') if m.get(k) and c<m[k])
    trend='이평선 모두 아래 약세' if below==3 else '이평선 위 추세 유지' if below==0 else '이평선 사이에서 방향 탐색'
    day=f"어제 {q['ch']:+.2f}%"
    tail=' · 과매도 구간' if q['rsi']<30 else ' · 과열 구간' if q['rsi']>70 else ''
    return f"{day}, 1달 {q['m1']:+}% · {trend}{tail}"
for q in issue['quotes']['list']:
    q['h']=HL.get(q['t']) or auto_h(q)
for c in issue['jintari']['cards']:
    c['h']='빠르게 빠진 반도체는 다시 오르는 일이 많았다 — ⑨ 급락 반등 신호가 켜졌어요'
json.dump(issue, open(f'drafts/{D}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')

"""제2호(2026-11-20 금, 미국 11/19 목 장) 초안 — build_issue1.py 틀을 그대로 돌린 뒤 글·일정·의견만 11/19 장 기준으로 바꾼다.
숫자는 data/*(야후 일봉, 11/19 종가)와 아래 출처의 확인값만 쓴다."""
import json, re

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1333.64"), ("D = '2026-11-19'", "D = '2026-11-20'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-19 16:00 ET 종가'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-20 08:00 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 2, 'weekday': '금'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-19(목) 뉴욕장'"),
       ("for c in JL['cards']:", "for c in [x for x in JL['cards'] if not x.get('quietCard')]:")]
for a, b in REP:
    assert a in src, a
    src = src.replace(a, b)
src = src[:src.rindex('json.dump(')]
ns = {}
exec(compile(src, 'build_issue1.py', 'exec'), ns)
issue, f, summ, Y, FX, TD = ns['issue'], ns['f'], ns['summ'], ns['Y'], ns['FX'], ns['TD']
N, row, CLOSE = ns['N'], ns['row'], ns['CLOSE']
won = lambda usd: (lambda v: f"약 {v/10000:.1f}만 원".replace('.0만', '만') if v < 1e5 else f"약 {round(v/1e4)}만 원")(usd * FX)

# ── 출처 ─────────────────────────────────────────────
AP = 'https://wsvn.com/news/us-world/wall-street-tumbles-to-its-longest-losing-streak-since-2024-as-the-dow-drops-1100-points/'
CBS = 'https://www.cbsnews.com/news/anthropic-ipo-nasdaq-debut-claude-ai/'
YANT = 'https://finance.yahoo.com/markets/stocks/articles/anthropic-set-start-trading-completing-135519162.html'
WMT_AP = 'https://www.washingtontimes.com/news/2026/nov/19/walmart-raises-outlook-year-3rd-time-solid-quarter-fueled-e-commerce/'
WMT_CN = 'https://www.cnbc.com/2026/11/19/walmart-wmt-q3-2026-earnings.html'
AH = 'https://www.investing.com/news/stock-market-news/afterhours-movers-bsp-intu-estc-gap-rost-432SI-5040092'
MLQ = 'https://mlq.ai/news/after-hours-movers-intuit-and-ross-fall-esco-and-gap-rise-keysight-posts-record-results-on-thursday-nov-19/'
STW = 'https://stocktwits.com/news-articles/markets/equity/what-to-expect-markets-this-week-nov-15-2026/cNbEXadR9Qu'
KT = 'https://www.khaleejtimes.com/business/from-spacex-to-anthropic-markets-have-a-new-playbook-for-mega-share-debuts'
FS = 'https://futuresearch.ai/app/p/a/anthropic-first-day-ipo-market-cap'
STT = 'https://stocktwits.com/news-articles/markets/equity/anthropic-ipo-not-the-real-test-market-strategist-says-what-happens-in-subsequent-weeks-matters-more/cNb78txR9Xx'
DU = 'https://www.thedailyupside.com/technology/artificial-intelligence/can-anthropic-buck-the-trend-of-2026-ipos/'
WM = 'https://www.wealthmanagement.com/investing-strategies/advisors-urge-patience-on-anthropic-ipo-shares'
BURRY = 'https://247wallst.com/investing/2026/11/13/amdl-2x-amd-etf-tumbles-18-as-amd-sinks-amid-michael-burrys-bearish-chip-bets/'
FG = 'https://edition.cnn.com/markets/fear-and-greed'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
CBOE = 'https://www.cboe.com/about/hours/us-options/'
FV = 'https://finviz.com/calendar/economic'
NQ09 = 'https://www.newsquawk.com/headlines/us-broker-moves-amd-upgraded-at-oppenheimer-dkng-downgraded-at-numerous-brokerages'
BABY = 'https://babypips.com/news/daily-financial-forex-market-recap-2026-11-18'
PT_BERN = 'https://www.kiplinger.com/news/live/nvidia-earnings-live-updates-and-commentary-november-2026'
FGv = {'v': 18.7, 'w': 40.3, 'm': 19.5}  # CNN 2026-11-19 22:49 UTC

g = lambda t: f(t, 'chg') if t in summ else TD[t][5]

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스',
 'title': '앤트로픽은 첫날 17% 올랐는데, S&P 500은 6일째 하락',
 'img': 'img/2026-11-20-ipo.jpg',
 'points': [
  {'t': '앤트로픽(ANT)은 미국 시간 정오 무렵 첫 거래를 시작해 115달러(약 15만 원) 위까지 올랐다가 97.17달러(약 13만 원), 공모가보다 17.1% 높게 마감했습니다.', 'src': AP},
  {'t': '첫 체결가는 111.50달러(약 14.9만 원)로 공모가 83달러(약 11만 원)보다 34% 높았습니다.', 'src': YANT},
  {'t': f"같은 날 S&P 500은 {f('^GSPC','chg'):+.2f}%로 6일 연속 내렸습니다. 2024년 이후 가장 긴 하락이고, 사상 최고치보다 8.2% 낮습니다.", 'src': AP},
  {'t': '장 초반 1.3% 올랐던 지수가 뒤집혔고, S&P 500 종목의 90% 넘게 떨어졌습니다. 엔비디아는 +4.7%에서 -3.3%로, 마이크론은 +7.8%에서 -2.1%로 돌아섰습니다.', 'src': AP},
  {'t': 'AP는 AI 거품 우려, 데이터센터 투자 대비 수익 의문, 높은 금리, 중간선거 뒤 AI 규제 강화 가능성, 젠슨 황 사임을 하락 이유로 꼽았습니다.', 'src': AP},
 ],
 'risks': [
  {'t': f"CNN 공포·탐욕 지수가 {FGv['v']}로 '극단적 공포'입니다. 1주 전 {FGv['w']}에서 빠르게 내려와, 팔 사람이 한쪽으로 몰렸다는 뜻이기도 합니다.", 'src': FG},
  {'t': '스페이스X·SK하이닉스는 상장 3일째 옵션 거래가 열리며 주가가 뛰었습니다. 앤트로픽도 첫 15거래일 동안 지수 편입을 앞둔 매수가 들어올 수 있다는 분석이 있습니다.', 'src': KT},
 ],
 'why': 'AI 대표 기업의 상장 흥행과 지수 급락이 같은 날 나왔습니다. AI에 대한 기대와 의심이 한꺼번에 가격에 찍힌 하루입니다.',
 'watch': [
  '앤트로픽이 둘째 날 97달러(약 13만 원) 위를 지키는지 — 일부 내부자는 첫날부터 보유 주식 일부를 팔 수 있습니다',
  f"S&P 500이 20일 저점 7,174 근처에서 7일째 하락을 멈추는지",
  '오늘 밤 월간 옵션 만기와 미시간대 소비자심리 확정치',
 ],
 'src': [{'t': 'AP', 'u': AP}, {'t': 'Yahoo Finance', 'u': YANT}, {'t': 'CBS', 'u': CBS}, {'t': 'CNN 공포·탐욕', 'u': FG}, {'t': 'Khaleej Times', 'u': KT}],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': '다우는 1,101포인트 빠졌고, 4대 지수가 모두 2% 넘게 내렸습니다. 장 초반 반등을 모두 내준 전형적인 반전 하락입니다.',
 'src': AP,
}

# ── 참고 지표 ─────────────────────────────────────────
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'close') / (1 + f('^TNX', 'chg') / 100), 2)
issue['indicators'] = [
 {'name': '공포·탐욕 지수', 'v': FGv['v'], 'd': 1, 'label': '극단적 공포', 'src': FG},
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
        x['v'] = N(FGv['v'], FG, '2026-11-19 장 마감'); x['note'] = f"1주 전 {FGv['w']} · 1달 전 {FGv['m']} (CNN, 25 아래는 극단적 공포)"
issue['macro'] = []

# ── 간밤 뉴스 ─────────────────────────────────────────
issue['news'] = [
 {'tag': '상장', 'img': 'img/2026-11-20-ipo.jpg', 'title': '앤트로픽 첫날 +17%, 장중엔 +38%까지',
  'line': '공모가 83달러(약 11만 원)로 상장해 장중 115달러(약 15만 원) 위까지 올랐다가 97.17달러(약 13만 원)에 마감했습니다.',
  'src': [{'t': 'AP', 'u': AP}, {'t': 'Yahoo Finance', 'u': YANT}]},
 {'tag': '시장', 'img': 'img/2026-11-20-spx.jpg', 'title': 'S&P 500 6일 연속 하락, 2024년 이후 최장',
  'line': f"장 초반 1.3% 오르다 뒤집혀 {f('^GSPC','chg'):+.2f}%로 마감했고, S&P 500 종목의 90% 넘게 떨어졌습니다.",
  'src': [{'t': 'AP', 'u': AP}]},
 {'tag': '반도체', 'img': 'img/2026-11-20-chip.jpg', 'title': 'AI 반도체, 장 초반 강세가 하락으로',
  'line': f"마이크론은 +7.8%에서 {g('MU'):+.2f}%로, 엔비디아는 +4.7%에서 {g('NVDA'):+.2f}%로 뒤집혔고 AMD는 {g('AMD'):+.2f}%였습니다.",
  'src': [{'t': 'AP', 'u': AP}, {'t': '야후 파이낸스', 'u': Y('AMD')}]},
 {'tag': '보안', 'img': 'img/2026-11-20-cyber.jpg', 'title': '팔로알토 +6.4%, 실적 호조에 대형 인수',
  'line': '예상을 넘은 실적과 함께 어플라이드 컴퓨트를 45억 달러(약 6조 원) 규모 주식 교환으로 사기로 했습니다.',
  'src': [{'t': 'AP', 'u': AP}]},
 {'tag': '실적', 'img': 'img/2026-11-20-wmt.jpg', 'title': '월마트, 연간 전망 세 번째 상향에도 -1%',
  'line': '매출 1,888억 달러(약 252조 원), 주당순이익 0.65달러(약 870원)로 예상을 넘었지만 주가는 1.04% 내렸습니다.',
  'src': [{'t': 'AP', 'u': WMT_AP}, {'t': 'CNBC', 'u': WMT_CN}]},
 {'tag': '시간외', 'img': 'img/2026-11-20-intu.jpg', 'title': '인튜이트 시간외 -13%, 로스스토어도 약세',
  'line': '인튜이트는 1분기는 예상을 넘었지만 연간 전망이 낮았고, 메일침프를 벤딩스푼스에 36.8억 달러(약 4.9조 원)에 팔기로 했습니다.',
  'src': [{'t': 'Investing.com', 'u': AH}, {'t': 'MLQ', 'u': MLQ}]},
 {'tag': '원자재', 'img': 'img/2026-11-20-gold.jpg', 'title': '금 -3%, 변동성 지수 VIX는 28로 급등',
  'line': f"금은 온스당 3,627.9달러(약 484만 원)로 {f('GC=F','chg'):.2f}% 내렸고, VIX는 {f('^VIX','chg'):.1f}% 뛴 {f('^VIX','close'):.2f}입니다.",
  'src': [{'t': '야후 파이낸스', 'u': Y('GC%3DF')}, {'t': '야후 파이낸스', 'u': Y('%5EVIX')}]},
]
for n in issue['news']:
    n['body'] = n['line']

issue['movers'] = [
 {'ticker': t, 'name': nm, 'close': N(TD[t][4], Y(t), CLOSE), 'chg_pct': N(TD[t][5], Y(t), CLOSE), 'won': won(TD[t][4]), 'why': why}
 for t, nm, why in [('NVDA', '엔비디아', '장 초반 +4.7%를 반납하고 6일 연속 하락'), ('AMD', 'AMD', 'AI 반도체 매도에 하루 -7.7%'),
                    ('PANW', '팔로알토', '실적 호조·45억 달러(약 6조 원) 인수 발표'), ('UNH', '유나이티드헬스', '이틀째 급락, 1달 -21%')]]

# ── 오늘 밤 일정 (한국 시간, 11/20 금) ─────────────────
issue['schedule'] = [
 {'kst': '장 전', 'type': '실적', 'name': "BJ's 홀세일 3분기 실적", 'star': 2, 'why': '창고형 할인점 실적. 월마트에 이어 미국 소비 체력을 봅니다.', 'src': STW},
 {'kst': '23:30', 'type': '개장', 'name': '뉴욕 정규장 개장 · 앤트로픽 둘째 날', 'star': 5, 'why': '첫날 종가 97.17달러(약 13만 원)를 지키는지. 일부 내부자는 상장 첫날부터 보유분 일부를 팔 수 있어 매물이 변수입니다.', 'src': FS},
 {'kst': '24:00', 'type': '지표', 'name': '11월 미시간대 소비자심리 확정치', 'star': 4, 'why': '소비자가 보는 1년·5년 뒤 물가 전망이 12월 금리 결정의 단서가 됩니다.', 'src': STW},
 {'kst': '밤', 'type': '연준', 'name': '월러 · 쿡 연준 이사 연설', 'star': 4, 'why': '월러 이사는 이번 주 12월 0.5%p 인상 가능성까지 언급했습니다. 발언 수위에 따라 금리·기술주가 흔들릴 수 있습니다.', 'src': STW},
 {'kst': '06:00', 'type': '만기', 'name': '11월 월간 옵션 만기 (셋째 금요일)', 'star': 3, 'why': '큰 옵션 물량이 정리되는 날이라 장 막판 변동이 커질 수 있습니다.', 'src': CBOE},
 {'kst': '다음 주', 'type': '휴장', 'name': '11/26(목) 추수감사절 휴장 · 11/27(금) 조기 폐장', 'star': 2, 'why': '거래일이 짧은 주라 거래량이 줄고 움직임이 커질 수 있습니다.', 'src': NYSE},
]
issue['schedule_note'] = '정규장은 한국 시간 23:30~06:00입니다. 연설 시각은 발표 기관 일정에 따라 바뀔 수 있습니다.'
issue['calendar'] = {
 'today': '2026-11-20',
 'days': [
  {'d': '2026-11-16', 'ev': [{'k': '연준', 't': '워시 의장 연설'}]},
  {'d': '2026-11-17', 'ev': [{'k': '실적', 't': '엔비디아', 'when': '장 후'}]},
  {'d': '2026-11-18', 'ev': [{'k': '연준', 't': 'FOMC 의사록'}, {'k': '실적', 't': '팔로알토', 'when': '장 후'}]},
  {'d': '2026-11-19', 'ev': [{'k': '상장', 't': '앤트로픽 +17%', 'hl': True}, {'k': '실적', 't': '월마트', 'when': '장 전'}, {'k': '실적', 't': '인튜이트·로스', 'when': '장 후'}]},
  {'d': '2026-11-20', 'ev': [{'k': '지표', 't': '미시간대 소비자심리', 'hl': True}, {'k': '연준', 't': '월러·쿡 연설'}, {'k': '만기', 't': '월간 옵션 만기'}]},
  {'d': '2026-11-23', 'ev': [{'k': '상장', 't': '앤트로픽 3일째(옵션 상장 예상)'}]}, {'d': '2026-11-24', 'ev': []}, {'d': '2026-11-25', 'ev': []},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장', 'hl': True}]},
  {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}]},
 ],
 'src': [{'t': 'Stocktwits 주간 일정', 'u': STW}, {'t': 'NYSE 휴장일', 'u': NYSE}],
}
issue['earnings'] = [
 {'date': '11/19(목)', 'time': '장 전', 'company': '월마트', 'ticker': 'WMT', 'done': True},
 {'date': '11/19(목)', 'time': '장 마감 후', 'company': '인튜이트', 'ticker': 'INTU', 'done': True},
 {'date': '11/19(목)', 'time': '장 마감 후', 'company': '로스스토어', 'ticker': 'ROST', 'done': True},
 {'date': '11/20(금)', 'time': '장 전', 'company': "BJ's 홀세일", 'ticker': 'BJ', 'done': False},
]

# ── 차트 분석 (어제 → 최근 대비 → 앞으로) ───────────────
CH = {
 '^IXIC': ('장 초반 강세를 모두 내주고 하루 저점에서 마감', [
   ('어제', f"나스닥은 {f('^IXIC','chg'):+.2f}%였습니다. 앤트로픽 상장으로 24,940까지 올랐다가 엔비디아({g('NVDA'):+.2f}%)·AMD({g('AMD'):+.2f}%)가 밀리며 하루 저점 23,871 바로 위 23,879에 끝났습니다."),
   ('최근 대비', f"1주 {f('^IXIC','w1'):+.1f}%, 1달 {f('^IXIC','m1'):+.1f}%이고 고점 대비 -13.9%로 조정 구간입니다. QQQ 거래량이 20일 평균의 1.36배라 하락에 매도가 실렸습니다."),
   ('앞으로', '종가가 20일 저점과 거의 같은 자리라, 이 선을 지키는지가 먼저입니다. 반등이 나오면 첫 기준은 200일선 25,157(+5.4%)이고, 깨지면 하락 추세가 길어질 수 있습니다.')]),
 '^GSPC': ('6일 연속 하락, 고가에서 저가까지 3% 넘게 밀린 하루', [
   ('어제', f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 6일째 내렸습니다. 장 초반 +1.3%에서 뒤집혔고, 종목의 90% 넘게 떨어졌습니다."),
   ('최근 대비', f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%입니다. 이틀 전 바로 아래였던 200일선(7,348)과의 거리가 -2.3%로 벌어졌고, SPY 거래량은 평균의 1.48배였습니다."),
   ('앞으로', '고점 대비 -8.5%라 흔히 조정이라 부르는 -10%(약 7,060)까지 1.6% 남았습니다. 200일선을 되찾으면 하락이 멈췄다는 신호, -10% 선 아래는 조정이 깊어진다는 신호로 볼 수 있습니다.')]),
 'SOXX': ('이틀 반등 뒤 다시 -2.75%, 장중 고점에서 7% 밀린 하루', [
   ('어제', f"반도체 ETF는 {f('SOXX','chg'):+.2f}%였습니다. 장중 148.59까지 올랐다가 AMD({g('AMD'):+.2f}%)·엔비디아({g('NVDA'):+.2f}%)·마이크론({g('MU'):+.2f}%)이 함께 밀렸습니다."),
   ('최근 대비', f"1주 {f('SOXX','w1'):+.1f}%, 1달 {f('SOXX','m1'):+.1f}%, 고점 대비 -36.9%로 세 지수 중 가장 약합니다. 거래량은 평균 수준(1.00배)이었습니다."),
   ('앞으로', '아래로는 20일 저점 130.75(-5.2%), 위로는 20일선 151.82(+10%)가 기준입니다. 저점을 지키며 거래량이 붙는 반등이 나오는지가 먼저입니다.')]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = '세 지수 모두 **20·50·200일선 아래**에서 **하루 저점 부근**에 마감했습니다. S&P 500은 **200일선과 -2.3%** 벌어졌습니다.'

# ── 트리맵 해설 ───────────────────────────────────────
tmi = issue['treemap']['items']; ups = sum(1 for i in tmi if i['ch'] > 0)
secw = {}
for i in tmi:
    a = secw.setdefault(i['s'], [0, 0]); a[0] += i['w']; a[1] += i['w'] * i['ch']
sw = {k: round(b / a, 1) for k, (a, b) in secw.items()}
gt = lambda t: next(i for i in tmi if i['t'] == t)['ch']
upn = sorted([i for i in tmi if i['ch'] > 0], key=lambda i: -i['ch'])
issue['treemap']['asof'] = CLOSE
issue['treemap']['comment'] = {
 'h': f"100개 중 {ups}개만 상승 — 보안주 몇 개 빼고 전부 밀린 날",
 't': (f"어제는 상위 100개 중 {ups}개만 올랐습니다. 오른 곳은 팔로알토(+{gt('PANW')}%)·크라우드스트라이크(+{gt('CRWD')}%)·인텔(+{gt('INTC')}%)·퀄컴(+{gt('QCOM')}%) 정도였습니다. "
       f"가장 약한 곳은 AMD({gt('AMD')}%)·유나이티드헬스({gt('UNH')}%)·마벨({gt('MRVL')}%)·우버({gt('UBER')}%)였고, 아마존({gt('AMZN')}%)·알파벳({gt('GOOGL')}%)·메타({gt('META')}%) 같은 큰 종목도 3% 넘게 빠졌습니다. "
       f"업종별로는 커뮤니케이션 {sw['커뮤니케이션']}%, 정보기술 {sw['정보기술']}%가 가장 크게 밀렸고, 에너지({sw['에너지']}%)·필수소비재({sw['필수소비재']}%)는 상대적으로 덜 빠졌습니다."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'AP', 'u': AP}, {'t': '야후 파이낸스', 'u': 'https://finance.yahoo.com'}]}

# ── 롱/숏 한마디 ──────────────────────────────────────
issue['street']['camps'] = {'long': [
 {'who': '모닝스타', 'role': '리서치 회사', 'sil': 'firm', 'say': '앤트로픽 기본 시나리오 가치는 1.7조 달러(약 2,270조 원)예요. 공모가는 오히려 싼 편이에요.', 'src': DU},
 {'who': '카르스텐 헤세', 'role': '베렌버그 지수 담당', 'sil': 'glasses', 'say': '첫 15거래일은 지수 편입 때문에 사야 하는 돈이 주가를 정해요.', 'src': KT},
 {'who': '오펜하이머', 'role': '증권사 (11/9)', 'sil': 'suit_g', 'say': 'AMD의 서버·AI 칩 성공은 이론의 여지가 없어요. 목표 600달러(약 80만 원).', 'src': NQ09},
 {'who': '마르타 노턴', 'role': '엠파워 투자책임자', 'sil': 'woman', 'say': '첫날보다 그다음 몇 주가 진짜 시험이에요.', 'src': STT},
], 'short': [
 {'who': '마이클 버리', 'role': '빅쇼트 투자자 (11/12)', 'sil': 'hood', 'say': '나스닥100 하락에 거는 풋옵션을 두 배로 늘렸어요.', 'src': BURRY},
 {'who': '라이언 디트릭', 'role': '카슨 그룹', 'sil': 'suit', 'say': '큰 IPO는 첫날 올라도 1년 안에 약해진 경우가 많았어요.', 'src': STT},
 {'who': '월러', 'role': '연준 이사 (11/18)', 'sil': 'suit', 'say': '물가가 거꾸로 가요. 12월엔 0.5%p 올려야 할 수도 있어요.', 'src': BABY},
 {'who': '번스타인', 'role': '증권사 (지난주)', 'sil': 'firm', 'say': '엔비디아 목표주가를 400달러에서 200달러(약 27만 원)로 반 토막 냈어요.', 'src': PT_BERN},
]}
issue['street']['title'] = '최근 2주 눈에 띈 증권사 의견'

# ── 내 종목 분석 ──────────────────────────────────────
KO = ns['KO']
WHY2 = {'NVDA': '장 초반 +4.7%를 반납하고 6일 연속 하락', 'AMD': 'AI 반도체 매도에 -7.72%', 'MU': '장 초반 +7.8%에서 -2.1%로 반전',
        'PANW': '실적 호조·45억 달러(약 6조 원) 인수 발표에 +6.4%', 'WMT': '실적·전망 상향에도 -1%', 'SOXL': '반도체 약세 3배 반영 -8%'}
TN2 = {
 'SOXL': {'y': [(f"반도체 ETF {f('SOXX','chg'):+.2f}%를 3배로 받아 하루 -8.04%, 1주 -30.9%", Y('SOXL')), ('수리수리진타리 ⑨ 반도체 급락 반등 신호 진행 중(B+)', 'https://stock.jintar.co.kr/c/9/')],
          't': [('오늘 밤 월간 옵션 만기·월러 연설로 변동성 주의', STW)]},
 'NVDA': {'y': [('장 초반 +4.7%를 모두 반납하고 -3.3%, 6일 연속 하락', AP)], 't': []},
 'AMD': {'y': [('AI 반도체 매도에 -7.72%, 1주 -16.4%', Y('AMD'))], 't': []},
 'MU': {'y': [('장 초반 +7.8%에서 -2.1%로 반전', AP)], 't': []},
 'SNDK': {'y': [('장중 846.76달러(약 113만 원)까지 올랐다가 755.16달러(약 101만 원)로 -2.69%', Y('SNDK'))], 't': []},
 'PANW': {'y': [('실적 예상 상회 + 어플라이드 컴퓨트 45억 달러(약 6조 원) 주식 교환 인수', AP)], 't': []},
 'WMT': {'y': [('매출 1,888억 달러(약 252조 원)로 예상 상회, 연간 전망 세 번째 상향', WMT_AP)], 't': []},
}
AI2 = {
 'SOXL': f"반도체 지수를 하루 3배로 따라가는 상품이라 어제 -8.04%, 1주 -30.9%, 고점 대비 -85%까지 밀렸습니다. 모든 이동평균선 아래라 추세는 약하고, 반도체 ETF가 20일 저점(130.75)까지 5% 남아 있어 그 자리를 시험할 수 있습니다. 3배 상품은 같은 폭으로 오르내려도 원금이 깎이는 구조라, 수리수리진타리 ⑨ 카드처럼 손절선을 미리 정해 두는 방식이 안전합니다.",
 'NVDA': '장 초반 +4.7%까지 올랐다가 -3.3%로 끝나 6일 연속 내렸습니다. RSI 20으로 깊은 과매도이고 1달 -34%입니다. 실적은 좋았지만 CEO 공백과 AI 투자 회의론이 주가를 누르고 있어, 과매도 반등이 나와도 후임 CEO 같은 재료가 없으면 힘이 약할 수 있습니다.',
 'AMD': '어제 -7.72%로 AI 반도체 중 가장 크게 밀렸고 20·50일선을 모두 내줬습니다. 200일선(428.63달러, 약 57만 원)은 아직 아래에 있어 중기 추세는 남아 있지만, 1주 -16%로 변동성이 매우 큰 구간입니다.',
 'SNDK': '장중 846.76달러(약 113만 원)까지 반등했다가 755.16달러(약 101만 원)로 밀려 위꼬리가 길게 남았습니다. 20일 저점 749달러(약 100만 원) 바로 위라 이 자리를 지키는지가 먼저이고, 3개월 -53%로 낸드 가격 지표가 바닥을 보여줘야 추세 전환을 말할 수 있습니다.',
 'MU': '장 초반 +7.8%까지 올랐다가 -2.1%로 뒤집혔습니다. 20일 저점 650달러(약 87만 원)까지 약 6% 남았고, 이동평균선이 모두 위에 있어 반등 때마다 저항이 겹겹입니다.',
 'PANW': '실적 호조와 45억 달러(약 6조 원) 인수 발표로 +6.42%, 거래량은 평균의 2.8배였습니다. 1주 +12%로 시장과 반대로 움직이는 보안주 대표이고, 200일선 위를 지키고 있습니다.',
 'WMT': '실적과 전망 상향에도 -1.04%였지만 50·200일선 위를 지키고 1달 +7%로 방어주 역할을 하고 있습니다.',
}
HL2 = {
 'SOXL': '반도체 -2.75%를 3배로 맞은 -8%, 1주 만에 31% 빠진 구간',
 'NVDA': '장 초반 +4.7%를 다 내주고 6일 연속 하락, RSI 20 깊은 과매도',
 'AMD': 'AI 반도체 중 가장 큰 -7.7%, 1주 -16%',
 'SNDK': '장중 +9%에서 -2.7%로, 20일 저점 749달러(약 100만 원) 코앞',
 'SNXX': '샌디스크 하락을 2배로 맞아 1주 -37%, 원금 회복이 가장 어려운 구간',
 'MU': '장 초반 +7.8%에서 -2.1%로 뒤집힌 하루',
 'PANW': '실적·인수 발표로 +6.4%, 하락장 속 거래량 2.8배 상승',
 'CRWD': '보안주 강세 이어 +2.7%, 200일선 위',
 'INTC': '하락장에서 +1.9%, 그래도 1달 -40%',
 'WMT': '전망 세 번째 상향에도 -1%, 방어주 흐름은 유지',
 'UNH': '이틀째 급락 -5.6%, 평소 3.5배 거래량',
 'QQQ': '20일 저점에서 마감, 200일선과 -5.6% 벌어져',
 'SOXX': '이틀 반등 뒤 다시 -2.75%, 고점 대비 -37%',
 'SPCX': '-3.5%로 나스닥보다 약했던 하루, 12월 보호예수 해제가 변수',
 'TSLA': '-2.4%로 50·200일선 아래로 내려온 하루',
 'AMZN': '-3.9%로 하루 만에 상승분 반납',
 'GOOGL': '-3.5%, 1달 -19%로 이평선 모두 아래',
 'META': '-3.3%, 1달 -15%',
 'MSFT': '-2.0%, 200일선은 아직 지키는 중',
 'AAPL': '-0.9%로 빅테크 중 가장 덜 빠진 하루',
}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY2.get(t, '')
    n = TN2.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = AI2.get(t) or ns['auto_ai'](q)
    q['h'] = HL2.get(t) or ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE

# ── 수리수리진타리 (stock.jintar.co.kr, 11/20 01:40 KST 슬롯 · 활성 신호) ──
JL = json.load(open('data/jintari_latest.json', encoding='utf-8'))
usd = lambda s: float(s.replace('$', '').replace(',', ''))
c = next(x for x in JL['cards'] if x['n'] == 'SOXL')
o, stop = 54.04, usd(c['stop'])
cl = next(q['c'] for q in issue['quotes']['list'] if q['t'] == 'SOXL')
issue['jintari'] = {'cards': [{
  'g': c['g'], 't': c['n'], 'kn': c['kn'], 's': c['s'], 'ln': c.get('ln', []),
  'rows': [('신호 기준가', f"{usd(c['pxSig'])}달러({won(usd(c['pxSig']))}) · 11/18 종가"),
           ('어제 시가 → 종가', f"{o}달러({won(o)}) → {cl}달러({won(cl)}), 시가 대비 {(cl/o-1)*100:.1f}%"),
           ('익절 · 손절', f"+40%({usd(c['tgt'])}달러, {won(usd(c['tgt']))}) · −20%({stop}달러, {won(stop)})"),
           ('손절선까지', f"종가 기준 {(stop/cl-1)*100:.1f}% 남음 · 최대 15거래일 보유")],
  'h': f"신호 첫날 시가 대비 {(cl/o-1)*100:.0f}% — 손절선까지 {abs((stop/cl-1)*100):.1f}% 남은 ⑨ 카드",
  'why': f"11/18 반도체 ETF가 20일 최고 종가보다 18.5% 낮아져 ⑨ 반도체 급락 반등 신호가 켜졌고, 어제 시가 {o}달러({won(o)})에 들어갔다면 하루 만에 {(cl/o-1)*100:.1f}%입니다. 규칙대로라면 {stop}달러({won(stop)}) 손절 주문이 걸려 있는 상태이고, 그 위에서는 최대 15거래일까지 기다립니다.",
  'img': 'https://stock.jintar.co.kr/c/9.jpg', 'u': 'https://stock.jintar.co.kr/c/9/'}],
 'cash': [],
 'note': '발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다. 장중 단타용 관찰 카드(⑦)는 당일 정리라 싣지 않았습니다.',
 'u': 'https://stock.jintar.co.kr/', 'asof': '2026-11-19 장 종료 기준 · 신호는 11/18 종가에 켜짐'}

issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 야후 파이낸스 일봉(11/19 종가) 기준이며, 증권사·전문가 의견은 보도된 내용을 옮긴 것입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

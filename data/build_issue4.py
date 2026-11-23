"""제4호(2026-11-24 화, 미국 11/23 월 장) — build_issue3.py 와 같이 build_issue1.py 틀을 돌린 뒤 글·일정·의견을 11/23 장 기준으로 바꾼다.
숫자는 data/*(CNBC 일봉, 11/23 종가)와 아래 출처의 확인값만 쓴다. 샌디스크는 8:1 액면분할 반영가."""
import json

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1341.86"), ("D = '2026-11-19'", "D = '2026-11-24'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-23 16:00 ET 종가'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-24 06:50 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 4, 'weekday': '화'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-23(월) 뉴욕장'"),
       ("'ma200':1284.66", "'ma200':160.79"),  # 샌디스크 8:1 분할 반영(tickers_mini 값)
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
YLIVE = 'https://finance.yahoo.com/markets/live/stock-market-today-monday-november-23-dow-sp-500-nasdaq-surge-after-nvidia-reinstates-jensen-huang-182039397.html'
YLIVE2 = 'https://finance.yahoo.com/markets/live/stock-market-today-monday-november-23-dow-sp-500-nasdaq-nvidia-reinstates-jensen-huang-141511975.html'
NVLIVE = 'https://finance.yahoo.com/markets/stocks/live/nvidia-live-updates-jensen-huang-reinstated-as-ceo-trump-says-he-convinced-board-165423793.html'
NV8K = 'https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000090/nov23pressrelease.htm'
BEIN = 'https://beinsure.com/news/us-stock-market-today-nasdaq-composite-surges-as-nvidia-jumps/'
INVC = 'https://in.investing.com/news/stock-market-news/united-states-shares-higher-at-close-of-trade-dow-jones-industrial-average-up-301-5721972'
MLQ954 = 'https://mlq.ai/news/nvidia-adds-a-record-954-billion-in-market-value-in-one-day-as-jensen-huang-returns/'
ST_NV = 'https://finance.yahoo.com/markets/stocks/articles/nvidia-reinstates-jensen-huang-ceo-140828635.html'
ST_APPL = 'https://stocktwits.com/news-articles/markets/equity/nvidia-is-now-second-to-apple-in-the-world-s-most-valued-companies-on-jensen-huang-optimism/cNbpeYcR9j0'
TNW = 'https://thenextweb.com/news/jensen-huang-return-reactions-musk-altman-ackman-burry'
DECR = 'https://decrypt.co/383820/jensen-huang-returns-nvidia-memes-gpu-jesus'
TSTR = 'https://techstrong.ai/articles/jensen-huangs-return-as-nvidia-ceo-sparks-relief-on-wall-street-and-in-silicon-valley-but-outrage-over-governance/'
BARR = 'https://barrettmedia.com/2026/11/23/cnbc-fox-business-nvidia-jensen-huang/'
BZ_CRM = 'https://www.benzinga.com/trading-ideas/movers/26/11/63556007/jim-cramer-anthony-pompliano-say-nvidia-board-has-to-resign-disloyalty-has-to-have-repercussions'
FOXB = 'https://www.foxbusiness.com/markets/what-jensen-huangs-return-means-nvidia-wall-street'
FORTG = 'https://fortune.com/2026/11/23/corporate-governance-experts-divided-nvidia-decision-rehire-jensen-huang/'
NEU = 'https://news.northeastern.edu/2026/11/23/nvidia-reinstates-jensen-huang-ceo/'
SENATE = 'https://stocktwits.com/news-articles/markets/equity/jensen-huang-s-nvidia-comeback-to-be-followed-by-public-senate-showdown-on-chip-exports-next-week/cNbpaJfR9jZ'
BBG_TR = 'https://www.bloomberg.com/news/articles/2026-11-23/huang-s-return-followed-unprecedented-intervention-by-trump'
SWISS = 'https://www.swissinfo.ch/eng/stocks-rally-as-nvidia-brings-back-huang-as-ceo:-markets-wrap/92421262'
ST_DOW = 'https://stocktwits.com/news-articles/markets/equity/dow-jumps-over-1-300-points-nasdaq-surges-nearly-7-as-jensen-huang-s-return-lifts-market-sentiment/cNbpPZhR9ja'
YUK = 'https://uk.finance.yahoo.com/news/ai-stocks-roar-back-brutal-145142041.html'
TIPB = 'https://www.tipranks.com/news/is-huangs-nvidia-return-the-market-bottom-heres-what-wall-street-thinks'
LPB = 'https://leprivatebanker.com/2026/11/23/wall-street-surges-as-huangs-nvidia-return-reverses-part-of-last-weeks-rout-with-the-nasdaq-100-up-as-much-as-7-9/'
BERN = 'https://www.tipranks.com/news/the-fly/nvidia-upgraded-to-outperform-at-bernstein-after-huangs-return-thefly-news'
CANT = 'https://www.benzinga.com/trading-ideas/movers/26/11/63549950/quick-spark-all-is-right-in-the-world-again-cantor-says-about-jensens-return-to-nvidia'
# 크라우드스트라이크·지스케일러
ZS_Y = 'https://finance.yahoo.com/markets/stocks/articles/crowdstrike-acquire-zscaler-43-9b-114133750.html'
ZS_TC = 'https://techcrunch.com/2026/11/23/crowdstrike-to-acquire-zscaler-for-44-billion/'
ZS_FOOL = 'https://www.fool.com/investing/2026/11/23/zscaler-stock-surged-on-crowdstrike-s-usd43-9-billion-buyout-here-s-how-much-shareholders-will-actually-get/'
ZS_TS = 'https://www.thestreet.com/investing/crowdstrike-record-quarter-zscaler-deal-crwd-zs'
ZS_GF = 'https://www.tradingview.com/news/gurufocus:df05460e3094b:0-crowdstrike-stocks-fall-9-67-on-43-9-billion-all-stock-deal-for-zscaler/'
ZS_JPM = 'https://stocktwits.com/news-articles/markets/equity/crowd-strike-s-zscaler-acquisition-could-broaden-security-platform-says-jp-morgan-analysts-weigh-opportunities-and-risks/cNbpTQZR9jT'
ZS_BTIG = 'https://www.tradingview.com/news/seekingalpha:92ba0c8b3094b:0-crowdstrike-buying-zscaler-has-strategic-positives-but-execution-risk-is-real-btig/'
ZS_RFL = 'https://www.investing.com/news/stock-market-news/crowdstrikes-zscaler-deal-sets-up-palo-alto-rivalry-rf-lafferty-analyst-says-5046242'
ZS_JEF = 'https://finance.yahoo.com/technology/articles/crowdstrike-zscaler-merger-could-cybersecurity-045948646.html'
ZS_MB = 'https://marketbeat.com/articles/crowdstrikes-44b-zscaler-bet-why-wall-street-sold-the-news/?amp='
ZS_FXL = 'https://www.fxleaders.com/news/2026/11/23/crwd-stock-risks-200-breakdown-as-zscaler-surges-following-crowdstrike-acquisition-announcement/'
ZS_TDC = 'https://www.tipranks.com/news/the-fly/td-says-crowdstrike-should-accelerate-penetration-of-enterprise-with-zscaler-thefly-news'
CRWD_FBN = 'https://www.investing.com/news/analyst-ratings/crowdstrike-stock-price-target-raised-to-235-by-fbn-securities-93CH-5046305'
ZS_FREE = 'https://www.investing.com/news/analyst-ratings/freedom-broker-cuts-zscaler-stock-price-target-to-260-on-acquisition-93CH-5046193'
CRWD_JEFR = 'https://www.investing.com/news/analyst-ratings/jefferies-reiterates-buy-on-crowdstrike-stock-after-zscaler-deal-93CH-5045982'
# 그 밖의 뉴스
MU_TR = 'https://www.tipranks.com/news/micron-stock-soars-over-18-as-jensen-huangs-return-clears-overhang-on-sold-out-ai-memory-demand'
SNDK_F = 'https://www.fool.com/investing/2026/11/23/why-nvidia-rehiring-jensen-huang-is-making-sandisk-stock-skyrocket-today/'
STX_GF = 'https://www.gurufocus.com/news/9215604/seagate-technology-stx-shares-surge-14-amid-sector-rally-on-november-23-2026'
ARM_W = 'https://247wallst.com/investing/2026/11/23/arm-ceo-will-stay-through-2033-shares-rise-16-should-investors-look-for-arm-stock-to-double-from-here/'
TSM_GF = 'https://www.gurufocus.com/news/9215299/taiwan-semiconductor-stocks-jump-1384-as-nvidia-ceo-return-revives-ai-foundry-bets'
INTC_GF = 'https://www.gurufocus.com/news/9215603/intel-intc-surges-1336-amid-tech-rally-and-hedge-fund-buying'
ORCL_GF = 'https://www.gurufocus.com/news/9215303/oracle-stocks-jump-1202-as-funding-pledge-and-nvidia-reversal-ease-ai-debt-fears'
TSLA_GF = 'https://www.gurufocus.com/news/9215414/tesla-stocks-surge-1367-as-spacex-merger-committees-and-cybercab-sales-draw-buyers'
PLTR_GF = 'https://www.gurufocus.com/news/9215469/why-is-palantir-pltr-stock-up-today-ai-rally-follows-nvidia-ceo-return'
QNT_W = 'https://247wallst.com/investing/2026/11/23/rigetti-surges-17-as-jensen-huangs-return-to-nvidia-lifts-quantum-stocks-d-wave-rallies-15-ionq-jumps-14/'
SPACE_W = 'https://247wallst.com/investing/2026/11/23/rocket-lab-rallies-11-after-its-worst-week-ever-as-cfo-eyes-higher-electron-prices-ast-spacemobile-jumps-14-spacex-surges-9/'
MSTR_CT = 'https://www.cryptotimes.io/2026/11/24/strategy-mstr-price-jumps-11-as-bitcoin-recovers-firm-adds-457-btc/'
BTC_N = 'https://news.bitcoin.com/market-updates/bitcoin-plunges-below-61k-hours-nvidia-ceo-return-rally/'
DXY_CD = 'https://www.coindesk.com/tech/2026/11/23/live-news-wall-street-rebounds-as-dollar-index-hits-highest-since-march-2025'
ZM_8K = 'https://www.sec.gov/Archives/edgar/data/0001585521/000158552126000170/zm-20261031ex991.htm'
ZM_INV = 'https://www.investing.com/news/stock-market-news/zoom-shares-fall-despite-earnings-beat-and-dividend-initiation-5046411'
HPE_SA = 'https://seekingalpha.com/news/4675761-hpe-falls-even-as-q4-results-guidance-top-estimates-by-wide-margin'
PMI_T = 'https://www.tmgm.com/en/analysis/market-news/article/us-sp-manufacturing-pmi-retreats-to-545-services-pmi-declines-to-547-202611231502'
PMI_IL = 'https://investinglive.com/news/s-p-global-us-services-november-flash-pmi-54-7-vs-55-7-expected/'
WIL = 'https://investinglive.com/central-banks/williams-keeps-december-fed-hike-in-play-as-inflation-seen-above-2-until-2028/'
FW96 = 'https://www.kucoin.com/news/flash/us-treasury-yields-rise-on-monday-10-year-hits-4-959'
ANT_W = 'https://247wallst.com/investing/2026/11/23/anthropic-fizzles-while-the-market-sizzles-is-ant-stock-headed-for-75-or-even-50/'
STL = 'https://www.stocktitan.net/articles/stock-market-today-live-november-23-2026'
DELL_W = 'https://247wallst.com/investing/2026/11/20/dell-stock-plunges-10-in-the-ai-selloff-and-heads-for-its-worst-month-since-its-2018-return-to-the-stock-market-earnings-are-tuesday/'
WK = 'https://www.infinituswealth.com/post/stock-market-this-week-thanksgiving-pce-dell'
HGT = 'https://www.heygotrade.com/en/news/weekly-economic-outlook-2026-11-23/'
NQE = 'https://www.newsquawk.com/headlines/newsquawk-daily-us-earnings-estimates---24th-november-2026-mdt-adi-dell'
STE = 'https://www.stocktitan.net/articles/earnings-calendar-week-of-november-23-2026'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
JL_U = 'https://stock.jintar.co.kr/'

q_ = {q['t']: q for q in issue['quotes']['list']}
g = lambda t: f(t, 'chg') if t in summ else (TD[t][5] if t in TD else q_[t]['ch'])
qc = lambda t: q_[t]['ch']
cap954 = 9540e8 * FX / 1e12  # 조 원
cap439 = 439e8 * FX / 1e12

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스',
 'title': "젠슨 황 CEO 복귀에 엔비디아 +31%, 나스닥 +6.5% '2025년 4월 이후 최고의 하루'",
 'img': 'img/2026-11-24-top.jpg',
 'points': [
  {'t': '엔비디아 이사회가 11/12 물러났던 젠슨 황을 사장·CEO·이사로 곧바로 복귀시켰습니다. 이사회는 미국 정부 고위층의 의견을 들었고, 복귀가 국가안보 위험이 아니라고 판단했다고 밝혔습니다.', 'src': NV8K},
  {'t': f"엔비디아는 {g('NVDA'):+.2f}%, 165.05달러({won(165.05)})로 마감했습니다. 2003년 5월 이후 가장 큰 하루 상승입니다.", 'src': INVC},
  {'t': f"하루 새 시가총액이 약 9,540억 달러(약 {cap954:,.0f}조 원) 늘었다는 집계가 나왔습니다. 시가총액 순위는 애플 다음 2위로 돌아왔습니다.", 'src': MLQ954},
  {'t': f"나스닥은 {f('^IXIC','chg'):+.2f}%, S&P 500은 {f('^GSPC','chg'):+.2f}%, 다우는 {f('^DJI','chg'):+.2f}%로 2025년 4월 이후 가장 좋은 하루였습니다. S&P 500의 7일 연속 하락도 끝났습니다.", 'src': YLIVE},
  {'t': "트럼프 대통령은 CNBC에 '내가 (이사회를) 설득했다'고 말했고, 트루스소셜에 올바른 결정이라고 썼습니다.", 'src': NVLIVE},
 ],
 'risks': [
  {'t': '황 CEO가 외국 정보기관의 표적이 됐다는 의혹에 대한 회사의 독립 조사는 계속됩니다. 지난주 보도된 SEC 회계 조사 건은 새 소식이 확인되지 않았습니다.', 'src': BEIN},
  {'t': "노무라의 찰리 맥엘리곳은 이번 반등을 '기계적 반등'이라며 아무것도 보장하지 않는다고 했습니다. 엔비디아는 아직 52주 최고가보다 32% 낮습니다.", 'src': YLIVE},
 ],
 'why': '지난주 시장을 끌어내린 가장 큰 불확실성, 엔비디아의 리더십 공백이 하루 만에 풀렸습니다. 다만 회계·안보 의혹과 금리 인상 걱정은 그대로라 반등이 바닥인지는 이번 주 숫자가 가립니다.',
 'watch': [
  '회사 독립 조사 결과와 다음 주 상원 반도체 수출 공개 청문회',
  f"엔비디아가 20일선 178.91달러({won(178.91)})를 되찾는지, S&P 500이 200일선 7,350을 회복하는지",
  '수요일 밤 10월 PCE 물가(근원 예상 전년 대비 3.2%)와 오늘 밤 델 실적',
 ],
 'src': [{'t': 'NVIDIA 8-K', 'u': NV8K}, {'t': '야후 파이낸스', 'u': YLIVE}, {'t': 'Investing.com 마감', 'u': INVC}, {'t': 'Beinsure', 'u': BEIN}, {'t': 'MLQ', 'u': MLQ954}],
 'react': [
  {'p': '스톡트윗', 't': '개인 투자자 분위기 "매우 낙관", 글 수는 하루 새 두 배 넘게 늘어 "매우 많음"', 'u': ST_NV},
  {'p': '스톡트윗', 't': '"다시 애플 다음 2위" — 시가총액 순위 복귀를 반기는 분위기', 'u': ST_APPL},
  {'p': 'X', 't': "머스크는 '실수가 바로잡혔다', 올트먼은 이름만 외치며 환영", 'u': TNW},
  {'p': 'X', 't': "'GPU 예수의 부활' 같은 밈이 쏟아지고, 앞서 비관론을 편 방송인을 놀리는 글도", 'u': DECR},
  {'p': 'X', 't': '공매도로 알려진 마이클 버리는 회사가 더 비굴해졌다며 SEC·법무부 조사를 계속하라고 반발', 'u': TNW},
  {'p': 'TV', 't': "CNBC 크레이머: '믿을 수 없다, 모든 게 이 한 사람에게 걸려 있었다'", 'u': BARR},
  {'p': 'TV', 't': '크레이머·폼플리아노는 황을 내보냈던 이사회가 물러나야 한다고 주장', 'u': BZ_CRM},
  {'p': '전문가', 't': '지배구조 전문가들 의견이 갈림 — "윤리가 뒷문으로 나갔다" vs "이사회 일은 주주 가치"', 'u': FORTG},
  {'p': '전문가', 't': '노스이스턴대 교수: 이사회가 스스로 웃음거리가 됐으니 사퇴해야', 'u': NEU},
  {'p': '분석', 't': "번스타인은 등급을 올리면서도 이사회의 오락가락을 '광대 같다'고 꼬집음", 'u': NVLIVE},
  {'p': '분석', 't': '댄 아이브스: 황이 있으면 300달러(약 40만 원), 없으면 225달러(약 30만 원)짜리 주식', 'u': FOXB},
 ],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': f"다우는 1,448포인트, 나스닥은 1,472포인트 올랐습니다. 필라델피아 반도체 지수는 {f('^SOX','chg'):+.2f}%, VIX는 {f('^VIX','chg'):.1f}% 내려 26.62로 진정됐습니다.",
 'src': INVC,
}

# ── 참고 지표 ─────────────────────────────────────────
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'close') / (1 + f('^TNX', 'chg') / 100), 2)
issue['indicators'] = [
 {'name': '12월 금리 인상 확률', 'v': 96, 'd': 0, 'suf': '%', 'src': FW96},
 {'name': 'VIX', 'v': f('^VIX', 'close'), 'd': 2, 'chg': f('^VIX', 'chg'), 'src': Y('%5EVIX')},
 {'name': '미 국채 10년', 'v': f('^TNX', 'close'), 'd': 2, 'suf': '%', 'chg': TNX_CH, 'chgsuf': '%p', 'src': Y('%5ETNX')},
 {'name': '달러인덱스', 'v': f('DX-Y.NYB', 'close'), 'd': 2, 'chg': f('DX-Y.NYB', 'chg'), 'src': Y('DX-Y.NYB')},
 {'name': 'WTI 유가', 'v': f('CL=F', 'close'), 'd': 2, 'chg': f('CL=F', 'chg'), 'src': Y('CL%3DF')},
 {'name': '금', 'v': f('GC=F', 'close'), 'd': 1, 'chg': f('GC=F', 'chg'), 'src': Y('GC%3DF')},
 {'name': '원/달러', 'v': FX, 'd': 2, 'chg': f('KRW=X', 'chg'), 'src': Y('KRW%3DX')},
]
issue['gauges'] = [x for x in issue.get('gauges', []) if x['name'] == 'VIX 변동성']
for x in issue['gauges']:
    x['note'] = f"하루 {f('^VIX','chg'):.1f}% · 11/20 장중 40.03에서 20대로 (CNN 공포·탐욕 지수 11/23 값은 확인 중)"
issue['macro'] = []

# ── 간밤 뉴스 (1면 두 건 제외) ────────────────────────
issue['news'] = [
 {'tag': '시장', 'img': 'img/2026-11-24-spx.jpg', 'title': '7일 연속 하락 끝, S&P 500 +4.73%로 7,237',
  'line': f"상위 100개 종목 중 82개가 올랐고 VIX는 {f('^VIX','chg'):.1f}% 내렸습니다. QQQ는 상장 뒤 가장 큰 폭으로 오르며 출발했고, 20일 평균의 1.27배가 거래됐습니다.",
  'src': [{'t': 'Investing.com 마감', 'u': INVC}, {'t': 'Beinsure', 'u': BEIN}]},
 {'tag': '메모리', 'img': 'img/2026-11-24-memory.jpg', 'title': f"마이크론 +19%, 샌디스크 +{g('SNDK'):.1f}%, 시게이트 +13.8%",
  'line': f"황 복귀로 'AI 메모리 품절' 이야기를 가로막던 짐이 걷혔다는 해석입니다. 샌디스크는 87.71달러({won(87.71)})로 분할 뒤 첫 반등을 했습니다.",
  'src': [{'t': 'TipRanks', 'u': MU_TR}, {'t': 'Motley Fool', 'u': SNDK_F}, {'t': 'GuruFocus', 'u': STX_GF}]},
 {'tag': '반도체', 'img': 'img/2026-11-24-chip.jpg', 'title': 'Arm +16.9% CEO 2033년까지 잔류, TSMC·인텔 +14~16%',
  'line': f"황의 후임 후보로 거론되던 르네 하스 Arm CEO가 2033년까지 남기로 했습니다. 반도체 지수는 {f('^SOX','chg'):+.2f}%로 지난주 낙폭을 대부분 되찾았습니다.",
  'src': [{'t': '24/7 Wall St.', 'u': ARM_W}, {'t': 'GuruFocus', 'u': TSM_GF}, {'t': 'GuruFocus', 'u': INTC_GF}]},
 {'tag': '실적', 'img': 'img/2026-11-24-earn.jpg', 'title': '줌 첫 배당·전망 상향, HPE 예상 상회에도 시간외 약세',
  'line': '줌은 분기 매출 12.9억 달러(약 1조 7,300억 원)에 연간 전망을 올리고 주당 0.25달러 배당을 시작했지만 주가는 내렸습니다. HPE도 실적·전망이 예상을 크게 넘었는데 하락했습니다.',
  'src': [{'t': '줌 실적 발표(SEC)', 'u': ZM_8K}, {'t': 'Investing.com', 'u': ZM_INV}, {'t': 'Seeking Alpha', 'u': HPE_SA}]},
 {'tag': '연준', 'img': 'img/2026-11-24-fed.jpg', 'title': '서비스업 PMI 54.7로 예상 밑돌아, 12월 인상 확률은 약 96%',
  'line': '11월 서비스업 PMI 속보치는 54.7로 예상 55.7보다 낮았고 제조업은 54.5로 예상과 같았습니다. 윌리엄스 뉴욕 연은 총재는 물가가 2028년까지 2% 위에 머문다며 12월 인상 가능성을 열어 뒀습니다.',
  'src': [{'t': 'TMGM', 'u': PMI_T}, {'t': 'investingLive', 'u': PMI_IL}, {'t': 'investingLive', 'u': WIL}, {'t': 'KuCoin(FedWatch)', 'u': FW96}]},
 {'tag': '자산', 'img': 'img/2026-11-24-gold.jpg', 'title': f"금 +{f('GC=F','chg'):.1f}%, 비트코인 6만 4천 달러 찍고 되밀려",
  'line': f"금 선물은 {f('GC=F','close'):,.2f}달러({won(f('GC=F','close'))})로 반등했습니다. 비트코인은 장중 6만 4,505달러({won(64505)})까지 올랐다가 6만 1천 달러 안팎으로 내려왔고, 비트코인 457개를 더 산 스트래티지는 {g('MSTR'):+.1f}%였습니다.",
  'src': [{'t': '야후 파이낸스', 'u': Y('GC%3DF')}, {'t': 'Bitcoin.com', 'u': BTC_N}, {'t': 'Crypto Times', 'u': MSTR_CT}]},
 {'tag': '소프트웨어', 'img': 'img/2026-11-24-soft.jpg', 'title': f"오라클 +{g('ORCL'):.1f}%, 테슬라 +{g('TSLA'):.1f}%, 팔란티어 +{g('PLTR'):.1f}%",
  'line': '오라클은 자금 조달 약속과 엔비디아 반전으로 AI 빚 걱정이 줄었다는 해석이 붙었습니다. 테슬라는 스페이스X 합병 위원회 소식과 사이버캡 판매가 거론됐습니다.',
  'src': [{'t': 'GuruFocus', 'u': ORCL_GF}, {'t': 'GuruFocus', 'u': TSLA_GF}, {'t': 'GuruFocus', 'u': PLTR_GF}]},
 {'tag': '상장', 'img': 'img/2026-11-24-ipo.jpg', 'title': '앤트로픽은 반등장에서 제자리걸음',
  'line': '시장 전체가 뛴 날에도 앤트로픽은 오르내리기를 반복했고, 오후 2시 무렵(미 동부) 87.69달러(약 11.8만 원)로 1%대 약세였습니다. 공모가는 83달러(약 11만 원)입니다.',
  'src': [{'t': 'Beinsure(장중)', 'u': BEIN}, {'t': '24/7 Wall St.', 'u': ANT_W}]},
]
for n in issue['news']:
    n['body'] = n['line']

issue['movers'] = [
 {'ticker': t, 'name': nm, 'close': N(TD[t][4], Y(t), CLOSE), 'chg_pct': N(TD[t][5], Y(t), CLOSE), 'won': won(TD[t][4]), 'why': why}
 for t, nm, why in [('NVDA', '엔비디아', '젠슨 황 CEO 복귀, 2003년 이후 최대 하루 상승'), ('DELL', '델', '지난주 -11% 급락 뒤 실적(11/24 장 후) 앞두고 반등'),
                    ('MU', '마이크론', 'AI 메모리 수요 걱정 해소 기대'), ('MRVL', '마벨', '지난주 맞춤칩 급락 뒤 반도체 동반 반등'),
                    ('INTC', '인텔', '기술주 반등·헤지펀드 매수 보도'), ('CRWD', '크라우드스트라이크', '지스케일러 439억 달러(약 59조 원) 주식 인수 발표, 희석 우려')]]

# ── 오늘 밤 일정 (한국 시간, 11/24 화 밤 ~) ─────────────
issue['schedule'] = [
 {'kst': '20:45~21:00', 'type': '실적', 'name': '메드트로닉 · 아날로그디바이스 · 베스트바이 실적 (장 전)', 'star': 3, 'why': '아날로그 반도체(ADI)는 주당 예상 3.89달러(약 5,200원), 베스트바이는 연말 소비 분위기를 봅니다.', 'src': NQE},
 {'kst': '23:00', 'type': '지표', 'name': '9월 케이스-실러 20개 도시 집값', 'star': 2, 'why': '전년 대비 예상 2.7%. 집값이 버티면 물가 걱정이 이어집니다.', 'src': WK},
 {'kst': '23:30', 'type': '개장', 'name': '뉴욕 정규장 개장 · 반등 이틀째 이어지나', 'star': 5, 'why': '하루 +31% 뒤 엔비디아가 버티는지, 반도체 반등이 이어지는지가 먼저입니다.', 'src': YLIVE},
 {'kst': '11/25(수) 00:00', 'type': '지표', 'name': '11월 컨퍼런스보드 소비자신뢰지수', 'star': 3, 'why': '예상 92.1, 이전 91.7. 연말 쇼핑 앞 소비자 체감입니다.', 'src': WK},
 {'kst': '11/25(수) 06:00~', 'type': '실적', 'name': '델 · 워크데이 · HP · 오토데스크 실적 (장 마감 후)', 'star': 5, 'why': '델은 AI 서버 주문이 꺾였는지 보여줄 대형 실적입니다. 매출 예상 약 493억 달러(약 66조 원), 주당 6.62달러(약 8,900원).', 'src': NQE},
 {'kst': '11/25(수) 22:30', 'type': '지표', 'name': '10월 PCE 물가 · 3분기 GDP 수정치 · 내구재 · 실업수당', 'star': 5, 'why': '근원 PCE 예상 전년 대비 3.2%(이전 3.1%), GDP 예상 3.5%. 12월 인상 폭을 가를 숫자입니다.', 'src': HGT},
 {'kst': '11/26(목) 04:00', 'type': '연준', 'name': '연준 베이지북', 'star': 3, 'why': '12월 9일 회의 전 지역 경기 보고서. 물가·고용 표현을 봅니다.', 'src': HGT},
 {'kst': '11/26(목) 밤', 'type': '휴장', 'name': '추수감사절 휴장 · 11/28(토) 03:00 KST 조기 폐장', 'star': 2, 'why': '27일(금)은 미 동부 13:00에 끝납니다. 거래가 얇아 움직임이 커질 수 있습니다.', 'src': NYSE},
]
issue['schedule_note'] = '시각은 한국 시간이며 발표 기관·회사 일정에 따라 바뀔 수 있습니다. 예상치는 집계 기관마다 조금씩 다릅니다.'
issue['calendar'] = {
 'today': '2026-11-24',
 'days': [
  {'d': '2026-11-16', 'ev': [{'k': '연준', 't': '워시 의장 연설'}]},
  {'d': '2026-11-17', 'ev': [{'k': '실적', 't': '엔비디아', 'when': '장 후'}]},
  {'d': '2026-11-18', 'ev': [{'k': '연준', 't': 'FOMC 의사록'}, {'k': '실적', 't': '팔로알토', 'when': '장 후'}]},
  {'d': '2026-11-19', 'ev': [{'k': '상장', 't': '앤트로픽 +17%'}, {'k': '실적', 't': '월마트·인튜이트'}]},
  {'d': '2026-11-20', 'ev': [{'k': '급락', 't': '엔비디아 -14% · S&P 조정'}, {'k': '연준', 't': '쿡 "더 올려야"'}]},
  {'d': '2026-11-23', 'ev': [{'k': '급등', 't': '황 복귀 · 엔비디아 +31%', 'hl': True}, {'k': '인수', 't': 'CRWD→ZS 인수'}, {'k': '실적', 't': 'HPE·줌', 'when': '장 후'}]},
  {'d': '2026-11-24', 'ev': [{'k': '지표', 't': '소비자신뢰'}, {'k': '실적', 't': '델·워크데이·HP', 'when': '장 후', 'hl': True}]},
  {'d': '2026-11-25', 'ev': [{'k': '지표', 't': 'PCE 물가·GDP', 'hl': True}, {'k': '연준', 't': '베이지북'}, {'k': '실적', 't': '디어', 'when': '장 전'}]},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장'}]},
  {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}]},
 ],
 'src': [{'t': 'Infinitus 주간 일정', 'u': WK}, {'t': 'HeyGoTrade 주간', 'u': HGT}, {'t': 'Newsquawk 실적 예상', 'u': NQE}, {'t': 'NYSE 휴장일', 'u': NYSE}],
}
issue['earnings'] = [
 {'date': '11/23(월)', 'time': '장 마감 후', 'company': 'HPE', 'ticker': 'HPE', 'done': True},
 {'date': '11/23(월)', 'time': '장 마감 후', 'company': '줌', 'ticker': 'ZM', 'done': True},
 {'date': '11/24(화)', 'time': '장 시작 전', 'company': '아날로그디바이스', 'ticker': 'ADI', 'done': False},
 {'date': '11/24(화)', 'time': '장 시작 전', 'company': '메드트로닉', 'ticker': 'MDT', 'done': False},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '델 테크놀로지스', 'ticker': 'DELL', 'done': False},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '워크데이', 'ticker': 'WDAY', 'done': False},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': 'HP', 'ticker': 'HPQ', 'done': False},
 {'date': '11/25(수)', 'time': '장 시작 전', 'company': '디어', 'ticker': 'DE', 'done': False},
]

# ── 차트 분석 (어제 → 최근 대비 → 앞으로) ───────────────
pct = lambda a, b: (a / b - 1) * 100
CH = {
 '^IXIC': ('+6.51%, 높게 시작해 하루 내내 버틴 장대 양봉', [
   ('어제', f"나스닥은 {f('^IXIC','chg'):+.2f}%로 24,090에 끝났습니다. 24,270에서 출발해 23,795까지 밀렸다가 다시 올라섰고, 엔비디아({g('NVDA'):+.2f}%)·마이크론({g('MU'):+.2f}%)·Arm({g('ARM'):+.2f}%)이 끌어올렸습니다."),
   ('최근 대비', f"이 하루로 1주 {f('^IXIC','w1'):+.1f}%까지 줄였지만 1달 {f('^IXIC','m1'):+.1f}%, 고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%입니다. QQQ 거래량은 20일 평균의 {f('QQQ','volr'):.2f}배였습니다."),
   ('앞으로', f"20일선 24,998이 {pct(24997.94, f('^IXIC','close')):+.1f}% 위, 200일선 25,163이 {pct(25162.76, f('^IXIC','close')):+.1f}% 위에 있습니다. RSI는 {f('^IXIC','rsi'):.0f}로 과매도에서 벗어났고, 20일선을 넘는지가 첫 관문입니다.")]),
 '^GSPC': ('7일 연속 하락 끝, 7,000선 위로 복귀', [
   ('어제', f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 7,237에 마감했습니다. 7,227에서 시작해 7,153~7,296 사이에서 움직였고 종가는 하루 고가 근처였습니다."),
   ('최근 대비', f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%입니다. 고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%로 조정 구간(-10%)에서는 벗어났고, SPY 거래량은 평균의 {f('SPY','volr'):.2f}배였습니다."),
   ('앞으로', f"200일선 7,350은 {pct(7350.10, f('^GSPC','close')):+.1f}% 위, 20일선 7,477은 {pct(7477.25, f('^GSPC','close')):+.1f}% 위입니다. 지난주 저점 6,883을 지키며 200일선을 되찾으면 반등이 이어진다는 신호로 볼 수 있습니다.")]),
 'SOXX': ('+13.63%, 하루 만에 지난주 낙폭 대부분 회복', [
   ('어제', f"반도체 ETF는 {f('SOXX','chg'):+.2f}%로 140.22달러({won(140.22)})에 끝났습니다. 142.11달러({won(142.11)})에서 시작해 136.64달러({won(136.64)})까지 밀린 뒤 140달러({won(140)}) 위에서 마감했습니다."),
   ('최근 대비', f"1주 {f('SOXX','w1'):+.1f}%로 지난주 하락을 거의 지웠지만 1달 {f('SOXX','m1'):+.1f}%, 고점 대비 {pct(f('SOXX','close'), f('SOXX','hi52')):.1f}%입니다. 거래량은 평균의 {f('SOXX','volr'):.2f}배였습니다."),
   ('앞으로', f"20일선 148.84달러({won(148.84)})가 {pct(148.84, f('SOXX','close')):+.1f}% 위, 200일선 161.09달러({won(161.09)})는 {pct(161.09, f('SOXX','close')):+.1f}% 위에 있습니다. 시가 142달러({won(142)})를 넘어 종가로 버티는지가 먼저입니다.")]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = f"세 지수 모두 **하루 고가 근처**에서 끝난 큰 양봉이지만 아직 **20·50·200일선 아래**입니다. S&P 500은 **고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%로 조정 구간을 벗어났고**, 반도체 ETF는 **하루 +13.6%**였습니다."

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
 'h': f"100개 중 {ups}개 상승 — 반도체가 앞장서고 에너지·필수소비재만 쉬어 간 날",
 't': (f"어제는 상위 100개 중 {ups}개가 올랐습니다. 엔비디아(+{gt('NVDA')}%)·델(+{gt('DELL')}%)·마이크론(+{gt('MU')}%)·마벨(+{gt('MRVL')}%)·인텔(+{gt('INTC')}%)이 가장 크게 뛰었고, 장비주 KLA(+{gt('KLAC')}%)·어플라이드(+{gt('AMAT')}%)·램리서치(+{gt('LRCX')}%)도 14% 넘게 올랐습니다. "
       f"내린 곳은 인수 발표로 희석 우려가 나온 크라우드스트라이크({gt('CRWD')}%)와 유가가 내린 에너지주 코노코필립스({gt('COP')}%)·엑슨모빌({gt('XOM')}%), 코카콜라({gt('KO')}%) 같은 방어주였습니다. "
       f"업종별로는 정보기술 {sw['정보기술']:+}%가 가장 크게 올랐고, 에너지({sw['에너지']:+}%)·필수소비재({sw['필수소비재']:+}%)는 쉬어 갔습니다."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'Investing.com 마감', 'u': INVC}, {'t': '야후 파이낸스', 'u': 'https://finance.yahoo.com'}]}

# ── 롱/숏 한마디 (11/22~11/23 실제 발언) ─────────────────
issue['street']['camps'] = {'long': [
 {'who': '마이클 윌슨', 'role': '모건스탠리 전략가 (11/23)', 'sil': 'suit_g', 'say': '우리가 기다려 온 치기 좋은 공이에요.', 'src': SWISS},
 {'who': '글렌 스미스', 'role': 'GDS 웰스매니지먼트', 'sil': 'suit', 'say': '주가는 이미 바닥을 찍었을 가능성이 커 보여요.', 'src': SWISS},
 {'who': '마니시 싱', 'role': '크로스브리지 캐피털', 'sil': 'firm', 'say': 'AI를 없던 일로 되돌릴 수는 없어요.', 'src': ST_DOW},
 {'who': '댄 아이브스', 'role': '기술주 애널리스트', 'sil': 'glasses', 'say': '황이 있으면 300달러(약 40만 원), 없으면 225달러(약 30만 원)짜리 주식이에요.', 'src': FOXB},
], 'short': [
 {'who': '찰리 맥엘리곳', 'role': '노무라 전략가 (11/23)', 'sil': 'glasses', 'say': '이번 기계적 반등이 보장해 주는 건 없어요.', 'src': YLIVE},
 {'who': '데이비드 로젠버그', 'role': '이코노미스트', 'sil': 'suit', 'say': '전형적인 죽은 고양이 반등 같아요.', 'src': YUK},
 {'who': '마이클 버리', 'role': '엔비디아 공매도 투자자', 'sil': 'hood', 'say': 'SEC와 법무부는 조사를 멈추면 안 돼요.', 'src': TNW},
 {'who': '루크먼 오투누가', 'role': 'FXTM 애널리스트', 'sil': 'woman', 'say': '수요일 물가가 뜨거우면 불에 기름을 붓는 셈이에요.', 'src': YUK},
]}
issue['street']['title'] = '최근 눈에 띈 증권사 의견'
issue['street']['headline'] = '엔비디아는 다시 올리고, 크라우드스트라이크·지스케일러는 인수 계산 다시'
issue['street']['summary'] = '황의 복귀 뒤 번스타인이 엔비디아 등급을 올렸고 캔터는 최선호주로 되돌렸습니다. 크라우드스트라이크는 인수 발표 뒤 목표가 조정이 엇갈렸습니다.'
issue['street']['summary_src'] = NVLIVE
issue['street']['rows'] = [
 {'stock': '엔비디아', 'firm': '번스타인', 'rating': '시장수익률 상회로 상향', 'to': '보도 엇갈려 확인 중', 'date': '11/23', 'dir': 1, 'src': BERN},
 {'stock': '엔비디아', 'firm': '캔터 피츠제럴드', 'rating': '최선호주 목록 복귀', 'to': '—', 'date': '11/23', 'dir': 1, 'src': CANT},
 {'stock': '엔비디아', 'firm': '요크빌 아이브스(댄 아이브스)', 'rating': '시장수익률 상회 유지', 'to': f"225달러({won(225)})", 'date': '11/23', 'dir': 0, 'src': FOXB, 't': 'NVDA'},
 {'stock': '크라우드스트라이크', 'firm': 'FBN 증권', 'rating': '목표 상향', 'to': f"235달러({won(235)})", 'date': '11/23', 'dir': 1, 'src': CRWD_FBN, 't': 'CRWD'},
 {'stock': '크라우드스트라이크', 'firm': 'JP모건', 'rating': '목표 제시', 'to': f"240달러({won(240)})", 'date': '11/23', 'dir': 0, 'src': ZS_JPM, 't': 'CRWD'},
 {'stock': '크라우드스트라이크', 'firm': '제프리스', 'rating': '매수 유지', 'to': '—', 'date': '11/23', 'dir': 0, 'src': CRWD_JEFR},
 {'stock': '지스케일러', 'firm': '프리덤 브로커', 'rating': '목표 하향(인수 반영)', 'to': f"260달러({won(260)})", 'date': '11/23', 'dir': -1, 'src': ZS_FREE},
 {'stock': '센티넬원', 'firm': '시티즌스', 'rating': '목표 상향(인수 후보 거론)', 'to': f"28달러({won(28)})", 'date': '11/23', 'dir': 1, 'src': ZS_JPM},
]
for r in issue['street']['rows']:
    t = r.pop('t', None); d_ = TD.get(t) if t else None
    if d_:
        tv = float(r['to'].split('달러')[0].replace(',', ''))
        r['c'] = d_[4]; r['rx'] = d_[5]; r['gap'] = round((tv / d_[4] - 1) * 100)

# ── 내 종목 분석 ──────────────────────────────────────
WHY4 = {'NVDA': '젠슨 황 CEO 복귀에 +31.5%', 'MU': 'AI 메모리 수요 걱정 해소 기대', 'SNDK': '황 복귀에 메모리 반등', 'SNXX': '샌디스크 +10.7%를 2배로',
        'SOXL': '반도체 +13.6%를 3배로 +39.9%', 'ARM': 'CEO 2033년까지 잔류 + 반도체 반등', 'TSM': 'AI 파운드리 기대 회복', 'INTC': '기술주 반등·헤지펀드 매수 보도',
        'STX': '메모리·저장장치 동반 반등', 'WDC': '메모리·저장장치 동반 반등', 'ORCL': '자금 조달 약속·AI 빚 걱정 완화', 'TSLA': '스페이스X 합병 위원회·사이버캡 판매 거론',
        'PLTR': 'AI 소프트웨어 반등', 'MSTR': '비트코인 반등·457개 추가 매입', 'CRWD': '지스케일러 주식 인수 발표에 희석 우려', 'IONQ': '양자컴퓨터주 동반 반등',
        'ASTS': '우주주 반등', 'RKLB': '최악의 한 주 뒤 반등, 발사 가격 인상 검토', 'QQQ': '나스닥100 +7.0%', 'SOXX': '반도체 ETF +13.6%',
        'AMD': '반도체 동반 반등', 'AVGO': '반도체 반등 속 상대적으로 약한 +3%', 'META': 'AI 투자 심리 회복', 'GOOGL': 'AI·클라우드 기대'}
TN4 = {
 'NVDA': {'y': [('이사회, 젠슨 황을 사장·CEO·이사로 즉시 복귀 · 정부 고위층 의견 들어 안보 위험 없다고 판단', NV8K), ('하루 +31.48%, 2003년 5월 이후 최대 상승', INVC), ('번스타인 등급 상향 · 캔터 최선호주 복귀', NVLIVE)],
          't': [('외국 정보기관 표적 의혹 독립 조사 계속 · 다음 주 상원 반도체 수출 청문회', SENATE)]},
 'SOXL': {'y': [(f"반도체 ETF {f('SOXX','chg'):+.2f}%를 3배로 받아 하루 {qc('SOXL'):+.2f}%", Y('SOXL')), ('수리수리진타리 ⑨ 카드: 11/20 손절선 아래 마감으로 규칙상 이미 정리된 카드', 'https://stock.jintar.co.kr/c/9/')],
          't': [('수요일 밤 PCE 물가 · 목요일 휴장', HGT)]},
 'MU': {'y': [('황 복귀로 AI 메모리 품절 이야기의 짐이 걷혔다는 해석, +19%', MU_TR)], 't': []},
 'SNDK': {'y': [('엔비디아 황 복귀에 메모리주 동반 반등, 분할 뒤 첫 상승', SNDK_F)], 't': []},
 'SNXX': {'y': [('기초자산 샌디스크 +10.7%를 2배로 반영', SNDK_F)], 't': []},
 'ARM': {'y': [('르네 하스 CEO 2033년까지 잔류 약속 · 황 후임 후보로 거론되던 인물', ARM_W)], 't': []},
 'TSM': {'y': [('엔비디아 CEO 복귀로 AI 파운드리 기대 회복', TSM_GF)], 't': []},
 'INTC': {'y': [('기술주 반등과 헤지펀드 매수 보도', INTC_GF)], 't': []},
 'STX': {'y': [('저장장치·메모리 업종 동반 반등', STX_GF)], 't': []},
 'ORCL': {'y': [('자금 조달 약속과 엔비디아 반전으로 AI 빚 걱정 완화', ORCL_GF)], 't': []},
 'TSLA': {'y': [('스페이스X 합병 위원회·사이버캡 판매 소식이 거론됨', TSLA_GF)], 't': []},
 'PLTR': {'y': [('엔비디아 CEO 복귀 뒤 AI 소프트웨어 반등', PLTR_GF)], 't': []},
 'MSTR': {'y': [('비트코인 반등 · 비트코인 457개 추가 매입', MSTR_CT)], 't': []},
 'CRWD': {'y': [('지스케일러를 약 439억 달러(약 59조 원) 전액 주식으로 인수 발표 · ZS 1주당 CRWD 1.135주', ZS_Y), ('같은 날 순신규 ARR 사상 최대 · 연간 전망 상향', ZS_TS)], 't': [('반독점 심사·통합 위험', ZS_BTIG)]},
 'IONQ': {'y': [('황 복귀에 양자컴퓨터주 동반 반등', QNT_W)], 't': []},
 'RKLB': {'y': [('최악의 한 주 뒤 반등, CFO 일렉트론 발사 가격 인상 검토', SPACE_W)], 't': []},
 'ASTS': {'y': [('우주주 동반 반등', SPACE_W)], 't': []},
 'QQQ': {'y': [('나스닥100 하루 +7.0%, 상장 뒤 가장 큰 폭으로 오르며 출발', BEIN)], 't': [('수리수리진타리 ① 급락 초입 신호(B+) 진행 중', 'https://stock.jintar.co.kr/c/1/')]},
}
REASON = {
 'NVDA': '이사회가 젠슨 황을 CEO로 다시 불러들이자 하루 31.5% 올랐습니다. 다만 외국 정보기관 표적 의혹에 대한 회사 독립 조사는 이어집니다.',
 'MU': '황 복귀로 AI 메모리 수요 걱정이 줄었다는 해석에 하루 19% 올랐습니다.',
 'SNDK': '8:1 분할 이틀째, 메모리주 반등에 10.7% 올랐습니다. 그래도 1달 전보다 43% 낮습니다.',
 'SOXL': '반도체 지수를 하루 3배로 따라가는 상품이라 어제 하루 39.9% 올랐습니다. 같은 폭으로 오르내려도 원금이 깎이는 구조입니다.',
 'CRWD': '지스케일러를 주식으로 사들이기로 하면서 새 주식이 약 19% 늘어나는 희석 우려로 8.9% 내렸습니다.',
 'ARM': 'CEO가 2033년까지 남기로 했다는 소식에 반도체 반등이 겹쳐 16.9% 올랐습니다.',
 'TSLA': '시장 반등 속에 스페이스X 합병 위원회·사이버캡 판매 소식이 거론되며 11.5% 올랐습니다.',
 'QQQ': '나스닥100 ETF는 하루 7.0% 올랐지만 아직 1달 전보다 7.6% 낮습니다.',
}
HL4 = {
 'NVDA': '황 복귀에 +31.5%, 2003년 이후 최대 하루 상승', 'SOXL': '하루 +39.9%, 3배 상품의 반대쪽 얼굴', 'MU': '+19%, AI 메모리 걱정 덜어',
 'SNDK': '분할 이틀째 +10.7% 반등', 'SNXX': '샌디스크 +10.7%를 2배로 +18.8%', 'ARM': 'CEO 2033년 잔류에 +16.9%', 'TSM': 'AI 파운드리 기대에 +14.1%',
 'INTC': '+16.3%, 기술주 반등 앞줄', 'CRWD': '지스케일러 인수 발표에 -8.9%', 'ORCL': 'AI 빚 걱정 덜며 +12.3%', 'TSLA': '+11.5%, 스페이스X·사이버캡 거론',
 'QQQ': '하루 +7.0%, 그래도 1달 전보다 -7.6%', 'SOXX': '하루 +13.6%, 지난주 낙폭 대부분 회복', 'MSTR': '비트코인 반등에 +8.5%',
}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY4.get(t, '')
    n = TN4.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = (REASON[t] + ' ' if t in REASON else '') + ns['auto_ai'](q)
    q['h'] = HL4.get(t) or ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE
issue['quotes']['default'] = ['NVDA']

# ── 수리수리진타리 (stock.jintar.co.kr) — 이번 실행은 최신 카드 파일을 못 받아 11/21 05:40 판 카드에 11/23 종가를 붙임 ──
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
  'h': f"신호 뒤 출렁였지만 기준가 대비 {(qq/s1-1)*100:+.1f}%로 돌아선 ① 급락 초입 카드",
  'why': f"11/19 S&P 500이 60일 고점보다 8.1% 낮아져 켜진 ① 급락 초입 카드입니다. 신호 다음 날 QQQ는 5% 넘게 더 빠졌지만, 어제 하루 7.0% 오르며 기준가 {s1}달러({won(s1)})를 넘어섰습니다. 2014~2026년 23번 중 40거래일 뒤 평균 +7.1%, 74%가 올랐다는 기록이지만 미래를 보장하지 않습니다.",
  'img': 'https://stock.jintar.co.kr/c/1.jpg', 'u': 'https://stock.jintar.co.kr/c/1/'})
c9 = next(x for x in JL['cards'] if x['n'] == 'SOXL')
o9, st9, t9 = 42.35, usd(c9['stop']), usd(c9['tgt'])
cl9 = q_['SOXL']['c']
cards.append({'g': c9['g'], 't': 'SOXL', 'kn': c9['kn'], 's': c9['s'], 'ln': c9.get('ln', []),
  'rows': [('카드 기준가', f"{o9}달러({won(o9)}) · 11/20 시가"),
           ('손절선', f"{st9}달러({won(st9)}) — 11/20 종가에서 아래로 마감"),
           ('어제 종가', f"{cl9}달러({won(cl9)}) · 하루 {qc('SOXL'):+.1f}%"),
           ('결과', '규칙상 11/20에 이미 손절 처리된 카드')],
  'h': f"손절 다음 거래일 {qc('SOXL'):+.0f}% — 규칙을 지킨 뒤의 반등",
  'why': f"⑨ 카드는 11/20 종가가 손절선 {st9}달러({won(st9)}) 아래로 내려가 규칙상 정리됐습니다. 바로 다음 거래일인 어제 SOXL은 {qc('SOXL'):+.1f}% 올라 {cl9}달러({won(cl9)})로 기준가 근처까지 돌아왔습니다. 3배 상품은 하루 만에 판단이 뒤집힐 만큼 출렁인다는 기록이며, 손절 규칙을 바꾸라는 뜻은 아닙니다.",
  'img': 'https://stock.jintar.co.kr/c/9.jpg', 'u': 'https://stock.jintar.co.kr/c/9/'})
issue['jintari'] = {'cards': cards, 'cash': [],
 'note': '발행인이 직접 만든 규칙 카드입니다. 정해진 조건이 켜졌다는 기록일 뿐 투자 권유가 아니며, 결과는 본인 책임입니다.',
 'u': JL_U, 'asof': '2026-11-23 장 종료 가격 · 카드 내용은 11/21 05:40 KST 판'}

# ── 1면 두 번째 기사 ─────────────────────────────────
cr = TD['CRWD']; crp = round(cr[4] / (1 + cr[5] / 100), 2)
issue['top2'] = {
 'kicker': '두 번째 큰 뉴스',
 'title': '크라우드스트라이크, 지스케일러 439억 달러(약 59조 원) 주식 인수…주가는 -8.9%',
 'img': 'img/2026-11-24-top2.jpg',
 'points': [
  {'t': f"크라우드스트라이크가 지스케일러를 전액 주식, 약 439억 달러(약 {cap439:.0f}조 원)에 사기로 했습니다. 지스케일러 1주에 크라우드스트라이크 1.135주를 주는 조건으로, 발표 기준 1주당 260.41달러({won(260.41)}), 웃돈 약 34%입니다.", 'src': ZS_Y},
  {'t': f"크라우드스트라이크는 {cr[5]:+.2f}%, {cr[4]}달러({won(cr[4])})로 마감했습니다. 지스케일러는 오후 3시 반 무렵 16.8% 오른 227.45달러({won(227.45)})였습니다.", 'src': ZS_FOOL},
  {'t': f"교환 비율이 고정이라 크라우드스트라이크 주가가 내리면 받는 몫도 줄어듭니다. 어제 종가로 계산하면 1주당 약 {1.135*cr[4]:.2f}달러({won(1.135*cr[4])})입니다.", 'src': ZS_FOOL},
  {'t': '같은 날 발표한 3분기 실적은 순신규 연간반복매출(ARR) 4.19억 달러(약 5,620억 원)로 사상 최대(+58%)였고, 연간 전망도 올렸습니다.', 'src': ZS_TS},
  {'t': '거래는 크라우드스트라이크 2028 회계연도 하반기에 마무리될 예정이고, 합친 회사의 84.1%를 크라우드스트라이크 주주가 갖습니다. 지분 약 34%의 창업자 측은 찬성 약정을 맺었습니다.', 'src': ZS_Y},
 ],
 'risks': [
  {'t': 'BTIG는 전략적으로는 장점이 많지만 두 회사를 합치는 실행 위험이 크다고 봤습니다.', 'src': ZS_BTIG},
  {'t': 'JP모건은 성장률과 현금흐름 마진이 묽어질 수 있다고 짚었고, 제프리스는 규제 심사 가능성을 언급했습니다.', 'src': ZS_JPM},
 ],
 'why': '보안 업계 최대급 인수로, 팔로알토와 정면으로 붙는 큰 보안 회사가 생깁니다. 다른 보안 회사들의 인수 경쟁에 불을 붙일 수 있습니다.',
 'watch': ['반독점 심사 일정과 지스케일러 주주 표결', '크라우드스트라이크가 200달러(약 27만 원) 선을 지키는지', '팔로알토·포티넷 등 경쟁사의 맞대응 인수'],
 'src': [{'t': '야후 파이낸스', 'u': ZS_Y}, {'t': 'TechCrunch', 'u': ZS_TC}, {'t': 'Motley Fool', 'u': ZS_FOOL}, {'t': 'TheStreet', 'u': ZS_TS}],
 'react': [
  {'p': '스톡트윗', 't': '지스케일러는 "매우 낙관", 크라우드스트라이크도 "낙관" — 길게 보는 AI 보안 성장 이야기로 받아들이는 분위기', 'u': ZS_Y},
  {'p': '분석', 't': 'TD 코웬: 보안 업계 통합이 본격적인 단계로 들어서는 신호', 'u': ZS_Y},
  {'p': '분석', 't': 'TD 코웬: 지스케일러로 대기업 고객을 더 빨리 파고들어야 한다는 주문', 'u': ZS_TDC},
  {'p': '분석', 't': 'JP모건: AI 보안 플랫폼으로는 좋은 자리, 다만 성장률·현금흐름 희석은 부담', 'u': ZS_JPM},
  {'p': '분석', 't': 'BTIG: 좋은 점이 더 많지만 통합 실행 위험은 진짜', 'u': ZS_BTIG},
  {'p': '분석', 't': 'R.F. 래퍼티: 고객이 통합을 원한다, 팔로알토와의 정면 승부가 시작', 'u': ZS_RFL},
  {'p': '분석', 't': '오펜하이머: 포티넷·체크포인트도 인수를 서둘러야 할 수 있다는 관측', 'u': ZS_JPM},
  {'p': '분석', 't': '시티즌스: 다음 인수 후보로 센티넬원을 거론', 'u': ZS_JPM},
  {'p': '시장', 't': '"소문에 사고 뉴스에 판다" — 발표 직후 차익 실현으로 읽는 시각', 'u': ZS_MB},
  {'p': '시장', 't': '크라우드스트라이크 200달러(약 27만 원) 선이 무너질지 지켜보자는 기술적 경계', 'u': ZS_FXL},
  {'p': '시장', 't': '지스케일러 주주가 실제로 받는 몫은 발표가보다 낮다는 계산', 'u': ZS_FOOL},
 ],
}

issue['site_v'] = 11
issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 CNBC 일봉(11/23 종가) 기준이며, 증권사·전문가 의견은 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

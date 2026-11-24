"""제5호(2026-11-25 수, 미국 11/24 화 장) — build_issue3.py 와 같이 build_issue1.py 틀을 돌린 뒤 글·일정·의견을 11/24 장 기준으로 바꾼다.
숫자는 data/*(CNBC 일봉, 11/24 종가)와 아래 출처의 확인값만 쓴다. 샌디스크는 8:1 액면분할 반영가."""
import json

src = open('data/build_issue1.py', encoding='utf-8').read()
REP = [("FX = 1330.28", "FX = 1340.95"), ("D = '2026-11-19'", "D = '2026-11-25'"),
       ("CLOSE = '2026-11-18 16:00 ET 종가'", "CLOSE = '2026-11-24 16:00 ET 종가'"),
       ("LIVE = '2026-11-19 11:20 KST 시세'", "LIVE = '2026-11-25 08:50 KST 시세'"),
       ("'no': 1, 'weekday': '목'", "'no': 5, 'weekday': '수'"),
       ("'2026-11-18(수) 뉴욕장'", "'2026-11-24(화) 뉴욕장'"),
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


jo = lambda usd_e8: f"약 {usd_e8 * 1e8 * FX / 1e12:,.0f}조 원"   # 억 달러 → 조 원
eok = lambda usd_e8: f"약 {usd_e8 * 1e8 * FX / 1e8:,.0f}억 원"   # 억 달러 → 억 원

# ── 출처 ─────────────────────────────────────────────
YLIVE = 'https://finance.yahoo.com/markets/live/stock-market-today-tuesday-november-24-dow-sp-500-nasdaq-chip-stocks-nvidia-140629923.html'
FOOL_NV = 'https://www.fool.com/coverage/stock-market-today/2026/11/24/stock-market-today-nov-24-nvidia-gives-back-usd240-billion-in-market-value-despite-wall-street-upgrade-signaling-29-upside/'
FOOL_MK = 'https://www.fool.com/coverage/stock-market-today/2026/11/24/stock-market-today-nov-24-tech-sell-off-drags-nasdaq-as-dow-gains-on-value-rotation/'
STL = 'https://www.stocktitan.net/articles/stock-market-today-live-november-24-2026'
EUR = 'https://eurasiabusinessnews.com/2026/11/24/stock-market-today-november-24-2026-nasdaq-falls-as-nvidia-and-anthropic-slide-oil-price-at-89-gold-drops-to-3620/'
INV_NV = 'https://www.investing.com/news/stock-market-news/nvidia-shares-fall-by-6-following-huang-return-rally-5048533'
BLB = 'https://en.bloomingbit.io/feed/news/125163'
ADI_F = 'https://www.fool.com/investing/2026/11/24/why-analog-devices-stock-fell-nearly-20-today/'
TXN_Y = 'https://finance.yahoo.com/markets/stocks/articles/texas-instruments-txn-stock-down-153245668.html'
MU_F = 'https://www.fool.com/investing/2026/11/24/why-micron-stock-dove-today/'
MU_ST = 'https://stocktwits.com/news-articles/markets/equity/mu-stock-downgraded-price-target-cut-by-almost-1-000-bnp-paribas-flags-2028-hyperscaler-capacity-risks/cNbsaFoR9ko'
BOFA_MU = 'https://finance.yahoo.com/markets/stocks/articles/warning-micron-investors-bank-america-201039465.html'
SNDK_I = 'https://ca.investing.com/news/stock-market-news/why-is-sandisk-stock-sliding-today-93CH-4978673'
WDC_I = 'https://www.investing.com/news/stock-market-news/why-is-western-digital-stock-sliding-today-93CH-5048595'
MEM_W = 'https://247wallst.com/investing/2026/11/24/micron-falls-7-as-nvidia-pullback-partially-reverses-mondays-ai-chip-rally-sandisk-and-sk-hynix-drop-6/'
QNS = 'https://www.quantisnow.com/articles/chip-selloff-hits-tech-alone-adi-and-hpe-fall-about-15-percent-equal-weight-stocks-rise'
INTC_F = 'https://www.fool.com/investing/2026/11/24/why-intel-stock-fell-today/'
AMD_Y = 'https://finance.yahoo.com/markets/stocks/articles/why-amd-amd-stock-down-173112516.html'
MRVL_W = 'https://wisevoter.com/world/us/2026/11/24/marvell-nvidia-shares-fall-congressional-scrutiny'
NV_SEC = 'https://www.fool.com/investing/2026/11/24/nvidia-faces-an-sec-probe-according-to-press-reports-should-you-still-buy-the-stock/'
NV_TH = 'https://finance.yahoo.com/markets/stocks/articles/nvidia-jensen-huang-apologizes-employees-200356995.html'
NV_TH2 = 'https://www.investing.com/news/stock-market-news/nvidias-jensen-huang-apologizes-to-employees-says-he-is-in-therapy-5048912'
NVLIVE = 'https://finance.yahoo.com/markets/stocks/live/nvidia-live-updates-nvidia-stock-falls-as-exuberance-fades-after-jensen-huangs-return-as-ceo-142100906.html'
BERN = 'https://www.investing.com/news/stock-market-news/bernstein-reverses-nvidia-downgrade-on-huangs-return-valuation-5047972'
ROSE = 'https://www.investing.com/news/analyst-ratings/rosenblatt-reiterates-nvidia-stock-rating-after-ceo-reinstatement-93CH-5047866'
ST_IVES = 'https://stocktwits.com/news-articles/markets/equity/dan-ives-calls-jensen-huang-return-to-nvidia-the-start-of-ai-godfather-part-2-but-warns-of-more-noise-ahead/cNbsIBLR9kL'
ST_EIS = 'https://stocktwits.com/news-articles/markets/equity/steve-eisman-says-ai-industry-dodged-a-big-bullet-with-jensen-huang-s-return-but-only-for-now/cNbsQGGR9ks'
BSURV = 'https://mblip.com/bloomberg-surveillance-11-24-2026/'
FOXV = 'https://www.foxbusiness.com/video/6408816030112'
EURO_R = 'https://finance.yahoo.com/technology/articles/jensen-huang-back-nvidia-reactions-103056272.html'
GS_RJ = 'https://www.investing.com/news/stock-market-news/nvidia-shares-surge-30-as-board-announces-jensen-huangs-reinstatement-5045795'
SHEE = 'https://www.investing.com/news/stock-market-news/nvidia-slips-as-investors-assess-risks-surrounding-huangs-return-as-ceo-5047757'
BURRY = 'https://www.tradingview.com/news/stocktwits:d0ffd2d32094b:0-michael-burry-says-nvidia-s-precarious-normal-returns-with-jensen-huang-back-at-the-helm-loads-up-on-jd-tencent-byd-stocks/'
CHK = 'https://finance.yahoo.com/markets/stocks/article/nvidia-stock-falls-after-epic-rally-on-jensen-huangs-return-as-ceo-094535877.html'
ALJ = 'https://www.aljazeera.com/economy/2026/11/24/nvidia-stock-cools-after-huangs-return-driven-surge'
# 델
DELL_PR = 'https://www.stocktitan.net/news/DELL/dell-technologies-delivers-third-quarter-fiscal-2027-financial-1b9dmbjoh63j.html'
DELL_IR = 'https://investors.delltechnologies.com/news-events/press-releases/detail/1665/dell-technologies-delivers-third-quarter-fiscal-2027-financial-results'
DELL_FF = 'https://financefeeds.com/dell-stock-rises-after-q3-revenue-of-54-94b-beats-50-6b-estimate/'
DELL_INV = 'https://uk.investing.com/news/stock-market-news/dell-q3-fy27-slides-revenue-doubles-ai-backlog-hits-132b-93CH-5002787'
DELL_SF = 'https://startupfortune.com/dell-lifts-its-annual-sales-forecast-to-202-billion-as-ai-server-orders-hit-a-record/'
DELL_FOOL = 'https://www.fool.com/investing/2026/11/24/dell-just-reported-earnings-and-raised-its-forecast-by-usd10-billion-is-the-stock-a-buy-after-tuesday-s-selloff/'
DELL_TK = 'https://www.tradingkey.com/news/market-movers/262320518-market-movers-dell-20261124'
DELL_ST = 'https://stocktwits.com/news-articles/markets/equity/dell-stock-gains-after-hours-as-ai-server-boom-leads-record-q3-prompts-third-annual-forecast-hike/cNbsV6sR9lG'
DELL_X1 = 'https://x.com/StockSavvyShay/status/2125336154858037691'
DELL_X2 = 'https://x.com/wallstengine/status/2125335489888526589'
DELL_XD = 'https://x.com/Dell/status/2125343747969871959'
DELL_SOZ = 'https://finance.yahoo.com/video/anthropic-falls-below-ipo-price-as-nvidia-gives-back-gains-214558309.html'
DELL_247 = 'https://247wallst.com/cards/dell-technologies-q3-2027-earnings-dell-01m87pfs2c9c73wyprgqr5d02e'
DELL_TS = 'https://www.thestreet.com/latest-news/dell-technologies-q3-2027-earnings-call-stock-updates'
DELL_MC = 'https://moneycheck.com/dell-stock-morgan-stanley-and-citi-cut-targets-ahead-of-earnings-today'
DELL_TR = 'https://www.tipranks.com/news/dell-crushes-earnings-estimates-heres-how-high-wall-street-thinks-the-stock-can-go'
DELL_TECHI = 'https://www.techi.com/dell-q3-results-ai-backlog-132-billion-forecast-implies-slower-growth/'
DELL_SS = 'https://streetsignal.substack.com/p/dell-eps-q-and-a'
DELL_INV2 = 'https://in.investing.com/news/stock-market-news/why-is-dell-technologies-stock-surging-today-93CH-5724489'
# 그 밖
WDAY = 'https://ng.investing.com/news/stock-market-news/workday-q3-fy27-slides-ai-arr-surges-130-but-stock-falls-on-outlook-93CH-2827803'
HPQ = 'https://www.investing.com/news/stock-market-news/why-is-hp-stock-gaining-today-93CH-5049304'
ADSK = 'https://www.investing.com/news/transcripts/autodesk-shares-fall-despite-q3-earnings-beat-strong-guidance-5049017'
AMBA = 'https://tradersagency.com/blog/ambarella-shares-plunge-after-hours-on-q3-miss-and-weak-q4-guidance-amid-memory-supply-crunch'
ANT_Y = 'https://finance.yahoo.com/technology/ai/articles/anthropic-stock-falls-below-ipo-203714977.html'
NKE_Y = 'https://finance.yahoo.com/markets/stocks/articles/nike-soars-6-competitor-calls-185716230.html'
LLY_I = 'https://www.investing.com/news/stock-market-news/why-is-eli-lilly-stock-rallying-today-93CH-5048619'
ABBV_T = 'https://www.tradingkey.com/news/market-movers/262320386-market-movers-abbv-20261124'
AMGN_U = 'https://unusualwhales.com/news/amgen-stock-rises-near-52-week-high-2026-11-24'
BTC_CD = 'https://www.coindesk.com/tech/2026/11/24/live-updates-bitcoin-pulls-back-to-usd60-000-as-stock-rally-fails-to-budge-crypto'
TARIFF = 'https://www.tovima.com/wsj/u-s-prepares-to-raise-tariffs-on-china-and-other-countries'
FW95 = 'https://en.coinotag.com/traders-price-december-fed-rate-hike-odds-pce'
FG18 = 'https://investrade.com/market-review-november-24-2026/'
SPACE_W = 'https://247wallst.com/investing/2026/11/24/ast-spacemobile-plunges-11-rocket-lab-tumbles-9-as-space-stocks-retrace-mondays-rally-spacex-falls-6-amid-reported-tesla-merger-talks/'
OKLO_W = 'https://247wallst.com/investing/2026/11/24/oklo-slides-7-as-mondays-nuclear-rebound-fades-nuscale-power-and-energy-fuels-drop-6/'
BLACK = 'https://finance.yahoo.com/technology/articles/u-blacklists-alibaba-owned-company-055000789.html'
CAL_INV = 'https://investing.com/news/stock-market-news/key-fed-events-and-economic-data-to-watch-this-week-93CH-5046211'
HGT = 'https://www.heygotrade.com/en/news/weekly-economic-outlook-2026-11-23/'
PCE_IL = 'https://investinglive.com/central-banks/us-pce-preview-inflation-seen-near-3-8-in-the-fed-s-last-read-before-a-december-hike/'
PCE_ST = 'https://www.stocktitan.net/articles/october-2026-pce-inflation-preview'
DE_INV = 'https://www.investing.com/news/stock-market-news/deere-polestar-and-more-set-to-report-earnings-wednesday-93CH-5048882'
LTYI = 'https://letterstoayounginvestor.substack.com/p/weekly-economic-calendar-november-3ec'
NYSE = 'https://www.nyse.com/markets/hours-calendars'
JL_U = 'https://stock.jintar.co.kr/'
BBY_J = 'https://www.investing.com/news/analyst-ratings/best-buy-stock-price-target-raised-to-101-from-84-by-jefferies-93CH-5048837'
DKS_T = 'https://www.tipranks.com/news/the-fly/dicks-sporting-price-target-raised-to-150-from-128-at-truist-thefly-news'
HPE_WF = 'https://www.marketscreener.com/news/wells-fargo-adjusts-price-target-on-hewlett-packard-enterprise-to-50-from-63-ce7851dbdb8eff20'
ZM_ST = 'https://stocktwits.com/news-articles/markets/equity/zm-stock-faces-wall-street-price-target-cuts-after-q3-beat/cNbsJ5vR9kj'

q_ = {q['t']: q for q in issue['quotes']['list']}
g = lambda t: f(t, 'chg') if t in summ else (TD[t][5] if t in TD else q_[t]['ch'])
qc = lambda t: q_[t]['ch']
SOX = f('^SOX', 'chg')

# ── 1면 ───────────────────────────────────────────────
issue['top'] = {
 'kicker': '지금 가장 중요한 뉴스',
 'title': f"반도체 하루 만에 되밀려…필라델피아 반도체 {SOX:+.1f}%, 엔비디아 {g('NVDA'):+.1f}%, ADI {g('ADI'):+.0f}%",
 'img': 'img/2026-11-25-top.jpg',
 'points': [
  {'t': f"전날 +14%였던 필라델피아 반도체 지수가 {SOX:+.2f}%로 되밀렸습니다. 나스닥은 {f('^IXIC','chg'):+.2f}%, S&P 500은 {f('^GSPC','chg'):+.2f}%였고, 다우는 {f('^DJI','chg'):+.2f}%로 5만 선 위에서 끝났습니다.", 'src': FOOL_MK},
  {'t': f"엔비디아는 {g('NVDA'):+.2f}%, 155.38달러({won(155.38)})로 마감해 하루 새 시가총액 약 2,400억 달러({jo(2400)})를 내줬습니다. 전날 +31%의 일부를 돌려준 셈입니다.", 'src': FOOL_NV},
  {'t': f"아날로그디바이스(ADI)는 4분기 실적이 예상을 넘었지만 1분기 전망이 시장 기대에 그치고 이익률이 낮아진다는 말에 {g('ADI'):+.2f}% 급락했습니다. 매출의 약 79%가 아날로그인 텍사스인스트루먼트도 {g('TXN'):+.2f}%였습니다.", 'src': ADI_F},
  {'t': f"마이크론은 BNP파리바가 투자의견을 '중립'으로 내리고 적정 주가를 1,700달러({won(1700)})에서 775달러({won(775)})로 깎자 {g('MU'):+.2f}%였습니다. 2027년 중반부터 메모리 공급과 수요가 비슷해져 값이 내릴 수 있다는 이유입니다.", 'src': MU_F},
  {'t': '황 CEO는 화요일 아침 직원 전체 회의에서 사과하고 치료를 받고 있다고 말한 것으로 보도됐습니다. 엔비디아 회계에 대한 SEC 초기 조사 보도와 12/1 의회 면담 일정도 다시 거론됐습니다.', 'src': NV_TH},
 ],
 'risks': [
  {'t': f"번스타인은 엔비디아를 '시장수익률 상회'로 다시 올리고 적정 주가로 200달러({won(200)})를 제시했습니다. 종가보다 약 29% 높은 값입니다.", 'src': BERN},
  {'t': "UBS 마크 헤펠레는 기술주의 출렁임이 'AI 투자 이야기가 깨졌다'는 신호는 아니라고 봤습니다. 돈은 헬스케어·소비주로 옮겨 다우는 올랐습니다.", 'src': STL},
 ],
 'why': '월요일 반등이 하루 만에 절반가량 꺾이면서 반도체 바닥이 아직 확인되지 않았다는 점이 드러났습니다. 실적이 좋아도 전망·이익률·메모리 값 같은 다음 숫자에 더 민감한 장입니다.',
 'watch': [
  f"반도체 ETF(SOXX)가 20일 지지선 122.20달러({won(122.20)})를 지키는지",
  '수요일 밤 10월 PCE 물가(근원 전년 대비 3.2% 예상)와 GDP 수정치',
  '12/1 황 CEO 의회 면담 · SEC 조사 보도 후속',
 ],
 'src': [{'t': 'Motley Fool 마감', 'u': FOOL_NV}, {'t': 'Motley Fool 마감②', 'u': FOOL_MK}, {'t': 'StockTitan 실시간', 'u': STL}, {'t': 'Motley Fool(ADI)', 'u': ADI_F}, {'t': 'Motley Fool(MU)', 'u': MU_F}, {'t': '야후 파이낸스', 'u': NV_TH}],
 'react': [
  {'p': '스톡트윗', 't': '엔비디아 게시판은 주가가 빠지는 중에도 "매우 낙관"·글 수 "매우 많음"을 유지', 'u': ST_EIS},
  {'p': '스톡트윗', 't': '3만 명 넘게 참여한 투표에서 63%가 "더 낙관적이 됐다"고 답함(급락 전 아침)', 'u': ST_IVES},
  {'p': 'TV', 't': "CNBC 스티브 아이스먼: AI 업계가 '큰 총알을 피했다', 다만 위험은 여전", 'u': ST_EIS},
  {'p': 'TV', 't': '블룸버그 서베일런스: "아직 순항은 아니다"·"AI 거래 숲을 못 빠져나왔다" vs "AI 수요는 꺾인 적 없다"', 'u': BSURV},
  {'p': 'TV', 't': '폭스비즈니스: D.A. 데이비슨 길 루리아가 황 복귀 뒤 주가가 밀린 이유를 짚음', 'u': FOXV},
  {'p': 'X', 't': '블랭크페인 전 골드만 CEO: 황은 돌아왔지만 이사회는 그럴 기회가 없을 것이라고 꼬집음', 'u': NVLIVE},
  {'p': 'X', 't': "'GPU 예수의 부활' 밈과 복귀의 도덕성을 비꼬는 글이 엇갈림", 'u': EURO_R},
  {'p': '분석', 't': "골드만 TMT 데스크: 분위기가 나아진 것과 반도체 걱정이 정리된 것은 다르다", 'u': GS_RJ},
  {'p': '전문가', 't': "노무라 맥엘리곳: 월요일은 기계적 매수였고 아무것도 보장하지 않는다", 'u': NVLIVE},
  {'p': '전문가', 't': '텔로스 웰스 댄 시핸: 월요일이 대단했어도 숲을 빠져나왔다는 신호는 아니다', 'u': SHEE},
  {'p': '분석', 't': "BofA: '반도체 전망치 하향이 시작됐다'며 마이크론에 경고", 'u': BOFA_MU},
  {'p': '전문가', 't': "마이클 버리: '불안한 정상'으로 돌아왔다며 엔비디아 공매도 논리는 그대로라고 주장", 'u': BURRY},
 ],
}

issue['market'] = {
 'rows': [row('S&P 500', '^GSPC'), row('나스닥 종합', '^IXIC'), row('다우', '^DJI'), row('필라델피아 반도체', '^SOX'), row('러셀 2000', '^RUT')],
 'note': f"다우는 423포인트 올라 50,019로 마감했고, 나스닥은 356포인트 내렸습니다. 반도체 지수는 {SOX:+.2f}%, VIX는 {f('^VIX','close'):.2f}로 거의 그대로였습니다.",
 'src': FOOL_NV,
}

# ── 참고 지표 ─────────────────────────────────────────
TNX_CH = round(f('^TNX', 'close') - f('^TNX', 'close') / (1 + f('^TNX', 'chg') / 100), 2)
issue['indicators'] = [
 {'name': '12월 금리 인상 확률', 'v': 95.1, 'd': 1, 'suf': '%', 'src': FW95},
 {'name': 'VIX', 'v': f('^VIX', 'close'), 'd': 2, 'chg': f('^VIX', 'chg'), 'src': Y('%5EVIX')},
 {'name': '미 국채 10년', 'v': f('^TNX', 'close'), 'd': 2, 'suf': '%', 'chg': TNX_CH, 'chgsuf': '%p', 'src': Y('%5ETNX')},
 {'name': '달러인덱스', 'v': f('DX-Y.NYB', 'close'), 'd': 2, 'chg': f('DX-Y.NYB', 'chg'), 'src': Y('DX-Y.NYB')},
 {'name': 'WTI 유가', 'v': f('CL=F', 'close'), 'd': 2, 'chg': f('CL=F', 'chg'), 'src': Y('CL%3DF')},
 {'name': '금', 'v': f('GC=F', 'close'), 'd': 1, 'chg': f('GC=F', 'chg'), 'src': Y('GC%3DF')},
 {'name': '원/달러', 'v': FX, 'd': 2, 'chg': f('KRW=X', 'chg'), 'src': Y('KRW%3DX')},
]
issue['gauges'] = [x for x in issue.get('gauges', []) if x['name'] == 'VIX 변동성']
for x in issue['gauges']:
    x['note'] = f"하루 {f('^VIX','chg'):+.1f}% · 장중 32.38까지 올랐다 내려옴 · CNN 공포·탐욕 지수 18(극단적 공포, Investrade 11/24 집계)"
issue['macro'] = []

# ── 간밤 뉴스 (1면 두 건 제외) ────────────────────────
issue['news'] = [
 {'tag': '시장', 'img': 'img/2026-11-25-spx.jpg', 'title': f"다우 +{f('^DJI','chg'):.2f}% 5만 선 회복, 나스닥 {f('^IXIC','chg'):.2f}%",
  'line': f"기술주에서 빠진 돈이 헬스케어·소비주로 옮겨 갔습니다. 암젠(+{TD['AMGN'][5]}%)·애브비(+{TD['ABBV'][5]}%)·일라이 릴리(+{TD['LLY'][5]}%)가 올랐고, 11월 소비자신뢰지수는 103.3으로 예상(약 92)을 크게 넘었습니다.",
  'src': [{'t': 'Motley Fool 마감', 'u': FOOL_MK}, {'t': 'TradingKey(애브비)', 'u': ABBV_T}, {'t': 'Investing.com(릴리)', 'u': LLY_I}]},
 {'tag': '메모리', 'img': 'img/2026-11-25-memory.jpg', 'title': f"마이크론 {g('MU'):.1f}%, 샌디스크 {g('SNDK'):.1f}%…BNP '2027년 중반 공급 균형'",
  'line': f"BNP파리바의 마이크론 하향과 트렌드포스의 내년 1분기 낸드 계약가 하락 전망이 겹쳤습니다. 샌디스크는 77.95달러({won(77.95)})로, 내부자 주식 매도 예정 신고(Form 144)도 거론됐습니다.",
  'src': [{'t': 'Motley Fool', 'u': MU_F}, {'t': 'Investing.com(샌디스크)', 'u': SNDK_I}, {'t': '24/7 Wall St.', 'u': MEM_W}]},
 {'tag': '실적', 'img': 'img/2026-11-25-earn.jpg', 'title': '워크데이 시간외 -7%, 오토데스크 -4%, 앰바렐라 -40%',
  'line': '워크데이는 실적이 예상을 넘었지만 4분기 전망이 신중해 시간외 7% 넘게 내렸습니다. 앰바렐라는 메모리 값과 공급 부족으로 고객이 전망을 낮춘다며 시간외 40% 넘게 빠졌고, HP는 보합권이었습니다.',
  'src': [{'t': 'Investing.com(워크데이)', 'u': WDAY}, {'t': 'Investing.com(오토데스크)', 'u': ADSK}, {'t': 'TradersAgency(앰바렐라)', 'u': AMBA}, {'t': 'Investing.com(HP)', 'u': HPQ}]},
 {'tag': '인수', 'img': 'img/2026-11-25-deal.jpg', 'title': f"사노피, 인스메드 약 410억 달러({jo(410)}) 현금 인수",
  'line': f"1주당 175달러({won(175)}), 인수설 보도 전날 종가보다 약 46% 높은 값입니다. 인스메드는 +14.13%로 170.15달러({won(170.15)})에 끝났고 2027년 상반기 마무리 예정입니다.",
  'src': [{'t': 'StockTitan(사노피 발표)', 'u': STL}]},
 {'tag': '소매', 'img': 'img/2026-11-25-retail.jpg', 'title': '딕스 +14.6%·달러트리 +11.2%, 소매 실적에 다우 힘',
  'line': f"딕스와 달러트리가 연간 이익 전망을 올렸고 콜스·애버크롬비는 19% 넘게 뛰었습니다. 딕스 실적에서 풋락커 매장 판매가 좋았다는 말에 나이키도 {g('NKE'):+.2f}%였습니다.",
  'src': [{'t': 'StockTitan', 'u': STL}, {'t': '야후 파이낸스(나이키)', 'u': NKE_Y}]},
 {'tag': '상장', 'img': 'img/2026-11-25-ipo.jpg', 'title': f'앤트로픽, 상장 나흘 만에 공모가 83달러({won(83)}) 아래로',
  'line': f"장중 약 76달러까지 13% 빠졌고 81.91달러({won(81.91)}) 무렵에서 끝났습니다. 공동창업자 7명이 상장 때 모두 19.6억 달러({eok(19.6)})어치를 팔았다는 공시가 매물 부담으로 거론됐습니다.",
  'src': [{'t': '야후 파이낸스', 'u': ANT_Y}, {'t': 'Motley Fool(종가 시세)', 'u': FOOL_NV}]},
 {'tag': '연준', 'img': 'img/2026-11-25-fed.jpg', 'title': '12월 0.25%p 인상 확률 약 95%, 오늘 밤 PCE 물가',
  'line': '선물시장은 12월 9일 회의에서 0.25%p 인상 확률을 약 95%, 0.5%p를 약 5%로 봤습니다. 소비자신뢰지수가 2년 만에 가장 높게 나와 물가 걱정은 더 커졌습니다.',
  'src': [{'t': 'Coinotag(금리 선물)', 'u': FW95}, {'t': 'Motley Fool 마감', 'u': FOOL_MK}, {'t': 'Eurasia Business News', 'u': EUR}]},
 {'tag': '자산', 'img': 'img/2026-11-25-gold.jpg', 'title': f"금 {f('GC=F','chg'):.1f}%, 비트코인 6만 달러({won(60000)}) 아래",
  'line': f"금 선물은 {f('GC=F','close'):,.1f}달러({won(f('GC=F','close'))})로 밀렸습니다. 미국이 중국·일본·한국 등에 관세를 올릴 준비를 한다는 WSJ 보도 뒤 비트코인은 6만 달러({won(60000)}) 아래로 내려왔고, 스트래티지는 {g('MSTR'):+.2f}%였습니다.",
  'src': [{'t': '야후 파이낸스(금)', 'u': Y('GC%3DF')}, {'t': 'CoinDesk', 'u': BTC_CD}, {'t': 'To Vima(WSJ 관세)', 'u': TARIFF}]},
]
for n in issue['news']:
    n['body'] = n['line']

issue['movers'] = [
 {'ticker': t, 'name': nm, 'close': N(TD[t][4], Y(t), CLOSE), 'chg_pct': N(TD[t][5], Y(t), CLOSE), 'won': won(TD[t][4]), 'why': why}
 for t, nm, why in [('ADI', '아날로그디바이스', '실적은 넘었지만 1분기 전망·이익률 하락 예고'), ('DELL', '델', 'HPE 이익률 경고 여파, 장 마감 후 실적은 예상 상회'),
                    ('TXN', '텍사스인스트루먼트', 'ADI 전망 실망에 아날로그 동반 하락'), ('MU', '마이크론', 'BNP파리바 투자의견 하향'),
                    ('MRVL', '마벨', '반도체 차익 실현·엔비디아 의회 조사 부담'), ('AMGN', '암젠', '기술주에서 헬스케어로 돈 이동')]]

# ── 오늘 밤 일정 (한국 시간, 11/25 수 밤 ~) ─────────────
issue['schedule'] = [
 {'kst': '20:30 무렵', 'type': '실적', 'name': '디어 실적 (장 전)', 'star': 2, 'why': f"주당 예상 4.03달러({won(4.03)}), 매출 104억 달러({jo(104)}). 농기계 경기를 봅니다.", 'src': DE_INV},
 {'kst': '22:30', 'type': '지표', 'name': '10월 PCE 물가 · 3분기 GDP 수정치 · 내구재 · 실업수당', 'star': 5, 'why': '근원 PCE 전년 대비 3.2% 예상(이전 3.1%), GDP 3.4% 안팎. 12월 인상 폭을 가를 연준의 마지막 물가 숫자입니다.', 'src': CAL_INV},
 {'kst': '23:30', 'type': '개장', 'name': '뉴욕 정규장 · 델 실적 반응', 'star': 4, 'why': '시간외에서 오른 델이 정규장에서 버티는지, 반도체가 이틀째 밀리는지 봅니다.', 'src': DELL_FF},
 {'kst': '11/26(목) 00:00', 'type': '지표', 'name': '10월 신규주택판매', 'star': 2, 'why': '예상 64.9만 채, 이전 67.6만 채.', 'src': CAL_INV},
 {'kst': '11/26(목) 04:00', 'type': '연준', 'name': '연준 베이지북', 'star': 3, 'why': '12월 9일 회의 전 지역 경기 보고서. 물가·고용 표현을 봅니다.', 'src': HGT},
 {'kst': '11/26(목) 밤', 'type': '휴장', 'name': '추수감사절 휴장', 'star': 2, 'why': '목요일은 미국 증시가 쉬어 11/27(금) 호는 쉽니다.', 'src': NYSE},
 {'kst': '11/28(토) 03:00', 'type': '단축', 'name': '금요일 조기 폐장(미 동부 13:00)', 'star': 2, 'why': '거래가 얇아 움직임이 커질 수 있습니다.', 'src': HGT},
]
issue['schedule_note'] = '시각은 한국 시간이며 발표 기관·회사 일정에 따라 바뀔 수 있습니다. 예상치는 집계 기관마다 조금씩 다릅니다.'
issue['calendar'] = {
 'today': '2026-11-25',
 'days': [
  {'d': '2026-11-16', 'ev': [{'k': '연준', 't': '워시 의장 연설'}]},
  {'d': '2026-11-17', 'ev': [{'k': '실적', 't': '엔비디아', 'when': '장 후'}]},
  {'d': '2026-11-18', 'ev': [{'k': '연준', 't': 'FOMC 의사록'}]},
  {'d': '2026-11-19', 'ev': [{'k': '상장', 't': '앤트로픽 +17%'}]},
  {'d': '2026-11-20', 'ev': [{'k': '급락', 't': '엔비디아 -14% · S&P 조정'}]},
  {'d': '2026-11-23', 'ev': [{'k': '급등', 't': '황 복귀 · 엔비디아 +31%'}, {'k': '인수', 't': 'CRWD→ZS 인수'}]},
  {'d': '2026-11-24', 'ev': [{'k': '급락', 't': '반도체 -7.9%', 'hl': True}, {'k': '실적', 't': '델·워크데이·HP', 'when': '장 후', 'hl': True}, {'k': '인수', 't': '사노피→인스메드'}]},
  {'d': '2026-11-25', 'ev': [{'k': '지표', 't': 'PCE 물가·GDP', 'hl': True}, {'k': '연준', 't': '베이지북'}, {'k': '실적', 't': '디어', 'when': '장 전'}]},
  {'d': '2026-11-26', 'ev': [{'k': '휴장', 't': '추수감사절 휴장'}]},
  {'d': '2026-11-27', 'ev': [{'k': '단축', 't': '조기 폐장(13:00 ET)'}, {'k': '예고', 't': '12/1 황 의회 면담 · 12/9 FOMC'}]},
 ],
 'src': [{'t': 'Investing.com 주간 일정', 'u': CAL_INV}, {'t': 'HeyGoTrade 주간', 'u': HGT}, {'t': 'Investing.com 실적 예정', 'u': DE_INV}, {'t': 'Wisevoter(의회 일정)', 'u': MRVL_W}, {'t': 'StockTitan(FOMC 날짜)', 'u': PCE_ST}]},
issue['calendar'] = issue['calendar'][0] if isinstance(issue['calendar'], tuple) else issue['calendar']
issue['earnings'] = [
 {'date': '11/24(화)', 'time': '장 시작 전', 'company': '아날로그디바이스', 'ticker': 'ADI', 'done': True},
 {'date': '11/24(화)', 'time': '장 시작 전', 'company': '베스트바이', 'ticker': 'BBY', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '델 테크놀로지스', 'ticker': 'DELL', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '워크데이', 'ticker': 'WDAY', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': 'HP', 'ticker': 'HPQ', 'done': True},
 {'date': '11/24(화)', 'time': '장 마감 후', 'company': '오토데스크', 'ticker': 'ADSK', 'done': True},
 {'date': '11/25(수)', 'time': '장 시작 전', 'company': '디어', 'ticker': 'DE', 'done': False},
]

# ── 차트 분석 (어제 → 최근 대비 → 앞으로) ───────────────
pct = lambda a, b: (a / b - 1) * 100
m = lambda s, k: f(s, k)
CH = {
 '^IXIC': (f"{f('^IXIC','chg'):+.2f}%, 시가 근처에서 출발해 아래로 밀린 음봉", [
   ('어제', f"나스닥은 {f('^IXIC','chg'):+.2f}%로 {f('^IXIC','close'):,.0f}에 끝났습니다. {m('^IXIC','open'):,.0f}에서 출발해 {m('^IXIC','low'):,.0f}까지 밀렸고, 엔비디아({g('NVDA'):+.2f}%)·마이크론({g('MU'):+.2f}%)·AMD({g('AMD'):+.2f}%)가 끌어내렸습니다."),
   ('최근 대비', f"1주 {f('^IXIC','w1'):+.1f}%, 1달 {f('^IXIC','m1'):+.1f}%, 고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%입니다. QQQ 거래량은 20일 평균의 {f('QQQ','volr'):.2f}배로 많지 않았습니다."),
   ('앞으로', f"20일선 {m('^IXIC','ma20'):,.0f}이 {pct(m('^IXIC','ma20'), f('^IXIC','close')):+.1f}% 위, 200일선 {m('^IXIC','ma200'):,.0f}이 {pct(m('^IXIC','ma200'), f('^IXIC','close')):+.1f}% 위에 있습니다. RSI는 {f('^IXIC','rsi'):.0f}, 아래로는 최근 20일 저점 {m('^IXIC','sup20'):,.0f}이 기준입니다.")]),
 '^GSPC': (f"{f('^GSPC','chg'):+.2f}%, 작은 몸통으로 7,200선 지켜", [
   ('어제', f"S&P 500은 {f('^GSPC','chg'):+.2f}%로 {f('^GSPC','close'):,.0f}에 마감했습니다. {m('^GSPC','low'):,.0f}~{m('^GSPC','high'):,.0f} 사이의 좁은 범위였고, 헬스케어가 반도체 하락을 상당 부분 메웠습니다."),
   ('최근 대비', f"1주 {f('^GSPC','w1'):+.1f}%, 1달 {f('^GSPC','m1'):+.1f}%, 고점 대비 {pct(f('^GSPC','close'), f('^GSPC','hi52')):.1f}%입니다. SPY 거래량은 평균의 {f('SPY','volr'):.2f}배였습니다."),
   ('앞으로', f"200일선 {m('^GSPC','ma200'):,.0f}은 {pct(m('^GSPC','ma200'), f('^GSPC','close')):+.1f}% 위, 20일선 {m('^GSPC','ma20'):,.0f}은 {pct(m('^GSPC','ma20'), f('^GSPC','close')):+.1f}% 위입니다. 지난주 저점 {m('^GSPC','sup20'):,.0f}이 아래 기준선입니다.")]),
 'SOXX': (f"{f('SOXX','chg'):+.2f}%, 전날 상승분 절반 넘게 반납", [
   ('어제', f"반도체 ETF는 {f('SOXX','chg'):+.2f}%로 {f('SOXX','close')}달러({won(f('SOXX','close'))})에 끝났습니다. {m('SOXX','open')}달러에서 시작해 {m('SOXX','low')}달러({won(m('SOXX','low'))})까지 밀렸습니다."),
   ('최근 대비', f"1주 {f('SOXX','w1'):+.1f}%, 1달 {f('SOXX','m1'):+.1f}%, 고점 대비 {pct(f('SOXX','close'), f('SOXX','hi52')):.1f}%입니다. 거래량은 평균의 {f('SOXX','volr'):.2f}배였습니다."),
   ('앞으로', f"20일선 {m('SOXX','ma20')}달러({won(m('SOXX','ma20'))})가 {pct(m('SOXX','ma20'), f('SOXX','close')):+.1f}% 위, 200일선 {m('SOXX','ma200')}달러는 {pct(m('SOXX','ma200'), f('SOXX','close')):+.1f}% 위입니다. 최근 20일 저점 {m('SOXX','sup20')}달러({won(m('SOXX','sup20'))})를 지키는지가 먼저입니다.")]),
}
for c in issue['charts']:
    if c['sym'] in CH: c['headline'], c['an'] = CH[c['sym']]
issue['chart_summary'] = f"세 지수 모두 **20·50·200일선 아래**에 머물렀습니다. 나스닥은 **고점 대비 {pct(f('^IXIC','close'), f('^IXIC','hi52')):.1f}%**, 반도체 ETF는 **하루 {f('SOXX','chg'):+.1f}%**로 월요일 반등의 절반 넘게를 되돌렸고, S&P 500은 **{f('^GSPC','chg'):+.2f}%**로 버텼습니다."

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
 'h': f"100개 중 {ups}개 상승 — 반도체만 크게 빠지고 헬스케어가 받친 날",
 't': (f"어제는 상위 100개 중 {ups}개가 올랐습니다. 가장 크게 내린 곳은 아날로그디바이스({gt('ADI')}%)·델({gt('DELL')}%)·텍사스인스트루먼트({gt('TXN')}%)·마이크론({gt('MU')}%)·마벨({gt('MRVL')}%)·AMD({gt('AMD')}%)로 거의 모두 반도체·AI 하드웨어였습니다. "
       f"반대로 암젠({gt('AMGN'):+}%)·애브비({gt('ABBV'):+}%)·일라이 릴리({gt('LLY'):+}%) 같은 제약주가 올랐습니다. "
       f"업종별로는 정보기술 {sw['정보기술']:+}%가 가장 약했고 헬스케어는 {sw['헬스케어']:+}%였습니다."),
 'src': [{'t': 'slickcharts', 'u': 'https://www.slickcharts.com/sp500'}, {'t': 'Motley Fool 마감', 'u': FOOL_MK}, {'t': 'StockTitan', 'u': STL}]}

# ── 롱/숏 한마디 (11/23~11/24 실제 발언) ─────────────────
issue['street']['camps'] = {'long': [
 {'who': '앙투안 치카이반', 'role': '뉴스트리트 리서치 (11/24)', 'sil': 'glasses', 'say': '저는 오늘도 엔비디아를 사는 쪽이에요.', 'src': CHK},
 {'who': '댄 아이브스', 'role': '기술주 애널리스트 (X)', 'sil': 'suit_g', 'say': '잡음은 남았지만 황이 돌아와 질서가 잡혔어요.', 'src': ST_IVES},
 {'who': '마크 헤펠레', 'role': 'UBS 글로벌 웰스 CIO', 'sil': 'suit', 'say': '기술주 출렁임이 AI 투자 이야기가 깨졌다는 신호는 아니에요.', 'src': STL},
 {'who': '마이클 모너핸', 'role': '파운더스 100 ETF 운용역', 'sil': 'firm', 'say': '창업자는 드물고, 비슷한 두 번째 사람은 거의 없어요.', 'src': ALJ},
], 'short': [
 {'who': '스티븐 도버', 'role': '프랭클린 템플턴 전략가', 'sil': 'suit', 'say': '돈이 더는 아주 싸지 않아요. 가치 평가를 따져야 해요.', 'src': YLIVE},
 {'who': '크리슈나 구하', 'role': '에버코어 ISI', 'sil': 'glasses', 'say': '워시 의장에게 이번이 진짜 시험대예요.', 'src': YLIVE},
 {'who': '댄 시핸', 'role': '텔로스 웰스 어드바이저스', 'sil': 'woman', 'say': '복귀 자체가 답한 만큼 질문도 던져요.', 'src': SHEE},
 {'who': '스티브 아이스먼', 'role': '투자자 (CNBC)', 'sil': 'hood', 'say': '그렇다고 환자에게 큰 위험이 없다는 뜻은 아니에요.', 'src': ST_EIS},
]}
issue['street']['title'] = '최근 눈에 띈 증권사 의견'
issue['street']['headline'] = '엔비디아는 다시 올리고, 마이크론은 반토막 목표가'
issue['street']['summary'] = '번스타인이 엔비디아를 다시 올렸고, BNP파리바는 메모리 값 하락을 내다보며 마이크론 목표가를 절반 넘게 깎았습니다. 실적을 낸 소매·HPE·줌은 목표가 조정이 엇갈렸습니다.'
issue['street']['summary_src'] = BERN
issue['street']['rows'] = [
 {'stock': '엔비디아', 'firm': '번스타인', 'rating': '시장수익률 → 시장수익률 상회', 'to': f"200달러({won(200)})", 'date': '11/24', 'dir': 1, 'src': BERN, 't': 'NVDA'},
 {'stock': '엔비디아', 'firm': '로젠블랫', 'rating': '매수 유지', 'to': f"300달러({won(300)})", 'date': '11/24', 'dir': 0, 'src': ROSE, 't': 'NVDA'},
 {'stock': '마이크론', 'firm': 'BNP파리바', 'rating': '시장수익률 상회 → 중립', 'to': f"1,700→775달러({won(775)})", 'date': '11/24', 'dir': -1, 'src': MU_ST},
 {'stock': 'HPE', 'firm': '웰스파고', 'rating': '목표 하향', 'to': f"63→50달러({won(50)})", 'date': '11/24', 'dir': -1, 'src': HPE_WF},
 {'stock': '베스트바이', 'firm': '제프리스', 'rating': '보유 유지', 'to': f"84→101달러({won(101)})", 'date': '11/24', 'dir': 1, 'src': BBY_J},
 {'stock': '딕스', 'firm': '트루이스트', 'rating': '보유 유지', 'to': f"128→150달러({won(150)})", 'date': '11/24', 'dir': 1, 'src': DKS_T},
 {'stock': '줌', 'firm': 'BofA', 'rating': '매수 유지', 'to': f"130→115달러({won(115)})", 'date': '11/24', 'dir': -1, 'src': ZM_ST},
 {'stock': '델', 'firm': '모건스탠리 · 씨티(실적 전)', 'rating': '목표 하향', 'to': f"403달러({won(403)}) · 550달러({won(550)})", 'date': '11/24', 'dir': -1, 'src': DELL_MC},
]
for r in issue['street']['rows']:
    t = r.pop('t', None); d_ = TD.get(t) if t else None
    if d_:
        tv = float(r['to'].split('달러')[0].replace(',', '').split('→')[-1])
        r['c'] = d_[4]; r['rx'] = d_[5]; r['gap'] = round((tv / d_[4] - 1) * 100)

# ── 내 종목 분석 ──────────────────────────────────────
WHY5 = {'NVDA': '전날 +31% 뒤 차익 실현·SEC 조사 보도', 'MU': 'BNP파리바 투자의견 하향', 'SNDK': '낸드 값 하락 전망·차익 실현', 'SNXX': '샌디스크 -11%를 2배로',
        'SOXL': '반도체 -8%를 3배로 -24.6%', 'SOXX': '반도체 ETF -8.3%', 'AMD': '반도체 동반 하락', 'INTC': '반도체 차익 실현·파운드리 적자 부담',
        'STX': '저장장치 동반 하락', 'WDC': '저장장치 동반 하락', 'SMCI': 'HPE 이익률 경고 여파', 'AVGO': '반도체 하락 속 -4%',
        'TSM': '반도체 동반 하락', 'QQQ': '나스닥100 -2.0%', 'TQQQ': '나스닥100 -2%를 3배로', 'MSTR': f'비트코인 6만 달러({won(60000)}) 아래',
        'COIN': '비트코인 약세', 'OKLO': '원전주 전날 반등 되돌림', 'RKLB': '우주주 차익 실현', 'ASTS': '우주주 차익 실현',
        'LLY': '헬스케어로 돈 이동·인수 소식', 'NKE': '딕스 실적에서 풋락커 호조', 'CRWD': '전날 급락 뒤 소폭 반등', 'ORCL': '기술주 약세'}
TN5 = {
 'NVDA': {'y': [(f"하루 {g('NVDA'):+.2f}%, 155.38달러({won(155.38)}) · 시가총액 약 2,400억 달러({jo(2400)}) 반납", FOOL_NV), ('황 CEO 직원 회의에서 사과, 치료 중이라고 밝혀', NV_TH2), (f'번스타인 시장수익률 상회 상향 · 적정 주가 200달러({won(200)})', BERN)],
          't': [('SEC 회계 조사 보도 · 12/1 의회 면담', NV_SEC)]},
 'MU': {'y': [(f'BNP파리바 중립 하향, 적정 주가 1,700→775달러({won(775)})', MU_F), ("BofA '반도체 전망 하향이 시작됐다'", BOFA_MU)], 't': []},
 'SNDK': {'y': [('트렌드포스 내년 1분기 낸드 계약가 하락 전망 · Form 144 내부자 매도 신고', SNDK_I)], 't': []},
 'SNXX': {'y': [('기초자산 샌디스크 -11.1%를 2배로 반영', SNDK_I)], 't': []},
 'SOXL': {'y': [(f"반도체 지수 {SOX:+.2f}%를 3배로 받아 하루 {qc('SOXL'):+.2f}%", Y('SOXL')), ('수리수리진타리 ⑨ 카드 새로 켜짐(B+)', 'https://stock.jintar.co.kr/c/9/')], 't': [('오늘 밤 PCE 물가 · 목요일 휴장', CAL_INV)]},
 'AMD': {'y': [('반도체 차익 실현 속 -8.9% · 헌터브룩 공매도 건 재거론', AMD_Y)], 't': []},
 'INTC': {'y': [(f'파운드리 영업손실 18.5억 달러({eok(18.5)}) · 내년 잉여현금흐름 플러스 어렵다는 CFO 발언 재부각', INTC_F)], 't': []},
 'WDC': {'y': [('회사 악재 없이 AI 저장장치 차익 실현', WDC_I)], 't': []},
 'STX': {'y': [('저장장치·메모리 동반 하락', MEM_W)], 't': []},
 'MSTR': {'y': [(f'비트코인 6만 달러({won(60000)}) 아래 · 2024년 초 이후 최저', BTC_CD)], 't': []},
 'COIN': {'y': [('비트코인 약세, 11월 현물 ETF 유출 사상 최대', BTC_CD)], 't': []},
 'RKLB': {'y': [('우주주 전날 반등 되돌림 · 스페이스X-테슬라 합병 협상 보도', SPACE_W)], 't': []},
 'ASTS': {'y': [('우주주 차익 실현', SPACE_W)], 't': []},
 'OKLO': {'y': [('원전주 전날 반등 되돌림', OKLO_W)], 't': []},
 'LLY': {'y': [(f'항암 신약 회사 로큐스23 최대 7.25억 달러({eok(7.25)}) 인수', LLY_I)], 't': []},
 'NKE': {'y': [('딕스 실적에서 풋락커 매장 판매 4% 넘게 증가', NKE_Y)], 't': []},
 'QQQ': {'y': [('나스닥100 하루 -1.99%', STL)], 't': [('수리수리진타리 ① 급락 초입 신호(B+) 진행 중', 'https://stock.jintar.co.kr/c/1/')]},
}
REASON = {
 'NVDA': '전날 31% 오른 뒤 하루 5.9% 되밀렸습니다. 번스타인이 등급을 올렸지만, SEC 조사 보도와 의회 면담 일정이 남아 있습니다.',
 'MU': 'BNP파리바가 2027년 중반부터 메모리 공급과 수요가 비슷해진다며 목표가를 절반 넘게 낮추자 11% 내렸습니다.',
 'SNDK': '분할 뒤 첫 반등 다음 날 11.1% 내렸습니다. 내년 1분기 낸드 계약가 하락 전망이 다시 거론됐습니다.',
 'SOXL': '반도체 지수를 하루 3배로 따라가는 상품이라 어제 하루 24.6% 내렸습니다. 이틀 새 +40%와 -25%를 오갔습니다.',
 'QQQ': '나스닥100 ETF는 하루 2.0% 내려 1달 전보다 10% 넘게 낮습니다.',
}
HL5 = {
 'NVDA': '+31% 다음 날 -5.9%', 'SOXL': '하루 -24.6%, 이틀 새 +40%·-25%', 'MU': 'BNP 하향에 -11%', 'SNDK': '하루 -11.1%, 낸드 값 걱정',
 'SNXX': '샌디스크 -11%를 2배로 -21%', 'AMD': '-8.9%, 반도체 동반 약세', 'INTC': '-8.2%, 파운드리 적자 부담', 'SOXX': '하루 -8.3%, 전날 반등 절반 반납',
 'QQQ': '하루 -2.0%', 'MSTR': f'비트코인 6만 달러({won(60000)}) 아래, -8.1%', 'NKE': '딕스 실적 덕에 +5.9%', 'LLY': '헬스케어 강세 +3.2%',
}
for q in issue['quotes']['list']:
    t = q['t']
    q['why'] = WHY5.get(t, '')
    n = TN5.get(t, {'y': [], 't': []}); q['news'] = {'y': [{'t': a, 'u': b} for a, b in n['y']], 't': [{'t': a, 'u': b} for a, b in n['t']]}
    q['ai'] = (REASON[t] + ' ' if t in REASON else '') + ns['auto_ai'](q)
    q['h'] = HL5.get(t) or ns['auto_h'](q)
issue['quotes']['asof'] = CLOSE
issue['quotes']['default'] = ['NVDA']

# ── 수리수리진타리 (stock.jintar.co.kr, c/latest.json 11/25 05:20 KST 판) ──
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
    nlab = '어제 종가' if c['n'] in q_ else '카드 시세(05:20 KST)'
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
 'u': JL_U, 'asof': f"2026-11-24 장 종료 가격 · 카드 내용은 {JL['time']} KST 판"}

# ── 1면 두 번째 기사 ─────────────────────────────────
dl = TD['DELL']
issue['top2'] = {
 'kicker': '두 번째 큰 뉴스 · 장 마감 후 실적',
 'title': f"델, AI 수주잔고 1,323억 달러({jo(1323)})…연매출 전망 2,020억 달러로 상향",
 'img': 'img/2026-11-25-top2.jpg',
 'points': [
  {'t': f"3분기 매출은 549.4억 달러({jo(549.4)})로 1년 전보다 103% 늘었고, 조정 주당순이익은 9.45달러({won(9.45)})였습니다. 시장 예상(매출 506억 달러, 주당 6.63달러 · {won(6.63)})을 크게 넘었습니다.", 'src': DELL_FF},
  {'t': f"분기 AI 서버 신규 주문이 602억 달러({jo(602)}), 쌓인 AI 수주잔고가 1,323억 달러로 사상 최대입니다. 지난 분기 말 950억 달러({jo(950)})에서 늘었습니다.", 'src': DELL_PR},
  {'t': f"연간 매출 전망을 1,920억 달러에서 2,020억 달러({jo(2020)})로, AI 서버 매출 전망을 740억에서 780억 달러로 올렸습니다. 4분기 매출 전망은 563억 달러({jo(563)})입니다.", 'src': DELL_PR},
  {'t': f"정규장에서는 HPE의 이익률 경고 여파로 {dl[5]:+.2f}% 내려 {dl[4]}달러({won(dl[4])})였고, 발표 직후 시간외에서 1.79% 오른 300.57달러(미 동부 16:37)로 반등했습니다.", 'src': DELL_FF},
  {'t': f'250억 달러({jo(250)}) 규모의 자사주 매입 한도를 새로 승인했습니다.', 'src': DELL_PR},
 ],
 'risks': [
  {'t': f'4분기 AI 서버 매출 전망(약 234억 달러, {jo(234)})이 3분기보다 약 6% 많은 데 그쳐, 성장 속도가 정점을 지났다는 해석도 나왔습니다.', 'src': DELL_TECHI},
  {'t': f'재고가 294억 달러({jo(294)})로 연초 104억 달러의 세 배 가까이 늘었고, 메모리 값 상승이 이익률을 누를 수 있다는 지적이 있습니다.', 'src': DELL_247},
 ],
 'why': 'AI 서버 주문이 꺾였는지 보여줄 첫 대형 실적이었는데, 주문과 수주잔고가 오히려 사상 최대였습니다. 반도체가 밀린 날 나온 숫자라 오늘 밤 AI 하드웨어 분위기를 가를 수 있습니다.',
 'watch': [f'정규장에서 시간외 반등(300달러 안팎, {won(300)})이 이어지는지', '메모리 값 상승이 4분기 이익률에 주는 영향', '수주잔고 중 다음 4분기에 실제 출하되는 몫(회사는 밝히지 않음)'],
 'src': [{'t': '델 실적 발표(BusinessWire)', 'u': DELL_PR}, {'t': '델 IR', 'u': DELL_IR}, {'t': 'FinanceFeeds', 'u': DELL_FF}, {'t': 'Investing.com', 'u': DELL_INV}, {'t': 'Motley Fool', 'u': DELL_FOOL}],
 'react': [
  {'p': '스톡트윗', 't': '개인 투자자 분위기 "매우 낙관", 글 수는 약 160% 늘어 "매우 많음"', 'u': DELL_ST},
  {'p': 'X', 't': '"델이 3분기를 박살냈다"며 예상 대비 숫자를 나열한 글이 빠르게 퍼짐', 'u': DELL_X1},
  {'p': 'X', 't': '매출·주당순이익·연간 전망이 모두 예상을 넘었다는 요약 게시물', 'u': DELL_X2},
  {'p': '회사', 't': '델 공식 계정: 매출·주당순이익·3분기 영업현금흐름 모두 사상 최대', 'u': DELL_XD},
  {'p': 'TV', 't': "야후 파이낸스 소치: '압도적인 분기', 시장이 HPE를 잘못 읽었다", 'u': DELL_SOZ},
  {'p': '분석', 't': 'TipRanks 집계: 긍정 의견 14·중립 7, 평균 적정 주가는 종가보다 크게 높음', 'u': DELL_TR},
  {'p': '분석', 't': '모건스탠리·씨티는 실적 직전 적정 주가를 낮춰 잡았음', 'u': DELL_MC},
  {'p': '분석', 't': f'에버코어는 AI 인프라 조정을 이유로 실적 전 적정 주가를 650→400달러({won(400)})로 낮춤', 'u': DELL_TS},
  {'p': '전문가', 't': 'Techi: 4분기 AI 서버 성장 둔화가 보인다며 정점 가능성 경계', 'u': DELL_TECHI},
  {'p': '전문가', 't': "모틀리풀: 이익 대비 10배 안팎이라 싸 보이지만 재고·빚·부품값은 위험", 'u': DELL_FOOL},
  {'p': '전문가', 't': "StreetSignal: 콜에서 'AI 투자 정점론'을 뒷받침할 근거는 거의 없었다", 'u': DELL_SS},
  {'p': '시장', 't': '정규장 급락은 HPE 이익률 경고·메모리 값·차익 실현이 겹친 결과라는 분석', 'u': DELL_TK},
 ],
}

issue['site_v'] = 11
issue['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 시세는 CNBC 일봉(11/24 종가) 기준이며, 시간외 가격·증권사·전문가 의견은 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
issue.pop('lead', None); issue['lead'] = ''
json.dump(issue, open(f"drafts/{issue['date']}.json", 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', issue['date'], issue['no'])

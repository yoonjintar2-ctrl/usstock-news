"""제7호(2026-11-27 금, 휴장일 호) — 미국 11/26(목) 추수감사절 휴장. 지수·차트·트리맵은 11/25 종가 그대로('휴장' 표기),
1면은 휴장 중 선물·아시아 증시. 숫자는 아래 출처(검색 결과 제목·요약)로 확인된 것만."""
import json
D = '2026-11-27'
d = json.load(open('drafts/2026-11-26.json', encoding='utf-8'))
FX = d['fx']['usdkrw']['v']
CHR = 'https://thecompanychronicle.com/story/before-the-bell-thanksgiving-november-26-2026'
JA = 'https://journalarta.com/en/2026/11/26/sp-500-futures-edge-higher-as-tariff-relief-offsets-nvidia-risks/'
JA2 = 'https://journalarta.com/en/2026/11/26/sp-500-futures-slip-as-tech-selloff-splits-wall-street/'
AIR = 'https://www.airnews.in/articles/f3481d6e23-nyse-and-nasdaq-close-for-thanksgiving-following-1-270-point-dow-intraday-rebound'
FIN = 'https://finviz.com/news/239512/stock-futures-climb-ahead-of-thanksgiving-break'
GR = 'https://www.goodreturns.in/news/us-stock-market-holiday-today-november-26-dow-nasdaq-s-p-500-shut-thanksgiving-wall-street-outlook-1549901.html'
MLQ = 'https://mlq.ai/news/taiex-jumps-25-and-nikkei-gains-09-as-asian-chip-stocks-rebound/'
AP = 'https://www.click2houston.com/business/2026/11/26/asian-shares-rebound-led-by-ai-stocks-after-wall-street-pares-sharp-losses/'
F24 = 'https://www.france24.com/en/live-news/20261126-asian-stocks-enjoy-another-bounce-as-tech-holds-court'
BNN = 'https://www.bnnbloomberg.ca/markets/2026/11/26/global-stocks-rise-and-tech-shares-rebound-as-us-closes-for-thanksgiving/'
GOLD = 'https://www.fxleaders.com/news/2026/11/26/gold-price-forecast-xau-usd-tests-3600-on-thanksgiving-short-covering/'
ATFX = 'https://www.atfxcapital.com/en/analysis/market-news/20261126-daily-market-highlight'
FXS = 'https://www.fxstreet.com/cryptocurrencies/news/bitcoin-and-gold-price-forecast-why-daily-technicals-flash-sell-amid-hawkish-fed-and-thanksgiving-liquidity-202611261718'
BIGGO = 'https://finance.biggo.com/news/bef38756-5740-4079-8784-f2d501914c9b'
IBT = 'https://www.ibtimes.com.au/us-markets-closed-thanksgiving-2026-1879444'
SFT = 'https://startupfortune.com/nasdaq-futures-sink-over-2-as-the-dow-sits-at-50000-before-thanksgiving/'

d.update(date=D, no=7, weekday='금', session='2026-11-26(목) 미국 휴장 · 추수감사절 (시세는 11/25 종가)')
d['fx']['usdkrw']['asof'] = '2026-11-26 06:40 KST 시세(휴장으로 갱신 없음)'
d['top'] = {
 'kicker': '휴장일 특집 · 선물이 말해 주는 것',
 'title': '추수감사절 휴장…S&P 500 선물 +0.7%, 수요일 급락 뒤 안정 찾나',
 'img': f'img/{D}-top.jpg',
 'points': [
  {'t': '미국 증시는 11/26(목) 추수감사절로 쉬었습니다. 지수·차트는 11/25(수) 종가 그대로입니다.', 'src': GR},
  {'t': '휴장 중 S&P 500 선물은 0.7% 안팎 올랐고 유럽 증시도 올랐다고 보도됐습니다.', 'src': CHR},
  {'t': 'S&P 500 선물은 7,225.50 근처에서 거래됐습니다. 관세 걱정이 조금 누그러진 점이 거론됐습니다.', 'src': JA},
  {'t': '수요일 다우는 장중 저점에서 1,270포인트 되오르며 끝났고, 그 반등이 선물로 이어졌다는 해석입니다.', 'src': AIR},
  {'t': '나스닥 100·다우 선물의 정확한 등락률은 확인 중입니다. 휴장일 선물은 거래가 얇아 금요일 현물 개장 때 달라질 수 있습니다.', 'src': FIN}],
 'risks': [
  {'t': '같은 날 일부 보도는 기술주 선물이 약하고 다우 선물만 버틴다고 전해, 업종별로 방향이 엇갈렸습니다.', 'src': JA2},
  {'t': '연휴 거래량이 적어 작은 주문에도 값이 크게 움직일 수 있습니다. 엔비디아·AI 신용 걱정은 그대로입니다.', 'src': FXS}],
 'why': '수요일 장중 급락을 대부분 되돌린 뒤 하루를 쉬었습니다. 선물이 오르면 금요일 짧은 장에서 반등이 이어질 수 있지만, 거래가 얇아 방향을 확정하긴 이릅니다.',
 'watch': ['금요일 개장 직후 나스닥 100 선물이 수요일 종가 위를 지키는지', '반도체 ETF(SOXX)가 수요일 장중 저점을 다시 시험하는지', '조기 폐장(한국 토요일 03:00) 전 거래량'],
 'src': [{'t': 'Company Chronicle', 'u': CHR}, {'t': 'JournalArta', 'u': JA}, {'t': 'AirNews', 'u': AIR}, {'t': 'Goodreturns', 'u': GR}],
 'react': [
  {'p': '시장', 't': '휴장 앞두고 선물이 올라 "숨 고르기 반등" 기대가 나옴', 'u': FIN},
  {'p': '분석', 't': '관세 걱정 완화가 엔비디아 위험을 상쇄한다는 해석', 'u': JA},
  {'p': '분석', 't': '기술주 선물은 약하고 다우만 버텨 업종별로 갈린다는 시각', 'u': JA2},
  {'p': '시장', 't': '수요일 장중 급락을 되돌린 반등을 긍정적으로 보는 분위기', 'u': AIR},
  {'p': '분석', 't': '휴장 전날엔 나스닥 선물이 2% 넘게 빠지기도 해 변동성 경계', 'u': SFT},
  {'p': '분석', 't': '연휴 얇은 거래 탓에 기술적 신호가 약세를 가리킨다는 경고', 'u': FXS}]}
d['top2'] = {
 'kicker': '두 번째 큰 뉴스 · 아시아 반도체',
 'title': '아시아 반도체 반등…대만 +2.5%, 일본 닛케이 +0.9%',
 'img': f'img/{D}-top2.jpg',
 'points': [
  {'t': '미국이 쉬는 동안 아시아 증시는 AI·반도체주를 중심으로 반등했습니다.', 'src': AP},
  {'t': '대만 가권지수는 2.5% 올랐고 일본 닛케이는 0.9% 올랐습니다.', 'src': MLQ},
  {'t': '미국 수요일 장이 장중 급락을 대부분 되돌린 것이 아시아 반등의 계기로 꼽혔습니다.', 'src': BNN}],
 'risks': [{'t': '전날 아시아는 AI주 급락으로 대부분 내렸습니다. 이틀 사이 방향이 바뀌어 아직 흔들리는 장입니다.', 'src': 'https://www.click2houston.com/business/2026/11/25/asian-stocks-mostly-decline-as-ai-shares-tumble-after-a-retreat-on-wall-street/'}],
 'why': '대만·일본 반도체주는 엔비디아·마이크론 같은 미국 반도체주와 함께 움직이는 일이 많아, 금요일 미국 반도체 흐름을 미리 보여 주는 신호로 볼 수 있습니다.',
 'watch': ['금요일 미국 반도체 ETF 출발', '한국 반도체주(삼성전자·SK하이닉스) 금요일 흐름'],
 'src': [{'t': 'MLQ', 'u': MLQ}, {'t': 'AP(Click2Houston)', 'u': AP}, {'t': 'BNN 블룸버그', 'u': BNN}],
 'react': [
  {'p': '시장', 't': '"기술주가 다시 주도권" — 아시아가 또 반등했다는 평', 'u': F24},
  {'p': '분석', 't': 'AI주가 이끈 반등, 미국 낙폭 축소가 계기라는 해석', 'u': AP},
  {'p': '시장', 't': '미국 휴장 속 세계 증시가 오르고 기술주가 돌아왔다는 분위기', 'u': BNN},
  {'p': '분석', 't': '대만·일본 칩주 반등 폭이 커 "저가 매수" 성격이라는 시각', 'u': MLQ}]}
d['news'] = [
 {'tag': '금', 'img': f'img/{D}-gold.jpg', 'title': '금값, 휴장 중 온스당 3,600달러(약 484만 원) 시험', 'line': '얇은 거래 속에 공매도 되사기가 들어오며 금값이 V자로 반등해 3,600달러(약 484만 원) 선을 시험했다고 보도됐습니다.', 'src': [{'t': 'FX Leaders', 'u': GOLD}, {'t': 'ATFX', 'u': ATFX}]},
 {'tag': '일정', 'img': f'img/{D}-bf.jpg', 'title': '금요일은 미 동부 13:00 조기 폐장(한국 토요일 03:00)', 'line': '블랙프라이데이 짧은 장입니다. 거래가 얇아 움직임이 커질 수 있습니다.', 'src': [{'t': 'BigGo', 'u': BIGGO}, {'t': 'IBTimes', 'u': IBT}]},
 {'tag': '코인', 'img': f'img/{D}-btc.jpg', 'title': '비트코인·금, 일봉 기술 신호는 약세', 'line': '연준의 매파적 분위기와 연휴 얇은 거래로 단기 기술 지표가 약세를 가리킨다는 분석이 나왔습니다.', 'src': [{'t': 'FXStreet', 'u': FXS}]}]
d['schedule'] = [
 {'kst': '11/27(금) 23:30', 'type': '개장', 'name': '미국 증시 금요일 개장(블랙프라이데이)', 'star': 2, 'why': '휴장 뒤 첫 거래. 선물 흐름이 현물로 이어지는지.', 'src': IBT},
 {'kst': '11/28(토) 03:00', 'type': '단축', 'name': '조기 폐장(미 동부 13:00)', 'star': 2, 'why': '거래가 얇아 움직임이 커질 수 있습니다.', 'src': BIGGO}] + [s for s in d['schedule'] if not s['kst'].startswith('11/26') and not s['kst'].startswith('11/28(토) 03')]
d['calendar']['today'] = D
days = [x for x in d['calendar']['days'] if x['d'] != D]
days.append({'d': D, 'ev': [{'k': '휴장', 't': '추수감사절 · 선물 +0.7%'}]})
d['calendar']['days'] = sorted(days, key=lambda x: x['d'])
d['chart_summary'] = '**휴장**으로 차트는 11/25(수) 종가 그대로입니다. ' + d['chart_summary']
d['disclaimer'] = '투자 권유가 아니며, 투자 판단과 책임은 본인에게 있습니다. 미국 11/26 휴장으로 시세는 CNBC 일봉(11/25 종가) 기준이며, 선물·아시아 증시는 보도된 내용을 옮긴 것입니다. 샌디스크는 8:1 액면분할을 반영한 가격입니다.'
d['lead'] = ''
json.dump(d, open(f'drafts/{D}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', D, d['no'])

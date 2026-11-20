"""시세 자동 수집 — GitHub Actions(인터넷 가능)에서 돌려 data/ 아래 지면용 파일을 만든다.
  python scripts/fetch_market.py            (마지막 정규장 기준)

만드는 파일(기존 크롬 수집과 같은 형식):
  data/summary.txt      SYM|date,close,prev,chg,open,high,low,ma20,...,w1,m1,m3
  data/raw_series.txt   D|MMDD...(120일) / SYM|종가×배율|거래량(10만 주)|MA20|MA50|MA200 (3일 간격 40개)
  data/idx_candles.json 지수 캔들 120일 압축(OHLC+이평 5개, 255=없음)
  data/tickers_mini.json 종목 22일 OHLC 압축 + 지지·저항·이평·거래량 배수
  data/movers_raw.txt   t,MM-DD,close,chg,w1,m1,hi,a50,a200,rsi
  data/sp500_top100.txt t,비중,등락,이름;...   (slickcharts)
  data/tm_daily.json    트리맵 팝업용 [date,o,h,l,c,chg,vol,vr,w1,m1,ma20,ma50,hi3m,lo3m,n]
  data/sndk_daily.json  일봉이 짧게 나오는 종목은 1시간봉을 묶은 일봉
  data/fg.json          CNN 공포·탐욕 지수
  data/market_meta.json 수집 시각·마지막 거래일
숫자는 받아 온 값으로만 계산한다.
"""
import base64, json, re, time, datetime as dt
import requests, sys

S = requests.Session()
S.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36'
SUMMARY = ['^IXIC', '^GSPC', '^DJI', 'SOXX', 'QQQ', 'SPY', '^VIX', '^TNX', 'DX-Y.NYB', 'KRW=X', 'CL=F', '^SOX', '^RUT', 'GC=F', 'NVDA', 'SNDK', 'MU']
IDX = {'^IXIC': (1, 'QQQ'), '^GSPC': (10, 'SPY'), 'SOXX': (100, 'SOXX')}
MOVERS = ('AAPL ADBE AMD AMZN ARM ASML ASTS AVGO BA BAC BRK-B COIN COST CRM CRWD CVX DIS GLD GOOGL HOOD IBIT INTC IONQ JNJ JPM KO LLY MA MCD '
          'META MSFT MSTR MU NFLX NKE NOW NVDA OKLO ORCL PANW PEP PFE PLTR QCOM QQQ RIVN RKLB SBUX SCHD SHOP SMCI SNDK SNOW SOFI SOXL SOXX SPY STX '
          'TLT TQQQ TSLA TSM UBER UNH V VOO WDC WMT XOM SPCX SNXX').split()


FAIL = {}
CN = {'^IXIC': '.IXIC', '^GSPC': '.SPX', '^DJI': '.DJI', '^VIX': '.VIX', '^TNX': 'US10Y', 'DX-Y.NYB': '.DXY', 'KRW=X': 'KRW=',
      'CL=F': '@CL.1', 'GC=F': '@GC.1', '^SOX': '.SOX', '^RUT': '.RUT'}


def cnbc(sym, days=380):
    """CNBC 일봉(깃허브 러너에서 야후가 429로 막혀 기본 소스로 씀)."""
    from urllib.parse import quote
    c = CN.get(sym, sym.replace('-', '.'))
    end = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1); st = end - dt.timedelta(days=days)
    url = f"https://ts-api.cnbc.com/harmony/app/bars/{quote(c)}/1D/{st:%Y%m%d}000000/{end:%Y%m%d}000000/adjusted/EST5EDT.json"
    for k in range(3):
        try:
            r = S.get(url, timeout=25)
            if r.status_code != 200: FAIL[sym] = f'cnbc {r.status_code}'; time.sleep(2 * (k + 1)); continue
            rows = []
            for b in (r.json().get('barData') or {}).get('priceBars') or []:
                t = b['tradeTime']; cl = float(b['close'])
                rows.append([f'{t[:4]}-{t[4:6]}-{t[6:8]}', float(b['open']), float(b['high']), float(b['low']), cl, int(b.get('volume') or 0)])
            if rows: FAIL.pop(sym, None); return rows
            FAIL[sym] = 'cnbc empty'
        except Exception as e:
            FAIL[sym] = 'cnbc ' + repr(e)[:80]; time.sleep(2 * (k + 1))
    return []


def yahoo(sym, rng='1y', itv='1d'):
    for host in ('query1', 'query2'):
        try:
            r = S.get(f'https://{host}.finance.yahoo.com/v8/finance/chart/{sym}', params={'range': rng, 'interval': itv}, timeout=20)
            if r.status_code != 200: FAIL[sym] = f'yahoo {r.status_code}'; continue
            res = r.json()['chart']['result'][0]
            q = res['indicators']['quote'][0]
            rows = []
            for i, t in enumerate(res.get('timestamp') or []):
                if q['close'][i] is None: continue
                d = (dt.datetime.fromtimestamp(t, dt.timezone.utc) + dt.timedelta(hours=-5)).strftime('%Y-%m-%d') if itv != '1d' else \
                    dt.datetime.fromtimestamp(t + res['meta'].get('gmtoffset', 0), dt.timezone.utc).strftime('%Y-%m-%d')
                rows.append([d, q['open'][i], q['high'][i], q['low'][i], q['close'][i], q['volume'][i] or 0])
            return rows
        except Exception as e:
            FAIL[sym] = 'yahoo ' + repr(e)[:80]
    return []


def chart(sym, rng='1y', itv='1d'):
    if itv == '1d':
        rows = cnbc(sym)
        if len(rows) >= 30: return rows
    rows = yahoo(sym, rng, itv)
    if not rows: print('FAIL', sym, FAIL.get(sym), file=sys.stderr)
    return rows


def cnbc_today(syms):
    """CNBC 지수 일봉은 당일 봉이 늦게 붙는다 → 시세 화면(quote)의 당일 시가·고가·저가·현재가로 마지막 날을 채운다."""
    from urllib.parse import quote
    out = {}
    syms = list(syms)
    for i in range(0, len(syms), 30):
        part = syms[i:i + 30]; cs = [CN.get(x, x.replace('-', '.')) for x in part]
        url = ('https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=' + quote('|'.join(cs), safe='') +
               '&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=0&output=json')
        try:
            qs = S.get(url, timeout=25).json()['FormattedQuoteResult']['FormattedQuote']
        except Exception as e:
            print('quote 실패', e, file=sys.stderr); continue
        by = {q.get('symbol'): q for q in qs}
        num = lambda v: float(str(v).replace(',', '').replace('%', '')) if v not in (None, '', '--', 'UNCH') else None
        for x, c in zip(part, cs):
            q = by.get(c)
            if not q: continue
            try:
                d = (q.get('last_time') or '')[:10]
                o, h, l, c_ = num(q.get('open')), num(q.get('high')), num(q.get('low')), num(q.get('last'))
                v = int(num(q.get('volume')) or 0) if q.get('volume') else 0
                if d and c_ is not None: out[x] = [d, o or c_, h or c_, l or c_, c_, v]
            except Exception:
                pass
    return out


def patch_today(D):
    """마지막 일봉 날짜가 시세 화면 날짜보다 이르면 당일 봉을 붙인다."""
    q = cnbc_today(D.keys())
    for s, row in q.items():
        rows = D.get(s) or []
        if rows and row[0] > rows[-1][0]:
            rows.append(row); print('당일 봉 보충', s, row[0], file=sys.stderr)


def daily(sym):
    rows = chart(sym)
    if len(rows) < 30:  # 일봉이 깨진 종목(예: SNDK) → 1시간봉을 일봉으로
        by = {}
        for d, o, h, l, c, v in chart(sym, '3mo', '1h'):
            b = by.setdefault(d, [d, o, h, l, c, 0]); b[2] = max(b[2], h); b[3] = min(b[3], l); b[4] = c; b[5] += v
        if len(by) > len(rows): rows = list(by.values()); rows[0].append('h')
    return rows


avg = lambda a: sum(a) / len(a) if a else None
def ma(cl, n, i=None):
    i = len(cl) - 1 if i is None else i
    return avg(cl[i - n + 1:i + 1]) if i - n + 1 >= 0 else None
def rsi(cl, n=14):
    if len(cl) <= n: return None
    g = [max(cl[i] - cl[i - 1], 0) for i in range(1, len(cl))]; l = [max(cl[i - 1] - cl[i], 0) for i in range(1, len(cl))]
    ag, al = avg(g[:n]), avg(l[:n])
    for i in range(n, len(g)): ag = (ag * (n - 1) + g[i]) / n; al = (al * (n - 1) + l[i]) / n
    return 100 if al == 0 else 100 - 100 / (1 + ag / al)
pct = lambda a, b: (a / b - 1) * 100 if a is not None and b else None
r2 = lambda v, k=2: '' if v is None else f'{v:.{k}f}'


def summary_row(rows):
    cl = [r[4] for r in rows]; vo = [r[5] for r in rows]; L = rows[-1]; n = len(cl)
    hi52 = max(rows[-252:], key=lambda r: r[2]); lo52 = min(rows[-252:], key=lambda r: r[3])
    m20, m50, m200 = ma(cl, 20), ma(cl, 50), ma(cl, 200)
    vr = vo[-1] / avg(vo[-21:-1]) if vo[-1] and avg(vo[-21:-1]) else None
    back = lambda k: cl[-1 - k] if n > k else None
    vals = [L[0], r2(L[4]), r2(cl[-2]), r2(pct(L[4], cl[-2])), r2(L[1]), r2(L[2]), r2(L[3]), r2(m20), r2(m50), r2(m200),
            r2(ma(cl, 20, n - 2)), r2(ma(cl, 50, n - 2)), r2(ma(cl, 200, n - 2)), r2(hi52[2]), hi52[0], r2(lo52[3]), lo52[0], r2(rsi(cl), 1),
            str(vo[-1] or ''), str(round(avg(vo[-21:-1]))) if avg(vo[-21:-1]) else '', r2(vr),
            r2(max(r[2] for r in rows[-20:])), r2(min(r[3] for r in rows[-20:])), r2(max(r[2] for r in rows[-60:])), r2(min(r[3] for r in rows[-60:])),
            r2(pct(L[4], back(5))), r2(pct(L[4], back(21))), r2(pct(L[4], back(63)))]
    return ','.join(vals)


def pack(vals, mn, mx, top=254, null=True):
    out = bytearray()
    for v in vals:
        out.append(255 if (v is None and null) else max(0, min(top, round((v - mn) / (mx - mn) * top))) if v is not None else 0)
    return base64.b64encode(bytes(out)).decode()


def main():
    D = {}
    for s in sorted(set(SUMMARY + MOVERS + [v[1] for v in IDX.values()])):
        D[s] = daily(s); time.sleep(0.3)
    patch_today(D)
    last = D['SPY'][-1][0]
    # summary
    head = 'sym|date,close,prev,chg,open,high,low,ma20,ma50,ma200,ma20p,ma50p,ma200p,hi52,hi52d,lo52,lo52d,rsi,vol,vol20,volr,res20,sup20,res60,sup60,w1,m1,m3'
    lines = [head] + [f'{s}|{summary_row(D[s])}' for s in SUMMARY if len(D.get(s, [])) > 25]
    open('data/summary.txt', 'w').write('\n'.join(lines) + '\n')
    # 지수: raw_series + 캔들 압축
    ref = D['SPY'][-120:]; dates = [r[0] for r in ref]
    rs = ['D|' + ' '.join(d[5:7] + d[8:10] for d in dates)]; C3 = {}
    for s, (sc, vsym) in IDX.items():
        rows = {r[0]: r for r in D[s]}; vrows = {r[0]: r for r in D[vsym]}
        cl_all = [r[4] for r in D[s]]; idx = {r[0]: i for i, r in enumerate(D[s])}
        sel = [rows.get(d) for d in dates]
        mas = {m: [ma(cl_all, m, idx[d]) if d in idx else None for d in dates] for m in (5, 20, 60, 120, 200)}
        vol = [vrows[d][5] if d in vrows else 0 for d in dates]
        rs.append('|'.join([s, ' '.join(str(round(r[4] * sc)) if r else '0' for r in sel), ' '.join(str(round(v / 1e5)) for v in vol)] +
                           [' '.join(str(round((mas[m][i] or 0) * sc)) for i in range(0, 120, 3)) for m in (20, 50 if False else 60, 200)]))
        allv = [x for r in sel if r for x in r[1:5]] + [v for m in mas.values() for v in m if v is not None]
        mn, mx = min(allv), max(allv)
        flat = []
        for i, r in enumerate(sel):
            flat += (r[1:5] if r else [None] * 4) + [mas[m][i] for m in (5, 20, 60, 120, 200)]
        vmax = max(vol) or 1
        C3[s] = {'d0': dates[0], 'd1': dates[-1], 'n': 120, 'mn': round(mn, 4), 'mx': round(mx, 4), 'mas': [5, 20, 60, 120, 200],
                 'b': pack(flat, mn, mx), 'vb': base64.b64encode(bytes(round(v / vmax * 255) for v in vol)).decode(), 'vmax': vmax}
    # raw_series 의 MA50 칸은 기존 파일과 같게 50일선으로 다시 계산
    for k, s in enumerate(IDX):
        sc = IDX[s][0]; cl_all = [r[4] for r in D[s]]; idx = {r[0]: i for i, r in enumerate(D[s])}
        p = rs[k + 1].split('|'); p[4] = ' '.join(str(round((ma(cl_all, 50, idx[dates[i]]) or 0) * sc)) if dates[i] in idx else '0' for i in range(0, 120, 3))
        rs[k + 1] = '|'.join(p)
    open('data/raw_series.txt', 'w').write('\n'.join(rs) + '\n')
    json.dump({'idx': C3}, open('data/idx_candles.json', 'w'))
    # 종목: movers_raw + 미니 차트
    mv, mini = [], {}
    for t in MOVERS:
        rows = D.get(t) or []
        if len(rows) < 25: mini[t] = None; continue
        cl = [r[4] for r in rows]; vo = [r[5] for r in rows]; L = rows[-1]
        hi52 = max(r[2] for r in rows[-252:])
        m50, m200 = ma(cl, 50), ma(cl, 200)
        mv.append(','.join([t, L[0][5:], f'{L[4]:.2f}', f'{pct(L[4], cl[-2]):.2f}', f'{pct(L[4], cl[-6]):.1f}', f'{pct(L[4], cl[-22]):.1f}' if len(cl) > 22 else '0',
                            f'{pct(L[4], hi52):.1f}', '1' if m50 and L[4] > m50 else '0', '1' if m200 and L[4] > m200 else '0', str(round(rsi(cl) or 50))]))
        last22 = rows[-22:]; mn = min(r[3] for r in last22); mx = max(r[2] for r in last22)
        mini[t] = [round(mn, 4), round(mx, 4), pack([v for r in last22 for v in r[1:5]], mn, mx, 255, False),
                   round(max(r[2] for r in rows[-20:]), 2), round(min(r[3] for r in rows[-20:]), 2),
                   *(round(x, 2) if x else None for x in (ma(cl, 5), ma(cl, 20), ma(cl, 50), ma(cl, 200))),
                   round(vo[-1] / avg(vo[-21:-1]), 2) if avg(vo[-21:-1]) else None]
    open('data/movers_raw.txt', 'w').write('\n'.join(mv) + '\n')
    json.dump(mini, open('data/tickers_mini.json', 'w'))
    if D.get('SNDK'): json.dump([[r[0], *(round(x, 2) for x in r[1:5]), r[5]] for r in D['SNDK'][-66:]], open('data/sndk_daily.json', 'w'))
    # S&P 500 비중 상위 100 (slickcharts) + 트리맵 팝업
    tm = []
    try:
        html = S.get('https://www.slickcharts.com/sp500', timeout=20).text
        for m in re.finditer(r'<tr>\s*<td>(\d+)</td>\s*<td[^>]*><a[^>]*>([^<]+)</a></td>\s*<td[^>]*><a[^>]*>([^<]+)</a></td>\s*<td>([\d.]+)%</td>.*?<td[^>]*>\s*(?:<[^>]+>)*\s*([-\d.]+)\s*(?:</[^>]+>)*\s*</td>\s*<td[^>]*>\s*(?:<[^>]+>)*\s*\(?([-\d.]+)%', html, re.S):
            if len(tm) >= 100: break
            tm.append((m.group(3).strip(), float(m.group(4)), float(m.group(6)), __import__('html').unescape(m.group(2).strip()).replace(';', ' ')))
    except Exception as e:
        print('slickcharts 실패', e)
    if len(tm) >= 50:
        open('data/sp500_top100.txt', 'w').write(';'.join(f'{t},{w:.2f},{c:.2f},{n}' for t, w, c, n in tm) + '\n')
        td = {}
        for t, *_ in tm:
            ys = t.replace('.', '-'); rows = D.get(ys) or daily(ys); time.sleep(0.3)
            if len(rows) < 25: td[ys] = 'ERR'; continue
            rows = rows[-63:]; n = len(rows); cl = [r[4] for r in rows]; vo = [r[5] for r in rows]; L = rows[-1]
            td[ys] = [L[0], *(round(x, 2) for x in L[1:5]), round(pct(L[4], cl[-2]), 2), L[5], round(L[5] / avg(vo[-21:-1]), 2) if avg(vo[-21:-1]) else None,
                      round(pct(L[4], cl[-6]), 1), round(pct(L[4], cl[max(0, n - 22)]), 1), round(ma(cl, 20), 2), round(ma(cl, 50), 2),
                      round(max(r[2] for r in rows), 2), round(min(r[3] for r in rows), 2), n]
        json.dump(td, open('data/tm_daily.json', 'w'))
    # 공포·탐욕
    try:
        fg = S.get('https://production.dataviz.cnn.io/index/fearandgreed/graphdata', timeout=20, headers={'Referer': 'https://edition.cnn.com/'}).json()
        json.dump({'score': round(fg['fear_and_greed']['score'], 1), 'rating': fg['fear_and_greed']['rating'],
                   'put_call': fg.get('put_call_options', {}).get('data', [{}])[-1].get('y'), 'ts': fg['fear_and_greed']['timestamp']},
                  open('data/fg.json', 'w'), ensure_ascii=False)
    except Exception as e:
        print('공포탐욕 실패', e)
    json.dump({'fetched_utc': dt.datetime.utcnow().isoformat(timespec='seconds'), 'last_session': last,
               'missing': [s for s, r in D.items() if len(r) < 25], 'via': 'cnbc', 'fail': FAIL}, open('data/market_meta.json', 'w'), ensure_ascii=False)
    print('마지막 거래일', last, '빠진 종목', [s for s, r in D.items() if len(r) < 25])


if __name__ == '__main__':
    main()

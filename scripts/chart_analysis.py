"""차트 분석 — 일봉 데이터에서 이동평균·지지/저항·거래량·RSI 를 계산해 지면용 'charts' 블록을 만든다.
  python3 scripts/chart_analysis.py data/raw_series.txt data/summary.txt > data/charts.json

입력 형식(브라우저에서 야후 파이낸스 일봉을 받아 만든 압축 텍스트)
  raw_series.txt : D|MMDD ...  /  SYM|종가...|거래량(10만 주)...|MA20(3일 간격)|MA50|MA200
  summary.txt    : SYM|date,close,prev,chg,... (헤더 첫 줄)
숫자를 지어내지 않는다: 모든 문장은 계산값에서만 만든다. 매수·매도 권유 표현 금지.
"""
import json, sys

CFG = {  # sym: (이름, 배율, 거래량 기준 ETF, 단위)
    '^IXIC': ('나스닥 종합', 1, 'QQQ', 'pt'),
    '^GSPC': ('S&P 500', 10, 'SPY', 'pt'),
    'SOXX': ('반도체 ETF SOXX', 100, 'SOXX', '달러'),
}
SRC = 'https://finance.yahoo.com/quote/{}/history'


def load(raw_p, sum_p, year='2026'):
    lines = open(raw_p, encoding='utf-8').read().strip().split('\n')
    dates = [f'{year}-{d[:2]}-{d[2:]}' for d in lines[0].split('|')[1].split()]
    series = {}
    for ln in lines[1:]:
        sym, c, v, m20, m50, m200 = ln.split('|')
        sc = CFG[sym][1]
        f = lambda s: [int(x) / sc if x != '0' else None for x in s.split()]
        series[sym] = {'close': f(c), 'vol': [int(x) / 10 for x in v.split()],  # 백만 주
                       'ma20': f(m20), 'ma50': f(m50), 'ma200': f(m200)}
    head, *rows = open(sum_p, encoding='utf-8').read().strip().split('\n')
    keys = head.split('|')[1].split(',')
    summ = {}
    for r in rows:
        sym, vals = r.split('|')
        o = {}
        for k, v in zip(keys, vals.split(',')):
            try: o[k] = float(v) if v not in ('',) and k not in ('date', 'hi52d', 'lo52d') else (v or None)
            except ValueError: o[k] = v
        summ[sym] = o
    return dates, series, summ


def pct(a, b): return (a / b - 1) * 100


def fmt(x, unit):
    return f'{x:,.2f}' if unit == '달러' else f'{x:,.0f}'


def analyse(sym, dates, s, S, V):
    name, _, vsym, unit = CFG[sym]
    c = S['close']; ma20, ma50, ma200 = S['ma20'], S['ma50'], S['ma200']
    hi, lo = S['hi52'], S['lo52']
    dd = pct(c, hi)
    vol = s['vol']; vmax = max(vol); vmax_d = dates[vol.index(vmax)]
    vr = V.get('volr')
    pts = []
    # 1) 추세 — 이동평균 위치
    above = [n for n, m in (('20일', ma20), ('50일', ma50), ('200일', ma200)) if c > m]
    below = [n for n, m in (('20일', ma20), ('50일', ma50), ('200일', ma200)) if c <= m]
    if not above:
        trend = f'20·50·200일선 아래 — 단기·중기·장기 모두 약세 구간'
    elif not below:
        trend = '20·50·200일선 위 — 추세 살아 있음'
    else:
        trend = f'{"·".join(above)}선 위, {"·".join(below)}선 아래'
    pts.append({'k': '추세', 't': trend})
    # 2) 200일선 — 돌파/이탈 자리
    g200 = pct(c, ma200)
    pts.append({'k': '200일선', 't': f'{fmt(ma200, unit)} (현재가와 {g200:+.1f}%) — '
                + ('위로 다시 올라서는지가 첫 관문' if g200 < 0 else '지켜야 할 장기 지지선')})
    # 3) 정배열·데드크로스
    if ma50 > ma200:
        gap = pct(ma50, ma200)
        pts.append({'k': '골든·데드크로스', 't': f'50일선이 200일선보다 {gap:.1f}% 위 — 아직 데드크로스 아님'
                    + (' (간격 좁아지는 중)' if (V['ma50p'] - V['ma200p']) > (ma50 - ma200) else '')})
    else:
        pts.append({'k': '골든·데드크로스', 't': '50일선이 200일선 아래 — 데드크로스 상태'})
    # 4) 고점 대비
    zone = '약세장(-20% 이상)' if dd <= -20 else '조정 구간(-10% 이상)' if dd <= -10 else '고점 대비 소폭 조정(-10% 이내)'
    pts.append({'k': '52주 고점 대비', 't': f'{dd:.1f}% · {zone} (고점 {fmt(hi, unit)}, {S["hi52d"]})'})
    # 5) 지지·저항 (최근 20거래일)
    pts.append({'k': '지지 · 저항', 't': f'아래 {fmt(S["sup20"], unit)}(최근 20일 저점) · 위 {fmt(ma20, unit)}(20일선) → {fmt(S["res20"], unit)}(20일 고점)'})
    # 6) 거래량
    vt = (f'{vsym} 거래량 20일 평균의 {vr:.2f}배' if vr else '')
    if vr is not None:
        vt += ' — 반등이어도 거래가 적어 힘이 약함' if (S['chg'] > 0 and vr < 1) else (' — 하락에 거래 증가, 매도세 확인' if (S['chg'] < 0 and vr > 1.2) else '')
    vt += f' · 최근 6개월 최대 거래일 {vmax_d[5:].replace("-", "/")}'
    pts.append({'k': '거래량', 't': vt})
    # 7) RSI
    r = S['rsi']
    pts.append({'k': 'RSI(14)', 't': f'{r:.0f} — ' + ('과매도(30 아래)' if r < 30 else '과매수(70 위)' if r > 70 else '중립~약세' if r < 50 else '중립~강세')})
    # 하이라이트(짧게) — 근거 문장 없이 핵심만
    tags = []
    tags.append({'t': '20·50·200일선 모두 아래' if not above else ('이평선 모두 위' if not below else f'{"·".join(below)}선 아래'), 'hl': not above})
    tags.append({'t': f'200일선 {g200:+.1f}%', 'hl': g200 < 0})
    tags.append({'t': f'고점 대비 {dd:.1f}%' + (' · 약세장' if dd <= -20 else ' · 조정' if dd <= -10 else ''), 'hl': dd <= -10})
    tags.append({'t': '데드크로스 아직' if ma50 > ma200 else '데드크로스', 'hl': ma50 <= ma200})
    if vr is not None:
        tags.append({'t': f'거래량 {vr:.2f}배' + (' · 약한 반등' if (S['chg'] > 0 and vr < 1) else ''), 'hl': False})
    tags.append({'t': f'RSI {r:.0f}' + (' 과매도' if r < 30 else ' 과매수' if r > 70 else ''), 'hl': r < 30 or r > 70})
    up_lv, up_nm = (ma200, '200일선') if g200 < 0 else (ma20, '20일선') if c < ma20 else (S['res20'], '20일 고점')
    watch = {'up': {'v': round(up_lv, 2), 'name': up_nm, 'gap': round(pct(up_lv, c), 1)},
             'down': {'v': round(S['sup20'], 2), 'name': '20일 저점', 'gap': round(pct(S['sup20'], c), 1)}}
    keys = {'reclaim': ma200 if g200 < 0 else ma20, 'support': S['sup20'], 'ma20': ma20, 'ma50': ma50, 'ma200': ma200, 'hi52': hi}
    return {
        'sym': sym, 'name': name, 'unit': unit, 'vol_sym': vsym,
        'close': {'v': c, 'src': SRC.format(sym.replace('^', '%5E')), 'asof': f'{S["date"]} 16:00 ET 종가'},
        'chg_pct': {'v': S['chg'], 'src': SRC.format(sym.replace('^', '%5E')), 'asof': f'{S["date"]} 16:00 ET 종가'},
        'points': pts, 'tags': tags, 'watch': watch, 'levels': {k: round(v, 2) for k, v in keys.items()},
        'ma_step': 3, 'ma_offset': 2, 'series': {'dates': dates, **{k: [None if x is None else round(x, 2) for x in v] for k, v in s.items()}},
        'asof': f'{S["date"]} 종가 · 야후 파이낸스 일봉으로 계산',
    }


def main(raw_p, sum_p):
    dates, series, summ = load(raw_p, sum_p)
    out = [analyse(sym, dates, series[sym], summ[sym], summ[CFG[sym][2]] | {'ma50p': summ[sym]['ma50p'], 'ma200p': summ[sym]['ma200p']}) for sym in CFG]
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:3])

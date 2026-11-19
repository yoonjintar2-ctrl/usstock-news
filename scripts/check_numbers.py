"""발행 전 숫자 검사 — 통과 못 하면 발행하지 않는다.
  python3 scripts/check_numbers.py drafts/2026-11-20.json
잡는 것: (1) {v,src,asof} 숫자 칸에 값은 있는데 출처·기준 시각이 빠짐 (2) 본문에 달러 금액이 있는데 같은 문장에 원화 환산이 없음
(3) 본문·제목에 '사라/팔라/매수 추천/목표가' 같은 권유 표현 (4) disclaimer 없음. 종료 코드 1 = 실패."""
import json, re, sys

BAD = re.compile(r'(사세요|사라|팔아라|파세요|매수\s*추천|매도\s*추천|강력\s*매수|목표\s*주가|목표가)')
USD = re.compile(r'(\d[\d,\.]*\s*(억|만|조)?\s*달러|\$\s*\d)')

def walk(o, path=''):
    if isinstance(o, dict):
        if set(o) >= {'v', 'src', 'asof'}:
            yield path, o
        for k, v in o.items():
            yield from walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')

SKIP = ('src', 'u', 'url', 'img', 'video', 'ai', 'sources', 'series', 'levels', 'unit', 'from', 'summary_src', 'short')

def texts(o, street=False):
    """(문장, 월가코너여부). 'n'(큰 숫자)은 옆 'won' 칸과 묶어서 본다. 'from'(이전 목표가)은 취소선 표시라 건너뜀."""
    if isinstance(o, str): yield o, street
    elif isinstance(o, dict):
        if 'n' in o and 'won' in o:
            yield f"{o['n']} {o['won'] or ''}".strip() + ('' if '달러' not in o['n'] else ''), street
        for k, v in o.items():
            if k in SKIP or k == 'n': continue
            yield from texts(v, street or k == 'street')
    elif isinstance(o, list):
        for v in o: yield from texts(v, street)

def main(p):
    D = json.load(open(p, encoding='utf-8')); err = []
    for path, n in walk(D):
        if n.get('v') is not None and (not n.get('src') or not n.get('asof')):
            err.append(f'출처·기준 시각 없음 {path} = {n.get("v")}')
    for t, street in texts(D):
        for s in re.split(r'(?<=[.!?。])\s+', t):
            if USD.search(s) and '원' not in s: err.append(f'원화 환산 없음: {s[:60]}')
            # 월가 코너는 증권사 목표주가를 '보도된 사실'로 옮기므로 목표주가 단어는 허용(권유 표현은 여전히 금지)
            bad = BAD.search(s)
            if bad and not (street and bad.group(0).replace(' ', '') in ('목표주가', '목표가')):
                err.append(f'권유 표현: {s[:60]}')
    if not D.get('disclaimer'): err.append('disclaimer 없음')
    for e in err: print('❌', e)
    print('통과' if not err else f'실패 {len(err)}건')
    return 1 if err else 0

if __name__ == '__main__': sys.exit(main(sys.argv[1]))

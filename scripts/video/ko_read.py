"""나레이션용 읽기 변환: 숫자·기호·영문 약어를 한국어 발음으로 바꾼다(자막은 원문 그대로)."""
import re

DIG = '영일이삼사오육칠팔구'
SMALL = ['', '십', '백', '천']
BIG = ['', '만', '억', '조']
NATIVE_H = {1: '한', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉', 10: '열', 11: '열한', 12: '열두'}
ABBR = {
    'S&P': '에스앤피', 'SEC': '에스이씨', 'AI': '에이아이', 'PCE': '피씨이', 'GDP': '지디피', 'PMI': '피엠아이', 'CPI': '씨피아이',
    'TPU': '티피유', 'GPU': '지피유', 'ETF': '이티에프', 'IPO': '아이피오', 'CEO': '씨이오', 'VIX': '빅스', 'RSI': '알에스아이',
    'TD': '티디', 'NAND': '낸드', 'TV': '티비', 'KST': '', 'ET': '', 'X': '엑스', 'CNN': '씨엔엔', 'CNBC': '씨엔비씨', 'AP': '에이피',
    'SOXL': '속슬', 'SOXX': '삭스', 'QQQ': '큐큐큐', 'NVDA': '엔비디아', 'AVGO': '브로드컴', 'AMD': '에이엠디', 'IBM': '아이비엠',
    'GE': '지이', 'UBS': '유비에스', 'JP모건': '제이피모건',
}


def sino(n: int) -> str:
    if n == 0:
        return '영'
    out, g = [], 0
    while n > 0:
        n, chunk = divmod(n, 10000)
        if chunk:
            s = ''
            for i, ch in enumerate(reversed(f'{chunk}')):
                d = int(ch)
                if d:
                    s = ('' if (d == 1 and i > 0) else DIG[d]) + SMALL[i] + s
            if g == 1 and chunk == 1:
                s = ''
            out.insert(0, s + BIG[g])
        g += 1
    return ''.join(out)


def num(tok: str) -> str:
    tok = tok.replace(',', '')
    if '.' in tok:
        a, b = tok.split('.', 1)
        b = b.rstrip('0')
        return sino(int(a or 0)) + ((' 점 ' + ''.join('공' if c == '0' else DIG[int(c)] for c in b)) if b else '')
    return sino(int(tok))


def read(text: str) -> str:
    t = text
    t = re.sub(r'(\d{1,2})/(\d{1,2})\(([월화수목금토일])\)', lambda m: f"{num(m[1])}월 {num(m[2])}일 {m[3]}요일", t)
    t = re.sub(r'(\d{1,2})/(\d{1,2})', lambda m: f"{num(m[1])}월 {num(m[2])}일", t)

    def hm(m):
        h, mi = int(m[1]), int(m[2])
        hh = h % 12 or 12
        pre = '밤 ' if h >= 18 else '새벽 ' if h < 6 else '오후 ' if h >= 12 else '오전 '
        return pre + f"{NATIVE_H[hh]} 시" + (f" {num(str(mi))}분" if mi else '')
    t = re.sub(r'(\d{1,2}):(\d{2})', hm, t)
    t = re.sub(r'(\d+):(\d+)', lambda m: f"{num(m[1])} 대 {num(m[2])}", t)
    for k in sorted(ABBR, key=len, reverse=True):
        t = re.sub(rf'(?<![A-Za-z]){re.escape(k)}(?![A-Za-z])', ABBR[k], t)
    t = re.sub(r'[-−]\s?(\d[\d,]*(?:\.\d+)?)\s?%', lambda m: '마이너스 ' + num(m[1]) + ' 퍼센트', t)
    t = re.sub(r'\+\s?(\d[\d,]*(?:\.\d+)?)\s?%', lambda m: '플러스 ' + num(m[1]) + ' 퍼센트', t)
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s?%p', lambda m: num(m[1]) + ' 퍼센트포인트', t)
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s?%', lambda m: num(m[1]) + ' 퍼센트', t)
    t = re.sub(r'(\d[\d,]*(?:\.\d+)?)\s?배', lambda m: num(m[1]) + ' 배', t)
    t = re.sub(r'\d[\d,]*(?:\.\d+)?', lambda m: num(m[0]), t)
    t = t.replace('·', ', ').replace('→', '에서 ').replace('~', ' 에서 ').replace('&', ' 앤 ')
    t = re.sub(r'[()「」\'"‘’“”]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


if __name__ == '__main__':
    for s in ['S&P 500은 -3.70%로 7일 연속 내렸습니다.', '11/25(수) 22:30 10월 PCE 물가', '약 4,910억 달러, 우리 돈 약 661조 원', '8:1 분할 첫날 79.24달러', 'AI칩 주문을 20% 줄였다']:
        print(read(s))

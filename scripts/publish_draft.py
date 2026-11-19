"""drafts/D.json → today.json + archive/D.json + archive/index.json (숫자 검사 통과해야 진행)
  python3 scripts/publish_draft.py 2026-11-20
audio/D-*.mp3 가 있으면 코너에 audio 를 붙인다. 최근 3개 호 밖의 음성은 지운다."""
import json, os, sys, glob, subprocess, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from make_og import make as make_og

SITE = 'https://stocknews.jintar.co.kr'
WD = '월화수목금토일'


def og_tags(d):
    dt = datetime.date.fromisoformat(d['date'])
    title = (d.get('top') or {}).get('title') or '간밤 뉴욕장과 오늘 밤 일정'
    t = f"{title} | 미국주식 늬우스 {dt.month}/{dt.day}({WD[dt.weekday()]})"
    desc = d.get('lead', '')
    img = f"{SITE}/og/{d['date']}.png"
    e = lambda x: html.escape(x, quote=True)
    return '\n'.join([f'<title>{e(t)}</title>', f'<meta name="description" content="{e(desc)}">',
        '<meta property="og:type" content="article">', '<meta property="og:site_name" content="미국주식 늬우스">',
        f'<meta property="og:title" content="{e(t)}">', f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:image" content="{img}">',
        '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:image" content="{img}">'])


def set_og(d, path='index.html'):
    s = open(path, encoding='utf-8').read()
    a, b = s.index('<!--OG-->'), s.index('<!--/OG-->')
    s = s[:a] + '<!--OG-->\n' + og_tags(d) + '\n' + s[b:]
    open(path, 'w', encoding='utf-8').write(s)

def main(D):
    src = f'drafts/{D}.json'
    if subprocess.run([sys.executable, 'scripts/check_numbers.py', src]).returncode:
        print('숫자 검사 실패 — 발행하지 않음'); return 1
    d = json.load(open(src, encoding='utf-8'))
    for mp3 in glob.glob(f'audio/{D}-*.mp3'):
        k = os.path.basename(mp3)[len(D) + 1:-4]
        if isinstance(d.get(k), dict): d[k]['audio'] = mp3
    os.makedirs('archive', exist_ok=True)
    for p in ('today.json', f'archive/{D}.json'):
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ip = 'archive/index.json'; idx = json.load(open(ip, encoding='utf-8')) if os.path.exists(ip) else []
    idx = [x for x in idx if x.get('date') != D]; idx.insert(0, {'date': D, 'no': d.get('no'), 'lead': d.get('lead', '')})
    json.dump(idx, open(ip, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    make_og(src); set_og(d)  # 공유 썸네일·미리보기 태그를 그날 1면으로
    keep = {x['date'] for x in idx[:3]}
    for mp3 in glob.glob('audio/*.mp3'):
        if os.path.basename(mp3)[:10] not in keep: os.remove(mp3)
    print('발행', D, '제', d.get('no'), '호'); return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1]))

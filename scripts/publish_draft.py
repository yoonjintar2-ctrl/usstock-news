"""drafts/D.json → today.json + archive/D.json + archive/index.json (숫자 검사 통과해야 진행)
  python3 scripts/publish_draft.py 2026-11-20
audio/D-*.mp3 가 있으면 코너에 audio 를 붙인다. 최근 3개 호 밖의 음성은 지운다."""
import json, os, sys, glob, subprocess

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
    keep = {x['date'] for x in idx[:3]}
    for mp3 in glob.glob('audio/*.mp3'):
        if os.path.basename(mp3)[:10] not in keep: os.remove(mp3)
    print('발행', D, '제', d.get('no'), '호'); return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1]))

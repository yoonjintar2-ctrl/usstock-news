"""8비트 대본(video/top/D.json) → 맥 qtts 작업 파일 (키트 없이 — 발행 작업이 클라우드에서 바로 만든다)
python3 scripts/video/top_job.py video/top/D.json 0usMMDD_2top OUT.json [--retake s01_0,s03_1]
id 규칙은 pixel_kit/top8.py(qtts_job) 와 같다: s{장면:02}_{줄}_c1"""
import json, sys
spec, name, out = sys.argv[1:4]
retake = set(sys.argv[sys.argv.index('--retake') + 1].split(',')) if '--retake' in sys.argv else None
S = json.load(open(spec, encoding='utf-8')); items = []
for k, sc in enumerate(S['scenes']):
    for i, ln in enumerate(sc['lines']):
        lid = f's{k:02d}_{i}'; n = ln[1]
        if retake is not None and lid not in retake: continue
        t = n.rstrip('.!?') + ('!' if n.endswith('!') else ('?' if n.endswith('?') else '.'))
        items.append({'id': f'{lid}_{"c2" if retake is not None else "c1"}', 'text': t, 'gen': {'non_streaming_mode': True}})
json.dump({'name': name, 'mode': 'clone', 'ref_audio': 'out/casual1/E_think.wav', 'ref_text': '음… 그럼 데이터센터는 이제 못 짓는 건가?',
           'gen': {'temperature': 0.65, 'top_p': 0.9}, 'reload_every': 4, 'retries': 4, 'items': items},
          open(out, 'w'), ensure_ascii=False, indent=1)
print(len(items), '줄 →', out)

"""요약 영상 대본(video/D.json) → 맥 qtts 작업 파일 (마스코트 목소리, c1 테이크만)
python3 scripts/video/sum_job.py video/D.json 0usMMDD_1sum OUT.json [--retake s03_01,s05_00]
 · id = s{장면:02}_{줄:02}_c1 (prep_sum.py → VOICE_DIR 이름 규칙과 맞춤)
 · --retake: 피치 튄 줄만 _c2 로 다시 만드는 작업 파일
 · 문장 끝에 ' 음.' 붙이지 않음, temperature 0.65 (11/26 발행인)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ko_read import read

spec, name, out = sys.argv[1:4]
retake = set(sys.argv[sys.argv.index('--retake') + 1].split(',')) if '--retake' in sys.argv else None
S = json.load(open(spec, encoding='utf-8'))
items = []
for k, sc in enumerate(S['scenes']):
    for i, line in enumerate(sc.get('lines', [])):
        lid = f's{k:02d}_{i:02d}'
        if retake is not None and lid not in retake: continue
        t = read(line).replace('최고가', '가장 높았던 때').strip()
        if t[-1] not in '.!?': t += '.'
        items.append({'id': f'{lid}_{"c2" if retake is not None else "c1"}', 'text': t, 'gen': {'non_streaming_mode': True}})
job = {'name': name, 'mode': 'clone', 'ref_audio': 'out/casual1/E_think.wav', 'ref_text': '음… 그럼 데이터센터는 이제 못 짓는 건가?',
       'gen': {'temperature': 0.65, 'top_p': 0.9}, 'reload_every': 4, 'retries': 4, 'items': items}
json.dump(job, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(items), '줄 →', out)

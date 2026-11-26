"""Qwen3-TTS 작업 대기기 v2 — 터미널 창 하나로 계속 돌며 qtts/jobs/*.json 을 처리한다.
 · mode "design"(기본): VoiceDesign 모델, 말로 설명한 목소리 + instruct
 · mode "clone": Base 모델, ref_audio(wav 경로, qtts 기준 상대경로 가능)+ref_text 의 음색을 그대로 복제
 · 이 파일(tts_worker.py)이 바뀌면 스스로 재시작 → 이후 업데이트에 사용자 클릭 불필요
job.json: {"name","mode","ref_audio","ref_text","gen":{...},"items":[{"id","text","instruct"}],"concat":[[name,[ids]]]}
결과: qtts/out/<name>/<id>.wav · 끝나면 out/<name>/DONE · 처리한 job은 qtts/jobs_done/ 으로 이동"""
import os, sys, json, time, glob, shutil, traceback, gc, torch, numpy as np, soundfile as sf
from qwen_tts import Qwen3TTSModel
HERE = os.path.dirname(os.path.abspath(__file__)); ME = os.path.abspath(__file__)
JOBS = os.path.join(HERE, 'jobs'); DONE = os.path.join(HERE, 'jobs_done')
os.makedirs(JOBS, exist_ok=True); os.makedirs(DONE, exist_ok=True)
DEV = 'mps' if torch.backends.mps.is_available() else 'cpu'
SRC = {'design': HERE, 'clone': os.environ.get('QTTS_BASE', 'Qwen/Qwen3-TTS-12Hz-1.7B-Base')}
cur = {'mode': None, 'tts': None, 'prompt': None}
MY_MTIME = os.path.getmtime(ME)

# 11/26 맥 없이 돌리기: 미국주식 늬우스 발행 작업(클라우드)이 깃허브 tts/queue/0us*.json 에 올린 작업을 대기기가 직접 가져온다.
# 저장소가 공개라 로그인 없이 읽기만 한다. 2분에 한 번, 실패해도 조용히 넘어간다.
GH_LIST = 'https://api.github.com/repos/yoonjintar2-ctrl/usstock-news/contents/tts/queue'
_gh = {'t': 0}
def _get(url):
    try:
        import requests
        r = requests.get(url, timeout=20, headers={'User-Agent': 'qtts'}); r.raise_for_status(); return r.content
    except ImportError:
        import urllib.request, ssl
        try:
            import certifi; ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            ctx = ssl.create_default_context()
        return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'qtts'}), timeout=20, context=ctx).read()
def gh_pull():
    if time.time() - _gh['t'] < 120: return
    _gh['t'] = time.time()
    try:
        for f in json.loads(_get(GH_LIST)):
            n = f.get('name', '')
            if not (n.startswith('0us') and n.endswith('.json')): continue
            name = n[:-5]
            if os.path.exists(os.path.join(JOBS, n)) or os.path.exists(os.path.join(DONE, n)) \
               or os.path.exists(os.path.join(HERE, 'out', name, 'DONE')): continue
            data = _get(f['download_url']); json.loads(data)
            tmp = os.path.join(JOBS, n + '.new'); open(tmp, 'wb').write(data); os.replace(tmp, os.path.join(JOBS, n))
            print(f'깃허브에서 작업 가져옴: {n}', flush=True)
    except Exception as e:
        print(f'깃허브 작업 확인 실패(넘어감): {str(e)[:80]}', flush=True)

class Preempt(Exception): pass
def urgent_waiting(cur_name):
    """급한 작업(이름이 0으로 시작)이 들어왔는데 지금 작업이 급한 게 아니면 잠시 멈추고 급한 것부터(완료분은 다음에 건너뜀)."""
    if str(cur_name).startswith('0'): return False
    return any(os.path.basename(p).startswith('0') for p in glob.glob(os.path.join(JOBS, '*.json')))


DT = {'bfloat16': torch.bfloat16, 'float16': torch.float16, 'float32': torch.float32}


def get(mode, dtype='bfloat16', src=None):
    key = (mode, dtype, src)
    if cur['mode'] != key:
        cur['tts'] = None; cur['prompt'] = None; gc.collect()
        if DEV == 'mps': torch.mps.empty_cache()
        t0 = time.time(); print(f'모델 불러오는 중: {mode}/{dtype} (처음이면 다운로드 포함)', flush=True)
        cur['tts'] = Qwen3TTSModel.from_pretrained(src or SRC[mode], device_map=DEV, dtype=DT[dtype])
        cur['mode'] = key; print(f'모델 준비: {mode}/{dtype} ({DEV}, {time.time() - t0:.0f}초)', flush=True)
    return cur['tts']


def broken(w, sr):
    """굉음·삐 소리·무음 같은 고장 테이크 감지 (사람 목소리면 크기가 출렁이고 유성음 비율이 높음)"""
    if len(w) < sr * 0.5: return '너무 짧음'
    clip = float((np.abs(w) > 0.98).mean())
    if clip > 0.005: return f'클리핑 {clip*100:.1f}%'
    hop = int(sr * 0.05); r = np.array([np.sqrt((w[i:i + hop] ** 2).mean()) for i in range(0, len(w) - hop, hop)])
    act = r[r > 0.02]
    if len(act) < 10: return '거의 무음'
    if act.std() / act.mean() < 0.3: return '크기가 일정(소음 의심)'
    import librosa
    y = librosa.resample(w, orig_sr=sr, target_sr=16000)
    f0, v, _ = librosa.pyin(y, fmin=70, fmax=600, sr=16000, frame_length=1024)
    if v.mean() < 0.35: return f'유성음 {v.mean()*100:.0f}%'
    if np.nanmedian(f0[v]) > 380: return '삐 소리 의심'
    return None


def run(job):
    mode = job.get('mode', 'design'); dt = job.get('dtype', 'bfloat16'); src = job.get('model')
    out = os.path.join(HERE, 'out', job['name']); os.makedirs(out, exist_ok=True)
    gen = job.get('gen', {}); clips = {}
    ref = job.get('ref_audio')
    if ref and not os.path.isabs(ref): ref = os.path.join(HERE, ref)

    def fresh(force=False):
        """모델(+복제 프롬프트) 준비. force=True면 통째로 새로 올림. 지역변수로 모델을 붙잡지 않는다."""
        if force: cur['mode'] = None
        for k in range(3):
            try:
                get(mode, dt, src)
                pk = (ref, job.get('ref_text'), bool(job.get('x_vector_only', False)))       # 11/12: 기준 음성이 바뀌면 복제 프롬프트도 새로 만든다(전엔 앞 작업의 프롬프트가 그대로 쓰였음)
                if mode == 'clone' and (cur.get('prompt') is None or cur.get('pkey') != pk):
                    cur['prompt'] = cur['tts'].create_voice_clone_prompt(ref_audio=ref, ref_text=job.get('ref_text'),
                                                                        x_vector_only_mode=job.get('x_vector_only', False)); cur['pkey'] = pk
                return
            except Exception as e:
                print(f'  모델 준비 중 오류 → 다시 ({str(e)[:60]})', flush=True); cur['mode'] = None; time.sleep(3)
        raise RuntimeError('모델 준비 3번 실패')
    fresh()
    every = job.get('reload_every', 5)   # 맥 GPU에서 생성이 쌓이면 고장 나는 현상 예방: N개마다 모델 새로 올림
    for n_it, it in enumerate(job['items']):
        t1 = time.time()
        done_p = os.path.join(out, it['id'] + '.wav')
        if job.get('resume', True) and os.path.exists(done_p):
            w, sr = sf.read(done_p, dtype='float32'); clips[it['id']] = (w, sr); continue
        if n_it and every and n_it % every == 0: fresh(force=True)
        gh_pull()
        if urgent_waiting(job.get('_file') or job.get('name', '')):
            print(f"급한 작업 도착 → [{job['name']}] 잠시 멈춤(이어서 다시)", flush=True); raise Preempt()
        if os.path.getmtime(ME) != MY_MTIME:      # 작업 중이라도 코드가 바뀌면 남은 작업은 새 코드로
            print('새 버전 감지(작업 중) → 재시작, 이 작업은 처음부터 다시', flush=True); os.execv(sys.executable, [sys.executable, ME])
        cap = {'max_new_tokens': int(12 * (3 + 0.22 * len(it['text'])))}   # 12Hz 코덱: 문장 길이 기준 상한
        for tri in range(job.get('retries', 4) + 1):
            try:
                if mode == 'clone':
                    wavs, sr = cur['tts'].generate_voice_clone(text=it['text'], language=it.get('language', 'Korean'),
                                                        voice_clone_prompt=cur['prompt'], **{**cap, **gen, **it.get('gen', {})})
                else:
                    wavs, sr = cur['tts'].generate_voice_design(text=it['text'], instruct=it.get('instruct', ''),
                                                         language=it.get('language', 'Korean'), **{**cap, **gen, **it.get('gen', {})})
                w = np.asarray(wavs[0], dtype=np.float32)
                why = broken(w, sr) if job.get('check', True) else None
            except Exception as e:                       # 맥 GPU 오류(MPS command buffer 등) → 모델 다시 올려 재시도
                w, sr, why = np.zeros(2400, np.float32), 24000, f'GPU 오류 {str(e)[:60]}'
            if not why: break
            print(f"  {it['id']} 고장 테이크({why}) → 모델 새로 올려서 다시 생성 {tri + 1}", flush=True)
            # 맥 GPU(MPS)에서 한 번 고장 나면 계속 고장 나는 경우가 있어, 모델을 통째로 다시 올린다
            wavs = None; fresh(force=True)
        clips[it['id']] = (w, sr)
        if DEV == 'mps': torch.mps.empty_cache()
        sf.write(os.path.join(out, it['id'] + '.wav'), w, sr)
        print(f"[{job['name']}] {it['id']}: {len(w) / sr:.1f}초 ({time.time() - t1:.0f}초 걸림)", flush=True)
    for cname, ids in job.get('concat', []):
        sr = clips[ids[0]][1]; segs = []
        for i in ids: segs += [clips[i][0], np.zeros(int(sr * 0.6), np.float32)]
        sf.write(os.path.join(out, cname + '.wav'), np.concatenate(segs), sr)
    open(os.path.join(out, 'DONE'), 'w').write(time.strftime('%H:%M:%S'))



def cleanup():
    """11/14 문학늬우스 '듣기': out/mnews-<날짜> 폴더는 3일 지나면, 전송용 out/mnews-*.tgz 는 하루 지나면 지운다(그 밖의 파일은 건드리지 않음)."""
    import datetime, re as _re
    lim = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
    for p in glob.glob(os.path.join(HERE, 'out', 'mnews-*')):
        try:
            b = os.path.basename(p); m = _re.fullmatch(r'mnews-(\d{4}-\d{2}-\d{2})', b)
            if m and os.path.isdir(p) and m.group(1) < lim:
                shutil.rmtree(p); print(f'정리: {b}', flush=True)
            elif _re.fullmatch(r'mnews-.*\.tgz', b) and time.time() - os.path.getmtime(p) > 86400:
                os.remove(p); print(f'정리: {b}', flush=True)
        except Exception as e:
            print(f'정리 실패 {p}: {e}', flush=True)


# 11/14: 발행인이 한동안 맥을 못 쓰는 상황 — 대기기 창이 열려 있는 동안만 맥이 저절로 잠들지 않게(caffeinate -i, 화면은 꺼져도 됨). 창을 닫으면 같이 끝남.
if sys.platform == 'darwin' and not os.environ.get('QTTS_CAFF'):
    try:
        import subprocess
        subprocess.Popen(['caffeinate', '-i', '-w', str(os.getpid())]); os.environ['QTTS_CAFF'] = '1'
        print('잠자기 방지 켬(대기기가 도는 동안)', flush=True)
    except Exception as e:
        print(f'잠자기 방지 실패: {e}', flush=True)

print(f'작업 대기기 v2 시작 ({DEV}) — 이 창은 열어 두세요.', flush=True)
open(os.path.join(HERE, 'WORKER_READY'), 'w').write(time.strftime('%Y-%m-%d %H:%M:%S') + ' v2')
last_clean = 0
while True:
    gh_pull()
    if time.time() - last_clean > 3600:
        cleanup(); last_clean = time.time()
    if os.path.getmtime(ME) != MY_MTIME:          # 코드가 업데이트되면 새 코드로 재시작
        print('새 버전 감지 → 재시작', flush=True); os.execv(sys.executable, [sys.executable, ME])
    for jp in sorted(glob.glob(os.path.join(JOBS, '*.json'))):
        try:
            J = json.load(open(jp, encoding='utf-8')); J['_file'] = os.path.basename(jp)
            if J.get('kind') in ('image', 'probe'):   # 11/18 문학늬우스 삽화: 그림 작업은 별도 프로세스(img_worker.py)로 — TTS 모델을 내려 메모리를 비우고 돌린다
                cur['tts'] = None; cur['prompt'] = None; cur['mode'] = None; gc.collect()
                if DEV == 'mps': torch.mps.empty_cache()
                import subprocess
                print(f"그림 작업: {J.get('name')}", flush=True)
                subprocess.run([sys.executable, os.path.join(HERE, 'img_worker.py'), jp], cwd=HERE)
            else:
                run(J)
        except Preempt:
            break                                   # 작업 파일은 jobs/ 에 그대로 두고 처음부터 다시 훑는다(급한 것 먼저)
        except Exception:
            err = traceback.format_exc(); print(err, flush=True)
            os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
            open(os.path.join(HERE, 'out', os.path.basename(jp) + '.ERROR.txt'), 'w').write(err)
        shutil.move(jp, os.path.join(DONE, os.path.basename(jp)))
        cleanup()
    time.sleep(2)

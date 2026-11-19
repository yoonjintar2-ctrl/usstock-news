"""문학늬우스 삽화 그리기(11/18) — tts_worker 가 kind=image|probe 작업을 받으면 이 파일을 따로 실행한다.
probe: 맥 사양·설치 상태를 out/probe.json 에. image: 아래 run_image 참고(처음 실행 때 필요한 패키지 설치)."""
import os, sys, json, subprocess, platform, time, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = os.path.join(HERE, 'out', J.get('name', 'img')); os.makedirs(OUT, exist_ok=True)
BIN = os.path.dirname(sys.executable)

def sh(*a):
    try: return subprocess.run(a, capture_output=True, text=True, timeout=600).stdout.strip()
    except Exception as e: return f'ERR {e}'

if J['kind'] == 'probe':
    import importlib.util as u
    info = {'mem_bytes': sh('sysctl', '-n', 'hw.memsize'), 'chip': sh('sysctl', '-n', 'machdep.cpu.brand_string'), 'macos': platform.mac_ver()[0],
            'python': sys.version, 'disk_free_gb': shutil.disk_usage(HERE).free / 1e9,
            'has': {m: bool(u.find_spec(m)) for m in ('mlx', 'mflux', 'diffusers', 'torch', 'transformers', 'accelerate')},
            'hf_cache': sh('du', '-sh', os.path.expanduser('~/.cache/huggingface'))}
    json.dump(info, open(os.path.join(OUT, 'probe.json'), 'w'), indent=1)
    open(os.path.join(OUT, 'DONE'), 'w').write(time.strftime('%H:%M:%S'))

# ── image: SDXL + SDXL-Lightning(4단계) — 맥 M2 8GB 에서 돌아가는 크기(발행인 11/18 승인). 라이선스: SDXL base 1.0·Lightning 모두 OpenRAIL++(상업 이용 가능)
#   작업: {"kind":"image","name":"img-D","items":[{"id":"classic-s1","prompt":"...","neg":"...","seeds":[1,2,3],"w":1344,"h":768}]}
#   결과: out/<name>/<id>_<seed>.png · 다 끝나면 out/<name>/DONE · 이미 있는 그림은 건너뜀(이어 하기)
if J['kind'] == 'image':
    os.environ.setdefault('PYTORCH_MPS_HIGH_WATERMARK_RATIO', '0.0')
    log = open(os.path.join(OUT, 'log.txt'), 'a')
    def say(m): print(m, flush=True); log.write(time.strftime('%H:%M:%S ') + m + '\n'); log.flush()
    try:
        import diffusers  # noqa
    except ImportError:
        say('처음 한 번: diffusers 설치'); uv = next((x for x in (os.path.expanduser('~/.local/bin/uv'), os.path.expanduser('~/.cargo/bin/uv'), shutil.which('uv') or '') if x and os.path.exists(x)), None)
        say(sh(uv, 'pip', 'install', '--python', sys.executable, 'diffusers==0.35.2', 'safetensors') if uv else 'uv 없음'); import importlib; importlib.invalidate_caches()
    import torch
    from diffusers import StableDiffusionXLPipeline, UNet2DConditionModel, EulerDiscreteScheduler
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file
    dev = 'mps' if torch.backends.mps.is_available() else 'cpu'; t0 = time.time()
    base = 'stabilityai/stable-diffusion-xl-base-1.0'
    unet = UNet2DConditionModel.from_config(base, subfolder='unet').to(torch.float16)
    unet.load_state_dict(load_file(hf_hub_download('ByteDance/SDXL-Lightning', 'sdxl_lightning_4step_unet.safetensors'), device='cpu'))
    pipe = StableDiffusionXLPipeline.from_pretrained(base, unet=unet, torch_dtype=torch.float16, variant='fp16').to(dev)
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing='trailing')
    pipe.enable_attention_slicing(); pipe.enable_vae_slicing(); pipe.enable_vae_tiling()
    # 11/19: 맥 8GB 에서 img2img 가 글 인코더에서 메모리 부족 → 글 인코더는 CPU(float32)에서 돌리고 결과만 GPU 로
    pipe.text_encoder.to('cpu', torch.float32); pipe.text_encoder_2.to('cpu', torch.float32)
    if dev == 'mps': torch.mps.empty_cache()
    def embeds(p, n):
        with torch.no_grad():
            pe, npe, ppe, nppe = pipe.encode_prompt(prompt=p, negative_prompt=n, device='cpu', num_images_per_prompt=1, do_classifier_free_guidance=False)
        return {k: v.to(dev, torch.float16) for k, v in (('prompt_embeds', pe), ('pooled_prompt_embeds', ppe)) if v is not None}
    say(f'모델 준비 {time.time() - t0:.0f}초 ({dev})')
    for it in J['items']:
        for sd in it.get('seeds', [1]):
            fp = os.path.join(OUT, f"{it['id']}_{sd}.png")
            if os.path.exists(fp): continue
            t1 = time.time()
            if it.get('init'):   # 11/19 밑그림 방식: 모양은 밑그림, 결·질감만 AI(모르는 음식·소품용). strength 낮을수록 밑그림에 가깝다
                from diffusers import StableDiffusionXLImg2ImgPipeline
                from PIL import Image as _I
                if 'i2i' not in globals(): globals()['i2i'] = StableDiffusionXLImg2ImgPipeline.from_pipe(pipe)
                st = float(it.get('strength', 0.55))
                img = i2i(**embeds(it['prompt'], it.get('neg')), image=_I.open(os.path.join(HERE, it['init'])).convert('RGB'), strength=st,
                          num_inference_steps=max(4, round(4 / st)), guidance_scale=0, generator=torch.Generator('cpu').manual_seed(sd)).images[0]
            else:
                img = pipe(**embeds(it['prompt'], it.get('neg')), num_inference_steps=4, guidance_scale=0,
                       width=it.get('w', 1344), height=it.get('h', 768), generator=torch.Generator('cpu').manual_seed(sd)).images[0]
            img.save(fp); say(f"{it['id']}_{sd} {time.time() - t1:.0f}초")
            if dev == 'mps': torch.mps.empty_cache()
    open(os.path.join(OUT, 'DONE'), 'w').write(time.strftime('%H:%M:%S'))

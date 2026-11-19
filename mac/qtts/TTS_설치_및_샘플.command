#!/bin/bash
# Qwen3-TTS 설치 + 샘플 생성 (더블클릭 실행)
# 맥 기본 파이썬(3.9)은 너무 낡아서, uv로 파이썬 3.12 전용 환경(~/qtts-env312)을 따로 만들어요. 시스템 파이썬·셸 설정은 안 건드려요.
cd "$(dirname "$0")"
LOG="$(pwd)/install_log.txt"
exec > >(tee "$LOG") 2>&1
echo "== $(date) Qwen3-TTS 설치 시작 (2차) =="
UV="$HOME/.local/bin/uv"
if [ ! -x "$UV" ]; then
  echo "== uv(파이썬 설치 도구) 설치 =="
  curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh || { echo "uv 설치 실패"; read -n1; exit 1; }
fi
ENV="$HOME/qtts-env312"
[ -x "$ENV/bin/python" ] || "$UV" venv --python 3.12 "$ENV" || { echo "파이썬 3.12 환경 생성 실패"; read -n1; exit 1; }
PY="$ENV/bin/python"; echo "python: $($PY --version)"
"$UV" pip install --python "$PY" torch torchaudio "transformers==4.57.3" "accelerate==1.12.0" librosa soundfile einops onnxruntime || { echo "패키지 설치 실패"; read -n1; exit 1; }
"$UV" pip install --python "$PY" --no-deps qwen-tts || { echo "qwen-tts 설치 실패"; read -n1; exit 1; }
SP=$("$PY" -c "import site;print(site.getsitepackages()[0])")
[ -f "$SP/sox.py" ] || echo "# stub (12Hz 모델은 sox 불필요)" > "$SP/sox.py"
echo "== 모델 파일 확인/다운로드 (Hugging Face Qwen 공식, 약 4.5GB · 처음 한 번만) =="
B=https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign/resolve/main
mkdir -p speech_tokenizer
get(){ want=$2; have=$(stat -f%z "$1" 2>/dev/null || echo 0); if [ "$have" != "$want" ]; then echo "받는 중: $1"; curl -L --fail -C - -o "$1" "$B/$1?download=true" || { echo "다운로드 실패: $1"; read -n1; exit 1; }; fi; }
get model.safetensors 3833402552
get speech_tokenizer/model.safetensors 682293092
echo "== 설치 완료, 샘플 생성 중 (몇 분 걸려요) =="
"$PY" sample_mac.py
echo "== 끝. 이 창은 닫아도 돼요 =="

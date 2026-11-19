# 문학늬우스에서 가져온 스크립트 (그대로는 안 돌아감 — 이 신문 형식에 맞게 고쳐 씀)
- tts/tts_jobs.py: 지면 JSON → 맥 음성 작업 파일 / tts_post.py: 테이크 고르기·mp3 / prosody_qa.py: 억양·길이 이상 문장 찾아 다시 읽히기
- shorts/make_short.py: 대본+테이크 → 영상(가로·세로) / qa_video.py: 음량·무음·자막 속도·본문 일치 검사 / make_srt.py · make_thumb.py · yt_desc.py · make_bgm.py
- img/img_job.py: 초안 ai 프롬프트 → 맥 그림 작업 / animate.py: 그림 → 8초 루프 영상
- make_share.py: 코너별 공유 카드·페이지 / publish_draft.py: 문학늬우스판(이 패키지의 scripts/publish_draft.py 가 단순판)
코너 이름(classic·modern·food…)을 market·stock·term… 으로 바꾸는 게 주된 수정입니다.

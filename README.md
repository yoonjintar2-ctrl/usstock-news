# 미국주식 늬우스 — stocknews.jintar.co.kr

발행인 **샌디스크 올인**(유튜브 @SNDK_lover). 매일 아침 간밤 뉴욕장, 차트 분석, 월가 의견, 오늘 밤 일정을 신문 한 장으로 냅니다.

- `index.html` — 지면(모바일 우선, 데스크톱 3단). `today.json` 또는 `?d=YYYY-MM-DD` 로 `archive/` 를 읽음
- `drafts/D.json` → `scripts/publish_draft.py D` → `today.json` + `archive/`
- `scripts/check_numbers.py` — 출처 없는 숫자·원화 환산 빠짐·권유 표현을 잡아 발행을 막음
- `scripts/chart_analysis.py` — 일봉 → 이동평균·지지/저항·거래량·RSI 분석
- 규칙: `docs/PROMPT.md`, 데이터 받기: `docs/DATA-FETCH.md`, 형식 예시: `drafts/2026-11-19.json`(창간호)

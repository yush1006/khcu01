# 사회복지전공 교육과정 로드맵 시안

- `src/data.js` : 교육과정, 자격증, 전공역량 데이터 (원본: khcu.ac.kr 교육과정로드맵 탭 캡처)
- `src/roadmap-a.html` : A안 학기 타임라인 (확정안). `<!--DATA-->` 자리에 data.js가 삽입됨
- `src/roadmap-b.html`, `src/roadmap-c.html` : B안 플래너, C안 가이드북 (미채택)
- `src/build.py` : data.js를 각 HTML에 인라인해 `dist/`에 생성
- `dist/roadmap-*.html` : 아티팩트에 게시한 본문 (doctype, html, head, body 없음. 아티팩트가 감싸줌)
- `dist/roadmap-*.standalone.html` : 브라우저에서 바로 열 수 있는 완성 파일

빌드: roadmap 폴더에서 `python src/build.py` 실행. dist/에 본문 파일과 standalone 파일이 함께 생성됨.
게시된 A안: https://claude.ai/artifact/7vVTWa8y8S8aMa3koHdEh7

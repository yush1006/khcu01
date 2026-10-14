"""data.js를 각 HTML에 인라인해 dist/에 완성 파일을 만든다.

사용법 (roadmap 폴더에서):
    python src/build.py

출력:
    dist/roadmap-a.html             아티팩트 게시용 본문 (골격 없음)
    dist/roadmap-a.standalone.html  브라우저에서 바로 여는 완성 파일
    (b, c도 동일)
"""
import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parent
DIST = SRC.parent / 'dist'
DIST.mkdir(exist_ok=True)

SKELETON_HEAD = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
                 '<meta name="viewport" content="width=device-width,initial-scale=1">\n</head>\n<body>\n')
SKELETON_TAIL = '\n</body>\n</html>\n'

data = (SRC / 'data.js').read_text(encoding='utf-8')

# 이미지 자산을 data URI로 내장 (아티팩트는 외부 이미지를 불러올 수 없음)
import base64
ASSETS = SRC.parent / 'assets'
def data_uri(name, mime):
    f = ASSETS / name
    return f'data:{mime};base64,' + base64.b64encode(f.read_bytes()).decode('ascii') if f.exists() else ''
IMAGES = {'{{LOGO}}': data_uri('logo.png', 'image/png'), '{{VISUAL}}': data_uri('bgSubTit02.jpg', 'image/jpeg')}
for v in 'abc':
    src = (SRC / f'roadmap-{v}.html').read_text(encoding='utf-8')
    assert '<!--DATA-->' in src, f'roadmap-{v}.html 에 <!--DATA--> 자리가 없습니다'
    body = src.replace('<!--DATA-->', data)
    for key, uri in IMAGES.items():
        body = body.replace(key, uri)
    (DIST / f'roadmap-{v}.html').write_text(body, encoding='utf-8')
    (DIST / f'roadmap-{v}.standalone.html').write_text(SKELETON_HEAD + body + SKELETON_TAIL, encoding='utf-8')
    dashes = len(re.findall('[—–]', body))
    print(f'roadmap-{v}: {len(body.encode()):,} bytes, em/en dash {dashes}')
print('done ->', DIST)

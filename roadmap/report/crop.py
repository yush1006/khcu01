import sys
from PIL import Image
src, dst, preview = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert('RGB')
w, h = im.size
# 아래쪽의 빈 흰 영역 잘라내기: 마지막으로 흰색이 아닌 행 찾기
px = im.load()
last = h - 1
while last > 0:
    row = [px[x, last] for x in range(0, w, 8)]
    if any(abs(r - 255) + abs(g - 255) + abs(b - 255) > 12 for r, g, b in row):
        break
    last -= 1
cut = min(h, last + 2 * 60)  # 60px(2x) 여백
im = im.crop((0, 0, w, cut))
im.save(dst, optimize=True)
pv = im.copy(); pv.thumbnail((900, 20000)); pv.save(preview)
print(dst, im.size)

import sys, pymupdf
from PIL import Image, ImageChops
src = sys.argv[1]; zoom = 3.0
doc = pymupdf.open(src)
pages = []
for pg in doc:
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
    pages.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
W, H = pages[0].size
print('page px', W, H)

def content_rows(im):
    """흰색이 아닌 첫 행과 마지막 행"""
    g = im.convert('L'); px = g.load(); w, h = g.size
    def nonwhite(y): return any(px[x, y] < 245 for x in range(0, w, 4))
    top = next(y for y in range(h) if nonwhite(y))
    bot = next(y for y in range(h - 1, -1, -1) if nonwhite(y))
    return top, bot
def content_cols(im):
    g = im.convert('L'); px = g.load(); w, h = g.size
    def nonwhite(x): return any(px[x, y] < 245 for y in range(0, h, 4))
    left = next(x for x in range(w) if nonwhite(x))
    right = next(x for x in range(w - 1, -1, -1) if nonwhite(x))
    return left, right

for i, im in enumerate(pages):
    print('page', i, 'rows', content_rows(im), 'cols', content_cols(im))

# 중간 페이지(1)의 위/아래 여백 = 페이지 공통 여백으로 사용
top1, bot1 = content_rows(pages[1]); top0, bot0 = content_rows(pages[0])
top_margin = min(top1, content_rows(pages[2])[0]); bottom_margin = min(H - 1 - bot0, H - 1 - bot1)
print('margins top/bottom', top_margin, bottom_margin)
left, right = content_cols(pages[0])

strips = []
strips.append(pages[0].crop((left, 0, right + 1, H - bottom_margin)))
strips.append(pages[1].crop((left, top_margin, right + 1, H - bottom_margin)))
t2, b2 = content_rows(pages[2])
strips.append(pages[2].crop((left, top_margin, right + 1, b2 + 1)))
total_h = sum(s.size[1] for s in strips)
out = Image.new('RGB', (right - left + 1, total_h), 'white')
y = 0
for s in strips:
    out.paste(s, (0, y)); y += s.size[1]
# 위쪽 빈 여백 제거
t0, _ = content_rows(pages[0])
out = out.crop((0, max(0, t0 - 0), out.size[0], out.size[1]))
out.save('before-original.png', optimize=True)
print('before-original.png', out.size)

# 사이트 상단(유틸바, GNB, 로고, 서브비주얼, 브레드크럼)과 왼쪽 LNB를 khcu.ac.kr 레이아웃대로 추가한다.
import pathlib, re

p = pathlib.Path(__file__).parent / 'roadmap-a.html'
s = p.read_text(encoding='utf-8')

LNB = ["전체 학부(과) 보기", "IT·디자인융합학부", "재난안전학부", "전자정보공학과", "스마트건축공학과", "AI기계제어공학과",
       "보건의료관리학과", "한방건강관리학과", "후마니타스학과", "미디어문예창작학과", "사회복지학부", "상담심리학과", "일본학과",
       "중국어문화학과", "미국문화영어학과", "한국어문화학부", "스포츠학부", "실용음악학과", "문화예술경영학과", "미디어영상홍보학과",
       "마케팅·리더십경영학부", "글로벌경영학과", "세무회계학과", "자산관리학부", "호텔경영학과", "관광레저항공경영학과",
       "외식조리경영학부", "글로벌자율학부", "교양교육(교양학부)"]
SUB = ["사회복지학부", "사회복지전공", "노인복지전공", "아동·가족전공", "아동·보육전공", "청소년·가족전공"]

lnb_items = []
for name in LNB:
    if name == "사회복지학부":
        subs = "".join(f'<li class="{"on" if x == "사회복지전공" else ""}"><span>{x}</span></li>' for x in SUB)
        lnb_items.append(f'<li class="on"><span>{name}</span><ul class="lnb-sub">{subs}</ul></li>')
    else:
        lnb_items.append(f'<li><span>{name}</span></li>')
LNB_HTML = "\n        ".join(lnb_items)

HEADER = f'''<header class="site">
  <div class="util">
    <div class="container">
      <div class="util-l"><span>입학지원센터</span><i class="sep"></i><span>대학원</span></div>
      <div class="util-r"><span class="gold">Sitemap</span><span class="gold">English</span><span class="btn-go">등교하기</span><span class="search" aria-label="검색"><i></i></span></div>
    </div>
  </div>
  <div class="head">
    <div class="container">
      <nav class="gnb gnb-l" aria-label="주메뉴 왼쪽"><span>경희소개</span><span>학과소개</span><span>입학안내</span></nav>
      <div class="logo" aria-label="경희사이버대학교">
        <div class="emblem"><span>KHCU</span></div>
        <b>경희사이버대학교</b>
        <small>KYUNG HEE CYBER UNIVERSITY</small>
      </div>
      <nav class="gnb gnb-r" aria-label="주메뉴 오른쪽"><span>학사안내</span><span>학습지원</span><span>대학생활</span></nav>
    </div>
  </div>
  <div class="visual">
    <h1>학과소개</h1>
    <div class="container crumbwrap">
      <div class="crumb"><span class="home" aria-label="홈"><i></i></span><span>학과소개<i class="chev"></i></span><span>사회복지학부<i class="chev"></i></span><span>사회복지전공<i class="chev"></i></span></div>
    </div>
  </div>
</header>

<div class="container layout">
  <aside class="lnb" aria-label="학과 메뉴">
    <ul>
        {LNB_HTML}
    </ul>
  </aside>
  <main class="content">
    <div class="deptbox">
      <h2>사회복지전공</h2>
      <p class="contact"><span class="lbl">전공문의</span><span class="ic">@</span><b>welfare@khcu.ac.kr</b><span class="ic">T</span><b>02-3299-8625</b></p>
    </div>
    <nav class="tabs" role="tablist" id="tabs"></nav>'''

# 1) header 교체 + main 열기
start = s.index('<header class="site">'); end = s.index('</header>') + len('</header>')
s = s[:start] + HEADER + s[end:]
s = s.replace('\n<main>\n', '\n', 1)
assert '</main>' in s
s = s.replace('</main>', '  </main>\n</div>', 1)

# 2) 헤더 CSS 교체
css_start = s.index('/* ---------- 헤더 ---------- */'); css_end = s.index('/* ---------- 섹션 ---------- */')
NEW_CSS = '''/* ---------- 사이트 크롬 (khcu.ac.kr 레이아웃) ---------- */
.container { width: 1240px; max-width: 100%; margin: 0 auto; padding-inline: 24px; }
@media (min-width: 1300px) { .container { padding-inline: 0; } }
.site { --khcu: #a6192e; --khcu-dark: #8f1426; --gold: #e3c56b; --ink: #262121; }
.util { background: var(--khcu); color: #fff; height: 40px; font-size: 15px; font-weight: 500; }
.util .container { display: flex; align-items: center; justify-content: space-between; height: 100%; }
.util-l, .util-r { display: flex; align-items: center; gap: 18px; height: 100%; }
.util-l .sep { width: 1px; height: 12px; background: rgba(255, 255, 255, 0.35); }
.util-r .gold { color: var(--gold); }
.util-r .btn-go { background: #b39a5b; color: #fff; height: 40px; padding: 0 20px; display: inline-flex; align-items: center; font-weight: 600; margin-left: 6px; }
.util-r .search { width: 40px; height: 40px; display: inline-grid; place-items: center; }
.util-r .search i { width: 14px; height: 14px; border: 2px solid #fff; border-radius: 50%; position: relative; display: block; }
.util-r .search i::after { content: ""; position: absolute; width: 2px; height: 7px; background: #fff; right: -4px; bottom: -6px; transform: rotate(-45deg); }
.head { background: #fff; height: 80px; position: relative; z-index: 3; }
.head .container { display: grid; grid-template-columns: 1fr 200px 1fr; align-items: center; height: 80px; }
.gnb { display: flex; justify-content: space-around; font-size: 19px; font-weight: 700; color: var(--ink); }
.gnb span { padding: 0 8px; cursor: default; transition: color 0.16s var(--ease); }
.gnb span:hover { color: var(--khcu); }
.logo { position: relative; height: 80px; }
.logo::before { content: ""; position: absolute; left: 0; right: 0; top: -40px; height: 184px; background: #fff; border-radius: 0 0 100px 100px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12); }
.logo .emblem, .logo b, .logo small { position: relative; display: block; text-align: center; }
.logo .emblem { width: 74px; height: 74px; margin: -22px auto 6px; border-radius: 50%; background: var(--khcu); border: 4px double var(--gold); display: grid; place-items: center; color: #fff; font-weight: 800; font-size: 15px; letter-spacing: 0.08em; }
.logo b { font-size: 15px; font-weight: 800; color: var(--khcu); letter-spacing: -0.02em; line-height: 1.1; }
.logo small { font-size: 8.5px; font-weight: 700; color: var(--ink); letter-spacing: 0.04em; margin-top: 2px; }
.visual { position: relative; height: 230px; background: linear-gradient(90deg, #42506c 0%, #6a7a97 45%, #4d5a76 100%); overflow: hidden; }
.visual::before { content: ""; position: absolute; inset: 0; background: radial-gradient(ellipse at 30% 110%, rgba(255, 255, 255, 0.18), transparent 55%), radial-gradient(ellipse at 80% -20%, rgba(255, 255, 255, 0.12), transparent 50%); }
.visual h1 { position: relative; text-align: center; color: #fff; font-size: 41px; font-weight: 500; letter-spacing: -0.02em; padding-top: 58px; line-height: 1.2; }
.crumbwrap { position: absolute; left: 0; right: 0; bottom: 0; display: flex; justify-content: flex-end; }
.crumb { display: flex; height: 50px; background: rgba(255, 255, 255, 0.62); backdrop-filter: blur(6px); font-size: 15px; color: #333; font-weight: 500; margin: 0; }
.crumb > span { display: inline-flex; align-items: center; gap: 36px; padding: 0 22px; border-left: 1px solid rgba(0, 0, 0, 0.12); min-width: 160px; }
.crumb .home { min-width: 60px; padding: 0 20px; justify-content: center; border-left: 0; }
.crumb .home i { width: 14px; height: 10px; border: 2px solid #555; border-top: 0; position: relative; display: block; margin-top: 6px; }
.crumb .home i::before { content: ""; position: absolute; left: -5px; top: -9px; width: 14px; height: 14px; border: 2px solid #555; border-right: 0; border-bottom: 0; transform: rotate(45deg); }
.crumb .chev { width: 7px; height: 7px; border-right: 2px solid #777; border-bottom: 2px solid #777; transform: rotate(45deg) translateY(-2px); display: inline-block; }

.layout { display: flex; gap: 52px; align-items: flex-start; padding-top: 44px; }
.lnb { width: 219px; flex: none; border-right: 1px solid #e3e3e3; text-align: right; padding-right: 20px; }
.lnb ul { list-style: none; margin: 0; padding: 0; }
.lnb > ul > li > span { display: block; font-size: 16px; font-weight: 600; color: #555; line-height: 32px; position: relative; word-break: keep-all; }
.lnb > ul > li.on > span { color: #a61212; }
.lnb li.on > span::after { content: ""; position: absolute; right: -24px; top: 50%; width: 5px; height: 5px; border-radius: 50%; background: #a61212; transform: translateY(-50%); }
.lnb-sub { padding: 8px 0 10px; }
.lnb-sub li span { display: block; font-size: 14px; font-weight: 500; color: #888; line-height: 21px; position: relative; }
.lnb-sub li.on span { color: #a61212; }
.lnb-sub li.on span::after { right: -20px; width: 4px; height: 4px; }
.content { width: 969px; flex: none; min-width: 0; }
main .wrap { max-width: none; padding-inline: 0; }

.deptbox { background: #b8475f; color: #fff; border-radius: 8px; padding: 44px 40px 40px; min-height: 168px; position: relative; overflow: hidden; }
.deptbox::after { content: ""; position: absolute; right: -60px; top: -80px; width: 320px; height: 320px; border-radius: 50%; background: rgba(255, 255, 255, 0.07); }
.deptbox h2 { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; color: #fff; }
.deptbox .contact { display: flex; align-items: center; gap: 12px; margin-top: 18px; font-size: 17px; font-weight: 500; }
.deptbox .lbl { padding-right: 14px; border-right: 1px solid rgba(255, 255, 255, 0.4); margin-right: 4px; }
.deptbox .ic { width: 28px; height: 28px; border-radius: 50%; background: rgba(255, 255, 255, 0.25); display: inline-grid; place-items: center; font-size: 13px; font-weight: 700; }
.deptbox b { font-weight: 500; margin-right: 10px; }

.tabs { display: grid; grid-template-columns: repeat(6, 1fr); margin: 50px 0 48px; border-bottom: 1px solid #c9c9c9; }
.tab {
  height: 60px;
  font-size: 15px;
  font-weight: 500;
  color: #1d1d1d;
  border: 1px solid transparent;
  border-left-color: #e2e2e2;
  margin-bottom: -1px;
  white-space: nowrap;
  transition: color 0.16s var(--ease);
}
.tab:first-child { border-left-color: transparent; }
.tab:hover { color: #990e17; }
.tab[aria-selected="true"] { color: #990e17; font-weight: 700; background: #fff; border-color: #990e17; border-bottom-color: #fff; }
.tab[aria-selected="true"] + .tab { border-left-color: transparent; }

'''
s = s[:css_start] + NEW_CSS + s[css_end:]

# 3) 본문 .wrap 는 콘텐츠 폭 그대로, 섹션 패딩 조정
s = s.replace('main .wrap { padding-block: 56px 112px; display: grid; gap: 96px; }',
              'main .wrap { padding-block: 0 112px; display: grid; gap: 96px; }')

# 4) 반응형: 좁은 화면에서 LNB 숨기고 한 열
s = s.replace('@media (max-width: 900px) {\n  .certs',
              '@media (max-width: 1100px) {\n  .layout { flex-direction: column; gap: 24px; }\n  .lnb { display: none; }\n  .content { width: 100%; }\n  .head .container { grid-template-columns: 1fr 160px 1fr; }\n  .gnb { font-size: 16px; }\n  .tabs { grid-template-columns: repeat(3, 1fr); }\n  .tab { height: 48px; }\n  .crumb > span { min-width: 0; gap: 14px; padding: 0 14px; }\n}\n@media (max-width: 900px) {\n  .certs')
s = s.replace('  .gnb { display: none; }\n  main .wrap', '  .gnb { display: none; }\n  .head .container { grid-template-columns: 1fr; justify-items: center; }\n  main .wrap')
s = s.replace('  .titleband h1 { font-size: 28px; }', '  .deptbox h2 { font-size: 26px; }\n  .deptbox { padding: 28px 22px; }\n  .deptbox .contact { flex-wrap: wrap; font-size: 15px; }\n  .visual h1 { font-size: 30px; }\n  .util { font-size: 13px; }\n  .util-l, .util-r { gap: 10px; }')

p.write_text(s, encoding='utf-8')
print('chrome applied')

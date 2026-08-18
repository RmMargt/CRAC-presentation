#!/usr/bin/env python3
"""Build a standalone HTML deck from the Claude Design .dc.html prototype."""
import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "project")
SRC = os.path.join(SRC_DIR, "CRAC2026 演讲PPT v5.dc.html")
OUT_DIR = os.path.join(ROOT, "dist")

src = open(SRC, encoding="utf-8").read()

# ---- extract the slide body from inside <x-import> ---------------------------
body = src.split("<x-import", 1)[1].split(">", 1)[1].rsplit("</x-import>", 1)[0]
# Drop commented-out superseded layouts (they reference a deleted asset).
body = re.sub(r"<!--.*?-->", "", body, flags=re.S)

sections = re.findall(r"<section\b.*?</section>", body, flags=re.S)
assert len(sections) == 23, len(sections)

# ---- renumber data-screen-label sequentially (fixes the 07b / dup 16,17) -----
slides = []
for i, sec in enumerate(sections, 1):
    def renum(m):
        text = re.sub(r"^\s*\d+[a-z]?\s*", "", m.group(1))
        return 'data-screen-label="%02d %s"' % (i, text)
    sec = re.sub(r'data-screen-label="([^"]*)"', renum, sec, count=1)
    label = re.search(r'data-label="([^"]*)"', sec)
    screen = re.search(r'data-screen-label="([^"]*)"', sec)
    notes = re.search(r'data-speaker-notes="([^"]*)"', sec)
    slides.append({
        "label": html.unescape(label.group(1)) if label else "Slide %d" % i,
        "screen": html.unescape(screen.group(1)) if screen else "",
        "notes": html.unescape(notes.group(1)) if notes else "",
    })
    sections[i - 1] = sec

# ---- copy the assets each slide actually references --------------------------
used = sorted(set(re.findall(r'src="((?:template_assets|uploads)/[^"]+)"', "".join(sections))))
if os.path.isdir(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.makedirs(OUT_DIR)
for rel in used:
    dst = os.path.join(OUT_DIR, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(SRC_DIR, rel), dst)

notes_json = json.dumps([s["notes"] for s in slides], ensure_ascii=False)
labels_json = json.dumps([s["label"] for s in slides], ensure_ascii=False)

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>从法规知识到决策智能｜CRAC CHINA 2026</title>
<!-- Fonts are self-hosted and subset to this deck's glyphs: the deck renders
     identically with no network, which is the point on a conference stage. -->
<link rel="stylesheet" href="fonts/fonts.css">
<style>
/* ── authored deck styles, carried over verbatim from the prototype helmet ── */
body{margin:0;background:#0E2A25;font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}
section *{text-wrap:pretty;}
a{color:#2FA37A;text-decoration:none;}a:hover{color:#238463;}
section > img[alt="CRAC 2026"]{opacity:.92;}
section [style*="box-shadow:0 1px 2px"]{box-shadow:0 8px 22px rgba(18,58,71,.05)!important;}
section [style*="box-shadow:0 2px 5px"]{box-shadow:0 14px 34px rgba(18,58,71,.075)!important;}

/* ── stage: fixed 1920x1080 canvas scaled to fit, letterboxed ── */
html,body{height:100%;overflow:hidden;}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
  transition:right .28s cubic-bezier(.2,.8,.2,1);}
/* With notes open the stage yields the drawer's width, so the slide stays whole. */
body[data-notes] #stage{right:min(440px,38vw);}
#canvas{position:relative;width:1920px;height:1080px;flex-shrink:0;background:#fff;transform-origin:center center;will-change:transform;}
#canvas > section{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;box-sizing:border-box!important;overflow:hidden;opacity:0;visibility:hidden;pointer-events:none;}
#canvas > section[data-active]{opacity:1;visibility:visible;pointer-events:auto;}

/* ── overlay: slide counter, fades out when idle ── */
#hud{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);display:flex;align-items:center;gap:14px;
  padding:7px 16px;background:rgba(0,0,0,.72);color:#fff;border-radius:999px;
  font:500 13px/1 Barlow,system-ui,sans-serif;letter-spacing:.02em;backdrop-filter:blur(8px);
  opacity:0;pointer-events:none;transition:opacity .26s ease;z-index:50;user-select:none;}
#hud[data-show]{opacity:1;}
#hud b{font-weight:700;font-variant-numeric:tabular-nums;}
#hud span{opacity:.62;max-width:34ch;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  font-family:"Noto Sans SC",sans-serif;}
#hud kbd{opacity:.42;font-family:inherit;}

/* ── speaker notes drawer ── */
#notes{position:fixed;right:0;top:0;bottom:0;width:min(440px,38vw);background:#0B1F1B;color:#D6E5E0;
  padding:30px 32px;box-sizing:border-box;overflow-y:auto;z-index:60;
  transform:translateX(100%);transition:transform .28s cubic-bezier(.2,.8,.2,1);
  border-left:1px solid rgba(255,255,255,.09);}
#notes[data-open]{transform:none;}
#notes h2{margin:0 0 4px;font:700 15px/1.4 Barlow,sans-serif;letter-spacing:.14em;color:#4FBF97;text-transform:uppercase;}
#notes h3{margin:0 0 20px;font:700 22px/1.45 "Noto Sans SC",sans-serif;color:#fff;}
#notes p{margin:0;font:400 17px/1.9 "Noto Sans SC",sans-serif;color:#B9CFC9;white-space:pre-wrap;}
#notes .empty{color:#5C7A73;font-style:normal;}

/* ── print: one slide per page at design size → clean PDF ── */
@page{size:1920px 1080px;margin:0;}
@media print{
  html,body{overflow:visible;background:#fff;}
  #stage{position:static;display:block;}
  #canvas{width:auto;height:auto;transform:none!important;background:none;}
  #canvas > section{position:relative!important;inset:auto!important;
    width:1920px!important;height:1080px!important;opacity:1!important;visibility:visible!important;
    page-break-after:always;break-after:page;}
  #canvas > section:last-child{page-break-after:auto;break-after:auto;}
  #hud,#notes{display:none!important;}
}
</style>
</head>
<body>

<div id="stage"><div id="canvas">
__SLIDES__
</div></div>

<div id="hud"><b id="hud-n">1 / 23</b><span id="hud-label"></span><kbd>← →</kbd></div>

<aside id="notes"><h2>Speaker notes</h2><h3 id="notes-title"></h3><p id="notes-body"></p></aside>

<script>
(function(){
  var NOTES  = __NOTES__;
  var LABELS = __LABELS__;
  var canvas = document.getElementById('canvas');
  var slides = Array.prototype.slice.call(canvas.querySelectorAll(':scope > section'));
  var hud = document.getElementById('hud'), hudN = document.getElementById('hud-n'),
      hudLabel = document.getElementById('hud-label');
  var notes = document.getElementById('notes'),
      notesTitle = document.getElementById('notes-title'),
      notesBody = document.getElementById('notes-body');
  var index = 0, hudTimer = null;

  var stage = document.getElementById('stage');

  function fit(){
    var s = Math.min(stage.clientWidth / 1920, stage.clientHeight / 1080);
    canvas.style.transform = 'scale(' + s + ')';
  }

  function toggleNotes(){
    var open = notes.toggleAttribute('data-open');
    document.body.toggleAttribute('data-notes', open);
    // Re-fit through the width transition so the slide never clips mid-slide.
    var t0 = Date.now(), iv = setInterval(function(){
      fit(); if (Date.now() - t0 > 340) clearInterval(iv);
    }, 16);
  }

  function flashHud(){
    hud.setAttribute('data-show','');
    clearTimeout(hudTimer);
    hudTimer = setTimeout(function(){ hud.removeAttribute('data-show'); }, 1900);
  }

  function show(i, skipHash){
    index = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach(function(s, n){
      if (n === index) s.setAttribute('data-active',''); else s.removeAttribute('data-active');
    });
    hudN.textContent = (index + 1) + ' / ' + slides.length;
    hudLabel.textContent = LABELS[index] || '';
    notesTitle.textContent = LABELS[index] || '';
    var n = NOTES[index];
    notesBody.textContent = n || '（这一页没有备注）';
    notesBody.className = n ? '' : 'empty';
    if (!skipHash) history.replaceState(null, '', '#' + (index + 1));
    flashHud();
  }

  window.addEventListener('resize', fit);
  fit();

  document.addEventListener('keydown', function(e){
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    var k = e.key;
    if (k === 'ArrowRight' || k === 'PageDown' || k === ' ' || k === 'Enter'){ show(index + 1); e.preventDefault(); }
    else if (k === 'ArrowLeft' || k === 'PageUp' || k === 'Backspace'){ show(index - 1); e.preventDefault(); }
    else if (k === 'Home'){ show(0); e.preventDefault(); }
    else if (k === 'End'){ show(slides.length - 1); e.preventDefault(); }
    else if (k === 'r' || k === 'R'){ show(0); e.preventDefault(); }
    else if (k === 'n' || k === 'N' || k === 's' || k === 'S'){ toggleNotes(); e.preventDefault(); }
    else if (k === 'Escape' && notes.hasAttribute('data-open')){ toggleNotes(); }
  });

  // Tap left / right half to navigate (touch and click alike).
  canvas.addEventListener('click', function(e){
    if (e.target.closest('a[href],button,input,select,textarea,summary,[role="button"]')) return;
    show(index + (e.clientX < window.innerWidth / 2 ? -1 : 1));
  });

  document.addEventListener('mousemove', flashHud);

  var start = parseInt((location.hash || '').slice(1), 10);
  show(isNaN(start) ? 0 : start - 1, true);
})();
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__SLIDES__", "\n\n".join(sections))
       .replace("__NOTES__", notes_json)
       .replace("__LABELS__", labels_json))

with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)

README = """# CRAC CHINA 2026 · 演讲 PPT（独立网页版）

从 Claude Design 原型 `CRAC2026 演讲PPT v5.dc.html` 生成的独立演示文稿，
不再依赖设计工具的运行时（`support.js` / `deck-stage.js`），双击即可打开。

## 怎么用

双击 `index.html`，用浏览器打开（Chrome / Edge / Safari 都行），按 F11 全屏。

| 按键 | 作用 |
|------|------|
| `→` `空格` `PgDn` | 下一页 |
| `←` `PgUp` | 上一页 |
| `Home` / `End` | 第一页 / 最后一页 |
| `N` 或 `S` | 打开／关闭演讲者备注（备注打开时画面自动缩窄，不遮挡内容） |
| `R` | 回到第一页 |
| `Esc` | 关闭备注 |

鼠标点击画面左半边／右半边也可以翻页。地址栏的 `#8` 表示当前页码，
刷新或分享链接都会回到那一页。

## 导出 PDF

在浏览器里 `Ctrl/Cmd + P` → 目标选择「另存为 PDF」→ 纸张 1920×1080（横向）、
边距设为「无」、勾选「背景图形」。每张幻灯片会占一页，共 23 页。

## 离线可用

字体（Noto Sans SC 400/500/700/900、Barlow 500/600/700）已下载到 `fonts/`，
并且只保留了本演示文稿用到的 761 个字形，七个字重合计约 400KB。
整个文件夹不联网也能正常显示，会场没有网络也不影响。

## 目录结构

```
index.html          幻灯片 + 演讲者备注 + 翻页逻辑（单文件）
fonts/              自托管字体（已按字形裁剪）
template_assets/    CRAC 母版底图与 CRAC / 瑞欧标识
uploads/            产品截图
```

整个文件夹是一个整体，拷贝或压缩时请一起带走（路径都是相对路径）。
"""
with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(README)

print("slides:", len(sections))
print("assets:", len(used))
for s in slides:
    print("  ", s["screen"])
size = sum(os.path.getsize(os.path.join(dp, f))
           for dp, _, fs in os.walk(OUT_DIR) for f in fs)
print("dist size: %.1f MB" % (size / 1024 / 1024))

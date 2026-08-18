# CRAC CHINA 2026 · 主题演讲

**从法规知识到决策智能：可信 AI 在化学品合规里怎么落地**
From Regulatory Knowledge to Decision Intelligence — Trusted AI for Global Chemical Compliance

演讲人：朱海东 Raymond Zhu ｜ 瑞欧科技 REACH24H ｜ 全 23 页，约 30 分钟

---

## 直接开讲

打开 `dist/index.html`（双击就行，Chrome / Edge / Safari 都可以），按 F11 全屏。

| 按键 | 作用 |
|------|------|
| `→` `空格` `PgDn` | 下一页 |
| `←` `PgUp` | 上一页 |
| `Home` / `End` | 第一页 / 最后一页 |
| `N` 或 `S` | 演讲者备注（打开时画面自动缩窄，不遮挡内容） |
| `R` | 回到第一页 |
| `Esc` | 关闭备注 |

鼠标点左半边／右半边也能翻页。地址栏的 `#8` 是当前页码，刷新或转发链接都会回到那一页。

**导出 PDF**：浏览器里 `Ctrl/Cmd + P` → 另存为 PDF → 纸张 1920×1080 横向、边距「无」、勾选「背景图形」，每页一张，共 23 页。

**不联网也能用**：字体已经下载到 `dist/fonts/`，并且只保留了本演示文稿用到的 761 个字形（七个字重合计约 400KB）。会场没网也不影响显示。

---

## 目录结构

```
dist/            打包好的独立网页版演示文稿 ← 要用的就是这个
project/         设计源文件（Claude Design 原型 + 母版素材 + 产品截图）
tools/           从原型重新生成 dist/ 的脚本
chats/           设计过程的对话记录，从初稿到定稿
HANDOFF.md       Claude Design 导出时附带的说明
```

`dist/` 是一个整体，拷贝或压缩时请整个文件夹一起带走（里面都是相对路径）。

---

## 改完设计后重新生成

演示文稿的正本是 `project/CRAC2026 演讲PPT v5.dc.html`（Claude Design 原型）。
改完之后跑：

```bash
python3 tools/build_deck.py     # 抽出幻灯片，生成 dist/index.html
python3 tools/subset_fonts.py   # 按新文案重新裁剪字体子集
```

需要 `fonttools` 和 `brotli`（`pip install fonttools brotli`）。字体首次会从 Google Fonts
下载完整 TTF 缓存到 `.fontcache/`（已在 .gitignore 里），之后就走缓存。

`build_deck.py` 做的事：从 `<x-import>` 里取出 23 个 `<section>` 原样搬过来，剥掉已废弃的
注释块，页码重新顺成 01–23，再套上翻页、备注、缩放和打印的外壳。幻灯片的标记一个字没改，
容器的盒模型跟 `deck-stage.js` 的 `::slotted(*)` 规则完全一致，所以版面不会跑。

---

## 说明

原型依赖 Claude Design 的运行时（`support.js` + `deck-stage.js`），脱离设计工具打不开。
`dist/` 把这层依赖去掉了，是一份到哪儿都能放的独立网页。

`project/` 里还留着 v1–v4 几版旧稿和一批没用上的素材，都按原样保留，没有删。

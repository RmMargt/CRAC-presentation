# 产品库与PPT调整

_Started 2026-07-25 14:40 UTC_

---

## User

Continuing from "峰会PPT设计方案".

## Assistant

We were building a 20-slide summit presentation for Raymond Zhu on "From Regulatory Knowledge to Decision Intelligence: Trusted AI for Global Chemical Compliance" — targeting 30 minutes for regulatory/registration staff and industry consultants. The goal was to transform abstract AI concepts into concrete visual storytelling using the CRAC 2026 template (green mother template, org logos, internal page style).

Decisions made:
- 25 slides total to allow breathing room and strategic pacing within 30 minutes.
- 11 custom vector diagrams embedded directly (inspection funnels, knowledge pyramids, regulatory networks, dual-track training comparison, controlled-growth loops, data-to-intelligence staircases, etc.) — all exportable and editable within PPTX.
- 5 system-screenshot placeholder slots left open (瑞查查 search/detail, KnowHub UI, Prowise workbench, impact analysis, Letter draft) for you to drop images into later without layout breaking.
- Speaker notes written in for every slide as a full draft script.
- Typography audit completed: all body text and diagram labels raised to 24px minimum; decorative side bars and chapter headers unchanged. Dense slides (05/13/15/19) verified for no overflow.

Current state: Presentation is structurally complete, diagram-heavy, and ready for screenshot insertion. The template is locked to CRAC house style.

Next steps:
- Provide the 5 system screenshots; I'll position them into the placeholder frames.
- Review speaker notes for tone/accuracy and request any rewrites.
- Adjust diagram complexity or labels if audience feedback suggests clarity gaps.

Files: CRAC 2026 模板（空白母版）.pptx, image-slot.js (helper for screenshot placement).

## User

根据这个智库的产品、数据中心的产品的仓库，了解这个产品真正要表达的，我的 PPT 的示意图以及文案也要对应调整，切合实际

## Assistant

_[tool: github_list_repos]_

_[tool: list_files]_

_[tool: github_get_tree]_

_[tool: github_get_tree]_

_[tool: github_read_files]_

_[tool: github_read_files]_

_[tool: github_get_tree]_

_[tool: grep]_

_[tool: github_read_files]_

_[tool: read_file]_

_[tool: read_file]_

_[tool: read_file]_

Now I have the real product picture. Rewriting the diagrams and copy to match the actual pipeline (数据管理中心 → 瑞查查总库 → KnowHub 企业私库 → Prowise Agent 运行时).

_[tool: run_script]_

_[tool: str_replace_edit]_

_[tool: write_file]_

_[tool: ready_for_verification]_

读完两个仓库（chemcheck-knowhub 的合规智库 PRD + Chemcheck_regulatory_database 的数据审核平台），最大的一处事实偏差是：**KnowHub 不是独立系统，它是瑞查查平台上的「企业私库」模块**，而且**数据管理中心（dbflow）是独立的上游一层**，之前的图里完全没有。已按真实链路改：

- **15 产品配合**（改动最大）：底层重画为 数据管理中心（采集·清洗·去重·人工审核）→ 瑞查查总库（已审核法规与名录）→ KnowHub 企业私库（画像匹配·人工确认·专题项目），上面才是 Prowise Agent 运行时 + 专家在环。
- **16**：改为「合规智库 KnowHub · 瑞查查上的企业私库」，四个真实模块：更新订阅（不进私库）／总库导入（画像匹配+人工审核）／企业私有库（优先级·业务标签·私有备注）／法规问答研判（法规源·对话·产出归档）。
- **19 场景**：不再声称 7 点才发现公告——改成上游管线前一晚已入库，7 点是企业画像匹配 → 人工确认入私库 → 关联私库与历史项目 → 8:20 出带引用的初稿 → 9 点专家审。
- **06**：环形图改为真实管线循环（监控抓取→清洗结构化→去重与版本关联→人工审核→入总库→质量与血缘）。
- **07/09/10/14/17/23**：字段与标签换成真的（法规层级、现行/废止、关联名录、条款切分、修订版本链、企业画像=行业标签+关注物质+企业描述、Agent 步骤可展开+引用跳回原文、操作全量留痕）。

两点待你确认：一是「数据管理中心」在对外演讲里是否用这个名字（还是说成"数据治理平台"）；二是要不要单加一页专讲数据治理（五维质量分、血缘与影响分析、审计留痕）——目前这些只作为要点散在 09/23 里。

## User

数据管理中心就行，我把最新的代码 push 上来了，叫 dbflow

## Assistant



## User

需要讲数据，高质量的数据是 AI 时代最重要的资产，这个理念要始终灌输

## Assistant

_[tool: github_get_tree]_

_[tool: github_get_tree]_

_[tool: github_list_repos]_

It's `chemcheck-dbflow`. Reading it now.

_[tool: github_get_tree]_

_[tool: github_read_files]_

_[tool: grep]_

_[tool: read_file]_

Adding two data-asset slides and threading the theme through, all grounded in the real DBFlow pipeline (五步清洗、字段级置信度、三级去重、审核台重提).

_[tool: str_replace_edit]_

_[tool: grep]_

Typo in one of my label edits — resending.

_[tool: str_replace_edit]_

Now renaming the section-02 eyebrow on the three existing slides.

_[tool: dc_html_str_replace]_

_[tool: str_replace_edit]_

_[tool: ready_for_verification]_

读了 chemcheck-dbflow（真实的五步清洗管线：取证 → 判相关性拆段 → 解读挂载 → 字段提取规范化 → 三级去重），把「数据即资产」做成了贯穿主线，现在 27 页：

**新增两页（第二部分开头）**
- **09 高质量数据，是 AI 时代最重要的资产**：核心论点页。左边一句重话「模型是可以买的，能不能拿它做判断，取决于你喂给它什么」；右边三个特征（准确 / 可用 / 可信）；底部对比图——同一个模型 ＋ 没清洗的 PDF → 看着像答案不敢用；＋ 结构化可追溯的数据 → 可以交付的判断。
- **10 每个字段都有来历**：用真实的 confidence_details 结构做了张字段表（发布机构 0.96 直接提取 / 实施日期 0.91 / 豁免情形 确认无此项 / 适用行业 0.62 待人工确认，高亮），配审核台三点（逐字段标注、并排看原文、单字段重提）＋ 三级去重，落在一句「低置信度的字段不会静悄悄进库」。

**贯穿的地方**
- 第二部分改名「数据资产、知识网络与经验」，副标「模型谁都买得到，高质量数据买不到」（目录同步）
- 06 副标改为「数据管理中心 DBFlow：采集 → 清洗 → 去重 → 人工审核 → 入库」，环上「质量与血缘」改为更贴实际的「置信度与留痕」
- 15 架构图里改叫「数据管理中心 · DBFlow」
- 26 收尾改为「缺的不是更强的模型，是高质量的数据和攒了很多年的经验」

27 页 30 分钟略紧，09/10 这两页值得慢讲，建议在 21 工作场景那页压缩节奏；要我做一版更紧的讲稿配速也可以。

## User

Found issues — fixing…

## Assistant

_[tool: str_replace_edit]_

_[tool: ready_for_verification]_

修好了两页的重叠：09 的三张卡片上移收紧、底部对比图改成 230 高的等比 viewBox（文字仍是 24px 以上）；10 的深色断言条下移到 800px，卡片间距收紧，底部两行上提。


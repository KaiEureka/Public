# 从零造一个前沿大模型（课程讲义整理版）

把 40 节课（第 0–39 课）的讲稿整理成的一本书：九篇、四十章，外加五个附录。

资料收集自飞书付费资源。课程讲义按章节整理，配有实验代码和复跑记录。

[阅读全书索引](INDEX.md) · [阅读前言](src/00_front.md)

- `src/`：全书的 Markdown 源文件。`00_front.md` 是前言（含阅读建议、图表标注与符号约定），`partN.md` 是各篇的扉页，`chNN.md` 是第 N 章，`appA.md`–`appE.md` 是附录。
- `code/`：书中所有实测结果的程序和数据，`chNN/` 对应第 N 章；`code/rerun_logs/` 是整理时把全部程序复跑一遍的输出。运行方法见附录 C。
- `figs/`：插图。`svglib.py` 是绘图工具；`p1.py`–`p7.py` 按篇生成 `figs/*.svg`；`spec_p*.py` 把图插入各章源文件（可重复运行，已插入的会跳过）；`data/` 里是作图用到的复跑数据。少数早期插图以内联 SVG 写在各章源文件里。
- `INDEX.md`：全书索引（每章的节、实验、图和习题，附源文件行号），由 `make_index.py` 生成。
- `fonts/`：排版 PDF 用的字体；`web/`：网页版的模板、样式、脚本和网页字体。
- `tools/`：排版检查与复跑实验的脚本。

## 构建 PDF

需要：Python 3（含 PyMuPDF）、pandoc 3.1 以上、Node.js 与 Playwright 自带的 Chromium。字体已放在 `fonts/` 下（均为 SIL OFL 授权，可自由分发）：

| 文件 | 来源 |
|---|---|
| NotoSerifCJKsc-Regular.otf、NotoSerifCJKsc-Bold.otf | Noto Serif CJK SC（notofonts） |
| NotoSansCJKsc-Regular.otf、NotoSansCJKsc-Bold.otf | Noto Sans CJK SC |
| STIXTwoText.ttf、STIXTwoMath-Regular.ttf | STIX Two（stixfonts 项目） |

代码字体使用系统中的 JetBrains Mono（没有时退回等宽字体）。

```bash
python3 build.py              # 输出 build/book.pdf；第二遍会把页码填进目录
python3 fill_appC.py         # 可选：用 code/rerun_logs/times.tsv 重新生成附录 C（src/appC.md）
for i in 1 2 3 4 5 6 7; do python3 figs/p$i.py; done   # 可选：重新绘制全部插图（p3 需要 PyTorch；p7 读取 figs/data/ch35_diffusion.json，可用 figs/data/dump_ch35_diffusion.py 重新生成）
```

`build.py` 的流程：Markdown → 把正文中的英文双引号换成中文引号 → pandoc（数学公式输出为 MathML）→ 内联 `figs/*.svg`、按章给图编号、把 `{{fig-…}}` 换成“图 N.k” → HTML + `book.css` → Chromium 打印成 PDF。

## 网站

```bash
python3 build.py              # 先构建 PDF（网页版提供它的下载）
python3 build_web.py          # 输出 site/
cd site && python3 -m http.server 8000   # 本地预览：http://localhost:8000
```

`build_web.py` 复用 `build.py` 的引号处理和插图编号，每个前言小节、篇、章、附录各生成一页，带侧边目录、全书搜索（`/` 键）、可点击的图号引用（跨章也能跳转）、点击放大插图、代码复制按钮，深浅色跟随阅读者的设置。中文用读者系统自带的字体，数学公式用随站点提供的 STIX Two Math（`web/fonts/`，woff2），不依赖任何外部 CDN。

PDF 的排版前提：第 34 章一个很宽的公式会让 Chromium 自动缩小页面，`render.js` 因此固定按 76.5% 打印，保证在任何机器上分页一致；`build.py` 最后会无损重新压缩 PDF（约 22 MB → 12 MB）。

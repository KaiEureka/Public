# 飞书 LLM 知识库整理

[阅读知识库目录](reference/飞书_LLMs知识库/目录.md)

主人分享的飞书知识库“LLMs（大语言模型）持续更新~”的完整导出（2026-10-31），共 135 个节点：九个部分（一：模型架构 …… 九：前沿与工程实践），132 篇文档 + 3 个 PDF 附件，692 张图片。

- `目录.md`：整棵树，带链接；`tree.json`：节点的原始信息（wiki_token、obj_token、类型）。
- 每篇文档是一个 `.md`，图片在同目录的 `media/`。原文有大量“文字 + 公式”的截图：692 张截图已逐张转写成 Markdown + LaTeX，存在 `_ocr/<图片名>.md`（由 Claude 子代理看图转写，2026-11-09）；`tools/feishu_polish.py` 用转写替换截图（原图以 `{.ocr-src}` 标记保留），并把复制坏的行内公式碎片（`s*s*`、`*λU*`、`*W*0`、`n=8*n*=8` 等）还原成 LaTeX；规则管不了的复杂公式（如 `83dmodel38*dmodel*`）逐条手写在 `tools/feishu_fixes.tsv` 里，左边是原始导出的写法。其中 41 张是真正的示意图，保留原图并以一句话说明作图注。知识库更新后，新增的截图需要再转写（清单可仿照 `_ocr/` 的命名生成）。
- PDF 附件旁有同名的 `.pdf.md`，是自动抽取的文字（`tools/pdf_to_md.py`）。
- 原文中嵌入的 100 个电子表格，已用 `tools/feishu_sheets.js` 从表格数据还原成 Markdown 表格（导出后要再跑一次这个脚本）；原文的“目录”组件被略去。

重新导出（知识库更新后）：

```
SPACE_ID=7597328668402174905 NODE_PATH=$(npm root -g) node tools/feishu_export.js \
  "https://lcnipys9u0xh.feishu.cn/wiki/GOflwsFQDicQ1YkkbUlcoi8lnFe" A7J5woWoRiJf2gkiyjVcJQ3AnYd "reference/飞书_LLMs知识库"
NODE_PATH=$(npm root -g) node tools/feishu_sheets.js reference/飞书_LLMs知识库
python3 tools/pdf_to_md.py reference/飞书_LLMs知识库
python3 tools/feishu_polish.py reference/飞书_LLMs知识库
```

脚本会跳过已存在的文件；要全部重来，先删掉输出目录。知识库是公开分享的，导出时不需要登录或密码。

运行 `python3 tools/build_ref_site.py` 可在 `ref_site/` 生成静态网页版。

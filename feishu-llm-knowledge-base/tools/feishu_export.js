// 把一个公开分享的飞书知识库（wiki）整棵树导出成 Markdown：目录、每篇文档、图片、附件（PDF 等）。
// 原理：用无头 Chromium 打开任意一页拿到匿名会话，然后直接调用网页版自己用的接口：
//   /space/api/wiki/v2/tree/get_node_child/   列子节点
//   /space/api/docx/pages/client_vars          取文档的全部 block（JSON）
//   /space/api/box/stream/download/all/<token>/  下载图片和附件
// 用法：NODE_PATH=$(npm root -g) node tools/feishu_export.js <任意一页的 URL> <根节点 wiki_token> <输出目录>
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [START, ROOT, OUT] = process.argv.slice(2);
const host = new URL(START).origin;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const safe = s => s.replace(/[\/\\:*?"<>|\n\r\t]/g, '_').replace(/\s+/g, ' ').trim().slice(0, 80);

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;  // Node 端请求也要走代理
  const browser = await chromium.launch({ proxy });
  const ctx = await browser.newContext({ proxy });
  const page = await ctx.newPage();
  await page.goto(START, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await sleep(6000);
  const spaceId = (await page.content()).match(/space_id["=:\\]+(\d{10,})/)?.[1] || process.env.SPACE_ID;
  async function getJSON(u) {
    for (let i = 0; i < 4; i++) {
      try { const t = await page.evaluate(async u => { const r = await fetch(u, { credentials: 'include' }); return r.ok ? r.text() : null; }, u); if (t) return JSON.parse(t); } catch (e) {}
      await sleep(1500 * (i + 1));
    }
    throw new Error('GET failed ' + u);
  }
  async function download(token, dest, mount, nodeTok) {
    if (fs.existsSync(dest)) return true;
    const urls = [`https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/${token}/?fallback_source=1&height=1280&mount_node_token=${nodeTok || ''}&mount_point=${mount}&policy=equal`,
                  `${host}/space/api/box/stream/download/all/${token}/?mount_point=${mount}`,
                  `https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/all/${token}/?mount_point=${mount}`,
                  `https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/v2/cover/${token}/?fallback_source=1&height=1280&mount_point=${mount}`];
    for (const u of urls) {
      try { const r = await ctx.request.get(u, { timeout: 120000, headers: { referer: host + '/' } }); if (r.ok()) { const b = await r.body(); if (b.length > 100) { fs.writeFileSync(dest, b); return true; } } } catch (e) {}
    }
    return false;
  }

  // ---------- 1. 目录树 ----------
  const nodes = [];                                    // {token, title, obj_type, obj_token, depth, parent}
  async function walk(token, depth) {
    const d = await getJSON(`/space/api/wiki/v2/tree/get_node_child/?space_id=${spaceId}&wiki_token=${token}&expand_shortcut=true`);
    const kids = (d.data && d.data[token]) || [];
    for (const k of kids) {
      const n = { token: k.wiki_token, title: k.title.trim(), obj_type: k.obj_type, obj_token: k.obj_token, depth, parent: token };
      nodes.push(n);
      if (k.has_child) await walk(k.wiki_token, depth + 1);
    }
  }
  const rootInfo = (await getJSON(`/space/api/wiki/v2/tree/get_info/?space_id=${spaceId}&with_space=true&expand_shortcut=true&need_shared=true&exclude_fields=5&wiki_token=${ROOT}`)).data.tree.nodes[ROOT];
  const rootTitle = rootInfo.title.trim();
  nodes.push({ token: ROOT, title: rootTitle, obj_type: rootInfo.obj_type, obj_token: rootInfo.obj_token, depth: 0, parent: null });
  await walk(ROOT, 1);
  console.log('nodes', nodes.length);

  // 每个节点的文件路径：按目录层级建文件夹
  const byToken = Object.fromEntries(nodes.map(n => [n.token, n]));
  for (const n of nodes) {
    const parts = []; let p = n;
    while (p && p.parent) { p = byToken[p.parent]; if (p && p.parent) parts.unshift(safe(p.title)); }
    n.dir = path.join(OUT, ...parts);
    n.file = path.join(n.dir, safe(n.title) + (n.obj_type === 22 ? '.md' : ''));
  }
  fs.mkdirSync(OUT, { recursive: true });

  // ---------- 2. 文档 → Markdown ----------
  function runs(textObj) {
    const t = textObj?.initialAttributedTexts; if (!t || !t.text) return '';
    const keys = Object.keys(t.text).sort((a, b) => a - b);
    const pool = textObj.apool?.numToAttrib || {};
    let out = '';
    for (const k of keys) {
      const s = t.text[k] || '', attribs = (t.attribs && t.attribs[k]) || ''; let pos = 0;
      const re = /((?:\*[0-9a-z]+)*)(?:\|[0-9a-z]+)?\+([0-9a-z]+)/g; let m, any = false;
      while ((m = re.exec(attribs))) {
        any = true; const len = parseInt(m[2], 36); let seg = s.slice(pos, pos + len); pos += len;
        const set = (m[1].match(/\*([0-9a-z]+)/g) || []).map(x => pool[parseInt(x.slice(1), 36)] || []);
        const has = n => set.find(a => a[0] === n);
        if (has('equation')) seg = `$${has('equation')[1] || seg}$`;
        else {
          if (has('inlineCode')) seg = '`' + seg + '`';
          if (has('bold') && seg.trim()) seg = `**${seg}**`;
          if (has('italic') && seg.trim()) seg = `*${seg}*`;
          if (has('strikethrough') && seg.trim()) seg = `~~${seg}~~`;
          const link = has('link'); if (link) { try { seg = `[${seg}](${decodeURIComponent(link[1])})`; } catch (e) {} }
        }
        out += seg;
      }
      if (!any || pos < s.length) out += s.slice(pos);
    }
    return out.replace(/​/g, '');
  }
  async function exportDoc(n) {
    if (fs.existsSync(n.file)) return;
    const bm = {}; let cursor = '', seq = [];
    for (let i = 0; i < 50; i++) {
      const d = (await getJSON(`/space/api/docx/pages/client_vars?id=${n.obj_token}&mode=7&limit=1000${cursor ? '&cursor=' + encodeURIComponent(cursor) : ''}`)).data;
      if (!d) break;
      const before = Object.keys(bm).length; Object.assign(bm, d.block_map || {}); seq = seq.concat(d.block_sequence || []);
      if (!d.has_more || !(d.next_cursors || []).length || Object.keys(bm).length === before) break;
      cursor = d.next_cursors[0];
    }
    const mediaDir = path.join(n.dir, 'media'); const lines = []; let imgs = 0, missing = 0;
    async function emit(id, depth, listIdx) {
      const b = bm[id]; if (!b) return; const D = b.data, type = D.type, ind = '  '.repeat(depth);
      const txt = runs(D.text);
      const kids = D.children || [];
      // 飞书的有序列表编号跨段落延续，遇到标题或分隔线才重新从 1 数
      const recur = async (dd) => { let k = 0; for (const c of kids) { const t = bm[c]?.data?.type; if (t === 'ordered') k = /^\d+$/.test(bm[c].data.seq) ? +bm[c].data.seq : k + 1; else if (/^heading|divider/.test(t || '')) k = 0; await emit(c, dd, k); } };
      if (type === 'page') { lines.push(`# ${txt || n.title}`, ''); await recur(0); return; }
      const h = type.match(/^heading(\d)$/);
      if (h) { lines.push(`${'#'.repeat(Math.min(+h[1] + 1, 6))} ${txt}`, ''); await recur(depth); return; }
      switch (type) {
        case 'text': if (txt.trim()) lines.push(ind + txt, ''); await recur(depth); break;
        case 'bullet': lines.push(`${ind}- ${txt}`); await recur(depth + 1); if (!depth) lines.push(''); break;
        case 'ordered': lines.push(`${ind}${listIdx}. ${txt}`); await recur(depth + 1); if (!depth) lines.push(''); break;
        case 'todo': lines.push(`${ind}- [${D.done ? 'x' : ' '}] ${txt}`); await recur(depth + 1); break;
        case 'code': lines.push('```' + (D.language || '').toString().toLowerCase(), runs(D.text), '```', ''); break;
        case 'equation': lines.push('$$', txt, '$$', ''); break;
        case 'quote': lines.push('> ' + txt, ''); break;
        case 'divider': lines.push('---', ''); break;
        case 'callout': case 'quote_container': { const start = lines.length; await recur(0); for (let i = start; i < lines.length; i++) lines[i] = lines[i] ? '> ' + lines[i] : '>'; lines.push(''); break; }
        case 'image': {
          const tok = D.image?.token; fs.mkdirSync(mediaDir, { recursive: true });
          const ext = (D.image?.mimeType || 'image/png').split('/')[1].replace('jpeg', 'jpg');
          const f = path.join(mediaDir, `${tok}.${ext}`);
          const ok = tok && await download(tok, f, 'docx_image', id); ok ? imgs++ : missing++;
          lines.push(`![${runs(D.image?.caption?.text)}](media/${tok}.${ext})${ok ? '' : ' <!-- 图片下载失败 -->'}`, ''); break;
        }
        case 'table': {
          const cols = (D.columns_id || []).length || 1; const cells = D.cells || kids;
          const texts = [];
          for (const c of cells) { const sub = []; const save = lines.length; await emitCell(c, sub); texts.push(sub.join(' ').replace(/\|/g, '\\|')); }
          for (let r = 0; r * cols < texts.length; r++) { lines.push('| ' + texts.slice(r * cols, r * cols + cols).join(' | ') + ' |'); if (r === 0) lines.push('|' + ' --- |'.repeat(cols)); }
          lines.push(''); break;
        }
        case 'grid': case 'grid_column': case 'view': await recur(depth); break;
        case 'sheet': lines.push(`> [嵌入的电子表格，未导出：${D.token}]`, ''); break;
        case 'isv': if (D.data && 'showCataLogLevel' in D.data) break;  // 飞书的“目录”组件，跳过
        case 'iframe': case 'diagram': case 'board': case 'mindnote': lines.push(`> [嵌入组件（${type}），未导出]`, ''); break;
        case 'file': { const tok = D.file?.token, name = D.file?.name || tok; fs.mkdirSync(mediaDir, { recursive: true });
          const ok = tok && await download(tok, path.join(mediaDir, safe(name)), 'docx_file', id); lines.push(`[附件：${name}](media/${encodeURI(safe(name))})${ok ? '' : ' <!-- 下载失败 -->'}`, ''); break; }
        default: if (txt.trim()) lines.push(ind + txt, ''); await recur(depth);
      }
    }
    async function emitCell(id, sink) {
      const b = bm[id]; if (!b) return; const t = runs(b.data.text); if (t.trim()) sink.push(t);
      for (const c of b.data.children || []) await emitCell(c, sink);
    }
    await emit(n.obj_token, 0, 0);
    fs.mkdirSync(n.dir, { recursive: true });
    fs.writeFileSync(n.file, lines.join('\n').replace(/\n{3,}/g, '\n\n') + '\n');
    console.log(`doc ${n.title}  blocks=${Object.keys(bm).length} imgs=${imgs} missing=${missing}`);
  }

  // ---------- 3. 逐个处理 ----------
  const index = [`# ${rootTitle}`, '', `从 ${START} 导出（根节点 ${ROOT}）。共 ${nodes.length} 个节点。`, ''];
  for (const n of nodes) {
    const rel = path.relative(OUT, n.file);
    index.push(`${'  '.repeat(Math.max(n.depth - 1, 0))}- [${n.title}](${encodeURI(rel)})${n.obj_type === 22 ? '' : `（附件，obj_type=${n.obj_type}）`}`);
    try {
      if (n.obj_type === 22) await exportDoc(n);
      else { fs.mkdirSync(n.dir, { recursive: true }); let ok = false; try { const r = await ctx.request.get(`${host}/space/api/box/stream/download/preview/${n.obj_token}/?preview_type=9`, { timeout: 180000, headers: { referer: host + '/' } }); const b = await r.body(); if (r.ok() && b.length > 100) { fs.writeFileSync(n.file, b); ok = true; } } catch (e) {} console.log(`file ${n.title} ${ok ? 'ok' : 'FAILED'}`); }
    } catch (e) { console.log('ERROR', n.title, e.message); }
  }
  fs.writeFileSync(path.join(OUT, '目录.md'), index.join('\n') + '\n');
  fs.writeFileSync(path.join(OUT, 'tree.json'), JSON.stringify(nodes.map(({ dir, file, ...r }) => ({ ...r, file: path.relative(OUT, file) })), null, 1));
  await browser.close();
})();

// 补全 feishu_export.js 留下的“嵌入的电子表格，未导出”占位：取出表格数据，还原成 Markdown 表格。
// 表格接口 /space/api/v3/sheet/client_vars 返回 gzip 过的 protobuf（无 schema，下面按实测结构解析）：
//   block.1.2.12.1  区域：2 = 起始列，4 = 结束列（不含）
//   block.1.2.12.2  字符串池：字段 2 依次是各字符串；字段 3 是富文本记录，其字段 1 指向字符串池
//   block.1.2.12.6  单元格：字段 1 是按行排列的“取值编号”（0 = 空格子），字段 2 是取值表：
//                   {1: 类型, 2: 下标}，类型 3 = 字符串池下标，类型 6 = 富文本下标
// 请求要带 x-csrftoken（取自 _csrf_token cookie）、docs-host-id（所在文档的 wiki token）和任意 memberId。
// 用法：NODE_PATH=$(npm root -g) node tools/feishu_sheets.js reference/飞书_LLMs知识库
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), zlib = require('zlib');
const OUT = process.argv[2];
const tree = JSON.parse(fs.readFileSync(path.join(OUT, 'tree.json'), 'utf8'));
const host = 'https://lcnipys9u0xh.feishu.cn';
const sleep = ms => new Promise(r => setTimeout(r, ms));

function fields(b) {                                  // 一层 protobuf：[[字段号, 值]]，值为数字或 Buffer
  let i = 0; const out = [];
  const varint = () => { let x = 0, s = 0, c; do { c = b[i++]; x += (c & 0x7f) * 2 ** s; s += 7; } while (c & 0x80); return x; };
  while (i < b.length) {
    const k = varint(), f = Math.floor(k / 8), wt = k & 7;
    if (wt === 0) out.push([f, varint()]);
    else if (wt === 2) { const n = varint(); out.push([f, b.subarray(i, i + n)]); i += n; }
    else if (wt === 1) { out.push([f, b.subarray(i, i + 8)]); i += 8; }
    else if (wt === 5) { out.push([f, b.subarray(i, i + 4)]); i += 4; }
    else throw new Error('wire type ' + wt);
  }
  return out;
}
const get = (fs_, n) => fs_.filter(x => x[0] === n).map(x => x[1]);
function packed(b) { const out = []; let i = 0; while (i < b.length) { let x = 0, s = 0, c; do { c = b[i++]; x += (c & 0x7f) * 2 ** s; s += 7; } while (c & 0x80); out.push(x); } return out; }

function blockToRows(buf) {                          // 返回 { colStart, rows: [[单元格文字]] }
  const m12 = get(fields(get(fields(get(fields(buf), 1)[0]), 2)[0]), 12)[0];
  const f = fields(m12);
  const range = Object.fromEntries(fields(get(f, 1)[0]).filter(x => typeof x[1] === 'number'));
  const poolMsg = fields(get(f, 2)[0]);
  const pool = get(poolMsg, 2).map(b => b.toString('utf8'));
  const rich = get(poolMsg, 3).map(b => get(fields(b), 1)[0]);
  const cellMsg = fields(get(f, 6)[0]);
  const order = packed(get(cellMsg, 1)[0]);
  const values = get(cellMsg, 2).map(b => b.length ? Object.fromEntries(fields(b).filter(x => typeof x[1] === 'number')) : null);
  const text = v => !v ? '' : v[1] === 3 ? pool[v[2]] ?? '' : v[1] === 6 ? pool[rich[v[2]]] ?? '' : (v[2] !== undefined ? String(pool[v[2]] ?? '') : '');
  const cols = (range[4] ?? 1) - (range[2] ?? 0);
  const rows = [];
  for (let r = 0; r * cols < order.length; r++) rows.push(order.slice(r * cols, r * cols + cols).map(k => text(values[k])));
  return { rowStart: range[1] ?? 0, rows };
}

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const page = await browser.newPage();
  await page.goto(`${host}/wiki/${tree[0].token}`, { waitUntil: 'domcontentloaded', timeout: 90000 });
  await sleep(6000);
  const csrf = (await page.context().cookies()).find(c => c.name === '_csrf_token')?.value || '';
  let done = 0, failed = 0;
  for (const n of tree) {
    if (n.obj_type !== 22) continue;
    const file = path.join(OUT, n.file);
    let md = fs.readFileSync(file, 'utf8');
    const toks = [...md.matchAll(/^> \[嵌入的电子表格，未导出：([^\]]+)\]$/gm)].map(m => m[1]);
    for (const tok of toks) {
      const [sheetTok, sheetId] = tok.split('_');
      let table = '';
      try {
        const d = await page.evaluate(async ([t, s, c, host]) => {
          const r = await fetch('/space/api/v3/sheet/client_vars', { method: 'POST', headers: { 'content-type': 'application/json', 'x-csrftoken': c, 'docs-host-id': host },
            body: JSON.stringify({ memberId: Date.now(), schemaVersion: 9, openType: 1, token: t, sheetRange: { sheetId: s }, clientVersion: 'v0.0.1' }) });
          return (await r.json()).data;
        }, [sheetTok, sheetId, csrf, n.token]);
        const parts = Object.values(d.snapshot.blocks || {}).map(v => blockToRows(zlib.gunzipSync(Buffer.from(v, 'base64'))));
        const rows = parts.sort((a, b) => a.rowStart - b.rowStart).flatMap(p => p.rows)
          .filter(r => r.some(c => c.trim()));
        if (rows.length) {
          const w = Math.max(1, ...rows.map(r => r.reduce((m, c, j) => (c || '').trim() ? j + 1 : m, 0)));  // 去掉末尾全空的列
          const cell = c => (c || '').replace(/\|/g, '\\|').replace(/\n+/g, '<br>');
          table = rows.map((r, i) => '| ' + Array.from({ length: w }, (_, j) => cell(r[j])).join(' | ') + ' |' + (i === 0 ? '\n|' + ' --- |'.repeat(w) : '')).join('\n');
        }
      } catch (e) { console.log('  error', tok, e.message); }
      if (table) { md = md.replace(`> [嵌入的电子表格，未导出：${tok}]`, table); done++; } else failed++;
      console.log(`${n.title.slice(0, 32)}  ${tok}  ${table ? 'ok' : 'FAILED'}`);
    }
    if (toks.length) fs.writeFileSync(file, md);
  }
  console.log(`tables restored: ${done}, failed: ${failed}`);
  await browser.close();
})();

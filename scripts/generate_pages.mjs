#!/usr/bin/env node
/**
 * 万物可视化 - 非破坏式页面生成脚本
 * Node >= 18，无第三方依赖
 */
import { promises as fs } from 'fs';
import path from 'path';

const ROOT = process.cwd();
const APP_DIR = path.join(ROOT, 'app');
const MODULES_DIR = path.join(APP_DIR, 'modules');
const ASSETS_CSS = path.join(APP_DIR, 'assets', 'style.css');

const AUTO_BEGIN = '<!-- AUTO-GENERATED:BEGIN -->';
const AUTO_END = '<!-- AUTO-GENERATED:END -->';

const argMap = parseArgs(process.argv.slice(2));
const FORCE = !!argMap.force;
const ONLY = argMap.module || null; // linear_algebra | probability_statistics | differential_geometry

const MODULE_META = {
  linear_algebra: { name: '线性代数可视化世界' },
  probability_statistics: { name: '概率与统计可视化世界' },
  differential_geometry: { name: '微分几何可视化世界', toc: 'toc_diffgeom.md' },
};

function parseArgs(argv) {
  const res = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--force') res.force = true;
    else if (a === '--module') res.module = argv[i + 1];
  }
  return res;
}

async function ensureDirs(dir) { await fs.mkdir(dir, { recursive: true }); }

function nowString() {
  const d = new Date(); const pad = n => n.toString().padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function escapeHTML(str) {
  return String(str).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
}
function escapeAttr(str) { return String(str).replaceAll('"', '&quot;').replaceAll("'", '&#39;'); }

// ----------- 索引页非破坏式写入 -----------
async function upsertAutoBlock(filePath, initialShellHTML, autoBlockHTML) {
  const exists = await fs.stat(filePath).catch(() => null);
  if (!exists) {
    const full = initialShellHTML.replace(AUTO_BEGIN + AUTO_END, AUTO_BEGIN + autoBlockHTML + AUTO_END);
    await ensureDirs(path.dirname(filePath));
    await fs.writeFile(filePath, full, 'utf-8');
    return 'created';
  }
  const old = await fs.readFile(filePath, 'utf-8');
  const beginIdx = old.indexOf(AUTO_BEGIN);
  const endIdx = old.indexOf(AUTO_END);
  if (beginIdx !== -1 && endIdx !== -1 && endIdx > beginIdx) {
    const before = old.slice(0, beginIdx + AUTO_BEGIN.length);
    const after = old.slice(endIdx);
    const next = before + autoBlockHTML + after;
    await fs.writeFile(filePath, next, 'utf-8');
    return 'updated_block';
  }
  // 若缺少标记，非破坏式：在 </body> 前插入标记块
  const injected = old.replace('</body>', `${AUTO_BEGIN}${autoBlockHTML}${AUTO_END}\n</body>`);
  await fs.writeFile(filePath, injected, 'utf-8');
  return 'injected_block';
}

// ----------- 线性代数/概率统计：扫描 pages 提取标题 -----------
async function scanModulePages(moduleKey) {
  const pagesDir = path.join(MODULES_DIR, moduleKey, 'pages');
  const entries = await fs.readdir(pagesDir).catch(() => []);
  const items = [];
  for (const f of entries) {
    if (!f.endsWith('.html')) continue;
    const fp = path.join(pagesDir, f);
    const raw = await fs.readFile(fp, 'utf-8').catch(() => '');
    const titleMatch = raw.match(/<title[^>]*>([^<]*)<\/title>/i);
    let title = titleMatch?.[1]?.trim();
    if (!title) {
      const h1Match = raw.match(/<h1[^>]*>([^<]*)<\/h1>/i);
      title = h1Match?.[1]?.trim();
    }
    const id = f.replace(/\.html$/i, '');
    items.push({ id, title: title || id, summary: '' });
  }
  return items;
}

// ----------- 微分几何：读取 TOC 并补页 -----------
async function readTOC_DG() {
  const tocPath = path.join(MODULES_DIR, 'differential_geometry', MODULE_META.differential_geometry.toc);
  try {
    const raw = await fs.readFile(tocPath, 'utf-8');
    const lines = raw.split(/\r?\n/).map(s => s.trim());
    const concepts = [];
    for (const line of lines) {
      if (!line || line.startsWith('#')) continue;
      const parts = line.split('|').map(s => s.trim());
      if (parts.length < 3) { console.warn('[WARN] 跳过非法 TOC 行(differential_geometry):', line); continue; }
      const [id, title, summary, viz = 'plotly', dataPath = ''] = parts;
      if (!id || !title) continue;
      concepts.push({ id, title, summary, viz, dataPath });
    }
    return concepts;
  } catch (e) {
    console.warn('[INFO] 微分几何未找到 TOC：', tocPath);
    return [];
  }
}

async function renderConceptHTML_DG(concept) {
  const tplPath = path.join(MODULES_DIR, 'differential_geometry', 'templates', 'concept.template.html');
  const tpl = await fs.readFile(tplPath, 'utf-8');
  return tpl
    .replaceAll('{{ID}}', escapeHTML(concept.id))
    .replaceAll('{{TITLE}}', escapeHTML(concept.title))
    .replaceAll('{{SUMMARY}}', escapeHTML(concept.summary))
    .replaceAll('{{MODULE}}', MODULE_META.differential_geometry.name)
    .replaceAll('{{VIZ}}', concept.viz || 'plotly')
    .replaceAll('{{DATAPATH}}', concept.dataPath || '');
}

async function ensureDGPages(concepts) {
  const pagesDir = path.join(MODULES_DIR, 'differential_geometry', 'pages');
  await ensureDirs(pagesDir);
  for (const c of concepts) {
    const fp = path.join(pagesDir, `${c.id}.html`);
    const exists = await fs.stat(fp).catch(() => null);
    if (exists && !FORCE) continue; // 非破坏式：存在则跳过，除非 --force
    const html = await renderConceptHTML_DG(c);
    await fs.writeFile(fp, html, 'utf-8');
  }
}

// ----------- 索引页渲染 -----------
function renderModuleIndexShell(moduleKey, modName) {
  const relCSS = '../../assets/style.css';
  const backRoot = '../../index.html';
  return `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <title>${modName}</title>\n  <link rel="stylesheet" href="${relCSS}" />\n</head>\n<body>\n  <div class="container">\n    <div class="header">\n      <h1>${modName}</h1>\n      <div class="actions">\n        <a class="button secondary" href="${backRoot}">返回“万物可视化”</a>\n      </div>\n    </div>\n\n    ${AUTO_BEGIN}${AUTO_END}\n\n  </div>\n</body>\n</html>`;
}

function renderModuleIndexAutoBlock(items) {
  const last = nowString();
  const search = `<div class="search"><input id="search" type="text" placeholder="搜索概念（标题/简介）" /></div>`;
  const cards = items.map(c => `\n    <div class=\"card\" data-q=\"${escapeAttr((c.title||'') + ' ' + (c.summary||''))}\">\n      <h3>${escapeHTML(c.title||'')}</h3>\n      <p>${escapeHTML(c.summary||'')}</p>\n      <div class=\"actions\">\n        <a class=\"button\" href=\"./pages/${encodeURI(c.id)}.html\">进入</a>\n      </div>\n    </div>`).join('\n');
  const grid = `<div class=\"grid\" id=\"cards\">${cards || '<p style=\"color:#6b7280\">暂无概念</p>'}</div>`;
  const footer = `<div class=\"footer\"><span>概念数量：${items.length}</span><span>最后生成时间：${last}</span></div>`;
  const script = `<script>(()=>{\n    const input=document.getElementById('search');\n    const cards=Array.from(document.querySelectorAll('#cards .card'));\n    input&&input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();cards.forEach(card=>{const t=(card.getAttribute('data-q')||'').toLowerCase();card.style.display=t.includes(q)?'':'none';});});\n  })();</script>`;
  return `${search}\n${grid}\n${footer}\n${script}`;
}

function renderRootIndexShell() {
  const relCSS = 'app/assets/style.css';
  return `<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n  <meta charset="UTF-8" />\n  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n  <title>万物可视化（概率论与数理统计 / 线性代数 / 微分几何）</title>\n  <link rel="stylesheet" href="${relCSS}" />\n</head>\n<body>\n  <div class="container">\n    <div class="header">\n      <h1>万物可视化</h1>\n    </div>\n\n    ${AUTO_BEGIN}${AUTO_END}\n\n  </div>\n</body>\n</html>`;
}

function renderRootIndexAutoBlock(stats, links) {
  const last = nowString();
  const cards = ['probability_statistics','linear_algebra','differential_geometry'].map(key => {
    const meta = MODULE_META[key];
    const count = stats.find(s => s.moduleKey === key)?.count || 0;
    const summary = key === 'probability_statistics' ? '概率论与数理统计的核心概念可视化'
      : key === 'linear_algebra' ? '线性代数的矩阵、向量与变换可视化'
      : '微分几何的曲率、测地线与平行移动可视化';
    const href = links?.[key] || `./app/modules/${key}/index.html`;
    return `\n      <div class=\"card\">\n        <h3>${meta.name}</h3>\n        <p>${summary}</p>\n        <div class=\"actions\">\n          <a class=\"button\" href=\"${href}\">进入 (${count})</a>\n        </div>\n      </div>`;
  }).join('\n');
  const grid = `<div class=\"grid\">${cards}</div>`;
  const footer = `<div class=\"footer\"><span>最后生成时间：${last}</span></div>`;
  return `${grid}\n${footer}`;
}

async function fileExists(p) { return !!(await fs.stat(p).catch(() => null)); }

function renderLegacyModuleAutoBlock(items, moduleKey) {
  const last = nowString();
  const title = moduleKey === 'linear_algebra' ? '可视化页面（自动）' : '可视化页面（自动）';
  const list = items.map(it => `\n        <li><a href=\"./pages/${encodeURI(it.id)}.html\">${escapeHTML(it.title || it.id)}</a></li>`).join('\n');
  return `\n  <section class=\"auto-section\">\n    <h2>${title}</h2>\n    <aside class=\"sidebar\">\n      <ul class=\"nav-list\">${list || '<li>暂无页面</li>'}</ul>\n    </aside>\n    <div class=\"footer\"><span>最后生成时间：${last}</span></div>\n  </section>`;
}

async function upsertLegacyModuleIndex(moduleKey, items) {
  const legacyPath = path.join(ROOT, moduleKey === 'linear_algebra' ? 'index-la.html' : 'index-prob.html');
  const shell = `<!DOCTYPE html>\n<html lang=\"zh-CN\">\n<head>\n  <meta charset=\"UTF-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n  <title>${MODULE_META[moduleKey].name}</title>\n  <link rel=\"stylesheet\" href=\"app/assets/style.css\" />\n</head>\n<body>\n  ${AUTO_BEGIN}${AUTO_END}\n</body>\n</html>`;
  const block = renderLegacyModuleAutoBlock(items, moduleKey);
  await upsertAutoBlock(legacyPath, shell, block);
}

// ----------- 每个模块处理 -----------
async function processLinearOrProbability(moduleKey) {
  const items = await scanModulePages(moduleKey);
  const shell = renderModuleIndexShell(moduleKey, MODULE_META[moduleKey].name);
  const block = renderModuleIndexAutoBlock(items);
  const indexPath = path.join(MODULES_DIR, moduleKey, 'index.html');
  await upsertAutoBlock(indexPath, shell, block);
  return { moduleKey, count: items.length };
}

async function processDifferentialGeometry() {
  const concepts = await readTOC_DG();
  await ensureDGPages(concepts); // 非破坏式补页（仅缺失或 --force）
  const items = concepts.map(c => ({ id: c.id, title: c.title, summary: c.summary }));
  const shell = renderModuleIndexShell('differential_geometry', MODULE_META.differential_geometry.name);
  const block = renderModuleIndexAutoBlock(items);
  const indexPath = path.join(MODULES_DIR, 'differential_geometry', 'index.html');
  await upsertAutoBlock(indexPath, shell, block);
  return { moduleKey: 'differential_geometry', count: items.length };
}

async function main() {
  const cssExists = await fs.stat(ASSETS_CSS).catch(() => null);
  if (!cssExists) console.warn('[WARN] 缺少通用样式 app/assets/style.css，建议创建以统一视觉风格。');

  const modules = ONLY ? [ONLY] : ['linear_algebra','probability_statistics','differential_geometry'];
  const stats = [];
  let laItems = null, probItems = null;
  for (const m of modules) {
    if (m === 'linear_algebra') {
      const sItems = await scanModulePages(m);
      laItems = sItems; stats.push(await processLinearOrProbability(m));
    } else if (m === 'probability_statistics') {
      const sItems = await scanModulePages(m);
      probItems = sItems; stats.push(await processLinearOrProbability(m));
    } else if (m === 'differential_geometry') {
      stats.push(await processDifferentialGeometry());
    }
  }

  // 旧版模块主页：注入自动页面列表（非破坏式，仅标记块）
  if (laItems) await upsertLegacyModuleIndex('linear_algebra', laItems);
  if (probItems) await upsertLegacyModuleIndex('probability_statistics', probItems);

  // 根索引：优先链接到旧版模块主页（存在时）
  const hasLA = await fileExists(path.join(ROOT, 'index-la.html'));
  const hasProb = await fileExists(path.join(ROOT, 'index-prob.html'));
  const links = {
    linear_algebra: hasLA ? './index-la.html' : './app/modules/linear_algebra/index.html',
    probability_statistics: hasProb ? './index-prob.html' : './app/modules/probability_statistics/index.html',
    differential_geometry: './app/modules/differential_geometry/index.html',
  };

  const rootShell = renderRootIndexShell();
  const rootBlock = renderRootIndexAutoBlock(stats, links);
  const rootIndexPath = path.join(ROOT, 'index.html');
  await upsertAutoBlock(rootIndexPath, rootShell, rootBlock);

  console.log('[DONE] 页面生成完成：', stats.map(s => `${s.moduleKey}:${s.count}`).join(', '));
}

main().catch(err => { console.error('[FATAL] 生成失败:', err); });
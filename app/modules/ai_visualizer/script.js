const API_BASE = 'http://localhost:5051'; // FastAPI server base
const RESOLVE_ENDPOINT = `${API_BASE}/api/resolve_or_generate`;
const STATIC_BASE = 'http://localhost:8001/';

async function loadExamples() {
  try {
    const resp = await fetch('examples.json');
    const data = await resp.json();
    const list = document.getElementById('examplesList');
    list.innerHTML = '';
    data.examples.forEach((ex) => {
      const li = document.createElement('li');
      li.textContent = ex;
      li.addEventListener('click', () => {
        document.getElementById('prompt').value = ex;
      });
      list.appendChild(li);
    });
  } catch (e) {
    console.error('加载示例失败', e);
  }
}

function setStatus(text, kind = 'info') {
  const el = document.getElementById('status');
  el.textContent = text;
  el.dataset.kind = kind;
}

function showInPreview(url) {
  const frame = document.getElementById('vizFrame');
  let finalUrl = url;
  if (!/^https?:\/\//.test(url)) {
    finalUrl = STATIC_BASE + url;
  }
  frame.src = finalUrl;
}

function showResult(url, kind) {
  const hint = document.getElementById('resultHint');
  let finalUrl = url;
  if (!/^https?:\/\//.test(url)) {
    finalUrl = STATIC_BASE + url;
  }
  if (kind === 'existing') {
    showInPreview(finalUrl);
    if (hint) hint.textContent = '命中已有可视化：右栏已展示';
  } else if (kind === 'generated') {
    window.open(finalUrl, '_blank');
    if (hint) hint.textContent = '已生成新页面：在新窗口打开，右栏也展示';
    showInPreview(finalUrl);
  }
}

async function onGenerate() {
  const prompt = document.getElementById('prompt').value.trim();
  if (!prompt) {
    setStatus('请输入可视化需求', 'warn');
    return;
  }
  setStatus('正在解析/生成中…', 'loading');
  try {
    const resp = await fetch(RESOLVE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, vizType: '自动', complexity: '中等' })
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    if (data && data.kind && data.url) {
      setStatus(data.kind === 'existing' ? '命中已有可视化' : '生成完成', 'ok');
      showResult(data.url, data.kind);
    } else {
      throw new Error('接口返回缺少必要字段');
    }
  } catch (e) {
    console.error(e);
    setStatus('生成失败：' + e.message, 'error');
    const hint = document.getElementById('resultHint');
    hint.textContent = '请稍后重试，或更换描述再试';
  }
}

function bindFullscreenButtons() {
  const pane = document.querySelector('.preview-pane');
  const winBtn = document.getElementById('btnWinFull');
  const sysBtn = document.getElementById('btnSysFull');

  if (winBtn) {
    winBtn.addEventListener('click', () => {
      const active = pane.classList.toggle('window-fullscreen');
      winBtn.textContent = active ? '退出全屏' : '窗口全屏';
    });
  }

  if (sysBtn) {
    sysBtn.addEventListener('click', async () => {
      try {
        if (!document.fullscreenElement) {
          await (pane.requestFullscreen ? pane.requestFullscreen() : document.documentElement.requestFullscreen());
          sysBtn.textContent = '退出电脑全屏';
        } else {
          await document.exitFullscreen();
          sysBtn.textContent = '电脑全屏';
        }
      } catch (e) {
        console.warn('全屏失败', e);
      }
    });
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement) {
        sysBtn.textContent = '电脑全屏';
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  loadExamples();
  document.getElementById('reloadExamples').addEventListener('click', loadExamples);
  document.getElementById('generateBtn').addEventListener('click', (ev) => {
    ev.preventDefault();
    onGenerate();
  });
  bindFullscreenButtons();
});
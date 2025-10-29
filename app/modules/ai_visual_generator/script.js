// AI Visualization Generator front-end logic

const examplesPath = 'examples.json';
// 将 API 指向后端服务端口（5050），避免静态服务器 8080 的 501 错误
const apiEndpoint = 'http://localhost:5050/api/generateVisualization';

async function loadExamples() {
  try {
    const res = await fetch(examplesPath);
    if (!res.ok) throw new Error('无法加载示例');
    const list = await res.json();
    const container = document.getElementById('examplesList');
    container.innerHTML = '';
    list.forEach(text => {
      const badge = document.createElement('span');
      badge.className = 'example-badge';
      badge.textContent = text;
      badge.addEventListener('click', () => {
        document.getElementById('promptInput').value = text;
      });
      container.appendChild(badge);
    });
  } catch (e) {
    console.error(e);
    const container = document.getElementById('examplesList');
    container.innerHTML = '<span style="color:#b00">加载示例失败</span>';
  }
}

function setStatus(text) {
  const el = document.getElementById('statusMessage');
  el.textContent = text;
}

function showResult(path) {
  const actions = document.getElementById('resultActions');
  actions.style.display = 'flex';
  const openLink = document.getElementById('openLink');
  const downloadLink = document.getElementById('downloadLink');
  openLink.href = path;
  downloadLink.href = path;
  const fname = path.split('/').pop();
  downloadLink.download = fname;
}

async function generate() {
  const prompt = document.getElementById('promptInput').value.trim();
  const vizType = document.getElementById('vizTypeSelect').value;
  const complexity = document.getElementById('complexitySelect').value;

  if (!prompt) {
    alert('请填写可视化需求描述');
    return;
  }

  setStatus('正在生成，请稍候…');
  document.getElementById('resultActions').style.display = 'none';

  try {
    const res = await fetch(apiEndpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, vizType, complexity })
    });

    if (!res.ok) {
      const txt = await res.text();
      throw new Error('生成失败: ' + txt);
    }
    const data = await res.json();
    if (data.status !== 'success' || !data.path) {
      throw new Error('生成失败或返回格式错误');
    }
    setStatus('生成成功！');
    showResult(data.path);
  } catch (e) {
    console.error(e);
    setStatus('生成失败：' + e.message);
    alert('生成失败：' + e.message);
  }
}

function bindEvents() {
  document.getElementById('generateBtn').addEventListener('click', generate);
  document.getElementById('regenerateBtn').addEventListener('click', () => {
    document.getElementById('promptInput').value = '';
    document.getElementById('resultActions').style.display = 'none';
    setStatus('尚未开始生成');
  });
}

window.addEventListener('DOMContentLoaded', () => {
  loadExamples();
  bindEvents();
});
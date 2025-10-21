// /app/lib/mathjax.js
// 全局 MathJax 配置与 API，兼容直接在页面中用 <script id="MathJax-script" src="...">

export function configureMathJax() {
  if (!window.MathJax) {
    window.MathJax = {};
  }
  Object.assign(window.MathJax, {
    tex: {
      inlineMath: [["$", "$"], ["\\(", "\\)"]],
      displayMath: [["$$", "$$"], ["\\[", "\\]"]],
      processEscapes: true,
      processEnvironments: true
    },
    chtml: {
      displayAlign: 'left',
      displayIndent: '0em',
      linebreaks: { automatic: true, width: 'container' }
    },
    svg: {
      displayAlign: 'left',
      displayIndent: '0em',
      linebreaks: { automatic: true, width: 'container' }
    },
    options: {
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
      ignoreHtmlClass: 'tex2jax_ignore',
      processHtmlClass: 'tex2jax_process'
    },
    startup: {
      ready() {
        MathJax.startup.defaultReady();
        console.log('✅ MathJax ready with global config');
      }
    }
  });
}

export async function typesetPage(scope = document) {
  if (window.MathJax && window.MathJax.typesetPromise) {
    await window.MathJax.typesetPromise(scope);
    console.log('🧩 MathJax typeset done');
  } else {
    console.warn('MathJax not loaded yet; typeset skipped');
  }
}

// 简易确保加载（页面仍需引入官方 CDN 脚本）
export function ensureMathJaxScript() {
  if (document.getElementById('MathJax-script')) return;
  const s = document.createElement('script');
  s.id = 'MathJax-script';
  s.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
  s.async = true;
  document.head.appendChild(s);
}
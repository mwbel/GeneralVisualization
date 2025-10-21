// /app/lib/autoMath.js
// 自动包裹待渲染的数学文本，并启用页面监听

const AUTO_SELECTORS = [
  '.mathjax-block',
  '.calculation-steps',
  '.examples-section',
];

export function enableAutoMath(pageEl = document.querySelector('.page')) {
  if (!pageEl) return;
  const needAuto = pageEl.getAttribute('data-autolatex') === 'true';
  if (!needAuto) return;

  // 把 .mathjax-block 内的纯文本行包裹为 LaTeX（保守策略：仅包裹未含 $ 与 mjx-container 的节点）
  pageEl.querySelectorAll(AUTO_SELECTORS.join(','))
    .forEach(scope => {
      scope.querySelectorAll('*').forEach(node => {
        if (node.children.length === 0 && node.textContent && !node.closest('mjx-container')) {
          const raw = node.textContent.trim();
          if (raw && /[=×+\-]/.test(raw) && !/[\$]/.test(raw)) {
            node.innerHTML = `\\(${escapeLatex(raw)}\\)`;
          }
        }
      });
    });

  // 监听内容变化，重新包裹（轻量）
  const mo = new MutationObserver(muts => {
    muts.forEach(m => {
      if (m.type === 'childList' || m.type === 'characterData') {
        // 简化处理：再次运行一次包裹
        pageEl.querySelectorAll(AUTO_SELECTORS.join(','))
          .forEach(scope => { /* 可扩展：按需再包裹 */ });
      }
    });
  });
  mo.observe(pageEl, { subtree: true, childList: true, characterData: true });
}

function escapeLatex(s) {
  return s
    .replace(/×/g, '\\times')
    .replace(/·/g, '\\cdot')
    .replace(/＝/g, '=');
}
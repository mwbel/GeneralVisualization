window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
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
    ready: function () {
      MathJax.startup.defaultReady();
      console.log('✅ MathJax ready — 全局配置加载完成');

      // 统一缩放：对所有 mjx-container（包含行内与块级）按父容器宽度自适应
      function fitAllMath(scope = document) {
        const equations = scope.querySelectorAll('mjx-container');
        console.log(`🔍 开始缩放 ${equations.length} 个公式容器`);
        
        equations.forEach((eq, index) => {
          try {
            // 重置缩放
            eq.style.transform = '';
            eq.style.transformOrigin = '';
            
            const parent = eq.parentElement;
            if (!parent) return;
            
            // 强制重新计算尺寸
            const parentRect = parent.getBoundingClientRect();
            const eqRect = eq.getBoundingClientRect();
            
            const parentWidth = parentRect.width;
            const eqWidth = eqRect.width;
            
            console.log(`📏 公式 ${index}: 父容器=${parentWidth.toFixed(1)}px, 公式=${eqWidth.toFixed(1)}px`);
            
            if (eqWidth > parentWidth && parentWidth > 50) { // 最小宽度检查
              const scale = Math.max(0.3, (parentWidth - 30) / eqWidth); // 最小缩放0.3，留30px边距
              console.log(`🔧 缩放公式 ${index}: ${scale.toFixed(3)}`);
              
              eq.style.transformOrigin = 'left center';
              eq.style.transform = `scale(${scale})`;
              
              // 调整父容器样式（缩小时避免换行）
              parent.style.overflowX = 'visible';
              parent.style.whiteSpace = 'nowrap';
            } else {
              // 宽度充足，恢复原始大小并重置父容器样式
              eq.style.transform = '';
              eq.style.transformOrigin = '';
              parent.style.whiteSpace = '';
              parent.style.overflowX = '';
            }
          } catch (error) {
            console.warn(`⚠️ 缩放公式 ${index} 时出错:`, error);
          }
        });
      }

      // 自动包裹文本为 LaTeX（仅在候选容器中执行，避免普通段落被误处理）
      const AUTO_SELECTORS = [
        '.formula', '.stat-formula', '.result-value',
        '.stat-label', '.stat-value',
        '.calculation-steps .step span',
        '#positive-terms', '#negative-terms', '#final-calculation',
        '#v1-display', '#v2-display', '#v3-display', '#det-display'
      ];

      function needsTypeset(el) {
        if (!el) return false;
        if (el.querySelector('mjx-container')) return false; // 已渲染
        const text = (el.textContent || '').trim();
        if (!text) return false;
        // 如果已包含显式的 LaTeX 定界符，则交给 MathJax 处理
        if (/\$\$|\\\(|\\\)|\\\[|\\\]/.test(text)) return true;
        // 启发式：若包含字母/数字/常见符号，则包裹为行内公式
        const maybeMath = /[A-Za-z0-9]/.test(text) && /[=+\-×·*^(){}\[\],]/.test(text);
        return maybeMath;
      }

      function toLatexContent(raw) {
        // 规范化符号，保证在 LaTeX 中显示正常
        return raw
          .replace(/[\uFF08\uFF09]/g, m => (m === '\uFF08' ? '(' : ')')) // 全角括号转半角
          .replace(/＝/g, '=')
          .replace(/×/g, '\\times')
          .replace(/·/g, '\\cdot');
      }

      function autoWrapAndTypeset(scope = document) {
        const candidates = AUTO_SELECTORS
          .flatMap(sel => Array.from(scope.querySelectorAll(sel)))
          .slice(0, 200); // 安全上限，避免过多节点

        let needRerender = false;
        candidates.forEach(el => {
          if (!needsTypeset(el)) return;
          const raw = (el.textContent || '').trim();
          if (!raw) return;
          const latex = toLatexContent(raw);
          // 使用行内公式包裹
          el.innerHTML = `\\(${latex}\\)`;
          needRerender = true;
        });

        if (needRerender && MathJax.typesetPromise) {
          MathJax.typesetPromise(candidates).then(() => {
            fitAllMath(scope);
            console.log('🔁 已自动包裹并渲染候选数学公式');
          });
        }
      }

      // 初次排版与缩放
      async function rerenderAndFit(scope = document) {
        if (window.MathJax && MathJax.typesetPromise) {
          await MathJax.typesetPromise(scope);
          setTimeout(() => fitAllMath(scope), 100);
          console.log('📐 自动缩放公式');
        }
      }

      // 页面加载完成后执行
      window.addEventListener('load', () => {
        autoWrapAndTypeset(document);
        rerenderAndFit(document);
      });

      // 每次窗口变化时重新缩放
      window.addEventListener('resize', () => {
        setTimeout(() => fitAllMath(document), 100);
      });

      // 方向变化与可见性变化时也重新缩放
      window.addEventListener('orientationchange', () => {
        setTimeout(() => fitAllMath(document), 100);
      });
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
          setTimeout(() => fitAllMath(document), 100);
        }
      });

      // 监听候选区域的内容变化，自动包裹与重排版
      const mo = new MutationObserver(mutations => {
        const scope = document;
        let changed = false;
        mutations.forEach(m => {
          if (m.type === 'childList' || m.type === 'characterData') {
            changed = true;
          }
        });
        if (changed) {
          autoWrapAndTypeset(scope);
        }
      });
      mo.observe(document.body, { subtree: true, childList: true, characterData: true });

      // Trae 的兜底触发
      document.addEventListener('readystatechange', () => {
        if (document.readyState === 'complete') {
          setTimeout(() => {
            autoWrapAndTypeset(document);
            rerenderAndFit(document);
          }, 300);
        }
      });
    }
  }
};

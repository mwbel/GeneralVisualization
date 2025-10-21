// /app/lib/responsive-math.js
// 统一的公式自适应缩放（可自动缩小与自动放大）

export function attachFormulaResizer(pageEl = document.querySelector('.page')) {
  const scope = pageEl || document;
  const fitAllMath = (root = scope) => {
    const equations = root.querySelectorAll('mjx-container');
    equations.forEach(eq => {
      try {
        const parent = eq.parentElement;
        if (!parent) return;
        // 重置缩放以获得真实尺寸
        eq.style.transform = '';
        eq.style.transformOrigin = '';
        const pw = parent.getBoundingClientRect().width;
        const ew = eq.getBoundingClientRect().width;
        if (ew > pw && pw > 50) {
          const scale = Math.max(0.3, (pw - 24) / ew);
          eq.style.transformOrigin = 'left center';
          eq.style.transform = `scale(${scale})`;
          parent.style.whiteSpace = 'nowrap';
          parent.style.overflowX = 'visible';
        } else {
          // 宽度充足，恢复原始大小
          eq.style.transform = '';
          eq.style.transformOrigin = '';
          parent.style.whiteSpace = '';
          parent.style.overflowX = '';
        }
      } catch (e) {}
    });
  };

  // 初次与延时触发一次
  setTimeout(() => fitAllMath(scope), 120);
  // 事件监听
  const reFit = () => setTimeout(() => fitAllMath(scope), 80);
  window.addEventListener('resize', reFit);
  window.addEventListener('orientationchange', reFit);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') reFit();
  });

  return { fitAllMath };
}
// 线性代数模块主入口
// 移除对 TypeScript 的直接导入以兼容原生浏览器环境

// MathJax 配置
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    skipHtmlTags: ["script", "noscript", "style", "textarea", "pre"],
  },
};

// 页面加载完成后的初始化
document.addEventListener("DOMContentLoaded", function () {
  console.log("线性代数模块已加载");
  if (typeof MathJax !== "undefined") {
    MathJax.typesetPromise().catch((err) => console.log(err.message));
  }
});
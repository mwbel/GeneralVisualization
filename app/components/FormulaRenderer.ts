// FormulaRenderer - 公式渲染组件
// 统一处理 MathJax 公式渲染

export interface FormulaConfig {
  inline?: boolean;
  displayMode?: boolean;
  delimiters?: {
    inline: [string, string];
    display: [string, string];
  };
}

export class FormulaRenderer {
  private static defaultConfig: FormulaConfig = {
    inline: true,
    displayMode: true,
    delimiters: {
      inline: ['\\(', '\\)'],
      display: ['\\[', '\\]']
    }
  };

  static render(element: HTMLElement, config?: FormulaConfig) {
    const finalConfig = { ...this.defaultConfig, ...config };
    
    // 检查 MathJax 是否已加载
    if (typeof (window as any).MathJax !== 'undefined') {
      (window as any).MathJax.typesetPromise([element]).catch((err: any) => {
        console.error('MathJax rendering error:', err);
      });
    } else {
      console.warn('MathJax not loaded, formula rendering skipped');
    }
  }

  static renderFormula(formula: string, inline: boolean = false): string {
    if (inline) {
      return `\\(${formula}\\)`;
    } else {
      return `\\[${formula}\\]`;
    }
  }

  static wrapInlineFormula(text: string): string {
    return `\\(${text}\\)`;
  }

  static wrapDisplayFormula(text: string): string {
    return `\\[${text}\\]`;
  }

  static processElement(element: HTMLElement) {
    // 处理元素中的公式标记
    const content = element.innerHTML;
    
    // 替换 $...$ 为 \(...\)
    const processedContent = content
      .replace(/\$([^$]+)\$/g, '\\($1\\)')
      .replace(/\$\$([^$]+)\$\$/g, '\\[$1\\]');
    
    element.innerHTML = processedContent;
    this.render(element);
  }
}
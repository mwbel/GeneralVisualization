// ExplainBox - 数学概念解释框组件
// 支持 MathJax 公式渲染和分步解释

export interface ExplainContent {
  title: string;
  formula?: string;
  explanation: string;
  steps?: string[];
}

export class ExplainBox {
  private container: HTMLElement;
  private content: ExplainContent;

  constructor(container: HTMLElement, content: ExplainContent) {
    this.container = container;
    this.content = content;
    this.render();
  }

  private render() {
    this.container.className = 'explain-box';
    
    const title = document.createElement('h3');
    title.textContent = this.content.title;
    this.container.appendChild(title);

    if (this.content.formula) {
      const formula = document.createElement('div');
      formula.className = 'formula';
      formula.innerHTML = `\\[${this.content.formula}\\]`;
      this.container.appendChild(formula);
    }

    const explanation = document.createElement('p');
    explanation.textContent = this.content.explanation;
    this.container.appendChild(explanation);

    if (this.content.steps && this.content.steps.length > 0) {
      const stepsList = document.createElement('ol');
      stepsList.className = 'steps-list';
      
      this.content.steps.forEach(step => {
        const stepItem = document.createElement('li');
        stepItem.textContent = step;
        stepsList.appendChild(stepItem);
      });
      
      this.container.appendChild(stepsList);
    }
  }

  updateContent(content: ExplainContent) {
    this.content = content;
    this.render();
  }

  show() {
    this.container.style.display = 'block';
  }

  hide() {
    this.container.style.display = 'none';
  }
}
// PlotCanvas - 通用绘图画布组件
// 支持 Plotly.js 和 D3.js 渲染

export interface PlotCanvasProps {
  id: string;
  width?: number;
  height?: number;
  data?: any[];
  layout?: any;
  config?: any;
}

export class PlotCanvas {
  private container: HTMLElement;
  private props: PlotCanvasProps;

  constructor(container: HTMLElement, props: PlotCanvasProps) {
    this.container = container;
    this.props = props;
    this.init();
  }

  private init() {
    this.container.id = this.props.id;
    this.container.style.width = `${this.props.width || 600}px`;
    this.container.style.height = `${this.props.height || 400}px`;
  }

  render(data: any[], layout?: any, config?: any) {
    // 实际渲染逻辑将在具体模块中实现
    console.log('PlotCanvas render:', { data, layout, config });
  }

  resize(width: number, height: number) {
    this.container.style.width = `${width}px`;
    this.container.style.height = `${height}px`;
  }
}
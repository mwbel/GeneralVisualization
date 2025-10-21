// ModuleLayout - 模块布局组件
// 提供统一的页面布局结构

export interface LayoutConfig {
  title: string;
  showSidebar?: boolean;
  showHeader?: boolean;
  theme?: 'light' | 'dark';
}

export class ModuleLayout {
  private container: HTMLElement;
  private config: LayoutConfig;

  constructor(container: HTMLElement, config: LayoutConfig) {
    this.container = container;
    this.config = config;
    this.init();
  }

  private init() {
    this.container.className = `module-layout theme-${this.config.theme || 'light'}`;
    
    if (this.config.showHeader !== false) {
      this.createHeader();
    }

    const mainContent = document.createElement('div');
    mainContent.className = 'main-content';

    if (this.config.showSidebar) {
      const sidebar = document.createElement('aside');
      sidebar.className = 'sidebar';
      sidebar.id = 'module-sidebar';
      mainContent.appendChild(sidebar);
    }

    const contentArea = document.createElement('main');
    contentArea.className = 'content-area';
    contentArea.id = 'module-content';
    mainContent.appendChild(contentArea);

    this.container.appendChild(mainContent);
  }

  private createHeader() {
    const header = document.createElement('header');
    header.className = 'module-header';

    const title = document.createElement('h1');
    title.textContent = this.config.title;
    header.appendChild(title);

    this.container.appendChild(header);
  }

  getSidebar(): HTMLElement | null {
    return this.container.querySelector('#module-sidebar');
  }

  getContentArea(): HTMLElement | null {
    return this.container.querySelector('#module-content');
  }

  setTitle(title: string) {
    const titleElement = this.container.querySelector('h1');
    if (titleElement) {
      titleElement.textContent = title;
    }
  }
}
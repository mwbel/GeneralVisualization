// ControlPanel - 通用控制面板组件
// 提供参数输入、滑块、按钮等交互控件

export interface ControlConfig {
  type: 'slider' | 'input' | 'button' | 'select';
  id: string;
  label: string;
  min?: number;
  max?: number;
  step?: number;
  value?: any;
  options?: string[];
  onChange?: (value: any) => void;
}

export class ControlPanel {
  private container: HTMLElement;
  private controls: ControlConfig[];

  constructor(container: HTMLElement, controls: ControlConfig[]) {
    this.container = container;
    this.controls = controls;
    this.render();
  }

  private render() {
    this.container.innerHTML = '';
    this.controls.forEach(control => {
      const wrapper = document.createElement('div');
      wrapper.className = 'control-item';
      
      const label = document.createElement('label');
      label.textContent = control.label;
      wrapper.appendChild(label);

      // 根据控件类型创建相应元素
      let element: HTMLElement;
      switch (control.type) {
        case 'slider':
          element = this.createSlider(control);
          break;
        case 'input':
          element = this.createInput(control);
          break;
        case 'button':
          element = this.createButton(control);
          break;
        case 'select':
          element = this.createSelect(control);
          break;
        default:
          element = document.createElement('div');
      }
      
      wrapper.appendChild(element);
      this.container.appendChild(wrapper);
    });
  }

  private createSlider(control: ControlConfig): HTMLInputElement {
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.id = control.id;
    slider.min = String(control.min || 0);
    slider.max = String(control.max || 100);
    slider.step = String(control.step || 1);
    slider.value = String(control.value || 0);
    
    if (control.onChange) {
      slider.addEventListener('input', (e) => {
        control.onChange!(parseFloat((e.target as HTMLInputElement).value));
      });
    }
    
    return slider;
  }

  private createInput(control: ControlConfig): HTMLInputElement {
    const input = document.createElement('input');
    input.type = 'number';
    input.id = control.id;
    input.value = String(control.value || 0);
    
    if (control.onChange) {
      input.addEventListener('change', (e) => {
        control.onChange!(parseFloat((e.target as HTMLInputElement).value));
      });
    }
    
    return input;
  }

  private createButton(control: ControlConfig): HTMLButtonElement {
    const button = document.createElement('button');
    button.id = control.id;
    button.textContent = control.label;
    
    if (control.onChange) {
      button.addEventListener('click', () => {
        control.onChange!(true);
      });
    }
    
    return button;
  }

  private createSelect(control: ControlConfig): HTMLSelectElement {
    const select = document.createElement('select');
    select.id = control.id;
    
    control.options?.forEach(option => {
      const optionElement = document.createElement('option');
      optionElement.value = option;
      optionElement.textContent = option;
      select.appendChild(optionElement);
    });
    
    if (control.onChange) {
      select.addEventListener('change', (e) => {
        control.onChange!((e.target as HTMLSelectElement).value);
      });
    }
    
    return select;
  }
}
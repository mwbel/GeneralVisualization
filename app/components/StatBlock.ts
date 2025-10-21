// StatBlock - 统计数据展示块组件
// 用于显示计算结果、统计指标等数值信息

export interface StatData {
  label: string;
  value: number | string;
  unit?: string;
  precision?: number;
  format?: 'number' | 'percentage' | 'scientific';
}

export class StatBlock {
  private container: HTMLElement;
  private stats: StatData[];

  constructor(container: HTMLElement, stats: StatData[]) {
    this.container = container;
    this.stats = stats;
    this.render();
  }

  private render() {
    this.container.className = 'stat-block';
    this.container.innerHTML = '';

    this.stats.forEach(stat => {
      const statItem = document.createElement('div');
      statItem.className = 'stat-item';

      const label = document.createElement('div');
      label.className = 'stat-label';
      label.textContent = stat.label;

      const value = document.createElement('div');
      value.className = 'stat-value';
      value.textContent = this.formatValue(stat);

      statItem.appendChild(label);
      statItem.appendChild(value);
      this.container.appendChild(statItem);
    });
  }

  private formatValue(stat: StatData): string {
    if (typeof stat.value === 'string') {
      return stat.value;
    }

    let formatted: string;
    const precision = stat.precision || 2;

    switch (stat.format) {
      case 'percentage':
        formatted = (stat.value * 100).toFixed(precision) + '%';
        break;
      case 'scientific':
        formatted = stat.value.toExponential(precision);
        break;
      default:
        formatted = stat.value.toFixed(precision);
    }

    return stat.unit ? `${formatted} ${stat.unit}` : formatted;
  }

  updateStats(stats: StatData[]) {
    this.stats = stats;
    this.render();
  }

  updateStat(label: string, value: number | string) {
    const stat = this.stats.find(s => s.label === label);
    if (stat) {
      stat.value = value;
      this.render();
    }
  }
}
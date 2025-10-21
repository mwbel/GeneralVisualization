
#!/usr/bin/env python3
"""
二项分布B(n,p)可视化 - 固定p=0.3，n变化
"""

import plotly.graph_objects as go
import numpy as np
from scipy.stats import binom
import plotly.express as px

def create_binomial_fixed_p():
    """创建固定p=0.3，n变化的二项分布可视化"""
    
    # 参数设置
    p_fixed = 0.3
    n_values = [5, 10, 20, 30, 50]
    colors = px.colors.qualitative.Set2
    
    fig = go.Figure()
    
    # 为每个n值绘制概率质量函数
    for i, n in enumerate(n_values):
        # 限制显示范围，避免图表过于拥挤
        k_max = min(n, int(n + 3 * np.sqrt(n * p_fixed * (1 - p_fixed))))
        k = np.arange(0, k_max + 1)
        pmf = binom.pmf(k, n, p_fixed)
        
        fig.add_trace(
            go.Scatter(
                x=k,
                y=pmf,
                mode='lines+markers',
                name=f'n = {n}',
                line=dict(
                    color=colors[i % len(colors)],
                    width=2
                ),
                marker=dict(
                    size=6,
                    color=colors[i % len(colors)]
                ),
                hovertemplate='<b>n = %{fullData.name}</b><br>' +
                            '成功次数 k: %{x}<br>' +
                            '概率 P(X=k): %{y:.4f}<extra></extra>'
            )
        )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '二项分布 B(n,0.3) - 固定p=0.3，n变化',
            'x': 0.5,
            'font': {'size': 18}
        },
        xaxis_title='成功次数 k',
        yaxis_title='概率 P(X = k)',
        width=900,
        height=600,
        legend=dict(
            x=0.7,
            y=0.95,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='rgba(0,0,0,0.2)',
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    # 添加网格
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def add_normal_approximation(fig):
    """添加正态分布近似曲线（当n较大时）"""
    
    p = 0.3
    n_values = [20, 30, 50]  # 只为较大的n值添加正态近似
    
    for i, n in enumerate(n_values):
        if n >= 20:  # 只有当n足够大时才显示正态近似
            mean = n * p
            std = np.sqrt(n * p * (1 - p))
            
            # 生成正态分布曲线
            x_norm = np.linspace(max(0, mean - 4*std), min(n, mean + 4*std), 100)
            y_norm = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_norm - mean) / std) ** 2)
            
            fig.add_trace(
                go.Scatter(
                    x=x_norm,
                    y=y_norm,
                    mode='lines',
                    name=f'正态近似 n={n}',
                    line=dict(
                        color=px.colors.qualitative.Set2[n_values.index(n) + 2],
                        width=2,
                        dash='dash'
                    ),
                    opacity=0.7,
                    hovertemplate='正态近似<br>' +
                                'μ = %.1f<br>' % mean +
                                'σ = %.2f<br>' % std +
                                'x: %{x:.1f}<br>' +
                                'y: %{y:.4f}<extra></extra>'
                )
            )
    
    return fig

def add_statistics_annotation_fixed_p(fig):
    """添加统计信息注释"""
    
    annotations = []
    p = 0.3
    n_values = [5, 10, 20, 30, 50]
    
    for i, n in enumerate(n_values):
        mean = n * p
        variance = n * p * (1 - p)
        std = np.sqrt(variance)
        
        annotations.append(
            dict(
                x=0.02,
                y=0.95 - i * 0.08,
                xref='paper',
                yref='paper',
                text=f'n={n}: μ={mean:.1f}, σ²={variance:.1f}, σ={std:.2f}',
                showarrow=False,
                font=dict(size=10, color=px.colors.qualitative.Set2[i % len(px.colors.qualitative.Set2)]),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor=px.colors.qualitative.Set2[i % len(px.colors.qualitative.Set2)],
                borderwidth=1
            )
        )
    
    fig.update_layout(annotations=annotations)
    return fig

if __name__ == "__main__":
    # 创建可视化
    fig = create_binomial_fixed_p()
    
    # 添加正态分布近似
    fig = add_normal_approximation(fig)
    
    # 添加统计信息
    fig = add_statistics_annotation_fixed_p(fig)
    
    # 保存为HTML文件
    fig.write_html("binomial_fixed_p_visualization.html")
    print("✅ 可视化已保存为: binomial_fixed_p_visualization.html")
    
    # 显示图表
    fig.show()
    
    print("\n📊 二项分布B(n,0.3)分析:")
    print("当p固定为0.3时，n的变化对分布的影响：")
    print("• n=5: 分布离散，概率相对较高")
    print("• n=10: 分布开始显现钟形特征")
    print("• n=20: 分布更加平滑，接近正态分布")
    print("• n=30: 分布明显趋向正态分布")
    print("• n=50: 分布非常接近正态分布（中心极限定理）")
    print("\n💡 观察要点:")
    print("• 随着n增大，分布的峰值降低但更加平滑")
    print("• 期望值μ=np线性增长")
    print("• 标准差σ=√(np(1-p))随√n增长")
    print("• 当n≥20且np≥5且n(1-p)≥5时，可用正态分布近似")

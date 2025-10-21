
#!/usr/bin/env python3
"""
二项分布B(n,p)可视化 - 固定n=20，p变化
"""

import plotly.graph_objects as go
import numpy as np
from scipy.stats import binom
import plotly.express as px

def create_binomial_fixed_n():
    """创建固定n=20，p变化的二项分布可视化"""
    
    # 参数设置
    n_fixed = 20
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    colors = px.colors.qualitative.Set1
    
    fig = go.Figure()
    
    # 为每个p值绘制概率质量函数
    for i, p in enumerate(p_values):
        k = np.arange(0, n_fixed + 1)  # 成功次数 0 到 n
        pmf = binom.pmf(k, n_fixed, p)  # 概率质量函数
        
        fig.add_trace(
            go.Scatter(
                x=k,
                y=pmf,
                mode='lines+markers',
                name=f'p = {p}',
                line=dict(
                    color=colors[i % len(colors)],
                    width=2
                ),
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)]
                ),
                hovertemplate='<b>p = %{fullData.name}</b><br>' +
                            '成功次数 k: %{x}<br>' +
                            '概率 P(X=k): %{y:.4f}<extra></extra>'
            )
        )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '二项分布 B(20,p) - 固定n=20，p变化',
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

def add_statistics_annotation(fig):
    """添加统计信息注释"""
    
    annotations = []
    n = 20
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for i, p in enumerate(p_values):
        mean = n * p
        variance = n * p * (1 - p)
        std = np.sqrt(variance)
        
        annotations.append(
            dict(
                x=0.02,
                y=0.95 - i * 0.08,
                xref='paper',
                yref='paper',
                text=f'p={p}: μ={mean:.1f}, σ²={variance:.1f}, σ={std:.2f}',
                showarrow=False,
                font=dict(size=10, color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)],
                borderwidth=1
            )
        )
    
    fig.update_layout(annotations=annotations)
    return fig

if __name__ == "__main__":
    # 创建可视化
    fig = create_binomial_fixed_n()
    
    # 添加统计信息
    fig = add_statistics_annotation(fig)
    
    # 保存为HTML文件
    fig.write_html("binomial_fixed_n_visualization.html")
    print("✅ 可视化已保存为: binomial_fixed_n_visualization.html")
    
    # 显示图表
    fig.show()
    
    print("\n📊 二项分布B(20,p)分析:")
    print("当n固定为20时，p的变化对分布的影响：")
    print("• p=0.1: 分布右偏，大部分概率集中在小的k值")
    print("• p=0.3: 分布仍然右偏，但峰值向右移动")
    print("• p=0.5: 分布对称，峰值在k=10附近")
    print("• p=0.7: 分布左偏，峰值在k=14附近")
    print("• p=0.9: 分布明显左偏，大部分概率集中在大的k值")

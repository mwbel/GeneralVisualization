#!/usr/bin/env python3
"""
二项分布B(n,p)可视化示例
展示参数n和p变化对分布的影响
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import binom
import plotly.express as px

def create_binomial_visualization():
    """创建二项分布的3D可视化"""
    
    # 创建子图布局
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            '固定n=20, p变化 (2D)',
            '固定p=0.3, n变化 (2D)', 
            '二项分布3D表面图 (n,p变化)',
            '概率质量函数热力图'
        ],
        specs=[
            [{"type": "scatter"}, {"type": "scatter"}],
            [{"type": "surface"}, {"type": "heatmap"}]
        ]
    )
    
    # 1. 固定n=20, p变化
    n_fixed = 20
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    colors = px.colors.qualitative.Set1
    
    for i, p in enumerate(p_values):
        x = np.arange(0, n_fixed + 1)
        y = binom.pmf(x, n_fixed, p)
        
        fig.add_trace(
            go.Scatter(
                x=x, y=y,
                mode='lines+markers',
                name=f'p={p}',
                line=dict(color=colors[i % len(colors)]),
                marker=dict(size=6)
            ),
            row=1, col=1
        )
    
    # 2. 固定p=0.3, n变化
    p_fixed = 0.3
    n_values = [5, 10, 20, 30, 50]
    
    for i, n in enumerate(n_values):
        x = np.arange(0, min(n + 1, 31))  # 限制显示范围
        y = binom.pmf(x, n, p_fixed)
        
        fig.add_trace(
            go.Scatter(
                x=x, y=y,
                mode='lines+markers',
                name=f'n={n}',
                line=dict(color=colors[i % len(colors)]),
                marker=dict(size=6),
                showlegend=False
            ),
            row=1, col=2
        )
    
    # 3. 3D表面图 - 展示n和p同时变化
    n_range = np.arange(5, 31, 2)
    p_range = np.arange(0.1, 1.0, 0.05)
    N, P = np.meshgrid(n_range, p_range)
    
    # 计算期望值作为Z轴 (E[X] = n*p)
    Z_mean = N * P
    
    fig.add_trace(
        go.Surface(
            x=N, y=P, z=Z_mean,
            colorscale='Viridis',
            name='期望值 E[X]=np',
            showscale=True
        ),
        row=2, col=1
    )
    
    # 4. 热力图 - 显示不同n,p组合下的方差
    # 方差 Var[X] = n*p*(1-p)
    Z_var = N * P * (1 - P)
    
    fig.add_trace(
        go.Heatmap(
            x=n_range, y=p_range, z=Z_var,
            colorscale='RdYlBu',
            name='方差 Var[X]=np(1-p)'
        ),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '二项分布 B(n,p) 参数影响可视化',
            'x': 0.5,
            'font': {'size': 20}
        },
        height=800,
        showlegend=True
    )
    
    # 更新各子图的轴标签
    fig.update_xaxes(title_text="k (成功次数)", row=1, col=1)
    fig.update_yaxes(title_text="P(X=k)", row=1, col=1)
    
    fig.update_xaxes(title_text="k (成功次数)", row=1, col=2)
    fig.update_yaxes(title_text="P(X=k)", row=1, col=2)
    
    fig.update_layout(scene=dict(
        xaxis_title='n (试验次数)',
        yaxis_title='p (成功概率)',
        zaxis_title='期望值 E[X]'
    ))
    
    return fig

def create_interactive_3d_binomial():
    """创建交互式3D二项分布可视化"""
    
    # 参数设置
    n_values = [10, 20, 30]
    p_values = [0.2, 0.5, 0.8]
    
    fig = go.Figure()
    
    # 为每个n,p组合创建3D散点图
    for n in n_values:
        for p in p_values:
            x = np.arange(0, n + 1)
            y = np.full_like(x, p)  # p值作为y轴
            z = np.full_like(x, n)  # n值作为z轴
            pmf = binom.pmf(x, n, p)
            
            # 使用概率质量函数值作为颜色和大小
            fig.add_trace(
                go.Scatter3d(
                    x=x,  # 成功次数
                    y=y,  # 概率p
                    z=z,  # 试验次数n
                    mode='markers',
                    marker=dict(
                        size=pmf * 100,  # 根据概率调整大小
                        color=pmf,
                        colorscale='Viridis',
                        opacity=0.8,
                        colorbar=dict(title="概率质量函数值")
                    ),
                    name=f'B({n},{p})',
                    text=[f'P(X={k})={pmf[i]:.4f}' for i, k in enumerate(x)],
                    hovertemplate='<b>%{text}</b><br>' +
                                '成功次数: %{x}<br>' +
                                '概率p: %{y}<br>' +
                                '试验次数n: %{z}<extra></extra>'
                )
            )
    
    fig.update_layout(
        title='交互式3D二项分布可视化',
        scene=dict(
            xaxis_title='成功次数 k',
            yaxis_title='成功概率 p',
            zaxis_title='试验次数 n',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=700
    )
    
    return fig

def main():
    """主函数 - 生成并保存可视化"""
    
    print("🎲 生成二项分布可视化...")
    
    # 创建综合可视化
    fig1 = create_binomial_visualization()
    fig1.write_html("binomial_distribution_comprehensive.html")
    print("✅ 综合可视化已保存: binomial_distribution_comprehensive.html")
    
    # 创建3D交互式可视化
    fig2 = create_interactive_3d_binomial()
    fig2.write_html("binomial_distribution_3d_interactive.html")
    print("✅ 3D交互式可视化已保存: binomial_distribution_3d_interactive.html")
    
    # 显示图表
    print("\n📊 显示可视化...")
    fig1.show()
    fig2.show()
    
    print("\n📈 二项分布特性说明:")
    print("1. 期望值: E[X] = n × p")
    print("2. 方差: Var[X] = n × p × (1-p)")
    print("3. 当p=0.5时，分布最对称")
    print("4. n增大时，分布趋向正态分布（中心极限定理）")
    print("5. p接近0或1时，分布偏斜明显")

if __name__ == "__main__":
    main()
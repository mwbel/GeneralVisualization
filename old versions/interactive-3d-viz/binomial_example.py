#!/usr/bin/env python3
"""
二项分布B(n,p)可视化示例
演示固定n变化p，以及固定p变化n的效果
"""

import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import binom
import math

def binomial_pmf(k, n, p):
    """计算二项分布的概率质量函数"""
    return binom.pmf(k, n, p)

def binomial_stats(n, p):
    """计算二项分布的统计量"""
    mean = n * p
    variance = n * p * (1 - p)
    std = math.sqrt(variance)
    return mean, variance, std

def create_fixed_n_varying_p():
    """固定n=20，变化p的可视化"""
    n = 20
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    
    fig = go.Figure()
    
    for i, p in enumerate(p_values):
        k_values = np.arange(0, n + 1)
        probabilities = [binomial_pmf(k, n, p) for k in k_values]
        
        mean, variance, std = binomial_stats(n, p)
        
        # 添加概率质量函数
        fig.add_trace(go.Scatter(
            x=k_values,
            y=probabilities,
            mode='lines+markers',
            name=f'p={p} (μ={mean:.1f}, σ²={variance:.1f}, σ={std:.2f})',
            line=dict(color=colors[i], width=2),
            marker=dict(size=6, color=colors[i])
        ))
        
        # 添加期望值垂直线
        fig.add_vline(
            x=mean,
            line=dict(color=colors[i], width=1, dash='dash'),
            opacity=0.5
        )
    
    fig.update_layout(
        title='二项分布B(20,p) - 固定n=20，变化p',
        xaxis_title='成功次数 k',
        yaxis_title='概率 P(X=k)',
        width=900,
        height=600,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        template='plotly_white'
    )
    
    return fig

def create_fixed_p_varying_n():
    """固定p=0.3，变化n的可视化"""
    p = 0.3
    n_values = [5, 10, 20, 30, 50]
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    
    fig = go.Figure()
    
    for i, n in enumerate(n_values):
        k_values = np.arange(0, n + 1)
        probabilities = [binomial_pmf(k, n, p) for k in k_values]
        
        mean, variance, std = binomial_stats(n, p)
        
        # 添加概率质量函数
        fig.add_trace(go.Scatter(
            x=k_values,
            y=probabilities,
            mode='lines+markers',
            name=f'n={n} (μ={mean:.1f}, σ²={variance:.1f}, σ={std:.2f})',
            line=dict(color=colors[i], width=2),
            marker=dict(size=4, color=colors[i])
        ))
        
        # 添加期望值垂直线
        fig.add_vline(
            x=mean,
            line=dict(color=colors[i], width=1, dash='dash'),
            opacity=0.5
        )
    
    fig.update_layout(
        title='二项分布B(n,0.3) - 固定p=0.3，变化n',
        xaxis_title='成功次数 k',
        yaxis_title='概率 P(X=k)',
        width=900,
        height=600,
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        template='plotly_white'
    )
    
    return fig

def create_3d_parameter_surface():
    """创建3D参数表面图"""
    n_range = np.arange(5, 51, 2)
    p_range = np.arange(0.05, 1.0, 0.05)
    
    N, P = np.meshgrid(n_range, p_range)
    
    # 计算期望值和方差
    Mean = N * P
    Variance = N * P * (1 - P)
    
    # 创建子图
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'surface'}]],
        subplot_titles=['期望值 E[X] = n×p', '方差 Var[X] = n×p×(1-p)']
    )
    
    # 期望值表面
    fig.add_trace(
        go.Surface(
            x=n_range,
            y=p_range,
            z=Mean,
            colorscale='viridis',
            name='期望值'
        ),
        row=1, col=1
    )
    
    # 方差表面
    fig.add_trace(
        go.Surface(
            x=n_range,
            y=p_range,
            z=Variance,
            colorscale='plasma',
            name='方差'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title='二项分布B(n,p)的统计特性3D表面图',
        width=1200,
        height=600,
        scene=dict(
            xaxis_title='试验次数 n',
            yaxis_title='成功概率 p',
            zaxis_title='期望值'
        ),
        scene2=dict(
            xaxis_title='试验次数 n',
            yaxis_title='成功概率 p',
            zaxis_title='方差'
        )
    )
    
    return fig

def create_comprehensive_analysis():
    """创建综合分析图"""
    # 创建2x2子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            '固定n=20，变化p',
            '固定p=0.3，变化n',
            '期望值vs方差关系',
            '变异系数分析'
        ],
        specs=[
            [{'type': 'xy'}, {'type': 'xy'}],
            [{'type': 'xy'}, {'type': 'xy'}]
        ]
    )
    
    # 子图1：固定n=20，变化p
    n = 20
    p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    colors = ['red', 'orange', 'green', 'blue', 'purple']
    
    for i, p in enumerate(p_values):
        k_values = np.arange(0, n + 1)
        probabilities = [binomial_pmf(k, n, p) for k in k_values]
        
        fig.add_trace(
            go.Scatter(
                x=k_values,
                y=probabilities,
                mode='lines+markers',
                name=f'p={p}',
                line=dict(color=colors[i]),
                marker=dict(size=4, color=colors[i]),
                showlegend=False
            ),
            row=1, col=1
        )
    
    # 子图2：固定p=0.3，变化n
    p = 0.3
    n_values = [5, 10, 20, 30]
    
    for i, n in enumerate(n_values):
        k_values = np.arange(0, n + 1)
        probabilities = [binomial_pmf(k, n, p) for k in k_values]
        
        fig.add_trace(
            go.Scatter(
                x=k_values,
                y=probabilities,
                mode='lines+markers',
                name=f'n={n}',
                line=dict(color=colors[i]),
                marker=dict(size=3, color=colors[i]),
                showlegend=False
            ),
            row=1, col=2
        )
    
    # 子图3：期望值vs方差关系
    p_range = np.linspace(0.01, 0.99, 100)
    n_values_for_variance = [10, 20, 30, 50]
    
    for i, n in enumerate(n_values_for_variance):
        means = n * p_range
        variances = n * p_range * (1 - p_range)
        
        fig.add_trace(
            go.Scatter(
                x=means,
                y=variances,
                mode='lines',
                name=f'n={n}',
                line=dict(color=colors[i]),
                showlegend=False
            ),
            row=2, col=1
        )
    
    # 子图4：变异系数分析
    for i, n in enumerate(n_values_for_variance):
        cv = np.sqrt((1 - p_range) / (n * p_range))
        
        fig.add_trace(
            go.Scatter(
                x=p_range,
                y=cv,
                mode='lines',
                name=f'n={n}',
                line=dict(color=colors[i]),
                showlegend=False
            ),
            row=2, col=2
        )
    
    fig.update_layout(
        title='二项分布B(n,p)综合分析',
        width=1000,
        height=800,
        template='plotly_white'
    )
    
    # 更新坐标轴标签
    fig.update_xaxes(title_text="成功次数 k", row=1, col=1)
    fig.update_yaxes(title_text="概率", row=1, col=1)
    fig.update_xaxes(title_text="成功次数 k", row=1, col=2)
    fig.update_yaxes(title_text="概率", row=1, col=2)
    fig.update_xaxes(title_text="期望值", row=2, col=1)
    fig.update_yaxes(title_text="方差", row=2, col=1)
    fig.update_xaxes(title_text="成功概率 p", row=2, col=2)
    fig.update_yaxes(title_text="变异系数", row=2, col=2)
    
    return fig

def main():
    """主函数"""
    print("🎯 二项分布B(n,p)可视化示例")
    print("=" * 50)
    
    # 生成各种可视化
    print("📊 生成可视化图表...")
    
    # 1. 固定n变化p
    fig1 = create_fixed_n_varying_p()
    fig1.write_html("binomial_fixed_n_varying_p.html")
    print("✅ 已生成：binomial_fixed_n_varying_p.html")
    
    # 2. 固定p变化n
    fig2 = create_fixed_p_varying_n()
    fig2.write_html("binomial_fixed_p_varying_n.html")
    print("✅ 已生成：binomial_fixed_p_varying_n.html")
    
    # 3. 3D参数表面
    fig3 = create_3d_parameter_surface()
    fig3.write_html("binomial_3d_parameter_surface.html")
    print("✅ 已生成：binomial_3d_parameter_surface.html")
    
    # 4. 综合分析
    fig4 = create_comprehensive_analysis()
    fig4.write_html("binomial_comprehensive_analysis.html")
    print("✅ 已生成：binomial_comprehensive_analysis.html")
    
    print("\n📈 二项分布特性总结：")
    print("1. 期望值：E[X] = n × p")
    print("2. 方差：Var[X] = n × p × (1-p)")
    print("3. 标准差：σ = √(n × p × (1-p))")
    print("4. 当p=0.5时分布对称，p≠0.5时分布偏斜")
    print("5. 当n增大时，分布趋向正态分布（中心极限定理）")
    print("6. 方差在p=0.5时达到最大值")
    
    print("\n🌐 在浏览器中查看生成的HTML文件以探索交互式可视化！")

if __name__ == "__main__":
    main()
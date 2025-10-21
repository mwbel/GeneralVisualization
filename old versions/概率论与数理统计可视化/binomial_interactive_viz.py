#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二项分布交互式可视化
Binomial Distribution Interactive Visualization

功能特点：
1. 两种模式：固定n变化p，固定p变化n
2. 实时PMF和CDF显示
3. 统计特性动态更新
4. 教育性注释和说明
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from scipy.stats import binom
import math

def calculate_binomial_stats(n, p):
    """计算二项分布的统计特性"""
    mean = n * p
    variance = n * p * (1 - p)
    std = math.sqrt(variance)
    skewness = (1 - 2*p) / math.sqrt(n * p * (1 - p)) if p != 0 and p != 1 else 0
    
    return {
        'mean': mean,
        'variance': variance,
        'std': std,
        'skewness': skewness
    }

def create_binomial_visualization():
    """创建二项分布交互式可视化"""
    
    # 初始参数
    initial_n = 20
    initial_p = 0.5
    
    # 计算初始数据
    x_values = np.arange(0, initial_n + 1)
    pmf_values = binom.pmf(x_values, initial_n, initial_p)
    cdf_values = binom.cdf(x_values, initial_n, initial_p)
    
    # 计算统计特性
    stats = calculate_binomial_stats(initial_n, initial_p)
    
    # 创建子图布局
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'概率质量函数 PMF - B({initial_n}, {initial_p:.2f})',
            f'累积分布函数 CDF - B({initial_n}, {initial_p:.2f})',
            '期望值与方差',
            '分布形状特征'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # PMF 柱状图
    fig.add_trace(
        go.Bar(
            x=x_values,
            y=pmf_values,
            name='PMF',
            marker_color='rgba(55, 128, 191, 0.7)',
            marker_line=dict(color='rgba(55, 128, 191, 1.0)', width=1),
            hovertemplate='<b>k=%{x}</b><br>P(X=%{x})=%{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # CDF 阶梯图
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=cdf_values,
            mode='lines+markers',
            name='CDF',
            line=dict(color='red', width=3, shape='hv'),
            marker=dict(size=6, color='red'),
            hovertemplate='<b>k=%{x}</b><br>P(X≤%{x})=%{y:.4f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 期望值线（PMF图中）
    fig.add_trace(
        go.Scatter(
            x=[stats['mean'], stats['mean']],
            y=[0, max(pmf_values) * 1.1],
            mode='lines',
            name=f'期望值 E[X]={stats["mean"]:.2f}',
            line=dict(color='green', width=3, dash='dash'),
            showlegend=True
        ),
        row=1, col=1
    )
    
    # 统计特性显示
    stats_text = [
        f"期望值 E[X] = np = {stats['mean']:.3f}",
        f"方差 Var[X] = np(1-p) = {stats['variance']:.3f}",
        f"标准差 σ = {stats['std']:.3f}",
        f"偏度 = {stats['skewness']:.3f}"
    ]
    
    fig.add_trace(
        go.Scatter(
            x=[0.1, 0.1, 0.1, 0.1],
            y=[0.8, 0.6, 0.4, 0.2],
            mode='text',
            text=stats_text,
            textposition='middle right',
            textfont=dict(size=14, color='darkblue'),
            showlegend=False,
            name='统计特性'
        ),
        row=2, col=1
    )
    
    # 分布形状特征
    shape_info = []
    if abs(stats['skewness']) < 0.5:
        shape_info.append("分布形状：近似对称")
    elif stats['skewness'] > 0.5:
        shape_info.append("分布形状：右偏")
    else:
        shape_info.append("分布形状：左偏")
    
    if initial_p == 0.5:
        shape_info.append("p=0.5时分布最对称")
    elif initial_p < 0.5:
        shape_info.append("p<0.5时分布右偏")
    else:
        shape_info.append("p>0.5时分布左偏")
    
    fig.add_trace(
        go.Scatter(
            x=[0.1, 0.1],
            y=[0.7, 0.3],
            mode='text',
            text=shape_info,
            textposition='middle right',
            textfont=dict(size=14, color='darkgreen'),
            showlegend=False,
            name='形状特征'
        ),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '🎲 二项分布 B(n,p) 交互式可视化<br><sub>模式：固定n变化p | 使用滑块调整参数观察分布变化</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'darkblue'}
        },
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        annotations=[
            dict(
                text="📚 二项分布特性：<br>" +
                     "• 描述n次独立试验中成功次数<br>" +
                     "• 每次试验成功概率为p<br>" +
                     "• 期望值 = np，方差 = np(1-p)<br>" +
                     "• p=0.5时分布最对称",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor="left", yanchor="top",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1,
                font=dict(size=12, color="darkblue")
            )
        ]
    )
    
    # 更新坐标轴
    fig.update_xaxes(title_text="成功次数 k", row=1, col=1)
    fig.update_yaxes(title_text="概率 P(X=k)", row=1, col=1)
    fig.update_xaxes(title_text="成功次数 k", row=1, col=2)
    fig.update_yaxes(title_text="累积概率 P(X≤k)", row=1, col=2)
    fig.update_xaxes(title_text="", row=2, col=1, showticklabels=False)
    fig.update_yaxes(title_text="", row=2, col=1, showticklabels=False)
    fig.update_xaxes(title_text="", row=2, col=2, showticklabels=False)
    fig.update_yaxes(title_text="", row=2, col=2, showticklabels=False)
    
    # 添加滑块控件
    # 模式1：固定n=20，变化p
    p_steps = []
    for p_val in np.arange(0.05, 1.0, 0.05):
        x_vals = np.arange(0, initial_n + 1)
        pmf_vals = binom.pmf(x_vals, initial_n, p_val)
        cdf_vals = binom.cdf(x_vals, initial_n, p_val)
        stats_new = calculate_binomial_stats(initial_n, p_val)
        
        # 形状特征更新
        shape_info_new = []
        if abs(stats_new['skewness']) < 0.5:
            shape_info_new.append("分布形状：近似对称")
        elif stats_new['skewness'] > 0.5:
            shape_info_new.append("分布形状：右偏")
        else:
            shape_info_new.append("分布形状：左偏")
        
        if p_val == 0.5:
            shape_info_new.append("p=0.5时分布最对称")
        elif p_val < 0.5:
            shape_info_new.append("p<0.5时分布右偏")
        else:
            shape_info_new.append("p>0.5时分布左偏")
        
        step = dict(
            method="restyle",
            args=[{
                "x": [x_vals, x_vals, [stats_new['mean'], stats_new['mean']], 
                      [0.1, 0.1, 0.1, 0.1], [0.1, 0.1]],
                "y": [pmf_vals, cdf_vals, [0, max(pmf_vals) * 1.1],
                      [0.8, 0.6, 0.4, 0.2], [0.7, 0.3]],
                "text": [None, None, None,
                        [f"期望值 E[X] = np = {stats_new['mean']:.3f}",
                         f"方差 Var[X] = np(1-p) = {stats_new['variance']:.3f}",
                         f"标准差 σ = {stats_new['std']:.3f}",
                         f"偏度 = {stats_new['skewness']:.3f}"],
                        shape_info_new],
                "name": [None, None, f'期望值 E[X]={stats_new["mean"]:.2f}', None, None]
            }, {
                "title": f'🎲 二项分布 B({initial_n},{p_val:.2f}) 交互式可视化<br><sub>模式：固定n={initial_n}变化p | 当前p={p_val:.2f}</sub>'
            }],
            label=f"p={p_val:.2f}"
        )
        p_steps.append(step)
    
    # 添加滑块
    sliders = [dict(
        active=9,  # 默认p=0.5
        currentvalue={"prefix": "概率参数 p = "},
        pad={"t": 50},
        steps=p_steps,
        x=0.1,
        y=0,
        len=0.8,
        ticklen=0,
        tickcolor="white"
    )]
    
    fig.update_layout(sliders=sliders)
    
    return fig

def create_binomial_fixed_p_visualization():
    """创建固定p变化n的二项分布可视化"""
    
    # 初始参数
    initial_p = 0.3
    initial_n = 10
    max_n = 50
    
    # 计算初始数据
    x_values = np.arange(0, initial_n + 1)
    pmf_values = binom.pmf(x_values, initial_n, initial_p)
    cdf_values = binom.cdf(x_values, initial_n, initial_p)
    
    # 计算统计特性
    stats = calculate_binomial_stats(initial_n, initial_p)
    
    # 创建子图布局
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            f'概率质量函数 PMF - B({initial_n}, {initial_p:.2f})',
            f'累积分布函数 CDF - B({initial_n}, {initial_p:.2f})',
            '期望值与方差变化',
            '分布形状演变'
        ),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # PMF 柱状图
    fig.add_trace(
        go.Bar(
            x=x_values,
            y=pmf_values,
            name='PMF',
            marker_color='rgba(255, 127, 14, 0.7)',
            marker_line=dict(color='rgba(255, 127, 14, 1.0)', width=1),
            hovertemplate='<b>k=%{x}</b><br>P(X=%{x})=%{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # CDF 阶梯图
    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=cdf_values,
            mode='lines+markers',
            name='CDF',
            line=dict(color='purple', width=3, shape='hv'),
            marker=dict(size=6, color='purple'),
            hovertemplate='<b>k=%{x}</b><br>P(X≤%{x})=%{y:.4f}<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 期望值线
    fig.add_trace(
        go.Scatter(
            x=[stats['mean'], stats['mean']],
            y=[0, max(pmf_values) * 1.1],
            mode='lines',
            name=f'期望值 E[X]={stats["mean"]:.2f}',
            line=dict(color='green', width=3, dash='dash'),
            showlegend=True
        ),
        row=1, col=1
    )
    
    # 统计特性显示
    stats_text = [
        f"期望值 E[X] = np = {stats['mean']:.3f}",
        f"方差 Var[X] = np(1-p) = {stats['variance']:.3f}",
        f"标准差 σ = {stats['std']:.3f}",
        f"变异系数 CV = {stats['std']/stats['mean']:.3f}"
    ]
    
    fig.add_trace(
        go.Scatter(
            x=[0.1, 0.1, 0.1, 0.1],
            y=[0.8, 0.6, 0.4, 0.2],
            mode='text',
            text=stats_text,
            textposition='middle right',
            textfont=dict(size=14, color='darkred'),
            showlegend=False,
            name='统计特性'
        ),
        row=2, col=1
    )
    
    # 分布形状特征
    shape_info = [
        f"试验次数 n = {initial_n}",
        f"成功概率 p = {initial_p:.2f}",
        f"随着n增大，分布趋向正态",
        f"np = {stats['mean']:.1f}, np(1-p) = {stats['variance']:.1f}"
    ]
    
    fig.add_trace(
        go.Scatter(
            x=[0.1, 0.1, 0.1, 0.1],
            y=[0.8, 0.6, 0.4, 0.2],
            mode='text',
            text=shape_info,
            textposition='middle right',
            textfont=dict(size=14, color='darkgreen'),
            showlegend=False,
            name='形状特征'
        ),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '🎲 二项分布 B(n,p) 交互式可视化<br><sub>模式：固定p变化n | 观察试验次数对分布形状的影响</sub>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': 'darkred'}
        },
        height=800,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        annotations=[
            dict(
                text="📈 固定p变化n的观察要点：<br>" +
                     "• n增大时，期望值线性增长<br>" +
                     "• 方差也随n线性增长<br>" +
                     "• 当np和n(1-p)都≥5时，<br>" +
                     "  分布近似正态分布<br>" +
                     "• 变异系数随n减小",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.02, y=0.98,
                xanchor="left", yanchor="top",
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1,
                font=dict(size=12, color="darkred")
            )
        ]
    )
    
    # 更新坐标轴
    fig.update_xaxes(title_text="成功次数 k", row=1, col=1)
    fig.update_yaxes(title_text="概率 P(X=k)", row=1, col=1)
    fig.update_xaxes(title_text="成功次数 k", row=1, col=2)
    fig.update_yaxes(title_text="累积概率 P(X≤k)", row=1, col=2)
    fig.update_xaxes(title_text="", row=2, col=1, showticklabels=False)
    fig.update_yaxes(title_text="", row=2, col=1, showticklabels=False)
    fig.update_xaxes(title_text="", row=2, col=2, showticklabels=False)
    fig.update_yaxes(title_text="", row=2, col=2, showticklabels=False)
    
    # 添加滑块控件 - 固定p变化n
    n_steps = []
    for n_val in range(5, max_n + 1, 2):
        x_vals = np.arange(0, n_val + 1)
        pmf_vals = binom.pmf(x_vals, n_val, initial_p)
        cdf_vals = binom.cdf(x_vals, n_val, initial_p)
        stats_new = calculate_binomial_stats(n_val, initial_p)
        
        # 正态近似判断
        normal_approx = "是" if (n_val * initial_p >= 5 and n_val * (1 - initial_p) >= 5) else "否"
        
        shape_info_new = [
            f"试验次数 n = {n_val}",
            f"成功概率 p = {initial_p:.2f}",
            f"可用正态近似：{normal_approx}",
            f"np = {stats_new['mean']:.1f}, np(1-p) = {stats_new['variance']:.1f}"
        ]
        
        step = dict(
            method="restyle",
            args=[{
                "x": [x_vals, x_vals, [stats_new['mean'], stats_new['mean']], 
                      [0.1, 0.1, 0.1, 0.1], [0.1, 0.1, 0.1, 0.1]],
                "y": [pmf_vals, cdf_vals, [0, max(pmf_vals) * 1.1],
                      [0.8, 0.6, 0.4, 0.2], [0.8, 0.6, 0.4, 0.2]],
                "text": [None, None, None,
                        [f"期望值 E[X] = np = {stats_new['mean']:.3f}",
                         f"方差 Var[X] = np(1-p) = {stats_new['variance']:.3f}",
                         f"标准差 σ = {stats_new['std']:.3f}",
                         f"变异系数 CV = {stats_new['std']/stats_new['mean']:.3f}"],
                        shape_info_new],
                "name": [None, None, f'期望值 E[X]={stats_new["mean"]:.2f}', None, None]
            }, {
                "title": f'🎲 二项分布 B({n_val},{initial_p:.2f}) 交互式可视化<br><sub>模式：固定p={initial_p:.2f}变化n | 当前n={n_val}</sub>'
            }],
            label=f"n={n_val}"
        )
        n_steps.append(step)
    
    # 添加滑块
    sliders = [dict(
        active=2,  # 默认n=10
        currentvalue={"prefix": "试验次数 n = "},
        pad={"t": 50},
        steps=n_steps,
        x=0.1,
        y=0,
        len=0.8,
        ticklen=0,
        tickcolor="white"
    )]
    
    fig.update_layout(sliders=sliders)
    
    return fig

def main():
    """主函数：生成两种模式的可视化"""
    
    print("🎲 正在生成二项分布交互式可视化...")
    
    # 生成固定n变化p的可视化
    print("📊 创建模式1：固定n变化p...")
    fig1 = create_binomial_visualization()
    
    # 保存第一个可视化
    html_file1 = "binomial_fixed_n_interactive.html"
    pyo.plot(fig1, filename=html_file1, auto_open=False)
    print(f"✅ 模式1可视化已保存为: {html_file1}")
    
    # 生成固定p变化n的可视化
    print("📊 创建模式2：固定p变化n...")
    fig2 = create_binomial_fixed_p_visualization()
    
    # 保存第二个可视化
    html_file2 = "binomial_fixed_p_interactive.html"
    pyo.plot(fig2, filename=html_file2, auto_open=False)
    print(f"✅ 模式2可视化已保存为: {html_file2}")
    
    print("\n🎉 二项分布交互式可视化创建完成！")
    print("\n📁 生成的文件：")
    print(f"   • {html_file1} - 固定n=20，变化p (0.05-0.95)")
    print(f"   • {html_file2} - 固定p=0.3，变化n (5-50)")
    print("\n🔧 使用方法：")
    print("   1. 用浏览器打开HTML文件")
    print("   2. 使用底部滑块调整参数")
    print("   3. 观察PMF、CDF和统计特性的变化")
    print("   4. 注意分布形状随参数的演变规律")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
二项分布B(n,p)的3D可视化 - n和p同时变化
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.stats import binom
import plotly.express as px

def create_3d_parameter_surface():
    """创建3D参数表面图"""
    
    # 参数网格
    n_range = np.arange(5, 51, 2)  # n从5到50
    p_range = np.arange(0.05, 1.0, 0.05)  # p从0.05到0.95
    N, P = np.meshgrid(n_range, p_range)
    
    # 计算期望值和方差
    Z_mean = N * P  # 期望值 E[X] = n*p
    Z_var = N * P * (1 - P)  # 方差 Var[X] = n*p*(1-p)
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            '期望值 E[X] = n×p',
            '方差 Var[X] = n×p×(1-p)',
            '标准差 σ = √(n×p×(1-p))',
            '变异系数 CV = σ/μ'
        ],
        specs=[
            [{"type": "surface"}, {"type": "surface"}],
            [{"type": "surface"}, {"type": "surface"}]
        ]
    )
    
    # 1. 期望值表面
    fig.add_trace(
        go.Surface(
            x=N, y=P, z=Z_mean,
            colorscale='Viridis',
            name='期望值',
            showscale=True,
            colorbar=dict(x=0.45, len=0.4, y=0.8)
        ),
        row=1, col=1
    )
    
    # 2. 方差表面
    fig.add_trace(
        go.Surface(
            x=N, y=P, z=Z_var,
            colorscale='Plasma',
            name='方差',
            showscale=True,
            colorbar=dict(x=1.02, len=0.4, y=0.8)
        ),
        row=1, col=2
    )
    
    # 3. 标准差表面
    Z_std = np.sqrt(Z_var)
    fig.add_trace(
        go.Surface(
            x=N, y=P, z=Z_std,
            colorscale='Cividis',
            name='标准差',
            showscale=True,
            colorbar=dict(x=0.45, len=0.4, y=0.2)
        ),
        row=2, col=1
    )
    
    # 4. 变异系数表面 (CV = σ/μ)
    Z_cv = Z_std / Z_mean
    Z_cv = np.where(Z_mean > 0, Z_cv, 0)  # 避免除零
    fig.add_trace(
        go.Surface(
            x=N, y=P, z=Z_cv,
            colorscale='RdYlBu',
            name='变异系数',
            showscale=True,
            colorbar=dict(x=1.02, len=0.4, y=0.2)
        ),
        row=2, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '二项分布B(n,p)参数影响的3D可视化',
            'x': 0.5,
            'font': {'size': 16}
        },
        height=800,
        width=1000
    )
    
    # 更新各个子图的轴标签
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_layout(**{
                f'scene{i*2+j-2 if i*2+j-2 > 1 else ""}': dict(
                    xaxis_title='试验次数 n',
                    yaxis_title='成功概率 p',
                    zaxis_title='值',
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
                )
            })
    
    return fig

def create_interactive_3d_pmf():
    """创建交互式3D概率质量函数可视化"""
    
    fig = go.Figure()
    
    # 选择几个代表性的参数组合
    param_combinations = [
        (10, 0.2), (10, 0.5), (10, 0.8),
        (20, 0.2), (20, 0.5), (20, 0.8),
        (30, 0.3), (30, 0.7)
    ]
    
    colors = px.colors.qualitative.Set3
    
    for i, (n, p) in enumerate(param_combinations):
        k = np.arange(0, n + 1)
        pmf = binom.pmf(k, n, p)
        
        # 创建3D散点，其中：
        # x轴：成功次数k
        # y轴：概率p
        # z轴：试验次数n
        # 点的大小和颜色表示概率质量函数值
        
        fig.add_trace(
            go.Scatter3d(
                x=k,
                y=np.full_like(k, p),
                z=np.full_like(k, n),
                mode='markers',
                marker=dict(
                    size=pmf * 200,  # 根据概率调整大小
                    color=pmf,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title="P(X=k)", x=1.1) if i == 0 else None,
                    showscale=True if i == 0 else False
                ),
                name=f'B({n},{p})',
                text=[f'P(X={k_val})={pmf_val:.4f}' for k_val, pmf_val in zip(k, pmf)],
                hovertemplate='<b>B(%{z},%{y})</b><br>' +
                            '成功次数 k: %{x}<br>' +
                            '概率: %{text}<br>' +
                            '<extra></extra>'
            )
        )
    
    # 更新布局
    fig.update_layout(
        title='交互式3D二项分布概率质量函数',
        scene=dict(
            xaxis_title='成功次数 k',
            yaxis_title='成功概率 p',
            zaxis_title='试验次数 n',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        height=700,
        width=900
    )
    
    return fig

def create_heatmap_analysis():
    """创建热力图分析"""
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            '期望值热力图',
            '方差热力图',
            '偏度分析',
            '峰度分析'
        ],
        specs=[
            [{"type": "heatmap"}, {"type": "heatmap"}],
            [{"type": "heatmap"}, {"type": "heatmap"}]
        ]
    )
    
    # 参数网格
    n_range = np.arange(5, 31, 1)
    p_range = np.arange(0.1, 1.0, 0.05)
    N, P = np.meshgrid(n_range, p_range)
    
    # 1. 期望值热力图
    Z_mean = N * P
    fig.add_trace(
        go.Heatmap(
            x=n_range,
            y=p_range,
            z=Z_mean,
            colorscale='Viridis',
            name='期望值'
        ),
        row=1, col=1
    )
    
    # 2. 方差热力图
    Z_var = N * P * (1 - P)
    fig.add_trace(
        go.Heatmap(
            x=n_range,
            y=p_range,
            z=Z_var,
            colorscale='Plasma',
            name='方差'
        ),
        row=1, col=2
    )
    
    # 3. 偏度分析 (Skewness = (1-2p)/√(np(1-p)))
    Z_skew = (1 - 2*P) / np.sqrt(N * P * (1 - P))
    Z_skew = np.where((N * P * (1 - P)) > 0, Z_skew, 0)
    fig.add_trace(
        go.Heatmap(
            x=n_range,
            y=p_range,
            z=Z_skew,
            colorscale='RdBu',
            name='偏度'
        ),
        row=2, col=1
    )
    
    # 4. 峰度分析 (Kurtosis = (1-6p(1-p))/(np(1-p)))
    Z_kurt = (1 - 6*P*(1-P)) / (N * P * (1 - P))
    Z_kurt = np.where((N * P * (1 - P)) > 0, Z_kurt, 0)
    fig.add_trace(
        go.Heatmap(
            x=n_range,
            y=p_range,
            z=Z_kurt,
            colorscale='Cividis',
            name='峰度'
        ),
        row=2, col=2
    )
    
    # 更新轴标签
    for i in range(1, 3):
        for j in range(1, 3):
            fig.update_xaxes(title_text="试验次数 n", row=i, col=j)
            fig.update_yaxes(title_text="成功概率 p", row=i, col=j)
    
    fig.update_layout(
        title='二项分布统计特性热力图分析',
        height=800,
        width=1000
    )
    
    return fig

if __name__ == "__main__":
    print("🎲 生成二项分布3D可视化...")
    
    # 1. 创建3D参数表面图
    fig1 = create_3d_parameter_surface()
    fig1.write_html("binomial_3d_surface.html")
    print("✅ 3D表面图已保存: binomial_3d_surface.html")
    
    # 2. 创建交互式3D PMF
    fig2 = create_interactive_3d_pmf()
    fig2.write_html("binomial_3d_interactive.html")
    print("✅ 交互式3D图已保存: binomial_3d_interactive.html")
    
    # 3. 创建热力图分析
    fig3 = create_heatmap_analysis()
    fig3.write_html("binomial_heatmap_analysis.html")
    print("✅ 热力图分析已保存: binomial_heatmap_analysis.html")
    
    # 显示图表
    print("\n📊 显示可视化...")
    fig1.show()
    fig2.show()
    fig3.show()
    
    print("\n📈 二项分布3D分析总结:")
    print("🔍 参数影响规律:")
    print("  • 期望值 E[X] = n×p 随n和p线性增长")
    print("  • 方差 Var[X] = n×p×(1-p) 在p=0.5时达到最大")
    print("  • 标准差 σ = √(n×p×(1-p)) 随√n增长")
    print("  • 变异系数 CV = σ/μ = √((1-p)/(n×p)) 随n减小")
    print("\n🎯 分布形状特征:")
    print("  • p=0.5时分布对称（偏度=0）")
    print("  • p<0.5时右偏（正偏度）")
    print("  • p>0.5时左偏（负偏度）")
    print("  • n增大时分布趋向正态分布")
    print("\n💡 实际应用指导:")
    print("  • 样本量设计：根据期望精度选择n")
    print("  • 假设检验：利用正态近似条件")
    print("  • 质量控制：监控过程稳定性")

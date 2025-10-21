"""
泊松分布交互式可视化
根据交互式3D可视化应用详细执行任务清单v1014创建
展示参数λ变化时泊松分布的动态效果，使用进度条控制参数
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

def poisson_pmf(k, lam):
    """
    计算泊松分布的概率质量函数
    P(X = k) = (λ^k * e^(-λ)) / k!
    """
    return (lam ** k) * np.exp(-lam) / math.factorial(k)

def create_poisson_visualization():
    """
    创建泊松分布的交互式可视化
    包含λ参数的滑块控制
    """
    
    # 定义参数范围
    lambda_min, lambda_max = 0.5, 15.0
    lambda_step = 0.1
    lambda_values = np.arange(lambda_min, lambda_max + lambda_step, lambda_step)
    
    # 定义k值范围（泊松分布的支撑集）
    k_max = 30
    k_values = np.arange(0, k_max + 1)
    
    # 创建子图：主图 + 统计信息图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('泊松分布概率质量函数 (PMF)', '累积分布函数 (CDF)', 
                       '期望值与方差', '分布形状特征'),
        specs=[[{"colspan": 2}, None],
               [{"type": "scatter"}, {"type": "scatter"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.1
    )
    
    # 初始λ值
    initial_lambda = 3.0
    
    # 计算初始PMF和CDF
    initial_pmf = [poisson_pmf(k, initial_lambda) for k in k_values]
    initial_cdf = np.cumsum(initial_pmf)
    
    # 主图：PMF柱状图
    fig.add_trace(
        go.Bar(
            x=k_values,
            y=initial_pmf,
            name=f'PMF (λ={initial_lambda})',
            marker=dict(
                color='rgba(55, 128, 191, 0.7)',
                line=dict(color='rgba(55, 128, 191, 1.0)', width=2)
            ),
            hovertemplate='<b>k=%{x}</b><br>P(X=k)=%{y:.4f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # CDF图
    fig.add_trace(
        go.Scatter(
            x=k_values,
            y=initial_cdf,
            mode='lines+markers',
            name=f'CDF (λ={initial_lambda})',
            line=dict(color='rgba(219, 64, 82, 0.8)', width=3),
            marker=dict(size=6),
            hovertemplate='<b>k=%{x}</b><br>P(X≤k)=%{y:.4f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    # 期望值和方差图（泊松分布的期望和方差都等于λ）
    lambda_range = np.linspace(lambda_min, lambda_max, 100)
    fig.add_trace(
        go.Scatter(
            x=lambda_range,
            y=lambda_range,  # E[X] = λ
            mode='lines',
            name='期望值 E[X] = λ',
            line=dict(color='green', width=3),
            hovertemplate='<b>λ=%{x:.2f}</b><br>E[X]=%{y:.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Scatter(
            x=lambda_range,
            y=lambda_range,  # Var[X] = λ
            mode='lines',
            name='方差 Var[X] = λ',
            line=dict(color='orange', width=3, dash='dash'),
            hovertemplate='<b>λ=%{x:.2f}</b><br>Var[X]=%{y:.2f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 添加当前λ值的标记点
    fig.add_trace(
        go.Scatter(
            x=[initial_lambda],
            y=[initial_lambda],
            mode='markers',
            name=f'当前 λ = {initial_lambda}',
            marker=dict(size=12, color='red', symbol='diamond'),
            hovertemplate='<b>当前λ=%{x:.1f}</b><br>E[X]=Var[X]=%{y:.1f}<extra></extra>'
        ),
        row=2, col=2
    )
    
    # 创建滑块步骤 - 使用简化的更新方式
    steps = []
    for lam in lambda_values:
        # 计算当前λ的PMF和CDF
        pmf = [poisson_pmf(k, lam) for k in k_values]
        cdf = np.cumsum(pmf)
        
        step = dict(
            method="restyle",
            args=[
                {
                    "y": [pmf, cdf, lambda_range, lambda_range, [lam]],
                    "name": [f'PMF (λ={lam:.1f})', f'CDF (λ={lam:.1f})', 
                            '期望值 E[X] = λ', '方差 Var[X] = λ', f'当前 λ = {lam:.1f}']
                }
            ],
            label=f"{lam:.1f}"
        )
        steps.append(step)
    
    # 配置滑块
    sliders = [dict(
        active=int((initial_lambda - lambda_min) / lambda_step),
        currentvalue={"prefix": "λ参数: "},
        pad={"t": 50},
        steps=steps,
        len=0.9,
        x=0.05,
        y=0,
        ticklen=5,
        tickcolor="lightgray",
        tickwidth=2
    )]
    
    # 更新布局
    fig.update_layout(
        title=dict(
            text=f"泊松分布交互式可视化 (λ = {initial_lambda})",
            x=0.5,
            font=dict(size=20, color='darkblue')
        ),
        sliders=sliders,
        showlegend=True,
        height=800,
        width=1200,
        template="plotly_white",
        font=dict(family="Arial, sans-serif", size=12),
        margin=dict(l=80, r=80, t=100, b=120)
    )
    
    # 更新各子图的坐标轴
    fig.update_xaxes(title_text="事件发生次数 k", row=1, col=1)
    fig.update_yaxes(title_text="概率 P(X = k)", row=1, col=1)
    
    fig.update_xaxes(title_text="事件发生次数 k", row=2, col=1)
    fig.update_yaxes(title_text="累积概率 P(X ≤ k)", row=2, col=1)
    
    fig.update_xaxes(title_text="参数 λ", row=2, col=2)
    fig.update_yaxes(title_text="数值", row=2, col=2)
    
    # 添加静态注释框
    fig.add_annotation(
        text="<b>泊松分布特性:</b><br>" +
             "• 期望值 E[X] = λ<br>" +
             "• 方差 Var[X] = λ<br>" +
             "• 适用于稀有事件计数<br>" +
             "• λ越大，分布越趋向正态",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        font=dict(size=11, color="darkgreen"),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="darkgreen",
        borderwidth=1
    )
    
    return fig

# 创建可视化
if __name__ == "__main__":
    fig = create_poisson_visualization()
    
    # 显示图表
    fig.show()
    
    # 可选：保存为HTML文件
    fig.write_html("poisson_interactive_visualization.html")
    print("泊松分布交互式可视化已创建完成！")
    print("- 使用底部滑块调整λ参数 (0.5 - 15.0)")
    print("- 观察PMF、CDF和统计特性的变化")
    print("- 图表已保存为 poisson_interactive_visualization.html")
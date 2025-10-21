import os
import sys
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# 添加config目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config'))

try:
    from discipline_router import analyze_and_route, classify_prompt, get_template_content
except ImportError as e:
    print(f"导入路由模块失败: {e}")
    sys.exit(1)

class AICodeGenerator:
    """AI代码生成器 - 整合学科分类、模板路由和多模型调用"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.generation_history = []
        self.supported_models = {
            "gpt-4": {"priority": 1, "complexity": "high", "cost": "high"},
            "gpt-3.5": {"priority": 3, "complexity": "medium", "cost": "low"},
            "claude-3.5-sonnet": {"priority": 2, "complexity": "high", "cost": "medium"},
            "gpt-4v": {"priority": 1, "complexity": "visual", "cost": "high"},
            "codellama": {"priority": 4, "complexity": "code", "cost": "low"},
            "deepseek": {"priority": 3, "complexity": "math", "cost": "low"}
        }
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("AICodeGenerator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def generate_visualization_code(self, user_input: str, 
                                  preferred_model: Optional[str] = None,
                                  complexity_override: Optional[str] = None) -> Dict:
        """
        生成可视化代码的主入口函数
        
        Args:
            user_input: 用户输入的需求描述
            preferred_model: 用户指定的模型（可选）
            complexity_override: 复杂度覆盖设置（可选）
            
        Returns:
            包含生成代码、元数据和分析结果的字典
        """
        try:
            # 1. 分析用户输入并路由到合适的学科模板
            self.logger.info(f"开始分析用户输入: {user_input[:50]}...")
            routing_result = analyze_and_route(user_input)
            
            # 2. 选择最佳模型
            selected_model = self._select_optimal_model(
                routing_result, preferred_model, complexity_override
            )
            
            # 3. 构建完整的提示词
            full_prompt = self._build_complete_prompt(user_input, routing_result)
            
            # 4. 生成代码（这里模拟AI模型调用）
            generated_code = self._simulate_ai_generation(full_prompt, selected_model, routing_result)
            
            # 5. 后处理和验证
            processed_result = self._post_process_code(generated_code, routing_result)
            
            # 6. 记录生成历史
            generation_record = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "routing_result": routing_result,
                "selected_model": selected_model,
                "success": processed_result["success"],
                "code_length": len(processed_result["code"]),
                "discipline": routing_result["classification"]["discipline"],
                "subfield": routing_result["classification"]["subfield"]
            }
            self.generation_history.append(generation_record)
            
            self.logger.info(f"代码生成完成 - 学科: {routing_result['classification']['discipline']}, "
                           f"模型: {selected_model}, 成功: {processed_result['success']}")
            
            return {
                "success": processed_result["success"],
                "code": processed_result["code"],
                "metadata": {
                    "discipline": routing_result["classification"]["discipline"],
                    "subfield": routing_result["classification"]["subfield"],
                    "template": routing_result["classification"]["template"],
                    "model_used": selected_model,
                    "confidence": routing_result["classification"]["confidence"],
                    "complexity": routing_result["complexity"],
                    "matched_keywords": routing_result["classification"]["matched_keywords"]
                },
                "analysis": routing_result,
                "suggestions": self._generate_suggestions(routing_result),
                "generation_id": len(self.generation_history)
            }
            
        except Exception as e:
            self.logger.error(f"代码生成失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "code": "# 代码生成失败，请检查输入或联系技术支持",
                "metadata": {},
                "analysis": {},
                "suggestions": ["请尝试更具体的描述", "检查输入是否包含有效的可视化需求"],
                "generation_id": None
            }
    
    def _select_optimal_model(self, routing_result: Dict, 
                            preferred_model: Optional[str] = None,
                            complexity_override: Optional[str] = None) -> str:
        """选择最优的AI模型"""
        
        # 如果用户指定了模型且该模型可用，优先使用
        if preferred_model and preferred_model in self.supported_models:
            return preferred_model
        
        # 获取推荐模型列表
        recommended_models = routing_result["classification"]["models"]
        complexity = complexity_override or routing_result["recommended_approach"]
        
        # 根据复杂度和可用性选择模型
        for model in recommended_models:
            if model in self.supported_models:
                model_info = self.supported_models[model]
                
                # 检查模型是否适合当前复杂度
                if complexity == "high_complexity" and model_info["complexity"] in ["high", "visual"]:
                    return model
                elif complexity == "medium_complexity" and model_info["complexity"] in ["high", "medium", "math"]:
                    return model
                elif complexity == "simple_visualization" and model_info["complexity"] in ["medium", "low", "code"]:
                    return model
        
        # 如果没有找到合适的模型，使用默认模型
        return "gpt-3.5"
    
    def _build_complete_prompt(self, user_input: str, routing_result: Dict) -> str:
        """构建完整的提示词"""
        
        template_content = routing_result["template_content"]
        classification = routing_result["classification"]
        complexity = routing_result["complexity"]
        
        # 构建上下文信息
        context_info = f"""
学科分类: {classification['discipline']} - {classification['subfield']}
置信度: {classification['confidence']:.2f}
匹配关键词: {', '.join(classification['matched_keywords'])}
复杂度评估: {complexity['complexity_score']}/5
"""
        
        # 构建完整提示词
        full_prompt = f"""
{template_content}

===== 上下文信息 =====
{context_info}

===== 用户需求 =====
{user_input}

===== 特殊要求 =====
1. 代码必须完整可执行，包含所有必要的import语句
2. 添加详细的中文注释说明
3. 包含错误处理和异常捕获
4. 优化代码性能，适合实际使用
5. 提供使用示例和参数说明
6. 确保代码符合PEP8规范

请根据以上要求生成高质量的可视化代码。
"""
        
        return full_prompt
    
    def _simulate_ai_generation(self, prompt: str, model: str, routing_result: Dict) -> str:
        """
        模拟AI模型生成代码
        在实际应用中，这里会调用真实的AI API
        """
        
        discipline = routing_result["classification"]["discipline"]
        subfield = routing_result["classification"]["subfield"]
        
        # 根据学科生成不同类型的示例代码
        if discipline == "Mathematics" and subfield == "LinearAlgebra":
            return self._generate_linear_algebra_code()
        elif discipline == "Statistics":
            return self._generate_statistics_code()
        elif discipline == "Physics":
            return self._generate_physics_code()
        elif discipline == "Biology":
            return self._generate_biology_code()
        elif discipline == "Chemistry":
            return self._generate_chemistry_code()
        elif discipline == "DataScience":
            return self._generate_data_science_code()
        else:
            return self._generate_general_code()
    
    def _generate_linear_algebra_code(self) -> str:
        """生成线性代数可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def visualize_matrix_determinant():
    """可视化矩阵行列式的几何意义"""
    
    # 创建2x2矩阵
    A = np.array([[2, 1], [1, 2]])
    
    # 计算行列式
    det_A = np.linalg.det(A)
    
    # 创建单位正方形的顶点
    unit_square = np.array([[0, 1, 1, 0, 0], [0, 0, 1, 1, 0]])
    
    # 应用线性变换
    transformed_square = A @ unit_square
    
    # 创建可视化
    fig = make_subplots(rows=1, cols=2, 
                       subplot_titles=('原始单位正方形', f'变换后图形 (行列式={det_A:.2f})'))
    
    # 原始正方形
    fig.add_trace(go.Scatter(x=unit_square[0], y=unit_square[1], 
                            mode='lines+markers', name='单位正方形',
                            line=dict(color='blue', width=3)), row=1, col=1)
    
    # 变换后的图形
    fig.add_trace(go.Scatter(x=transformed_square[0], y=transformed_square[1], 
                            mode='lines+markers', name='变换后图形',
                            line=dict(color='red', width=3)), row=1, col=2)
    
    # 添加面积填充
    fig.add_trace(go.Scatter(x=transformed_square[0], y=transformed_square[1], 
                            fill='toself', fillcolor='rgba(255,0,0,0.3)',
                            mode='none', name=f'面积={abs(det_A):.2f}'), row=1, col=2)
    
    fig.update_layout(title='线性变换与行列式的几何意义',
                     showlegend=True, height=500)
    
    return fig

# 生成并显示图形
fig = visualize_matrix_determinant()
fig.show()
'''
    
    def _generate_statistics_code(self) -> str:
        """生成统计分布可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import plotly.express as px

def interactive_distribution_visualization():
    """交互式概率分布可视化"""
    
    # 参数设置
    x = np.linspace(-4, 4, 1000)
    
    # 创建子图
    fig = make_subplots(rows=2, cols=2,
                       subplot_titles=('正态分布PDF', '正态分布CDF', 
                                     '多分布比较', '3D概率密度'))
    
    # 正态分布PDF
    for mu, sigma, color in [(0, 1, 'blue'), (0, 0.5, 'red'), (1, 1, 'green')]:
        y_pdf = stats.norm.pdf(x, mu, sigma)
        fig.add_trace(go.Scatter(x=x, y=y_pdf, 
                                name=f'N({mu},{sigma}²)', 
                                line=dict(color=color)), row=1, col=1)
    
    # 正态分布CDF
    y_cdf = stats.norm.cdf(x, 0, 1)
    fig.add_trace(go.Scatter(x=x, y=y_cdf, 
                            name='标准正态CDF', 
                            line=dict(color='purple')), row=1, col=2)
    
    # 多分布比较
    distributions = {
        '正态分布': stats.norm(0, 1),
        't分布': stats.t(df=3),
        '拉普拉斯分布': stats.laplace(0, 1)
    }
    
    for name, dist in distributions.items():
        y = dist.pdf(x)
        fig.add_trace(go.Scatter(x=x, y=y, name=name), row=2, col=1)
    
    # 3D概率密度（二元正态分布）
    x_3d = np.linspace(-3, 3, 50)
    y_3d = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x_3d, y_3d)
    
    # 二元正态分布
    mu = [0, 0]
    sigma = [[1, 0.5], [0.5, 1]]
    pos = np.dstack((X, Y))
    rv = stats.multivariate_normal(mu, sigma)
    Z = rv.pdf(pos)
    
    fig.add_trace(go.Surface(x=X, y=Y, z=Z, 
                            colorscale='Viridis',
                            name='二元正态分布'), row=2, col=2)
    
    fig.update_layout(title='交互式概率分布可视化',
                     height=800, showlegend=True)
    
    return fig

# 生成并显示图形
fig = interactive_distribution_visualization()
fig.show()
'''
    
    def _generate_general_code(self) -> str:
        """生成通用可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_interactive_3d_visualization():
    """创建交互式3D数据可视化"""
    
    # 生成示例数据
    n_points = 500
    
    # 创建3D散点数据
    np.random.seed(42)
    x = np.random.randn(n_points)
    y = np.random.randn(n_points)
    z = x**2 + y**2 + np.random.randn(n_points) * 0.1
    
    # 创建颜色映射
    colors = z
    
    # 创建3D散点图
    fig = go.Figure()
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=colors,
            colorscale='Viridis',
            colorbar=dict(title="Z值"),
            opacity=0.8
        ),
        text=[f'点{i}: ({x[i]:.2f}, {y[i]:.2f}, {z[i]:.2f})' for i in range(len(x))],
        hovertemplate='<b>坐标</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>',
        name='数据点'
    ))
    
    # 添加拟合曲面
    x_surf = np.linspace(x.min(), x.max(), 20)
    y_surf = np.linspace(y.min(), y.max(), 20)
    X_surf, Y_surf = np.meshgrid(x_surf, y_surf)
    Z_surf = X_surf**2 + Y_surf**2
    
    fig.add_trace(go.Surface(
        x=X_surf, y=Y_surf, z=Z_surf,
        opacity=0.3,
        colorscale='Blues',
        showscale=False,
        name='拟合曲面'
    ))
    
    # 更新布局
    fig.update_layout(
        title='交互式3D数据可视化',
        scene=dict(
            xaxis_title='X轴',
            yaxis_title='Y轴',
            zaxis_title='Z轴',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=800,
        height=600
    )
    
    return fig

# 生成并显示图形
fig = create_interactive_3d_visualization()
fig.show()
'''
    
    def _generate_physics_code(self) -> str:
        """生成物理可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def solar_system_simulation():
    """太阳系轨道模拟"""
    
    # 轨道参数（简化模型）
    earth_orbit_radius = 1.0
    moon_orbit_radius = 0.1
    
    # 时间参数
    t = np.linspace(0, 4*np.pi, 200)
    
    # 地球轨道（围绕太阳）
    earth_x = earth_orbit_radius * np.cos(t)
    earth_y = earth_orbit_radius * np.sin(t)
    earth_z = np.zeros_like(t)
    
    # 月球轨道（围绕地球）
    moon_x = earth_x + moon_orbit_radius * np.cos(12*t)  # 月球公转更快
    moon_y = earth_y + moon_orbit_radius * np.sin(12*t)
    moon_z = np.zeros_like(t)
    
    # 创建3D图形
    fig = go.Figure()
    
    # 太阳
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=20, color='yellow'),
        name='太阳'
    ))
    
    # 地球轨道
    fig.add_trace(go.Scatter3d(
        x=earth_x, y=earth_y, z=earth_z,
        mode='lines',
        line=dict(color='blue', width=2),
        name='地球轨道'
    ))
    
    # 地球
    fig.add_trace(go.Scatter3d(
        x=[earth_x[-1]], y=[earth_y[-1]], z=[earth_z[-1]],
        mode='markers',
        marker=dict(size=10, color='blue'),
        name='地球'
    ))
    
    # 月球轨道
    fig.add_trace(go.Scatter3d(
        x=moon_x, y=moon_y, z=moon_z,
        mode='lines',
        line=dict(color='gray', width=1),
        name='月球轨道'
    ))
    
    # 月球
    fig.add_trace(go.Scatter3d(
        x=[moon_x[-1]], y=[moon_y[-1]], z=[moon_z[-1]],
        mode='markers',
        marker=dict(size=5, color='gray'),
        name='月球'
    ))
    
    # 更新布局
    fig.update_layout(
        title='太阳-地球-月球系统轨道模拟',
        scene=dict(
            xaxis_title='X (AU)',
            yaxis_title='Y (AU)',
            zaxis_title='Z (AU)',
            aspectmode='cube'
        ),
        width=800,
        height=600
    )
    
    return fig

# 生成并显示图形
fig = solar_system_simulation()
fig.show()
'''
    
    def _generate_biology_code(self) -> str:
        """生成生物学可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def dna_structure_visualization():
    """DNA双螺旋结构可视化"""
    
    # 参数设置
    t = np.linspace(0, 4*np.pi, 200)
    radius = 1.0
    pitch = 0.5  # 螺距
    
    # 第一条链
    x1 = radius * np.cos(t)
    y1 = radius * np.sin(t)
    z1 = pitch * t
    
    # 第二条链（相位差π）
    x2 = radius * np.cos(t + np.pi)
    y2 = radius * np.sin(t + np.pi)
    z2 = pitch * t
    
    # 创建3D图形
    fig = go.Figure()
    
    # 第一条DNA链
    fig.add_trace(go.Scatter3d(
        x=x1, y=y1, z=z1,
        mode='lines+markers',
        line=dict(color='red', width=6),
        marker=dict(size=3),
        name='DNA链1'
    ))
    
    # 第二条DNA链
    fig.add_trace(go.Scatter3d(
        x=x2, y=y2, z=z2,
        mode='lines+markers',
        line=dict(color='blue', width=6),
        marker=dict(size=3),
        name='DNA链2'
    ))
    
    # 添加碱基对连接
    for i in range(0, len(t), 10):  # 每10个点添加一个连接
        fig.add_trace(go.Scatter3d(
            x=[x1[i], x2[i]], 
            y=[y1[i], y2[i]], 
            z=[z1[i], z2[i]],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))
    
    # 更新布局
    fig.update_layout(
        title='DNA双螺旋结构',
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z (沿轴向)',
            camera=dict(
                eye=dict(x=2, y=2, z=1)
            )
        ),
        width=800,
        height=600
    )
    
    return fig

# 生成并显示图形
fig = dna_structure_visualization()
fig.show()
'''
    
    def _generate_chemistry_code(self) -> str:
        """生成化学可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go

def molecular_orbital_visualization():
    """分子轨道可视化"""
    
    # 创建3D网格
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    z = np.linspace(-3, 3, 50)
    X, Y, Z = np.meshgrid(x, y, z)
    
    # 氢原子1s轨道波函数（简化）
    r1 = np.sqrt(X**2 + Y**2 + Z**2)
    psi_1s = np.exp(-r1)
    
    # p轨道波函数（简化）
    psi_px = X * np.exp(-r1)
    psi_py = Y * np.exp(-r1)
    psi_pz = Z * np.exp(-r1)
    
    # 创建等值面
    fig = go.Figure()
    
    # 1s轨道
    fig.add_trace(go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=psi_1s.flatten(),
        isomin=0.1,
        isomax=0.5,
        surface_count=3,
        colorscale='Blues',
        name='1s轨道',
        opacity=0.6
    ))
    
    # px轨道
    fig.add_trace(go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=np.abs(psi_px.flatten()),
        isomin=0.05,
        isomax=0.3,
        surface_count=2,
        colorscale='Reds',
        name='px轨道',
        opacity=0.4,
        visible=False
    ))
    
    # 添加原子核
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers',
        marker=dict(size=10, color='black'),
        name='原子核'
    ))
    
    # 更新布局
    fig.update_layout(
        title='原子轨道可视化',
        scene=dict(
            xaxis_title='X (Bohr)',
            yaxis_title='Y (Bohr)',
            zaxis_title='Z (Bohr)',
            aspectmode='cube'
        ),
        width=800,
        height=600,
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(label="1s轨道",
                         method="update",
                         args=[{"visible": [True, False, True]}]),
                    dict(label="px轨道",
                         method="update",
                         args=[{"visible": [False, True, True]}]),
                    dict(label="全部显示",
                         method="update",
                         args=[{"visible": [True, True, True]}])
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.01,
                xanchor="left",
                y=1.02,
                yanchor="top"
            ),
        ]
    )
    
    return fig

# 生成并显示图形
fig = molecular_orbital_visualization()
fig.show()
'''
    
    def _generate_data_science_code(self) -> str:
        """生成数据科学可视化代码示例"""
        return '''
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA

def ml_visualization_dashboard():
    """机器学习可视化仪表板"""
    
    # 生成分类数据集
    X, y = make_classification(n_samples=500, n_features=10, n_classes=3, 
                              n_redundant=0, n_informative=3, random_state=42)
    
    # PCA降维
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X)
    
    # 创建子图
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('3D PCA可视化', '特征重要性', '类别分布', '决策边界'),
        specs=[[{"type": "scatter3d"}, {"type": "bar"}],
               [{"type": "pie"}, {"type": "scatter"}]]
    )
    
    # 3D PCA散点图
    colors = ['red', 'blue', 'green']
    for i in range(3):
        mask = y == i
        fig.add_trace(go.Scatter3d(
            x=X_pca[mask, 0],
            y=X_pca[mask, 1],
            z=X_pca[mask, 2],
            mode='markers',
            marker=dict(size=5, color=colors[i]),
            name=f'类别 {i}'
        ), row=1, col=1)
    
    # 特征重要性
    feature_importance = np.abs(pca.components_[0])
    fig.add_trace(go.Bar(
        x=[f'特征{i}' for i in range(len(feature_importance))],
        y=feature_importance,
        name='特征重要性'
    ), row=1, col=2)
    
    # 类别分布饼图
    unique, counts = np.unique(y, return_counts=True)
    fig.add_trace(go.Pie(
        labels=[f'类别{i}' for i in unique],
        values=counts,
        name='类别分布'
    ), row=2, col=1)
    
    # 2D决策边界（使用前两个主成分）
    for i in range(3):
        mask = y == i
        fig.add_trace(go.Scatter(
            x=X_pca[mask, 0],
            y=X_pca[mask, 1],
            mode='markers',
            marker=dict(color=colors[i]),
            name=f'2D类别{i}'
        ), row=2, col=2)
    
    # 更新布局
    fig.update_layout(
        title='机器学习数据可视化仪表板',
        height=800,
        showlegend=True
    )
    
    return fig

# 生成并显示图形
fig = ml_visualization_dashboard()
fig.show()
'''
    
    def _post_process_code(self, code: str, routing_result: Dict) -> Dict:
        """后处理生成的代码"""
        
        try:
            # 基本验证
            if not code or len(code.strip()) < 50:
                return {
                    "success": False,
                    "code": "# 生成的代码过短，请重新尝试",
                    "error": "代码长度不足"
                }
            
            # 检查必要的import语句
            required_imports = ["import", "plotly", "numpy"]
            has_imports = any(imp in code for imp in required_imports)
            
            if not has_imports:
                code = "import numpy as np\nimport plotly.graph_objects as go\n\n" + code
            
            # 添加执行说明
            code += "\n\n# 使用说明：\n# 1. 确保已安装必要的库：pip install plotly numpy scipy\n"
            code += "# 2. 运行代码后会显示交互式图表\n"
            code += "# 3. 可以通过鼠标进行缩放、旋转等操作\n"
            
            return {
                "success": True,
                "code": code,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "code": f"# 代码后处理失败: {str(e)}",
                "error": str(e)
            }
    
    def _generate_suggestions(self, routing_result: Dict) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        classification = routing_result["classification"]
        complexity = routing_result["complexity"]
        
        # 基于置信度的建议
        if classification["confidence"] < 0.5:
            suggestions.append("建议提供更具体的学科关键词以提高分类准确性")
        
        # 基于复杂度的建议
        if complexity["complexity_score"] < 2:
            suggestions.append("可以尝试添加更多参数和交互功能")
        elif complexity["complexity_score"] > 4:
            suggestions.append("建议分步骤实现，先完成基础功能")
        
        # 基于学科的建议
        discipline = classification["discipline"]
        if discipline == "Mathematics":
            suggestions.append("建议添加数学公式说明和理论背景")
        elif discipline == "Physics":
            suggestions.append("建议包含物理单位和实际参数值")
        elif discipline == "Biology":
            suggestions.append("建议添加生物学术语解释和功能说明")
        
        # 通用建议
        suggestions.extend([
            "可以尝试不同的颜色方案和视觉效果",
            "建议添加数据导出和保存功能",
            "考虑添加动画效果增强可视化体验"
        ])
        
        return suggestions[:5]  # 限制建议数量
    
    def get_generation_history(self, limit: int = 10) -> List[Dict]:
        """获取生成历史记录"""
        return self.generation_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """获取生成统计信息"""
        if not self.generation_history:
            return {"total_generations": 0}
        
        total = len(self.generation_history)
        successful = sum(1 for record in self.generation_history if record["success"])
        
        # 学科分布统计
        discipline_counts = {}
        for record in self.generation_history:
            discipline = record.get("discipline", "Unknown")
            discipline_counts[discipline] = discipline_counts.get(discipline, 0) + 1
        
        return {
            "total_generations": total,
            "successful_generations": successful,
            "success_rate": successful / total if total > 0 else 0,
            "discipline_distribution": discipline_counts,
            "average_code_length": np.mean([r["code_length"] for r in self.generation_history])
        }

# 全局代码生成器实例
code_generator = AICodeGenerator()

def generate_code(user_input: str, **kwargs) -> Dict:
    """便捷函数：生成可视化代码"""
    return code_generator.generate_visualization_code(user_input, **kwargs)
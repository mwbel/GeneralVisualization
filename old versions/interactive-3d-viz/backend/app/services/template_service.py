"""
Template management service for code generation
"""
import json
from typing import List, Dict, Any, Optional
from enum import Enum
import json
import time
from functools import lru_cache
from dataclasses import dataclass
from ..models.visualization import VisualizationType


class TemplateCategory(Enum):
    """Template categories"""
    BASIC = "basic"
    SCIENTIFIC = "scientific"
    BUSINESS = "business"
    STATISTICAL = "statistical"
    MACHINE_LEARNING = "machine_learning"
    GEOSPATIAL = "geospatial"
    FINANCIAL = "financial"
    EDUCATIONAL = "educational"


class TemplateDifficulty(Enum):
    """Template difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class TemplateMetadata:
    """Template metadata"""
    id: str
    name: str
    description: str
    category: TemplateCategory
    difficulty: TemplateDifficulty
    tags: List[str]
    author: str
    version: str
    created_at: str
    updated_at: str
    usage_count: int = 0
    rating: float = 0.0


@dataclass
class CodeTemplate:
    """Code template structure"""
    metadata: TemplateMetadata
    code: str
    explanation: str
    dependencies: List[str]
    parameters: Dict[str, Any]
    examples: List[Dict[str, Any]]
    visualization_type: VisualizationType


class TemplateService:
    """Template management service"""
    
    def __init__(self):
        self.templates: Dict[str, CodeTemplate] = {}
        self._cache = {}
        self._cache_timeout = 300  # 5分钟缓存
        self._load_default_templates()
    
    def _get_cache_key(self, method_name: str, **kwargs) -> str:
        """生成缓存键"""
        key_parts = [method_name]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        return "|".join(key_parts)
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """从缓存获取数据"""
        if cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_timeout:
                return data
            else:
                del self._cache[cache_key]
        return None
    
    def _set_cache(self, cache_key: str, data: Any) -> None:
        """设置缓存数据"""
        self._cache[cache_key] = (data, time.time())
    
    def _load_default_templates(self):
        """Load default templates"""
        
        # 基础3D散点图模板
        self.templates["basic_scatter_3d"] = CodeTemplate(
            metadata=TemplateMetadata(
                id="basic_scatter_3d",
                name="基础3D散点图",
                description="创建简单的3D散点图，适合展示三维数据点的分布",
                category=TemplateCategory.BASIC,
                difficulty=TemplateDifficulty.BEGINNER,
                tags=["3d", "scatter", "plotly", "basic"],
                author="System",
                version="1.0.0",
                created_at="2024-01-01",
                updated_at="2024-01-01"
            ),
            code='''
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 生成示例数据
n_points = {n_points}
x = np.random.randn(n_points)
y = np.random.randn(n_points)
z = np.random.randn(n_points)
colors = np.random.randn(n_points)

# 创建3D散点图
fig = go.Figure(data=go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size={marker_size},
        color=colors,
        colorscale='{colorscale}',
        opacity={opacity},
        showscale=True
    ),
    text=[f'Point {{i}}' for i in range(n_points)],
    hovertemplate='<b>%{{text}}</b><br>X: %{{x}}<br>Y: %{{y}}<br>Z: %{{z}}<extra></extra>'
))

# 更新布局
fig.update_layout(
    title='{title}',
    scene=dict(
        xaxis_title='{x_label}',
        yaxis_title='{y_label}',
        zaxis_title='{z_label}',
        camera=dict(
            eye=dict(x=1.2, y=1.2, z=1.2)
        )
    ),
    width={width},
    height={height}
)

# 显示图表
fig.show()
''',
            explanation="这是一个基础的3D散点图模板，可以展示三维空间中的数据点分布。支持自定义颜色映射、点大小和透明度。",
            dependencies=["plotly", "numpy", "pandas"],
            parameters={
                "n_points": {"type": "int", "default": 100, "min": 10, "max": 10000},
                "marker_size": {"type": "int", "default": 5, "min": 1, "max": 20},
                "colorscale": {"type": "str", "default": "viridis", "options": ["viridis", "plasma", "inferno", "magma", "cividis"]},
                "opacity": {"type": "float", "default": 0.8, "min": 0.1, "max": 1.0},
                "title": {"type": "str", "default": "3D散点图"},
                "x_label": {"type": "str", "default": "X轴"},
                "y_label": {"type": "str", "default": "Y轴"},
                "z_label": {"type": "str", "default": "Z轴"},
                "width": {"type": "int", "default": 800, "min": 400, "max": 1600},
                "height": {"type": "int", "default": 600, "min": 300, "max": 1200}
            },
            examples=[
                {
                    "name": "随机数据散点图",
                    "description": "使用随机生成的数据创建3D散点图",
                    "parameters": {"n_points": 200, "colorscale": "plasma"}
                }
            ],
            visualization_type=VisualizationType.SCATTER_3D
        )
        
        # 高级3D曲面图模板
        self.templates["advanced_surface_3d"] = CodeTemplate(
            metadata=TemplateMetadata(
                id="advanced_surface_3d",
                name="高级3D曲面图",
                description="创建复杂的3D曲面图，支持多种数学函数和自定义着色",
                category=TemplateCategory.SCIENTIFIC,
                difficulty=TemplateDifficulty.INTERMEDIATE,
                tags=["3d", "surface", "mathematical", "scientific"],
                author="System",
                version="1.0.0",
                created_at="2024-01-01",
                updated_at="2024-01-01"
            ),
            code='''
import plotly.graph_objects as go
import numpy as np

# 定义网格
x = np.linspace({x_min}, {x_max}, {grid_size})
y = np.linspace({y_min}, {y_max}, {grid_size})
X, Y = np.meshgrid(x, y)

# 计算Z值 - 可以选择不同的函数
if '{function_type}' == 'sincos':
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.cos(X * Y)
elif '{function_type}' == 'gaussian':
    Z = np.exp(-(X**2 + Y**2) / {sigma})
elif '{function_type}' == 'ripple':
    Z = np.sin(X) * np.cos(Y) * np.exp(-0.1 * (X**2 + Y**2))
elif '{function_type}' == 'saddle':
    Z = X**2 - Y**2
else:
    Z = np.sin(np.sqrt(X**2 + Y**2))

# 创建3D曲面图
fig = go.Figure(data=go.Surface(
    x=X,
    y=Y,
    z=Z,
    colorscale='{colorscale}',
    showscale=True,
    opacity={opacity},
    contours=dict(
        x=dict(show={show_contours}, color="white", width=2),
        y=dict(show={show_contours}, color="white", width=2),
        z=dict(show={show_contours}, color="white", width=2)
    )
))

# 更新布局
fig.update_layout(
    title='{title}',
    scene=dict(
        xaxis_title='{x_label}',
        yaxis_title='{y_label}',
        zaxis_title='{z_label}',
        camera=dict(
            eye=dict(x={camera_x}, y={camera_y}, z={camera_z})
        ),
        aspectmode='cube'
    ),
    width={width},
    height={height}
)

# 显示图表
fig.show()
''',
            explanation="高级3D曲面图模板，支持多种数学函数（正弦余弦、高斯、波纹、马鞍面等），可以自定义网格密度、颜色映射和等高线显示。",
            dependencies=["plotly", "numpy"],
            parameters={
                "x_min": {"type": "float", "default": -5.0},
                "x_max": {"type": "float", "default": 5.0},
                "y_min": {"type": "float", "default": -5.0},
                "y_max": {"type": "float", "default": 5.0},
                "grid_size": {"type": "int", "default": 50, "min": 20, "max": 200},
                "function_type": {"type": "str", "default": "sincos", "options": ["sincos", "gaussian", "ripple", "saddle"]},
                "sigma": {"type": "float", "default": 2.0, "min": 0.5, "max": 10.0},
                "colorscale": {"type": "str", "default": "viridis", "options": ["viridis", "plasma", "inferno", "magma", "RdYlBu"]},
                "opacity": {"type": "float", "default": 0.9, "min": 0.1, "max": 1.0},
                "show_contours": {"type": "bool", "default": False},
                "title": {"type": "str", "default": "3D曲面图"},
                "x_label": {"type": "str", "default": "X轴"},
                "y_label": {"type": "str", "default": "Y轴"},
                "z_label": {"type": "str", "default": "Z轴"},
                "camera_x": {"type": "float", "default": 1.2},
                "camera_y": {"type": "float", "default": 1.2},
                "camera_z": {"type": "float", "default": 1.2},
                "width": {"type": "int", "default": 800},
                "height": {"type": "int", "default": 600}
            },
            examples=[
                {
                    "name": "高斯函数曲面",
                    "description": "展示高斯函数的3D曲面",
                    "parameters": {"function_type": "gaussian", "sigma": 3.0}
                },
                {
                    "name": "波纹效果曲面",
                    "description": "创建波纹效果的3D曲面",
                    "parameters": {"function_type": "ripple", "show_contours": True}
                }
            ],
            visualization_type=VisualizationType.SURFACE_3D
        )
        
        # 商业数据3D柱状图模板
        self.templates["business_bar_3d"] = CodeTemplate(
            metadata=TemplateMetadata(
                id="business_bar_3d",
                name="商业数据3D柱状图",
                description="专为商业数据设计的3D柱状图，支持多维度数据展示",
                category=TemplateCategory.BUSINESS,
                difficulty=TemplateDifficulty.INTERMEDIATE,
                tags=["3d", "bar", "business", "analytics"],
                author="System",
                version="1.0.0",
                created_at="2024-01-01",
                updated_at="2024-01-01"
            ),
            code='''
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 生成商业数据示例
categories = {categories}
regions = {regions}
months = {months}

# 创建数据
np.random.seed(42)
data = []
for month in months:
    for region in regions:
        for category in categories:
            value = np.random.randint({min_value}, {max_value})
            data.append({{
                'month': month,
                'region': region,
                'category': category,
                'value': value
            }})

df = pd.DataFrame(data)

# 创建3D柱状图
fig = go.Figure()

colors = ['{color1}', '{color2}', '{color3}', '{color4}']
for i, category in enumerate(categories):
    category_data = df[df['category'] == category]
    
    fig.add_trace(go.Scatter3d(
        x=category_data['month'],
        y=category_data['region'],
        z=category_data['value'],
        mode='markers',
        marker=dict(
            size=category_data['value'] / {size_scale},
            color=colors[i % len(colors)],
            opacity={opacity},
            symbol='square'
        ),
        name=category,
        text=[f'{{cat}}<br>{{reg}}<br>{{mon}}<br>值: {{val}}' 
              for cat, reg, mon, val in zip(
                  category_data['category'],
                  category_data['region'],
                  category_data['month'],
                  category_data['value']
              )],
        hovertemplate='%{{text}}<extra></extra>'
    ))

# 更新布局
fig.update_layout(
    title='{title}',
    scene=dict(
        xaxis_title='{x_label}',
        yaxis_title='{y_label}',
        zaxis_title='{z_label}',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    ),
    width={width},
    height={height},
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor='rgba(255,255,255,0.8)'
    )
)

# 显示图表
fig.show()
''',
            explanation="专为商业数据分析设计的3D柱状图模板，可以同时展示多个维度的数据（如时间、地区、产品类别等）。",
            dependencies=["plotly", "numpy", "pandas"],
            parameters={
                "categories": {"type": "list", "default": ["产品A", "产品B", "产品C", "产品D"]},
                "regions": {"type": "list", "default": ["北区", "南区", "东区", "西区"]},
                "months": {"type": "list", "default": ["1月", "2月", "3月", "4月", "5月", "6月"]},
                "min_value": {"type": "int", "default": 10, "min": 1},
                "max_value": {"type": "int", "default": 100, "min": 10},
                "size_scale": {"type": "float", "default": 5.0, "min": 1.0, "max": 20.0},
                "opacity": {"type": "float", "default": 0.8, "min": 0.1, "max": 1.0},
                "color1": {"type": "str", "default": "red"},
                "color2": {"type": "str", "default": "blue"},
                "color3": {"type": "str", "default": "green"},
                "color4": {"type": "str", "default": "orange"},
                "title": {"type": "str", "default": "商业数据3D分析"},
                "x_label": {"type": "str", "default": "月份"},
                "y_label": {"type": "str", "default": "地区"},
                "z_label": {"type": "str", "default": "销售额"},
                "width": {"type": "int", "default": 900},
                "height": {"type": "int", "default": 700}
            },
            examples=[
                {
                    "name": "季度销售分析",
                    "description": "分析不同产品在各地区的季度销售情况",
                    "parameters": {"months": ["Q1", "Q2", "Q3", "Q4"]}
                }
            ],
            visualization_type=VisualizationType.BAR_3D
        )
        
        # 机器学习聚类可视化模板
        self.templates["ml_clustering_3d"] = CodeTemplate(
            metadata=TemplateMetadata(
                id="ml_clustering_3d",
                name="机器学习聚类3D可视化",
                description="使用机器学习算法进行数据聚类并在3D空间中可视化结果",
                category=TemplateCategory.MACHINE_LEARNING,
                difficulty=TemplateDifficulty.ADVANCED,
                tags=["3d", "clustering", "machine-learning", "sklearn"],
                author="System",
                version="1.0.0",
                created_at="2024-01-01",
                updated_at="2024-01-01"
            ),
            code='''
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler

# 生成示例数据
n_samples = {n_samples}
n_features = 3
n_clusters = {n_clusters}
random_state = {random_state}

X, y_true = make_blobs(
    n_samples=n_samples,
    centers=n_clusters,
    n_features=n_features,
    random_state=random_state,
    cluster_std={cluster_std}
)

# 数据标准化
if {standardize}:
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
else:
    X_scaled = X

# 执行K-means聚类
kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
y_pred = kmeans.fit_predict(X_scaled)

# 获取聚类中心
centers = kmeans.cluster_centers_
if {standardize}:
    centers = scaler.inverse_transform(centers)

# 创建颜色映射
colors = ['{color1}', '{color2}', '{color3}', '{color4}', '{color5}', '{color6}']

# 创建3D散点图
fig = go.Figure()

# 添加数据点
for i in range(n_clusters):
    cluster_points = X[y_pred == i]
    fig.add_trace(go.Scatter3d(
        x=cluster_points[:, 0],
        y=cluster_points[:, 1],
        z=cluster_points[:, 2],
        mode='markers',
        marker=dict(
            size={point_size},
            color=colors[i % len(colors)],
            opacity={point_opacity}
        ),
        name=f'聚类 {{i+1}}',
        text=[f'聚类 {{i+1}}<br>点 {{j}}' for j in range(len(cluster_points))],
        hovertemplate='%{{text}}<br>X: %{{x:.2f}}<br>Y: %{{y:.2f}}<br>Z: %{{z:.2f}}<extra></extra>'
    ))

# 添加聚类中心
if {show_centers}:
    fig.add_trace(go.Scatter3d(
        x=centers[:, 0],
        y=centers[:, 1],
        z=centers[:, 2],
        mode='markers',
        marker=dict(
            size={center_size},
            color='black',
            symbol='diamond',
            opacity=1.0
        ),
        name='聚类中心',
        text=[f'中心 {{i+1}}' for i in range(n_clusters)],
        hovertemplate='%{{text}}<br>X: %{{x:.2f}}<br>Y: %{{y:.2f}}<br>Z: %{{z:.2f}}<extra></extra>'
    ))

# 更新布局
fig.update_layout(
    title='{title}',
    scene=dict(
        xaxis_title='{x_label}',
        yaxis_title='{y_label}',
        zaxis_title='{z_label}',
        camera=dict(
            eye=dict(x=1.2, y=1.2, z=1.2)
        )
    ),
    width={width},
    height={height}
)

# 显示图表
fig.show()

# 打印聚类结果统计
print(f"聚类完成！")
print(f"数据点总数: {{n_samples}}")
print(f"聚类数量: {{n_clusters}}")
for i in range(n_clusters):
    count = np.sum(y_pred == i)
    print(f"聚类 {{i+1}}: {{count}} 个点")
''',
            explanation="机器学习聚类3D可视化模板，使用K-means算法对3D数据进行聚类分析，并可视化聚类结果和聚类中心。",
            dependencies=["plotly", "numpy", "pandas", "scikit-learn"],
            parameters={
                "n_samples": {"type": "int", "default": 300, "min": 50, "max": 2000},
                "n_clusters": {"type": "int", "default": 4, "min": 2, "max": 10},
                "random_state": {"type": "int", "default": 42},
                "cluster_std": {"type": "float", "default": 1.5, "min": 0.5, "max": 5.0},
                "standardize": {"type": "bool", "default": True},
                "show_centers": {"type": "bool", "default": True},
                "point_size": {"type": "int", "default": 6, "min": 2, "max": 15},
                "center_size": {"type": "int", "default": 15, "min": 10, "max": 30},
                "point_opacity": {"type": "float", "default": 0.7, "min": 0.1, "max": 1.0},
                "color1": {"type": "str", "default": "red"},
                "color2": {"type": "str", "default": "blue"},
                "color3": {"type": "str", "default": "green"},
                "color4": {"type": "str", "default": "orange"},
                "color5": {"type": "str", "default": "purple"},
                "color6": {"type": "str", "default": "brown"},
                "title": {"type": "str", "default": "K-means聚类3D可视化"},
                "x_label": {"type": "str", "default": "特征1"},
                "y_label": {"type": "str", "default": "特征2"},
                "z_label": {"type": "str", "default": "特征3"},
                "width": {"type": "int", "default": 900},
                "height": {"type": "int", "default": 700}
            },
            examples=[
                {
                    "name": "客户分群分析",
                    "description": "对客户数据进行聚类分析",
                    "parameters": {"n_clusters": 3, "n_samples": 500}
                }
            ],
            visualization_type=VisualizationType.SCATTER_3D
        )
        
        # 地理空间3D可视化模板
        self.templates["geospatial_3d"] = CodeTemplate(
            metadata=TemplateMetadata(
                id="geospatial_3d",
                name="地理空间3D可视化",
                description="创建地理空间数据的3D可视化，支持地形、人口、经济等数据展示",
                category=TemplateCategory.GEOSPATIAL,
                difficulty=TemplateDifficulty.ADVANCED,
                tags=["3d", "geospatial", "geography", "terrain"],
                author="System",
                version="1.0.0",
                created_at="2024-01-01",
                updated_at="2024-01-01"
            ),
            code='''
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# 生成地理空间数据示例
# 创建经纬度网格
lat_min, lat_max = {lat_min}, {lat_max}
lon_min, lon_max = {lon_min}, {lon_max}
grid_size = {grid_size}

lat = np.linspace(lat_min, lat_max, grid_size)
lon = np.linspace(lon_min, lon_max, grid_size)
LON, LAT = np.meshgrid(lon, lat)

# 生成高程数据（模拟地形）
np.random.seed({random_seed})
if '{terrain_type}' == 'mountain':
    # 山地地形
    elevation = 1000 * np.exp(-((LON - (lon_min + lon_max)/2)**2 + (LAT - (lat_min + lat_max)/2)**2) / {terrain_scale})
    elevation += 200 * np.random.randn(grid_size, grid_size)
elif '{terrain_type}' == 'valley':
    # 山谷地形
    elevation = -500 * np.exp(-((LON - (lon_min + lon_max)/2)**2 + (LAT - (lat_min + lat_max)/2)**2) / {terrain_scale})
    elevation += 100 * np.random.randn(grid_size, grid_size)
elif '{terrain_type}' == 'plateau':
    # 高原地形
    elevation = 800 + 200 * np.sin(LON * 2) * np.cos(LAT * 2)
    elevation += 150 * np.random.randn(grid_size, grid_size)
else:
    # 随机地形
    elevation = 500 * np.random.randn(grid_size, grid_size)

# 确保高程为正值
elevation = np.maximum(elevation, 0)

# 生成人口密度数据（可选）
if {show_population}:
    population = np.random.exponential(scale=100, size=(grid_size, grid_size))
    population = population * (elevation > 200)  # 高海拔地区人口较少

# 创建3D地形图
fig = go.Figure()

# 添加地形表面
fig.add_trace(go.Surface(
    x=LON,
    y=LAT,
    z=elevation,
    colorscale='{terrain_colorscale}',
    showscale=True,
    name='地形',
    hovertemplate='经度: %{{x:.2f}}<br>纬度: %{{y:.2f}}<br>海拔: %{{z:.0f}}m<extra></extra>'
))

# 添加人口密度数据点（如果启用）
if {show_population}:
    # 选择一些采样点显示人口密度
    sample_indices = np.random.choice(grid_size*grid_size, size={population_samples}, replace=False)
    sample_lon = LON.flatten()[sample_indices]
    sample_lat = LAT.flatten()[sample_indices]
    sample_elevation = elevation.flatten()[sample_indices]
    sample_population = population.flatten()[sample_indices]
    
    fig.add_trace(go.Scatter3d(
        x=sample_lon,
        y=sample_lat,
        z=sample_elevation + 50,  # 稍微抬高显示
        mode='markers',
        marker=dict(
            size=sample_population / {population_scale},
            color=sample_population,
            colorscale='{population_colorscale}',
            opacity={population_opacity},
            showscale=True,
            colorbar=dict(
                title="人口密度",
                x=1.1
            )
        ),
        name='人口密度',
        text=[f'人口: {{pop:.0f}}' for pop in sample_population],
        hovertemplate='%{{text}}<br>经度: %{{x:.2f}}<br>纬度: %{{y:.2f}}<br>海拔: %{{z:.0f}}m<extra></extra>'
    ))

# 更新布局
fig.update_layout(
    title='{title}',
    scene=dict(
        xaxis_title='经度',
        yaxis_title='纬度',
        zaxis_title='海拔 (m)',
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.2)
        ),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=0.5)
    ),
    width={width},
    height={height}
)

# 显示图表
fig.show()

# 打印统计信息
print(f"地理区域统计:")
print(f"经度范围: {{lon_min:.2f}} - {{lon_max:.2f}}")
print(f"纬度范围: {{lat_min:.2f}} - {{lat_max:.2f}}")
print(f"最高海拔: {{np.max(elevation):.0f}}m")
print(f"最低海拔: {{np.min(elevation):.0f}}m")
print(f"平均海拔: {{np.mean(elevation):.0f}}m")
''',
            explanation="地理空间3D可视化模板，可以创建地形图、人口分布图等地理空间数据的3D展示。支持多种地形类型和人口密度叠加显示。",
            dependencies=["plotly", "numpy", "pandas"],
            parameters={
                "lat_min": {"type": "float", "default": 30.0},
                "lat_max": {"type": "float", "default": 40.0},
                "lon_min": {"type": "float", "default": 100.0},
                "lon_max": {"type": "float", "default": 120.0},
                "grid_size": {"type": "int", "default": 50, "min": 20, "max": 100},
                "random_seed": {"type": "int", "default": 42},
                "terrain_type": {"type": "str", "default": "mountain", "options": ["mountain", "valley", "plateau", "random"]},
                "terrain_scale": {"type": "float", "default": 2.0, "min": 0.5, "max": 10.0},
                "terrain_colorscale": {"type": "str", "default": "terrain", "options": ["terrain", "earth", "viridis", "plasma"]},
                "show_population": {"type": "bool", "default": True},
                "population_samples": {"type": "int", "default": 200, "min": 50, "max": 1000},
                "population_scale": {"type": "float", "default": 20.0, "min": 5.0, "max": 100.0},
                "population_colorscale": {"type": "str", "default": "reds", "options": ["reds", "blues", "oranges", "viridis"]},
                "population_opacity": {"type": "float", "default": 0.8, "min": 0.1, "max": 1.0},
                "title": {"type": "str", "default": "地理空间3D可视化"},
                "width": {"type": "int", "default": 1000},
                "height": {"type": "int", "default": 800}
            },
            examples=[
                {
                    "name": "中国地形图",
                    "description": "展示中国某地区的地形和人口分布",
                    "parameters": {"lat_min": 35.0, "lat_max": 45.0, "lon_min": 110.0, "lon_max": 125.0}
                }
            ],
            visualization_type=VisualizationType.SURFACE_3D
        )
    
    def get_all_templates(self) -> List[CodeTemplate]:
        """Get all available templates"""
        return list(self.templates.values())
    
    def get_template_by_id(self, template_id: str) -> Optional[CodeTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: TemplateCategory) -> List[CodeTemplate]:
        """Get templates by category"""
        return [template for template in self.templates.values() 
                if template.metadata.category == category]
    
    def get_templates_by_difficulty(self, difficulty: TemplateDifficulty) -> List[CodeTemplate]:
        """Get templates by difficulty"""
        return [template for template in self.templates.values() 
                if template.metadata.difficulty == difficulty]
    
    def get_templates_by_tags(self, tags: List[str]) -> List[CodeTemplate]:
        """Get templates by tags"""
        result = []
        for template in self.templates.values():
            if any(tag in template.metadata.tags for tag in tags):
                result.append(template)
        return result
    
    def search_templates_old(self, query: str) -> List[CodeTemplate]:
        """Search templates by name, description, or tags"""
        # 检查缓存
        cache_key = self._get_cache_key("search_templates", query=query)
        cached_result = self._get_from_cache(cache_key)
        if cached_result is not None:
            return cached_result
        
        query = query.lower()
        result = []
        for template in self.templates.values():
            if (query in template.metadata.name.lower() or 
                query in template.metadata.description.lower() or
                any(query in tag.lower() for tag in template.metadata.tags)):
                result.append(template)
        
        # 缓存结果
        self._set_cache(cache_key, result)
        return result
    
    def customize_template(self, template_id: str, parameters: Dict[str, Any]) -> str:
        """Customize template with given parameters"""
        template = self.get_template_by_id(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        code = template.code
        for param_name, param_value in parameters.items():
            if param_name in template.parameters:
                # 根据参数类型进行格式化
                param_config = template.parameters[param_name]
                if param_config["type"] == "str":
                    formatted_value = f"'{param_value}'"
                elif param_config["type"] == "list":
                    formatted_value = str(param_value)
                else:
                    formatted_value = str(param_value)
                
                code = code.replace(f"{{{param_name}}}", formatted_value)
        
        return code
    
    def get_template_metadata_list(self) -> List[Dict[str, Any]]:
        """Get list of template metadata for API responses"""
        result = []
        for template in self.templates.values():
            result.append({
                "id": template.metadata.id,
                "name": template.metadata.name,
                "description": template.metadata.description,
                "category": template.metadata.category.value,
                "difficulty": template.metadata.difficulty.value,
                "tags": template.metadata.tags,
                "author": template.metadata.author,
                "version": template.metadata.version,
                "dependencies": template.dependencies,
                "visualization_type": template.visualization_type.value,
                "parameters": template.parameters,
                "examples": template.examples
            })
        return result
    
    def get_categories(self) -> List[str]:
        """Get list of available template categories"""
        categories = set()
        for template in self.templates.values():
            categories.add(template.metadata.category.value)
        return sorted(list(categories))
    
    def get_templates_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get templates filtered by category"""
        filtered_templates = []
        for template in self.templates.values():
            if template.metadata.category.value.lower() == category.lower():
                filtered_templates.append({
                    'id': template.metadata.id,
                    'name': template.metadata.name,
                    'description': template.metadata.description,
                    'category': template.metadata.category.value,
                    'difficulty': template.metadata.difficulty.value,
                    'tags': template.metadata.tags,
                    'dependencies': template.dependencies,
                    'visualization_type': template.visualization_type.value
                })
        return filtered_templates
    
    def search_templates(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        page: int = 1,
        page_size: int = 12
    ) -> Dict[str, Any]:
        """搜索模板，支持分页"""
        # 检查缓存（不包含分页参数）
        cache_key = self._get_cache_key("search_templates", 
                                       query=query or "", 
                                       category=category or "", 
                                       difficulty=difficulty or "")
        cached_result = self._get_from_cache(cache_key)
        
        if cached_result is None:
            results = []
            
            for template in self.templates.values():
                # 检查查询条件
                if query:
                    query_lower = query.lower()
                    if not (query_lower in template.metadata.name.lower() or
                           query_lower in template.metadata.description.lower() or
                           any(query_lower in tag.lower() for tag in template.metadata.tags)):
                        continue
                
                # 检查分类
                if category and template.metadata.category.value.lower() != category.lower():
                    continue
                
                # 检查难度
                if difficulty and template.metadata.difficulty.value.lower() != difficulty.lower():
                    continue
                
                results.append({
                    "id": template.metadata.id,
                    "name": template.metadata.name,
                    "description": template.metadata.description,
                    "category": template.metadata.category.value,
                    "difficulty": template.metadata.difficulty.value,
                    "tags": template.metadata.tags,
                    "dependencies": template.dependencies,
                    "visualization_type": template.visualization_type.value
                })
            
            # 缓存结果
            self._set_cache(cache_key, results)
        else:
            results = cached_result
        
        # 应用分页
        total_count = len(results)
        total_pages = (total_count + page_size - 1) // page_size
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_results = results[start_index:end_index]
        
        return {
            "templates": paginated_results,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }

 
# 全局模板服务实例
template_service = TemplateService()
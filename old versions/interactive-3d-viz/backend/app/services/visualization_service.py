import uuid
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..models.visualization import (
    VisualizationRequest,
    VisualizationResponse,
    VisualizationType,
    DataFormat,
    VisualizationExample,
    HTMLGenerationRequest,
    HTMLGenerationResponse
)

class VisualizationService:
    """Service for handling 3D visualization generation"""
    
    def __init__(self):
        self.examples = self._load_examples()
    
    async def generate_visualization(self, request: VisualizationRequest) -> VisualizationResponse:
        """Generate a 3D visualization based on the request"""
        try:
            # Generate unique ID
            viz_id = str(uuid.uuid4())
            
            # Process data based on format
            processed_data = self._process_data(request.data, request.data_format)
            
            # Generate Python code based on visualization type
            python_code = self._generate_python_code(
                request.visualization_type,
                processed_data,
                request.parameters,
                request.style_options
            )
            
            # Generate HTML output (for preview)
            html_output = self._generate_html_output(
                request.visualization_type,
                processed_data,
                request.parameters,
                request.style_options
            )
            
            return VisualizationResponse(
                id=viz_id,
                title=request.title,
                description=request.description,
                visualization_type=request.visualization_type,
                python_code=python_code,
                html_output=html_output,
                preview_url=f"/api/v1/visualization/{viz_id}/preview",
                download_url=f"/api/v1/visualization/{viz_id}/download",
                created_at=datetime.now(),
                status="completed"
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate visualization: {str(e)}")
    
    def _process_data(self, data: Dict[str, Any], data_format: DataFormat) -> Dict[str, Any]:
        """Process input data based on format"""
        if data_format == DataFormat.JSON:
            return data
        elif data_format == DataFormat.CSV:
            # Convert CSV string to DataFrame
            if isinstance(data.get('csv_data'), str):
                df = pd.read_csv(data['csv_data'])
                return df.to_dict('records')
        elif data_format == DataFormat.NUMPY:
            # Handle numpy arrays
            processed = {}
            for key, value in data.items():
                if isinstance(value, list):
                    processed[key] = np.array(value)
                else:
                    processed[key] = value
            return processed
        
        return data
    
    def _generate_python_code(
        self,
        viz_type: VisualizationType,
        data: Dict[str, Any],
        parameters: Dict[str, Any],
        style_options: Dict[str, Any]
    ) -> str:
        """Generate Python code for the visualization"""
        
        if viz_type == VisualizationType.SCATTER_3D:
            return self._generate_scatter_3d_code(data, parameters, style_options)
        elif viz_type == VisualizationType.SURFACE_3D:
            return self._generate_surface_3d_code(data, parameters, style_options)
        elif viz_type == VisualizationType.MESH_3D:
            return self._generate_mesh_3d_code(data, parameters, style_options)
        elif viz_type == VisualizationType.VOLUME_3D:
            return self._generate_volume_3d_code(data, parameters, style_options)
        elif viz_type == VisualizationType.NETWORK_3D:
            return self._generate_network_3d_code(data, parameters, style_options)
        elif viz_type == VisualizationType.MOLECULAR:
            return self._generate_molecular_code(data, parameters, style_options)
        else:
            return self._generate_custom_code(data, parameters, style_options)
    
    def _generate_scatter_3d_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for 3D scatter plot"""
        return f'''
import plotly.graph_objects as go
import numpy as np

# Sample data (replace with your actual data)
x = {data.get('x', list(np.random.randn(100)))}
y = {data.get('y', list(np.random.randn(100)))}
z = {data.get('z', list(np.random.randn(100)))}

# Create 3D scatter plot
fig = go.Figure(data=go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size={style_options.get('marker_size', 5)},
        color={style_options.get('color_scale', 'viridis')},
        colorscale='{style_options.get('colorscale', 'viridis')}',
        opacity={style_options.get('opacity', 0.8)}
    )
))

# Update layout
fig.update_layout(
    title='{parameters.get('title', '3D Scatter Plot')}',
    scene=dict(
        xaxis_title='{parameters.get('x_label', 'X Axis')}',
        yaxis_title='{parameters.get('y_label', 'Y Axis')}',
        zaxis_title='{parameters.get('z_label', 'Z Axis')}'
    ),
    width={parameters.get('width', 800)},
    height={parameters.get('height', 600)}
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("3d_scatter_plot.html")
'''
    
    def _generate_surface_3d_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for 3D surface plot"""
        return f'''
import plotly.graph_objects as go
import numpy as np

# Generate sample data (replace with your actual data)
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create 3D surface plot
fig = go.Figure(data=go.Surface(
    x=X,
    y=Y,
    z=Z,
    colorscale='{style_options.get('colorscale', 'viridis')}',
    opacity={style_options.get('opacity', 1.0)}
))

# Update layout
fig.update_layout(
    title='{parameters.get('title', '3D Surface Plot')}',
    scene=dict(
        xaxis_title='{parameters.get('x_label', 'X Axis')}',
        yaxis_title='{parameters.get('y_label', 'Y Axis')}',
        zaxis_title='{parameters.get('z_label', 'Z Axis')}'
    ),
    width={parameters.get('width', 800)},
    height={parameters.get('height', 600)}
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("3d_surface_plot.html")
'''
    
    def _generate_mesh_3d_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for 3D mesh plot"""
        return '''
import plotly.graph_objects as go
import numpy as np

# Generate sample mesh data
u = np.linspace(0, 2 * np.pi, 50)
v = np.linspace(0, np.pi, 50)
u, v = np.meshgrid(u, v)

x = np.cos(u) * np.sin(v)
y = np.sin(u) * np.sin(v)
z = np.cos(v)

# Create 3D mesh plot
fig = go.Figure(data=go.Mesh3d(
    x=x.flatten(),
    y=y.flatten(),
    z=z.flatten(),
    opacity=0.7,
    color='lightblue'
))

# Update layout
fig.update_layout(
    title='3D Mesh Plot',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    width=800,
    height=600
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("3d_mesh_plot.html")
'''
    
    def _generate_volume_3d_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for 3D volume plot"""
        return '''
import plotly.graph_objects as go
import numpy as np

# Generate sample volume data
X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
values = np.sin(X*Y*Z) / (X*Y*Z)

# Create 3D volume plot
fig = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    isomin=0.1,
    isomax=0.8,
    opacity=0.1,
    surface_count=17,
))

# Update layout
fig.update_layout(
    title='3D Volume Plot',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    width=800,
    height=600
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("3d_volume_plot.html")
'''
    
    def _generate_network_3d_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for 3D network plot"""
        return '''
import plotly.graph_objects as go
import numpy as np
import networkx as nx

# Create a sample network
G = nx.random_geometric_graph(50, 0.3, dim=3)
pos = nx.get_node_attributes(G, 'pos')

# Extract node and edge coordinates
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]
node_z = [pos[node][2] for node in G.nodes()]

edge_x = []
edge_y = []
edge_z = []

for edge in G.edges():
    x0, y0, z0 = pos[edge[0]]
    x1, y1, z1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])
    edge_z.extend([z0, z1, None])

# Create 3D network plot
fig = go.Figure(data=[
    go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='gray', width=2),
        name='Edges'
    ),
    go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(size=8, color='red'),
        name='Nodes'
    )
])

# Update layout
fig.update_layout(
    title='3D Network Graph',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    width=800,
    height=600
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("3d_network_plot.html")
'''
    
    def _generate_molecular_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate code for molecular visualization"""
        return '''
import plotly.graph_objects as go
import numpy as np

# Sample molecular data (water molecule)
atoms = [
    {'element': 'O', 'x': 0, 'y': 0, 'z': 0, 'color': 'red', 'size': 20},
    {'element': 'H', 'x': 0.96, 'y': 0, 'z': 0, 'color': 'white', 'size': 10},
    {'element': 'H', 'x': -0.24, 'y': 0.93, 'z': 0, 'color': 'white', 'size': 10}
]

bonds = [
    {'from': 0, 'to': 1},
    {'from': 0, 'to': 2}
]

# Create molecular visualization
fig = go.Figure()

# Add atoms
for atom in atoms:
    fig.add_trace(go.Scatter3d(
        x=[atom['x']],
        y=[atom['y']],
        z=[atom['z']],
        mode='markers',
        marker=dict(
            size=atom['size'],
            color=atom['color']
        ),
        name=atom['element'],
        showlegend=False
    ))

# Add bonds
for bond in bonds:
    atom1 = atoms[bond['from']]
    atom2 = atoms[bond['to']]
    fig.add_trace(go.Scatter3d(
        x=[atom1['x'], atom2['x']],
        y=[atom1['y'], atom2['y']],
        z=[atom1['z'], atom2['z']],
        mode='lines',
        line=dict(color='gray', width=5),
        showlegend=False
    ))

# Update layout
fig.update_layout(
    title='Molecular Structure (H2O)',
    scene=dict(
        xaxis_title='X (Å)',
        yaxis_title='Y (Å)',
        zaxis_title='Z (Å)'
    ),
    width=800,
    height=600
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("molecular_structure.html")
'''
    
    def _generate_custom_code(self, data: Dict[str, Any], parameters: Dict[str, Any], style_options: Dict[str, Any]) -> str:
        """Generate custom visualization code"""
        return '''
import plotly.graph_objects as go
import numpy as np

# Custom 3D visualization
# Replace this with your custom visualization logic

# Sample data
x = np.random.randn(100)
y = np.random.randn(100)
z = np.random.randn(100)

# Create custom plot
fig = go.Figure(data=go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    marker=dict(
        size=5,
        color=z,
        colorscale='viridis',
        opacity=0.8
    )
))

# Update layout
fig.update_layout(
    title='Custom 3D Visualization',
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis'
    ),
    width=800,
    height=600
)

# Show the plot
fig.show()

# Save as HTML
fig.write_html("custom_3d_plot.html")
'''
    
    def _generate_html_output(
        self,
        viz_type: VisualizationType,
        data: Dict[str, Any],
        parameters: Dict[str, Any],
        style_options: Dict[str, Any]
    ) -> str:
        """Generate HTML output for preview"""
        # This would generate actual plotly HTML
        # For now, return a placeholder
        title = parameters.get('title', '3D Visualization')
        
        html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="plotly-div" style="width:100%;height:600px;"></div>
    <script>
        // Plotly visualization code would go here
        var data = [{{
            x: [1, 2, 3, 4],
            y: [10, 11, 12, 13],
            z: [2, 3, 4, 5],
            type: 'scatter3d',
            mode: 'markers'
        }}];
        
        var layout = {{
            title: '{title}',
            scene: {{
                xaxis: {{title: 'X Axis'}},
                yaxis: {{title: 'Y Axis'}},
                zaxis: {{title: 'Z Axis'}}
            }}
        }};
        
        Plotly.newPlot('plotly-div', data, layout);
    </script>
</body>
</html>
'''
        return html_template
    
    def _generate_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for statistical distribution visualization"""
        dist_type = analysis.get('distribution_type', 'normal')
        
        if dist_type == 'binomial':
            return self._generate_binomial_html(analysis, include_interactivity)
        elif dist_type == 'normal':
            return self._generate_normal_distribution_html(analysis, include_interactivity)
        elif dist_type == 'poisson':
            return self._generate_poisson_distribution_html(analysis, include_interactivity)
        elif dist_type == 'exponential':
            return self._generate_exponential_distribution_html(analysis, include_interactivity)
        elif dist_type == 'uniform':
            return self._generate_uniform_distribution_html(analysis, include_interactivity)
        else:
            return self._generate_generic_distribution_html(analysis, include_interactivity)
    
    def _generate_chart_type_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for specific chart types"""
        chart_type = analysis.get('chart_type', 'scatter')
        
        if chart_type == 'scatter':
            return self._generate_scatter_3d_html(analysis, include_interactivity)
        elif chart_type == 'surface':
            return self._generate_surface_3d_html(analysis, include_interactivity)
        elif chart_type == 'bar':
            return self._generate_bar_3d_html(analysis, include_interactivity)
        elif chart_type == 'heatmap':
            return self._generate_heatmap_3d_html(analysis, include_interactivity)
        elif chart_type == 'network':
            return self._generate_network_3d_html(analysis, include_interactivity)
        elif chart_type == 'molecular':
            return self._generate_molecular_3d_html(analysis, include_interactivity)
        else:
            return self._generate_scatter_3d_html(analysis, include_interactivity)
    
    def _generate_math_function_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for mathematical function visualization"""
        functions = analysis.get('math_functions', [])
        
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .controls {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        .control-group {{
            display: inline-block;
            margin: 10px;
        }}
        .control-group label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        .control-group input, .control-group select {{
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 120px;
        }}
        #plotDiv {{
            height: 600px;
            margin: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="functionType">函数类型:</label>
                <select id="functionType" onchange="updatePlot()">
                    <option value="sin">正弦函数 (sin)</option>
                    <option value="cos">余弦函数 (cos)</option>
                    <option value="tan">正切函数 (tan)</option>
                    <option value="exp">指数函数 (exp)</option>
                    <option value="log">对数函数 (log)</option>
                    <option value="polynomial">多项式函数</option>
                    <option value="combined">组合函数</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="amplitude">振幅/系数:</label>
                <input type="range" id="amplitude" min="0.1" max="5" step="0.1" value="1" onchange="updatePlot()">
                <span id="amplitudeValue">1</span>
            </div>
            
            <div class="control-group">
                <label for="frequency">频率:</label>
                <input type="range" id="frequency" min="0.1" max="3" step="0.1" value="1" onchange="updatePlot()">
                <span id="frequencyValue">1</span>
            </div>
            
            <div class="control-group">
                <label for="phase">相位:</label>
                <input type="range" id="phase" min="0" max="6.28" step="0.1" value="0" onchange="updatePlot()">
                <span id="phaseValue">0</span>
            </div>
        </div>
        
        <div id="plotDiv"></div>
    </div>

    <script>
        function updatePlot() {{
            const functionType = document.getElementById('functionType').value;
            const amplitude = parseFloat(document.getElementById('amplitude').value);
            const frequency = parseFloat(document.getElementById('frequency').value);
            const phase = parseFloat(document.getElementById('phase').value);
            
            // 更新显示值
            document.getElementById('amplitudeValue').textContent = amplitude;
            document.getElementById('frequencyValue').textContent = frequency;
            document.getElementById('phaseValue').textContent = phase.toFixed(2);
            
            // 生成数据
            const x = [], y = [], z = [];
            const range = 10;
            const step = 0.2;
            
            for (let i = -range; i <= range; i += step) {{
                for (let j = -range; j <= range; j += step) {{
                    x.push(i);
                    y.push(j);
                    
                    let zValue;
                    switch(functionType) {{
                        case 'sin':
                            zValue = amplitude * Math.sin(frequency * Math.sqrt(i*i + j*j) + phase);
                            break;
                        case 'cos':
                            zValue = amplitude * Math.cos(frequency * Math.sqrt(i*i + j*j) + phase);
                            break;
                        case 'tan':
                            zValue = amplitude * Math.tan(frequency * (i + j) + phase);
                            if (Math.abs(zValue) > 10) zValue = Math.sign(zValue) * 10; // 限制范围
                            break;
                        case 'exp':
                            zValue = amplitude * Math.exp(-frequency * (i*i + j*j) / 10);
                            break;
                        case 'log':
                            const r = Math.sqrt(i*i + j*j);
                            zValue = r > 0 ? amplitude * Math.log(frequency * r + 1) : 0;
                            break;
                        case 'polynomial':
                            zValue = amplitude * (frequency * (i*i + j*j) - (i*i*i + j*j*j) / 10);
                            break;
                        case 'combined':
                            zValue = amplitude * (Math.sin(frequency * i + phase) * Math.cos(frequency * j + phase));
                            break;
                        default:
                            zValue = amplitude * Math.sin(frequency * Math.sqrt(i*i + j*j) + phase);
                    }}
                    
                    z.push(zValue);
                }}
            }}
            
            const trace = {{
                x: x,
                y: y,
                z: z,
                type: 'scatter3d',
                mode: 'markers',
                marker: {{
                    size: 3,
                    color: z,
                    colorscale: 'Viridis',
                    showscale: true,
                    colorbar: {{
                        title: 'Z值'
                    }}
                }}
            }};
            
            const layout = {{
                title: `${{functionType.toUpperCase()}}函数3D可视化`,
                scene: {{
                    xaxis: {{ title: 'X轴' }},
                    yaxis: {{ title: 'Y轴' }},
                    zaxis: {{ title: 'Z轴' }},
                    camera: {{
                        eye: {{ x: 1.5, y: 1.5, z: 1.5 }}
                    }}
                }},
                margin: {{ l: 0, r: 0, b: 0, t: 50 }}
            }};
            
            Plotly.newPlot('plotDiv', [trace], layout, {{responsive: true}});
        }}
        
        // 初始化
        updatePlot();
    </script>
</body>
</html>'''
        
        return html_template.format(
            title=analysis['title'],
            description=analysis['description']
        )
    
    def _generate_intelligent_custom_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate intelligent custom visualization based on user prompt"""
        prompt = analysis.get('original_prompt', '')
        parameters = analysis.get('parameters', {})
        
        # 根据用户输入的具体内容生成相应的可视化
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .prompt-info {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #667eea;
            margin: 20px;
            border-radius: 5px;
        }}
        .controls {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .control-group {{
            display: flex;
            flex-direction: column;
            min-width: 150px;
        }}
        .control-group label {{
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }}
        .control-group input, .control-group select {{
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        #plotDiv {{
            height: 600px;
            margin: 20px;
        }}
        .data-info {{
            background: #e3f2fd;
            padding: 15px;
            margin: 20px;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        
        <div class="prompt-info">
            <h3>📝 用户需求分析</h3>
            <p><strong>原始输入:</strong> {prompt}</p>
            <p><strong>识别的特征:</strong> {features}</p>
            <p><strong>提取的参数:</strong> {parameters}</p>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="vizType">可视化类型:</label>
                <select id="vizType" onchange="updateVisualization()">
                    <option value="adaptive">智能适配</option>
                    <option value="scatter">3D散点图</option>
                    <option value="surface">3D表面图</option>
                    <option value="bar">3D柱状图</option>
                    <option value="line">3D线图</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="dataPoints">数据点数:</label>
                <input type="range" id="dataPoints" min="50" max="1000" value="{default_points}" onchange="updateVisualization()">
                <span id="dataPointsValue">{default_points}</span>
            </div>
            
            <div class="control-group">
                <label for="colorScheme">配色方案:</label>
                <select id="colorScheme" onchange="updateVisualization()">
                    <option value="Viridis">Viridis</option>
                    <option value="Plasma">Plasma</option>
                    <option value="Blues">Blues</option>
                    <option value="Reds">Reds</option>
                    <option value="Rainbow">Rainbow</option>
                </select>
            </div>
            
            <div class="control-group">
                <label for="animationSpeed">动画速度:</label>
                <input type="range" id="animationSpeed" min="100" max="2000" value="1000" onchange="updateVisualization()">
                <span id="animationSpeedValue">1000ms</span>
            </div>
            
            <button onclick="regenerateData()" style="padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer;">
                🔄 重新生成数据
            </button>
        </div>
        
        <div class="data-info">
            <h4>📊 当前数据信息</h4>
            <div id="dataInfo">正在生成数据...</div>
        </div>
        
        <div id="plotDiv"></div>
    </div>

    <script>
        let currentData = null;
        
        function generateIntelligentData() {{
            const points = parseInt(document.getElementById('dataPoints').value);
            document.getElementById('dataPointsValue').textContent = points;
            
            // 根据用户输入智能生成数据
            const prompt = "{prompt}";
            const x = [], y = [], z = [];
            
            // 分析用户输入，生成相应的数据模式
            if (prompt.includes('随机') || prompt.includes('random')) {{
                // 随机数据
                for (let i = 0; i < points; i++) {{
                    x.push((Math.random() - 0.5) * 20);
                    y.push((Math.random() - 0.5) * 20);
                    z.push((Math.random() - 0.5) * 20);
                }}
            }} else if (prompt.includes('螺旋') || prompt.includes('spiral')) {{
                // 螺旋数据
                for (let i = 0; i < points; i++) {{
                    const t = (i / points) * 4 * Math.PI;
                    x.push(Math.cos(t) * t);
                    y.push(Math.sin(t) * t);
                    z.push(t);
                }}
            }} else if (prompt.includes('波浪') || prompt.includes('wave')) {{
                // 波浪数据
                for (let i = 0; i < points; i++) {{
                    const xi = (i / points - 0.5) * 20;
                    const yi = (Math.random() - 0.5) * 20;
                    x.push(xi);
                    y.push(yi);
                    z.push(Math.sin(xi) * Math.cos(yi));
                }}
            }} else if (prompt.includes('聚类') || prompt.includes('cluster')) {{
                // 聚类数据
                const clusters = 3;
                for (let c = 0; c < clusters; c++) {{
                    const centerX = (Math.random() - 0.5) * 15;
                    const centerY = (Math.random() - 0.5) * 15;
                    const centerZ = (Math.random() - 0.5) * 15;
                    
                    for (let i = 0; i < points / clusters; i++) {{
                        x.push(centerX + (Math.random() - 0.5) * 5);
                        y.push(centerY + (Math.random() - 0.5) * 5);
                        z.push(centerZ + (Math.random() - 0.5) * 5);
                    }}
                }}
            }} else {{
                // 默认：基于数学函数的数据
                for (let i = 0; i < points; i++) {{
                    const t = (i / points) * 4 * Math.PI;
                    x.push(t * Math.cos(t));
                    y.push(t * Math.sin(t));
                    z.push(Math.sin(t * 2) * 5);
                }}
            }}
            
            currentData = {{ x, y, z }};
            
            // 更新数据信息
            const dataInfo = document.getElementById('dataInfo');
            dataInfo.innerHTML = `
                <p><strong>数据点数:</strong> ${{points}}</p>
                <p><strong>X范围:</strong> [${{Math.min(...x).toFixed(2)}}, ${{Math.max(...x).toFixed(2)}}]</p>
                <p><strong>Y范围:</strong> [${{Math.min(...y).toFixed(2)}}, ${{Math.max(...y).toFixed(2)}}]</p>
                <p><strong>Z范围:</strong> [${{Math.min(...z).toFixed(2)}}, ${{Math.max(...z).toFixed(2)}}]</p>
                <p><strong>生成模式:</strong> 基于用户输入"${{prompt}}"的智能适配</p>
            `;
        }}
        
        function updateVisualization() {{
            if (!currentData) generateIntelligentData();
            
            const vizType = document.getElementById('vizType').value;
            const colorScheme = document.getElementById('colorScheme').value;
            const animationSpeed = parseInt(document.getElementById('animationSpeed').value);
            document.getElementById('animationSpeedValue').textContent = animationSpeed + 'ms';
            
            let trace;
            
            if (vizType === 'adaptive' || vizType === 'scatter') {{
                trace = {{
                    x: currentData.x,
                    y: currentData.y,
                    z: currentData.z,
                    type: 'scatter3d',
                    mode: 'markers',
                    marker: {{
                        size: 5,
                        color: currentData.z,
                        colorscale: colorScheme,
                        showscale: true,
                        colorbar: {{ title: 'Z值' }}
                    }}
                }};
            }} else if (vizType === 'line') {{
                trace = {{
                    x: currentData.x,
                    y: currentData.y,
                    z: currentData.z,
                    type: 'scatter3d',
                    mode: 'lines+markers',
                    line: {{ color: colorScheme, width: 3 }},
                    marker: {{ size: 3 }}
                }};
            }}
            
            const layout = {{
                title: {{
                    text: '🎯 智能生成的3D可视化',
                    font: {{ size: 20 }}
                }},
                scene: {{
                    xaxis: {{ title: 'X轴' }},
                    yaxis: {{ title: 'Y轴' }},
                    zaxis: {{ title: 'Z轴' }},
                    camera: {{
                        eye: {{ x: 1.5, y: 1.5, z: 1.5 }}
                    }}
                }},
                margin: {{ l: 0, r: 0, b: 0, t: 50 }},
                transition: {{
                    duration: animationSpeed,
                    easing: 'cubic-in-out'
                }}
            }};
            
            Plotly.newPlot('plotDiv', [trace], layout, {{responsive: true}});
        }}
        
        function regenerateData() {{
            generateIntelligentData();
            updateVisualization();
        }}
        
        // 初始化
        generateIntelligentData();
        updateVisualization();
    </script>
</body>
</html>'''
        
        # 设置默认参数
        default_points = parameters.get('points', 200)
        features_str = ', '.join(analysis.get('features', ['智能分析']))
        parameters_str = ', '.join([f"{k}: {v}" for k, v in parameters.items()]) if parameters else '无特定参数'
        
        return html_template.format(
            title=analysis['title'],
            description=analysis['description'],
            prompt=prompt,
            features=features_str,
            parameters=parameters_str,
            default_points=default_points
        )
    
    def _generate_normal_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for normal distribution visualization"""
        # 实现正态分布的具体可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>正态分布可视化功能开发中...</p></body></html>"
    
    def _generate_poisson_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for Poisson distribution visualization"""
        # 实现泊松分布的具体可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>泊松分布可视化功能开发中...</p></body></html>"
    
    def _generate_exponential_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for exponential distribution visualization"""
        # 实现指数分布的具体可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>指数分布可视化功能开发中...</p></body></html>"
    
    def _generate_uniform_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for uniform distribution visualization"""
        # 实现均匀分布的具体可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>均匀分布可视化功能开发中...</p></body></html>"
    
    def _generate_generic_distribution_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for generic distribution visualization"""
        # 实现通用分布的可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>通用分布可视化功能开发中...</p></body></html>"
    
    def _generate_heatmap_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D heatmap visualization"""
        # 实现3D热力图的可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>3D热力图可视化功能开发中...</p></body></html>"
    
    def _generate_network_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D network visualization"""
        # 实现3D网络图的可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>3D网络图可视化功能开发中...</p></body></html>"
    
    def _generate_molecular_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D molecular visualization"""
        # 实现3D分子结构的可视化
        return f"<html><body><h1>{analysis['title']}</h1><p>3D分子结构可视化功能开发中...</p></body></html>".format(title=title)
    
    def _load_examples(self) -> List[VisualizationExample]:
        """Load visualization examples"""
        return [
            VisualizationExample(
                id="scatter_3d_basic",
                title="Basic 3D Scatter Plot",
                description="Simple 3D scatter plot with random data points",
                visualization_type=VisualizationType.SCATTER_3D,
                code_snippet="fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='markers'))",
                full_code_url="/api/v1/examples/scatter_3d_basic/code",
                difficulty_level="Beginner",
                tags=["scatter", "basic", "3d"]
            ),
            VisualizationExample(
                id="surface_3d_function",
                title="3D Mathematical Surface",
                description="3D surface plot of a mathematical function",
                visualization_type=VisualizationType.SURFACE_3D,
                code_snippet="fig = go.Figure(data=go.Surface(x=X, y=Y, z=Z))",
                full_code_url="/api/v1/examples/surface_3d_function/code",
                difficulty_level="Intermediate",
                tags=["surface", "mathematics", "function"]
            ),
            VisualizationExample(
                id="molecular_water",
                title="Water Molecule Structure",
                description="3D visualization of H2O molecular structure",
                visualization_type=VisualizationType.MOLECULAR,
                code_snippet="# Atoms and bonds visualization",
                full_code_url="/api/v1/examples/molecular_water/code",
                difficulty_level="Advanced",
                tags=["molecular", "chemistry", "structure"]
            )
        ]
    
    async def get_examples(self) -> List[VisualizationExample]:
        """Get all visualization examples"""
        return self.examples
    
    async def get_example_by_id(self, example_id: str) -> Optional[VisualizationExample]:
        """Get a specific example by ID"""
        for example in self.examples:
            if example.id == example_id:
                return example
        return None
    
    async def generate_html_visualization(self, request: HTMLGenerationRequest) -> HTMLGenerationResponse:
        """Generate a complete HTML visualization page based on natural language prompt"""
        try:
            # Generate unique ID
            viz_id = str(uuid.uuid4())
            
            # Analyze prompt to determine visualization type and requirements
            analysis = self._analyze_prompt(request.prompt)
            
            # Generate HTML content based on analysis
            html_content = self._generate_complete_html(
                prompt=request.prompt,
                viz_type=request.visualization_type or analysis['visualization_type'],
                complexity=request.complexity,
                include_interactivity=request.include_interactivity,
                theme=request.theme,
                analysis=analysis
            )
            
            return HTMLGenerationResponse(
                id=viz_id,
                prompt=request.prompt,
                html_content=html_content,
                title=analysis['title'],
                description=analysis['description'],
                visualization_type=request.visualization_type or analysis['visualization_type'],
                complexity=request.complexity,
                features=analysis['features'],
                created_at=datetime.now(),
                status="success"
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate HTML visualization: {str(e)}")
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the prompt to extract visualization requirements"""
        prompt_lower = prompt.lower()
        
        # Store original prompt for later use
        analysis = {
            'original_prompt': prompt,
            'prompt_lower': prompt_lower
        }
        
        # Determine visualization type based on content
        viz_type = VisualizationType.CUSTOM
        
        # Statistical distributions
        if any(word in prompt_lower for word in ['二项分布', 'binomial', '二项式']):
            viz_type = VisualizationType.CUSTOM
            analysis['distribution_type'] = 'binomial'
        elif any(word in prompt_lower for word in ['正态分布', 'normal', 'gaussian']):
            viz_type = VisualizationType.CUSTOM
            analysis['distribution_type'] = 'normal'
        elif any(word in prompt_lower for word in ['泊松分布', 'poisson']):
            viz_type = VisualizationType.CUSTOM
            analysis['distribution_type'] = 'poisson'
        elif any(word in prompt_lower for word in ['指数分布', 'exponential']):
            viz_type = VisualizationType.CUSTOM
            analysis['distribution_type'] = 'exponential'
        elif any(word in prompt_lower for word in ['均匀分布', 'uniform']):
            viz_type = VisualizationType.CUSTOM
            analysis['distribution_type'] = 'uniform'
        
        # Chart types
        elif any(word in prompt_lower for word in ['散点图', 'scatter', '点图']):
            viz_type = VisualizationType.SCATTER_3D
            analysis['chart_type'] = 'scatter'
        elif any(word in prompt_lower for word in ['表面图', 'surface', '曲面']):
            viz_type = VisualizationType.SURFACE_3D
            analysis['chart_type'] = 'surface'
        elif any(word in prompt_lower for word in ['柱状图', 'bar', '条形图']):
            viz_type = VisualizationType.BAR_3D
            analysis['chart_type'] = 'bar'
        elif any(word in prompt_lower for word in ['热力图', 'heatmap', '热图']):
            viz_type = VisualizationType.CUSTOM
            analysis['chart_type'] = 'heatmap'
        elif any(word in prompt_lower for word in ['网络图', 'network', '图论']):
            viz_type = VisualizationType.CUSTOM
            analysis['chart_type'] = 'network'
        elif any(word in prompt_lower for word in ['分子', 'molecular', '原子']):
            viz_type = VisualizationType.CUSTOM
            analysis['chart_type'] = 'molecular'
        
        # Extract data characteristics
        analysis['data_characteristics'] = []
        if any(word in prompt_lower for word in ['随机', 'random', '随机数']):
            analysis['data_characteristics'].append('random_data')
        if any(word in prompt_lower for word in ['时间序列', 'time series', '时序']):
            analysis['data_characteristics'].append('time_series')
        if any(word in prompt_lower for word in ['多维', 'multidimensional', '高维']):
            analysis['data_characteristics'].append('multidimensional')
        
        # Extract mathematical functions or equations
        analysis['math_functions'] = []
        if any(word in prompt_lower for word in ['sin', 'cos', 'tan', '正弦', '余弦', '正切']):
            analysis['math_functions'].append('trigonometric')
        if any(word in prompt_lower for word in ['exp', '指数', 'exponential']):
            analysis['math_functions'].append('exponential')
        if any(word in prompt_lower for word in ['log', '对数', 'logarithm']):
            analysis['math_functions'].append('logarithmic')
        if any(word in prompt_lower for word in ['多项式', 'polynomial', 'x²', 'x^2']):
            analysis['math_functions'].append('polynomial')
        
        # Extract parameters and ranges
        analysis['parameters'] = {}
        import re
        
        # Look for number ranges
        range_patterns = [
            r'(\d+)\s*到\s*(\d+)',
            r'(\d+)\s*-\s*(\d+)',
            r'从\s*(\d+)\s*到\s*(\d+)',
            r'range\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)'
        ]
        
        for pattern in range_patterns:
            matches = re.findall(pattern, prompt_lower)
            if matches:
                analysis['parameters']['range'] = [int(matches[0][0]), int(matches[0][1])]
                break
        
        # Look for specific parameter values
        param_patterns = [
            (r'n\s*=\s*(\d+)', 'n'),
            (r'p\s*=\s*([\d.]+)', 'p'),
            (r'μ\s*=\s*([\d.-]+)', 'mu'),
            (r'σ\s*=\s*([\d.]+)', 'sigma'),
            (r'λ\s*=\s*([\d.]+)', 'lambda'),
            (r'点数\s*[:：]\s*(\d+)', 'points'),
            (r'数据点\s*[:：]\s*(\d+)', 'points')
        ]
        
        for pattern, param_name in param_patterns:
            matches = re.findall(pattern, prompt_lower)
            if matches:
                try:
                    analysis['parameters'][param_name] = float(matches[0])
                except ValueError:
                    pass
        
        # Extract features
        features = []
        if any(word in prompt_lower for word in ['交互', 'interactive', '滑动条', 'slider']):
            features.append('交互式控件')
        if any(word in prompt_lower for word in ['参数', 'parameter', '调节']):
            features.append('参数调节')
        if any(word in prompt_lower for word in ['统计', 'statistics', '均值', 'mean', '方差', 'variance']):
            features.append('统计信息')
        if any(word in prompt_lower for word in ['3d', '三维', '立体']):
            features.append('3D可视化')
        if any(word in prompt_lower for word in ['动画', 'animation', '动态']):
            features.append('动画效果')
        if any(word in prompt_lower for word in ['颜色', 'color', '彩色']):
            features.append('颜色映射')
        
        # Generate intelligent title and description based on analysis
        title = self._generate_intelligent_title(analysis)
        description = self._generate_intelligent_description(analysis)
        
        analysis.update({
            'visualization_type': viz_type,
            'title': title,
            'description': description,
            'features': features
        })
        
        return analysis
    
    def _generate_intelligent_title(self, analysis: Dict[str, Any]) -> str:
        """Generate intelligent title based on analysis"""
        prompt_lower = analysis['prompt_lower']
        
        if 'distribution_type' in analysis:
            dist_names = {
                'binomial': '二项分布',
                'normal': '正态分布',
                'poisson': '泊松分布',
                'exponential': '指数分布',
                'uniform': '均匀分布'
            }
            return f"{dist_names.get(analysis['distribution_type'], '概率分布')}可视化"
        
        elif 'chart_type' in analysis:
            chart_names = {
                'scatter': '3D散点图',
                'surface': '3D表面图',
                'bar': '3D柱状图',
                'heatmap': '3D热力图',
                'network': '3D网络图',
                'molecular': '分子结构图'
            }
            return chart_names.get(analysis['chart_type'], '3D图表')
        
        elif analysis['math_functions']:
            return '数学函数3D可视化'
        
        else:
            # Try to extract meaningful words from prompt
            meaningful_words = []
            for word in ['数据', '函数', '模型', '分析', '图表', '可视化']:
                if word in prompt_lower:
                    meaningful_words.append(word)
            
            if meaningful_words:
                return f"{''.join(meaningful_words[:2])}3D可视化"
            else:
                return "智能3D可视化"
    
    def _generate_intelligent_description(self, analysis: Dict[str, Any]) -> str:
        """Generate intelligent description based on analysis"""
        prompt = analysis['original_prompt']
        
        if 'distribution_type' in analysis:
            dist_descriptions = {
                'binomial': '交互式二项分布可视化，支持参数n和p的动态调节',
                'normal': '正态分布概率密度函数的3D可视化展示',
                'poisson': '泊松分布概率质量函数的交互式可视化',
                'exponential': '指数分布概率密度函数的3D可视化',
                'uniform': '均匀分布的3D可视化展示'
            }
            return dist_descriptions.get(analysis['distribution_type'], '概率分布的3D可视化')
        
        elif 'chart_type' in analysis:
            return f"基于用户需求生成的{analysis['chart_type']}类型3D可视化"
        
        else:
            # Generate description based on prompt content
            if len(prompt) > 50:
                return f"根据用户需求'{prompt[:50]}...'生成的智能3D可视化"
            else:
                return f"根据用户需求'{prompt}'生成的智能3D可视化"
    
    def _generate_complete_html(
        self,
        prompt: str,
        viz_type: VisualizationType,
        complexity: str,
        include_interactivity: bool,
        theme: str,
        analysis: Dict[str, Any]
    ) -> str:
        """Generate complete HTML page for visualization"""
        
        # Check if this is a binomial distribution request
        if '二项分布' in prompt.lower() or 'binomial' in prompt.lower():
            return self._generate_binomial_html(analysis, include_interactivity)
        elif '正态分布' in prompt.lower() or 'normal' in prompt.lower():
            return self._generate_normal_html(analysis, include_interactivity)
        elif '泊松分布' in prompt.lower() or 'poisson' in prompt.lower():
            return self._generate_poisson_html(analysis, include_interactivity)
        else:
            return self._generate_generic_html(analysis, viz_type, include_interactivity)
    
    def _generate_binomial_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for binomial distribution visualization"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
        }}
        
        .control-group {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            gap: 20px;
        }}
        
        .control-label {{
            font-weight: 600;
            color: #333;
            min-width: 120px;
        }}
        
        .slider-container {{
            flex: 1;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .slider {{
            flex: 1;
            height: 8px;
            border-radius: 4px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }}
        
        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        
        .slider::-moz-range-thumb {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        }}
        
        .value-display {{
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: 600;
            min-width: 80px;
            text-align: center;
        }}
        
        .plot-container {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 8px;
            font-weight: 500;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: 700;
            color: #333;
        }}
        
        .explanation {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 20px;
            margin-top: 30px;
            border-radius: 0 8px 8px 0;
        }}
        
        .explanation h3 {{
            color: #1976d2;
            margin-bottom: 15px;
        }}
        
        .explanation p {{
            color: #333;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 {title}</h1>
            <p>{description}</p>
        </div>
        
        <div class="content">
            <div class="controls">
                <h3 style="margin-bottom: 20px; color: #333;">🎛️ 参数控制</h3>
                
                <div class="control-group">
                    <label class="control-label">试验次数 (n):</label>
                    <div class="slider-container">
                        <input type="range" id="nSlider" class="slider" min="5" max="100" value="20" step="1">
                        <div class="value-display" id="nValue">20</div>
                    </div>
                </div>
                
                <div class="control-group">
                    <label class="control-label">成功概率 (p):</label>
                    <div class="slider-container">
                        <input type="range" id="pSlider" class="slider" min="0.01" max="0.99" value="0.3" step="0.01">
                        <div class="value-display" id="pValue">0.30</div>
                    </div>
                </div>
            </div>
            
            <div class="plot-container">
                <div id="plotDiv" style="width: 100%; height: 600px;"></div>
            </div>
            
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-label">期望值 E(X)</div>
                    <div class="stat-value" id="meanValue">6.00</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">方差 Var(X)</div>
                    <div class="stat-value" id="varianceValue">4.20</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">标准差 σ</div>
                    <div class="stat-value" id="stdValue">2.05</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">变异系数 CV</div>
                    <div class="stat-value" id="cvValue">0.34</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">众数 Mode</div>
                    <div class="stat-value" id="modeValue">6</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">偏度 Skewness</div>
                    <div class="stat-value" id="skewnessValue">0.20</div>
                </div>
            </div>
            
            <div class="explanation">
                <h3>📚 二项分布说明</h3>
                <p><strong>二项分布 B(n,p)</strong> 描述了在n次独立的伯努利试验中成功次数的概率分布。</p>
                <p><strong>参数说明：</strong></p>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li><strong>n</strong>：试验次数（必须为正整数）</li>
                    <li><strong>p</strong>：每次试验成功的概率（0 ≤ p ≤ 1）</li>
                </ul>
                <p><strong>关键观察：</strong></p>
                <ul style="margin-left: 20px; line-height: 1.8;">
                    <li>当 p = 0.5 时，分布对称</li>
                    <li>当 p < 0.5 时，分布右偏；当 p > 0.5 时，分布左偏</li>
                    <li>当 n 增大且 np ≥ 5, n(1-p) ≥ 5 时，可用正态分布近似</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        // 二项分布概率质量函数
        function binomialPMF(k, n, p) {{
            function factorial(num) {{
                if (num <= 1) return 1;
                return num * factorial(num - 1);
            }}
            
            function combination(n, k) {{
                if (k > n) return 0;
                return factorial(n) / (factorial(k) * factorial(n - k));
            }}
            
            return combination(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
        }}
        
        // 更新图表
        function updatePlot() {{
            const n = parseInt(document.getElementById('nSlider').value);
            const p = parseFloat(document.getElementById('pSlider').value);
            
            // 更新显示值
            document.getElementById('nValue').textContent = n;
            document.getElementById('pValue').textContent = p.toFixed(2);
            
            // 生成数据
            const x = [];
            const y = [];
            for (let k = 0; k <= n; k++) {{
                x.push(k);
                y.push(binomialPMF(k, n, p));
            }}
            
            // 计算统计量
            const mean = n * p;
            const variance = n * p * (1 - p);
            const std = Math.sqrt(variance);
            const cv = std / mean;
            const mode = Math.floor((n + 1) * p);
            const skewness = (1 - 2 * p) / std;
            
            // 更新统计信息
            document.getElementById('meanValue').textContent = mean.toFixed(2);
            document.getElementById('varianceValue').textContent = variance.toFixed(2);
            document.getElementById('stdValue').textContent = std.toFixed(2);
            document.getElementById('cvValue').textContent = cv.toFixed(2);
            document.getElementById('modeValue').textContent = mode;
            document.getElementById('skewnessValue').textContent = skewness.toFixed(2);
            
            // 创建图表
            const trace1 = {{
                x: x,
                y: y,
                type: 'bar',
                name: `B(${{n}}, ${{p.toFixed(2)}})`,
                marker: {{
                    color: 'rgba(102, 126, 234, 0.8)',
                    line: {{
                        color: 'rgba(102, 126, 234, 1)',
                        width: 2
                    }}
                }}
            }};
            
            // 添加期望值线
            const meanLine = {{
                x: [mean, mean],
                y: [0, Math.max(...y)],
                type: 'scatter',
                mode: 'lines',
                name: `期望值 = ${{mean.toFixed(2)}}`,
                line: {{
                    color: 'red',
                    width: 3,
                    dash: 'dash'
                }}
            }};
            
            // 添加标准差范围
            const stdRange = {{
                x: [Math.max(0, mean - std), Math.min(n, mean + std)],
                y: [Math.max(...y) * 0.1, Math.max(...y) * 0.1],
                type: 'scatter',
                mode: 'lines',
                name: `±1σ 范围`,
                line: {{
                    color: 'orange',
                    width: 5
                }}
            }};
            
            const layout = {{
                title: {{
                    text: `二项分布 B(${{n}}, ${{p.toFixed(2)}}) 概率质量函数`,
                    font: {{ size: 18, color: '#333' }}
                }},
                xaxis: {{
                    title: '成功次数 (k)',
                    gridcolor: '#f0f0f0'
                }},
                yaxis: {{
                    title: '概率 P(X = k)',
                    gridcolor: '#f0f0f0'
                }},
                plot_bgcolor: 'white',
                paper_bgcolor: 'white',
                showlegend: true,
                legend: {{
                    x: 0.7,
                    y: 0.9
                }}
            }};
            
            Plotly.newPlot('plotDiv', [trace1, meanLine, stdRange], layout, {{responsive: true}});
        }}
        
        // 事件监听器
        document.getElementById('nSlider').addEventListener('input', updatePlot);
        document.getElementById('pSlider').addEventListener('input', updatePlot);
        
        // 初始化
        updatePlot();
    </script>
</body>
</html>'''
        
        return html_template.format(
            title=analysis['title'],
            description=analysis['description']
        )
    
    def _generate_normal_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for normal distribution visualization"""
        # Similar structure for normal distribution
        return f"<html><body><h1>{analysis['title']}</h1><p>正态分布可视化功能开发中...</p></body></html>"
    
    def _generate_poisson_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for Poisson distribution visualization"""
        # Similar structure for Poisson distribution
        return f"<html><body><h1>{analysis['title']}</h1><p>泊松分布可视化功能开发中...</p></body></html>"
    
    def _generate_generic_html(self, analysis: Dict[str, Any], viz_type: VisualizationType, include_interactivity: bool) -> str:
        """Generate HTML for generic visualization"""
        if viz_type == VisualizationType.SCATTER_3D:
            return self._generate_scatter_3d_html(analysis, include_interactivity)
        elif viz_type == VisualizationType.SURFACE_3D:
            return self._generate_surface_3d_html(analysis, include_interactivity)
        elif viz_type == VisualizationType.BAR_3D:
            return self._generate_bar_3d_html(analysis, include_interactivity)
        elif viz_type == VisualizationType.CUSTOM:
            return self._generate_custom_html(analysis, include_interactivity)
        else:
            return self._generate_default_3d_html(analysis, include_interactivity)
    
    def _generate_scatter_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D scatter plot"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .controls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }}
        
        .control-group {{
            display: flex;
            flex-direction: column;
            gap: 5px;
        }}
        
        .control-group label {{
            font-weight: 600;
            color: #333;
            font-size: 0.9em;
        }}
        
        .control-group input, .control-group select {{
            padding: 8px 12px;
            border: 2px solid #e9ecef;
            border-radius: 6px;
            font-size: 14px;
            transition: border-color 0.3s;
        }}
        
        .control-group input:focus, .control-group select:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.2s;
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
        }}
        
        #plotDiv {{
            width: 100%;
            height: 600px;
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        
        <div class="content">
            {controls_html}
            
            <div id="plotDiv"></div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value" id="pointCount">100</div>
                    <div class="stat-label">数据点数量</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="xRange">[-10, 10]</div>
                    <div class="stat-label">X轴范围</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="yRange">[-10, 10]</div>
                    <div class="stat-label">Y轴范围</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="zRange">[-10, 10]</div>
                    <div class="stat-label">Z轴范围</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // 生成随机数据
        function generateData(count = 100, xRange = [-10, 10], yRange = [-10, 10], zRange = [-10, 10]) {{
            const x = [];
            const y = [];
            const z = [];
            const colors = [];
            
            for (let i = 0; i < count; i++) {{
                const xVal = Math.random() * (xRange[1] - xRange[0]) + xRange[0];
                const yVal = Math.random() * (yRange[1] - yRange[0]) + yRange[0];
                const zVal = Math.random() * (zRange[1] - zRange[0]) + zRange[0];
                
                x.push(xVal);
                y.push(yVal);
                z.push(zVal);
                colors.push(Math.sqrt(xVal*xVal + yVal*yVal + zVal*zVal));
            }}
            
            return {{ x, y, z, colors }};
        }}
        
        // 创建3D散点图
        function createPlot() {{
            const pointCount = parseInt(document.getElementById('pointCount').textContent);
            const data = generateData(pointCount);
            
            const trace = {{
                x: data.x,
                y: data.y,
                z: data.z,
                mode: 'markers',
                type: 'scatter3d',
                marker: {{
                    size: 5,
                    color: data.colors,
                    colorscale: 'Viridis',
                    showscale: true,
                    colorbar: {{
                        title: '距离原点',
                        titleside: 'right'
                    }}
                }},
                text: data.x.map((x, i) => `X: ${{x.toFixed(2)}}<br>Y: ${{data.y[i].toFixed(2)}}<br>Z: ${{data.z[i].toFixed(2)}}`),
                hovertemplate: '%{{text}}<extra></extra>'
            }};
            
            const layout = {{
                title: {{
                    text: '3D散点图可视化',
                    font: {{ size: 20 }}
                }},
                scene: {{
                    xaxis: {{ title: 'X轴' }},
                    yaxis: {{ title: 'Y轴' }},
                    zaxis: {{ title: 'Z轴' }},
                    camera: {{
                        eye: {{ x: 1.5, y: 1.5, z: 1.5 }}
                    }}
                }},
                margin: {{ l: 0, r: 0, b: 0, t: 50 }},
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            }};
            
            const config = {{
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d']
            }};
            
            Plotly.newPlot('plotDiv', [trace], layout, config);
        }}
        
        // 更新数据点数量
        function updatePointCount() {{
            const count = parseInt(document.getElementById('pointCountInput').value);
            document.getElementById('pointCount').textContent = count;
            createPlot();
        }}
        
        // 随机生成新数据
        function regenerateData() {{
            createPlot();
        }}
        
        // 初始化图表
        createPlot();
    </script>
</body>
</html>'''
        
        controls_html = ""
        if include_interactivity:
            controls_html = '''
            <div class="controls">
                <div class="control-group">
                    <label for="pointCountInput">数据点数量:</label>
                    <input type="number" id="pointCountInput" value="100" min="10" max="1000" onchange="updatePointCount()">
                </div>
                <button class="btn" onclick="regenerateData()">重新生成数据</button>
                <button class="btn" onclick="createPlot()">刷新图表</button>
            </div>
            '''
        
        return html_template.format(
            title=analysis.get('title', '3D散点图'),
            description=analysis.get('description', '交互式3D散点图可视化'),
            controls_html=controls_html
        )
    
    def _generate_surface_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D surface plot"""
        return f"<html><body><h1>{analysis['title']}</h1><p>3D表面图功能开发中...</p></body></html>"
    
    def _generate_bar_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for 3D bar chart"""
        return f"<html><body><h1>{analysis['title']}</h1><p>3D柱状图功能开发中...</p></body></html>"
    
    def _generate_default_3d_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for default 3D visualization"""
        return f"<html><body><h1>{analysis['title']}</h1><p>通用可视化功能开发中...</p></body></html>"
    
    def _generate_custom_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate HTML for custom visualization based on prompt analysis"""
        
        # 根据分析结果选择合适的生成方法
        if 'distribution_type' in analysis:
            return self._generate_distribution_html(analysis, include_interactivity)
        elif 'chart_type' in analysis:
            return self._generate_chart_type_html(analysis, include_interactivity)
        elif analysis.get('math_functions'):
            return self._generate_math_function_html(analysis, include_interactivity)
        else:
            # 生成基于用户具体需求的智能可视化
            return self._generate_intelligent_custom_html(analysis, include_interactivity)
    
    def _generate_multi_purpose_html(self, analysis: Dict[str, Any], include_interactivity: bool) -> str:
        """Generate a multi-purpose visualization interface"""
        html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自定义3D可视化</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 30px 60px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .content {
            padding: 30px;
        }
        
        .controls {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
        }
        
        .control-group {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            gap: 15px;
        }
        
        .control-group label {
            font-weight: 600;
            color: #495057;
            min-width: 120px;
        }
        
        select, input, button {
            padding: 10px 15px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            cursor: pointer;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        #plotDiv {
            width: 100%;
            height: 600px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .viz-type-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .viz-type-buttons button {
            flex: 1;
            min-width: 120px;
        }
        
        .active {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>自定义3D可视化</h1>
            <p>智能多功能可视化平台</p>
        </div>
        
        <div class="content">
            <div class="controls">
                <div class="control-group">
                    <label>可视化类型:</label>
                    <div class="viz-type-buttons">
                        <button onclick="setVizType('scatter')" id="scatterBtn" class="active">3D散点图</button>
                        <button onclick="setVizType('surface')" id="surfaceBtn">3D曲面图</button>
                        <button onclick="setVizType('bar')" id="barBtn">3D柱状图</button>
                        <button onclick="setVizType('mesh')" id="meshBtn">3D网格图</button>
                    </div>
                </div>
                
                <div class="control-group">
                    <label>数据点数量:</label>
                    <input type="range" id="pointCount" min="50" max="500" value="100" oninput="updatePointCount()">
                    <span id="pointCountValue">100</span>
                </div>
                
                <div class="control-group">
                    <label>颜色主题:</label>
                    <select id="colorTheme" onchange="updateVisualization()">
                        <option value="Viridis">Viridis</option>
                        <option value="Plasma">Plasma</option>
                        <option value="Rainbow">Rainbow</option>
                        <option value="Blues">Blues</option>
                        <option value="Reds">Reds</option>
                    </select>
                </div>
                
                <div class="control-group">
                    <button onclick="regenerateData()">重新生成数据</button>
                    <button onclick="exportData()">导出数据</button>
                </div>
            </div>
            
            <div id="plotDiv"></div>
        </div>
    </div>

    <script>
        let currentVizType = 'scatter';
        let currentData = null;
        
        function setVizType(type) {
            // 更新按钮状态
            document.querySelectorAll('.viz-type-buttons button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(type + 'Btn').classList.add('active');
            
            currentVizType = type;
            updateVisualization();
        }
        
        function generateData() {
            const count = parseInt(document.getElementById('pointCount').value);
            
            switch(currentVizType) {
                case 'scatter':
                    return generateScatterData(count);
                case 'surface':
                    return generateSurfaceData();
                case 'bar':
                    return generateBarData();
                case 'mesh':
                    return generateMeshData();
                default:
                    return generateScatterData(count);
            }
        }
        
        function generateScatterData(count) {
            const x = [], y = [], z = [], colors = [];
            for (let i = 0; i < count; i++) {
                const xi = (Math.random() - 0.5) * 20;
                const yi = (Math.random() - 0.5) * 20;
                const zi = (Math.random() - 0.5) * 20;
                x.push(xi);
                y.push(yi);
                z.push(zi);
                colors.push(Math.sqrt(xi*xi + yi*yi + zi*zi));
            }
            return { x, y, z, colors };
        }
        
        function generateSurfaceData() {
            const size = 20;
            const x = [], y = [], z = [];
            
            for (let i = 0; i < size; i++) {
                x.push([]);
                y.push([]);
                z.push([]);
                for (let j = 0; j < size; j++) {
                    const xi = (i - size/2) * 0.5;
                    const yi = (j - size/2) * 0.5;
                    x[i].push(xi);
                    y[i].push(yi);
                    z[i].push(Math.sin(Math.sqrt(xi*xi + yi*yi)) * 3);
                }
            }
            return { x, y, z };
        }
        
        function generateBarData() {
            const categories = ['A', 'B', 'C', 'D', 'E'];
            const series = ['系列1', '系列2', '系列3'];
            const x = [], y = [], z = [];
            
            categories.forEach((cat, i) => {
                series.forEach((ser, j) => {
                    x.push(cat);
                    y.push(ser);
                    z.push(Math.random() * 100 + 10);
                });
            });
            
            return { x, y, z };
        }
        
        function generateMeshData() {
            const count = 50;
            const x = [], y = [], z = [], i = [], j = [], k = [];
            
            // 生成随机点
            for (let n = 0; n < count; n++) {
                x.push((Math.random() - 0.5) * 10);
                y.push((Math.random() - 0.5) * 10);
                z.push((Math.random() - 0.5) * 10);
            }
            
            // 生成三角形面
            for (let n = 0; n < count - 3; n += 3) {
                i.push(n);
                j.push(n + 1);
                k.push(n + 2);
            }
            
            return { x, y, z, i, j, k };
        }
        
        function updateVisualization() {
            currentData = generateData();
            const colorTheme = document.getElementById('colorTheme').value;
            
            let trace;
            
            switch(currentVizType) {
                case 'scatter':
                    trace = {
                        x: currentData.x,
                        y: currentData.y,
                        z: currentData.z,
                        mode: 'markers',
                        type: 'scatter3d',
                        marker: {
                            size: 5,
                            color: currentData.colors,
                            colorscale: colorTheme,
                            showscale: true,
                            colorbar: { title: '距离原点' }
                        }
                    };
                    break;
                    
                case 'surface':
                    trace = {
                        x: currentData.x,
                        y: currentData.y,
                        z: currentData.z,
                        type: 'surface',
                        colorscale: colorTheme,
                        showscale: true
                    };
                    break;
                    
                case 'bar':
                    trace = {
                        x: currentData.x,
                        y: currentData.y,
                        z: currentData.z,
                        type: 'scatter3d',
                        mode: 'markers',
                        marker: {
                            size: 8,
                            color: currentData.z,
                            colorscale: colorTheme,
                            showscale: true
                        }
                    };
                    break;
                    
                case 'mesh':
                    trace = {
                        x: currentData.x,
                        y: currentData.y,
                        z: currentData.z,
                        i: currentData.i,
                        j: currentData.j,
                        k: currentData.k,
                        type: 'mesh3d',
                        colorscale: colorTheme,
                        intensity: currentData.z,
                        showscale: true
                    };
                    break;
            }
            
            const layout = {
                title: {
                    text: `自定义3D可视化 - ${getVizTypeName()}`,
                    font: { size: 20 }
                },
                scene: {
                    xaxis: { title: 'X轴' },
                    yaxis: { title: 'Y轴' },
                    zaxis: { title: 'Z轴' },
                    camera: {
                        eye: { x: 1.5, y: 1.5, z: 1.5 }
                    }
                },
                margin: { l: 0, r: 0, b: 0, t: 50 },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            };
            
            const config = {
                responsive: true,
                displayModeBar: true
            };
            
            Plotly.newPlot('plotDiv', [trace], layout, config);
        }
        
        function getVizTypeName() {
            const names = {
                'scatter': '散点图',
                'surface': '曲面图',
                'bar': '柱状图',
                'mesh': '网格图'
            };
            return names[currentVizType] || '未知类型';
        }
        
        function updatePointCount() {
            const value = document.getElementById('pointCount').value;
            document.getElementById('pointCountValue').textContent = value;
            if (currentVizType === 'scatter') {
                updateVisualization();
            }
        }
        
        function regenerateData() {
            updateVisualization();
        }
        
        function exportData() {
            if (!currentData) return;
            
            const dataStr = JSON.stringify(currentData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `visualization_data_${currentVizType}.json`;
            link.click();
            URL.revokeObjectURL(url);
        }
        
        // 初始化
        updateVisualization();
    </script>
</body>
</html>'''
        
        return html_template
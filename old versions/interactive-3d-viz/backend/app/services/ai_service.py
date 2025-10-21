import uuid
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import openai
from openai import OpenAI

from ..models.visualization import (
    CodeGenerationRequest,
    CodeGenerationResponse,
    VisualizationType
)
from ..core.config import settings
from .dependency_service import dependency_analyzer
from .template_service import template_service

class AICodeGenerationService:
    """Service for AI-powered code generation"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
    
    async def generate_code(self, request: CodeGenerationRequest) -> CodeGenerationResponse:
        """Generate Python code based on natural language prompt"""
        try:
            # Generate unique ID
            generation_id = str(uuid.uuid4())
            
            # Analyze prompt to determine visualization type
            detected_viz_type = self._detect_visualization_type(request.prompt)
            viz_type = request.visualization_type or detected_viz_type
            
            # Generate code using AI or templates
            if self.client and settings.OPENAI_API_KEY:
                python_code, explanation, dependencies = await self._generate_with_ai(request, viz_type)
            else:
                python_code, explanation, dependencies = self._generate_with_templates(request, viz_type)
            
            # Analyze dependencies intelligently
            dependency_analysis = dependency_analyzer.analyze_code_dependencies(python_code)
            enhanced_dependencies = dependency_analysis['core_dependencies']
            
            # Merge with original dependencies and remove duplicates
            all_dependencies = list(set(dependencies + enhanced_dependencies))
            
            # Estimate complexity
            complexity = self._estimate_complexity(python_code)
            
            return CodeGenerationResponse(
                id=generation_id,
                prompt=request.prompt,
                python_code=python_code,
                explanation=explanation,
                dependencies=all_dependencies,
                visualization_type=viz_type,
                estimated_complexity=complexity,
                created_at=datetime.now(),
                dependency_analysis=dependency_analysis  # Add analysis results
            )
            
        except Exception as e:
            raise Exception(f"Failed to generate code: {str(e)}")
    
    def _detect_visualization_type(self, prompt: str) -> VisualizationType:
        """Detect visualization type from prompt"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['scatter', 'points', 'dots']):
            return VisualizationType.SCATTER_3D
        elif any(word in prompt_lower for word in ['surface', 'mesh', 'grid']):
            return VisualizationType.SURFACE_3D
        elif any(word in prompt_lower for word in ['volume', 'volumetric', '3d data']):
            return VisualizationType.VOLUME_3D
        elif any(word in prompt_lower for word in ['network', 'graph', 'nodes', 'edges']):
            return VisualizationType.NETWORK_3D
        elif any(word in prompt_lower for word in ['molecule', 'molecular', 'atom', 'chemical']):
            return VisualizationType.MOLECULAR
        elif any(word in prompt_lower for word in ['mesh', 'triangular', 'wireframe']):
            return VisualizationType.MESH_3D
        elif any(word in prompt_lower for word in ['bar', 'column', 'histogram']):
            return VisualizationType.BAR_3D
        elif any(word in prompt_lower for word in ['line', 'trend', 'time series']):
            return VisualizationType.LINE_3D
        elif any(word in prompt_lower for word in ['heatmap', 'heat map', 'intensity']):
            return VisualizationType.HEATMAP_3D
        elif any(word in prompt_lower for word in ['contour', 'level', 'isoline']):
            return VisualizationType.CONTOUR_3D
        elif any(word in prompt_lower for word in ['point cloud', 'lidar', 'scan']):
            return VisualizationType.POINT_CLOUD
        elif any(word in prompt_lower for word in ['terrain', 'elevation', 'topography']):
            return VisualizationType.TERRAIN
        elif any(word in prompt_lower for word in ['financial', 'stock', 'price', 'trading']):
            return VisualizationType.FINANCIAL
        elif any(word in prompt_lower for word in ['statistical', 'distribution', 'probability']):
            return VisualizationType.STATISTICAL
        elif any(word in prompt_lower for word in ['geographic', 'map', 'geo', 'location']):
            return VisualizationType.GEOGRAPHIC
        else:
            return VisualizationType.SCATTER_3D  # Default
    
    async def _generate_with_ai(self, request: CodeGenerationRequest, viz_type: VisualizationType) -> tuple[str, str, List[str]]:
        """Generate code using OpenAI API"""
        try:
            system_prompt = self._create_system_prompt(viz_type)
            user_prompt = self._create_user_prompt(request)
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the response to extract code, explanation, and dependencies
            python_code, explanation, dependencies = self._parse_ai_response(content)
            
            return python_code, explanation, dependencies
            
        except Exception as e:
            # Fallback to templates if AI fails
            return self._generate_with_templates(request, viz_type)
    
    def _generate_with_templates(self, request: CodeGenerationRequest, viz_type: VisualizationType) -> tuple[str, str, List[str]]:
        """Generate code using predefined templates"""
        # 根据可视化类型查找合适的模板
        templates = template_service.get_all_templates()
        suitable_template = None
        
        for template in templates:
            if template.visualization_type == viz_type:
                suitable_template = template
                break
        
        # 如果没找到合适的模板，使用基础散点图模板
        if not suitable_template:
            suitable_template = template_service.get_template_by_id("basic_scatter_3d")
        
        if not suitable_template:
            raise ValueError("No suitable template found")
        
        # 使用模板服务自定义模板
        python_code = self._customize_template_with_service(suitable_template, request)
        explanation = suitable_template.explanation
        dependencies = suitable_template.dependencies
        
        return python_code, explanation, dependencies
    
    def _create_system_prompt(self, viz_type: VisualizationType) -> str:
        """Create system prompt for AI"""
        return f"""You are an expert Python developer specializing in 3D data visualization using libraries like Plotly, Matplotlib, and Three.js.

Your task is to generate high-quality Python code for {viz_type.value} visualizations based on user requirements.

Guidelines:
1. Use modern Python practices and clear, readable code
2. Include proper imports and dependencies
3. Add helpful comments explaining key concepts
4. Use Plotly as the primary visualization library
5. Include error handling where appropriate
6. Make the code modular and reusable
7. Provide sample data if none is specified

Response format:
```python
# Your Python code here
```

EXPLANATION:
[Provide a clear explanation of what the code does and how to use it]

DEPENDENCIES:
[List required Python packages]
"""
    
    def _create_user_prompt(self, request: CodeGenerationRequest) -> str:
        """Create user prompt for AI"""
        prompt = f"Create a 3D visualization for: {request.prompt}"
        
        if request.data_sample:
            prompt += f"\n\nData structure: {request.data_sample}"
        
        if request.requirements:
            prompt += f"\n\nSpecific requirements: {', '.join(request.requirements)}"
        
        if request.style_preferences:
            prompt += f"\n\nStyle preferences: {request.style_preferences}"
        
        return prompt
    
    def _parse_ai_response(self, content: str) -> tuple[str, str, List[str]]:
        """Parse AI response to extract code, explanation, and dependencies"""
        # Extract Python code
        code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
        python_code = code_match.group(1) if code_match else content
        
        # Extract explanation
        explanation_match = re.search(r'EXPLANATION:\s*(.*?)(?=DEPENDENCIES:|$)', content, re.DOTALL)
        explanation = explanation_match.group(1).strip() if explanation_match else "Generated 3D visualization code"
        
        # Extract dependencies
        deps_match = re.search(r'DEPENDENCIES:\s*(.*?)$', content, re.DOTALL)
        if deps_match:
            deps_text = deps_match.group(1).strip()
            dependencies = [dep.strip() for dep in deps_text.split('\n') if dep.strip()]
        else:
            dependencies = ['plotly', 'numpy', 'pandas']
        
        return python_code, explanation, dependencies
    
    def _customize_template(self, template_code: str, request: CodeGenerationRequest) -> str:
        """Customize template code based on request (legacy method)"""
        # Simple template customization
        # In a real implementation, this would be more sophisticated
        customized_code = template_code
        
        # Replace placeholders with actual values from request
        if request.data_sample:
            # Customize data based on sample
            pass
        
        return customized_code
    
    def _customize_template_with_service(self, template, request: CodeGenerationRequest) -> str:
        """Customize template using template service"""
        # 从请求中提取参数
        parameters = {}
        
        # 根据请求内容智能设置参数
        prompt_lower = request.prompt.lower()
        
        # 设置标题
        if "标题" in request.prompt or "title" in prompt_lower:
            parameters["title"] = self._extract_title_from_prompt(request.prompt)
        
        # 设置数据点数量
        if "点" in request.prompt or "数据" in request.prompt:
            n_points = self._extract_number_from_prompt(request.prompt, default=100)
            parameters["n_points"] = min(max(n_points, 10), 10000)
        
        # 设置颜色方案
        if "颜色" in request.prompt or "color" in prompt_lower:
            if "红" in request.prompt or "red" in prompt_lower:
                parameters["colorscale"] = "reds"
            elif "蓝" in request.prompt or "blue" in prompt_lower:
                parameters["colorscale"] = "blues"
            elif "绿" in request.prompt or "green" in prompt_lower:
                parameters["colorscale"] = "greens"
        
        # 使用模板服务自定义代码
        try:
            return template_service.customize_template(template.metadata.id, parameters)
        except Exception:
            # 如果自定义失败，返回原始代码
            return template.code
    
    def _extract_title_from_prompt(self, prompt: str) -> str:
        """Extract title from prompt"""
        # 简单的标题提取逻辑
        if "标题" in prompt:
            parts = prompt.split("标题")
            if len(parts) > 1:
                title_part = parts[1].split("，")[0].split("。")[0].strip()
                return title_part if title_part else "3D可视化图表"
        return "3D可视化图表"
    
    def _extract_number_from_prompt(self, prompt: str, default: int = 100) -> int:
        """Extract number from prompt"""
        import re
        numbers = re.findall(r'\d+', prompt)
        if numbers:
            return int(numbers[0])
        return default
    
    def _estimate_complexity(self, code: str) -> str:
        """Estimate code complexity"""
        lines = len(code.split('\n'))
        imports = len(re.findall(r'^import|^from', code, re.MULTILINE))
        functions = len(re.findall(r'def ', code))
        
        if lines < 50 and imports < 5:
            return "simple"
        elif lines < 150 and imports < 10:
            return "medium"
        else:
            return "complex"
    
    async def get_available_templates(self) -> List[Dict[str, Any]]:
        """Get list of available code templates"""
        return template_service.get_template_metadata_list()
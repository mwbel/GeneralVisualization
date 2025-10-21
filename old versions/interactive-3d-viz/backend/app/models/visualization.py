from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class VisualizationType(str, Enum):
    SCATTER_3D = "scatter_3d"
    SURFACE_3D = "surface_3d"
    MESH_3D = "mesh_3d"
    VOLUME_3D = "volume_3d"
    NETWORK_3D = "network_3d"
    MOLECULAR = "molecular"
    BAR_3D = "bar_3d"
    LINE_3D = "line_3d"
    HEATMAP_3D = "heatmap_3d"
    CONTOUR_3D = "contour_3d"
    STREAMLINE_3D = "streamline_3d"
    POINT_CLOUD = "point_cloud"
    TERRAIN = "terrain"
    FINANCIAL = "financial"
    STATISTICAL = "statistical"
    GEOGRAPHIC = "geographic"
    CUSTOM = "custom"

class DataFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    NUMPY = "numpy"
    PANDAS = "pandas"

class VisualizationRequest(BaseModel):
    title: str = Field(..., description="Title of the visualization")
    description: Optional[str] = Field(None, description="Description of the visualization")
    visualization_type: VisualizationType = Field(..., description="Type of 3D visualization")
    data_format: DataFormat = Field(DataFormat.JSON, description="Format of input data")
    data: Dict[str, Any] = Field(..., description="Input data for visualization")
    parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Visualization parameters")
    style_options: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Style and appearance options")

class VisualizationResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the visualization")
    title: str = Field(..., description="Title of the visualization")
    description: Optional[str] = Field(None, description="Description of the visualization")
    visualization_type: VisualizationType = Field(..., description="Type of 3D visualization")
    python_code: str = Field(..., description="Generated Python code")
    html_output: Optional[str] = Field(None, description="Generated HTML output")
    preview_url: Optional[str] = Field(None, description="URL for preview")
    download_url: Optional[str] = Field(None, description="URL for downloading code")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    status: str = Field(default="completed", description="Generation status")

class CodeGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt for code generation")
    visualization_type: Optional[VisualizationType] = Field(None, description="Preferred visualization type")
    data_sample: Optional[Dict[str, Any]] = Field(None, description="Sample data structure")
    requirements: Optional[List[str]] = Field(default_factory=list, description="Specific requirements")
    style_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Style preferences")

class CodeGenerationResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the generated code")
    prompt: str = Field(..., description="Original prompt")
    python_code: str = Field(..., description="Generated Python code")
    explanation: str = Field(..., description="Explanation of the generated code")
    dependencies: List[str] = Field(default_factory=list, description="Required Python packages")
    visualization_type: VisualizationType = Field(..., description="Detected/assigned visualization type")
    estimated_complexity: str = Field(..., description="Complexity level (simple/medium/complex)")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    dependency_analysis: Optional[Dict[str, Any]] = Field(None, description="Detailed dependency analysis")

class VisualizationExample(BaseModel):
    id: str = Field(..., description="Example identifier")
    title: str = Field(..., description="Example title")
    description: str = Field(..., description="Example description")
    visualization_type: VisualizationType = Field(..., description="Type of visualization")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    code_snippet: str = Field(..., description="Code snippet preview")
    full_code_url: str = Field(..., description="URL to full code")
    difficulty_level: str = Field(..., description="Difficulty level")
    tags: List[str] = Field(default_factory=list, description="Tags for categorization")

class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    version: str = Field(..., description="API version")
    service_name: str = Field(..., description="Service name")

class DetailedHealthResponse(HealthCheckResponse):
    environment: str = Field(..., description="Environment (dev/prod)")
    features: Dict[str, bool] = Field(..., description="Feature availability")
    dependencies: Dict[str, str] = Field(..., description="Dependency status")
    uptime: str = Field(..., description="Service uptime")

class HTMLGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt for visualization")
    visualization_type: Optional[VisualizationType] = Field(VisualizationType.CUSTOM, description="Type of visualization")
    complexity: Optional[str] = Field("medium", description="Complexity level (simple/medium/complex)")
    include_interactivity: Optional[bool] = Field(True, description="Include interactive controls")
    theme: Optional[str] = Field("modern", description="Visual theme")

class HTMLGenerationResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the generated visualization")
    prompt: str = Field(..., description="Original prompt")
    html_content: str = Field(..., description="Complete HTML page content")
    title: str = Field(..., description="Generated title for the visualization")
    description: str = Field(..., description="Description of the visualization")
    visualization_type: VisualizationType = Field(..., description="Type of visualization")
    complexity: str = Field(..., description="Complexity level")
    features: List[str] = Field(default_factory=list, description="List of included features")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    status: str = Field(default="success", description="Generation status")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
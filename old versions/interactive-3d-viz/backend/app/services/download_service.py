import os
import zipfile
import tempfile
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime

from ..core.config import settings
from .download_history_service import download_history_service

class DownloadService:
    """Service for handling file downloads and packaging"""
    
    def __init__(self):
        self.downloads_dir = Path(settings.UPLOAD_DIR) / "downloads"
        self.downloads_dir.mkdir(exist_ok=True)
    
    async def create_code_package(
        self,
        code: str,
        dependencies: List[str],
        filename: str = "visualization",
        include_requirements: bool = True,
        include_readme: bool = True,
        include_sample_data: bool = False,
        include_setup_script: bool = True,
        include_docker: bool = False,
        include_jupyter_notebook: bool = False,
        python_version: str = "3.8",
        package_format: str = "zip"
    ) -> str:
        """Create a downloadable package with code and dependencies"""
        
        # Create temporary directory for package
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / filename
            package_dir.mkdir(exist_ok=True)
            
            # Write main Python file
            main_file = package_dir / f"{filename}.py"
            with open(main_file, 'w', encoding='utf-8') as f:
                f.write(self._add_header_comment(code, filename))
            
            # Create requirements.txt if requested
            if include_requirements and dependencies:
                requirements_file = package_dir / "requirements.txt"
                with open(requirements_file, 'w', encoding='utf-8') as f:
                    enhanced_deps = self._enhance_dependencies(dependencies, python_version)
                    for dep in enhanced_deps:
                        f.write(f"{dep}\n")
            
            # Create README.md if requested
            if include_readme:
                readme_file = package_dir / "README.md"
                with open(readme_file, 'w', encoding='utf-8') as f:
                    f.write(self._generate_readme(filename, dependencies, python_version))
            
            # Create sample data if requested
            if include_sample_data:
                await self._create_sample_data(package_dir)
            
            # Create setup script if requested
            if include_setup_script:
                setup_file = package_dir / "setup.py"
                with open(setup_file, 'w', encoding='utf-8') as f:
                    f.write(self._generate_setup_script(filename, dependencies))
            
            # Create Dockerfile if requested
            if include_docker:
                await self._create_dockerfile(package_dir, filename, dependencies, python_version)
            
            # Create Jupyter notebook if requested
            if include_jupyter_notebook:
                await self._create_jupyter_notebook(package_dir, filename, code)
            
            # Create package info
            info_file = package_dir / "package_info.json"
            files_list = [f"{filename}.py"]
            if include_requirements:
                files_list.append("requirements.txt")
            if include_readme:
                files_list.append("README.md")
            if include_setup_script:
                files_list.append("setup.py")
            if include_sample_data:
                files_list.append("sample_data.csv")
            if include_docker:
                files_list.extend(["Dockerfile", "docker-compose.yml"])
            if include_jupyter_notebook:
                files_list.append(f"{filename}.ipynb")
            
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "name": filename,
                    "created_at": datetime.now().isoformat(),
                    "python_version": python_version,
                    "dependencies": dependencies,
                    "package_format": package_format,
                    "options": {
                        "include_requirements": include_requirements,
                        "include_readme": include_readme,
                        "include_sample_data": include_sample_data,
                        "include_setup_script": include_setup_script,
                        "include_docker": include_docker,
                        "include_jupyter_notebook": include_jupyter_notebook
                    },
                    "files": files_list
                }, f, indent=2)
            
            # Create ZIP file
            zip_filename = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            zip_path = self.downloads_dir / zip_filename
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(package_dir)
                        zipf.write(file_path, arcname)
            
            # 记录下载历史
            file_size = zip_path.stat().st_size
            download_history_service.add_download_record(
                filename=zip_filename,
                code=code,
                dependencies=dependencies,
                options={
                    "include_requirements": include_requirements,
                    "include_readme": include_readme,
                    "include_sample_data": include_sample_data,
                    "include_setup_script": include_setup_script,
                    "include_docker": include_docker,
                    "include_jupyter_notebook": include_jupyter_notebook,
                    "python_version": python_version,
                    "package_format": package_format
                },
                file_size=file_size,
                success=True
            )
            
            return str(zip_path)
    
    def _add_header_comment(self, code: str, filename: str) -> str:
        """Add header comment to the code"""
        header = f'''"""
{filename.replace('_', ' ').title()} - 3D Visualization
Generated by Interactive 3D Visualization Platform
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This file contains Python code for creating 3D visualizations.
Make sure to install the required dependencies before running.

Usage:
    python {filename}.py

Requirements:
    See requirements.txt for the list of required packages.
"""

'''
        return header + code
    
    def _generate_readme(self, filename: str, dependencies: List[str], python_version: str = "3.8") -> str:
        """Generate README.md content"""
        return f"""# {filename.replace('_', ' ').title()}

This package contains a 3D visualization generated by the Interactive 3D Visualization Platform.

## Installation

1. Install Python {python_version} or higher
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the visualization:

```bash
python {filename}.py
```

## Dependencies

The following Python packages are required:

{chr(10).join(f'- {dep}' for dep in dependencies)}

## Files

- `{filename}.py` - Main visualization script
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup script
- `package_info.json` - Package metadata

## Support

For support and documentation, visit: https://github.com/your-repo/interactive-3d-viz

## License

This code is generated by the Interactive 3D Visualization Platform.
Feel free to modify and use it according to your needs.
"""
    
    def _generate_setup_script(self, filename: str, dependencies: List[str]) -> str:
        """Generate setup.py script"""
        return f'''#!/usr/bin/env python3
"""
Setup script for {filename}
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    dependencies = {dependencies}
    
    print("Installing dependencies...")
    for dep in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✓ Installed {{dep}}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {{dep}}")
            return False
    
    return True

def run_visualization():
    """Run the visualization"""
    try:
        subprocess.check_call([sys.executable, "{filename}.py"])
    except subprocess.CalledProcessError:
        print("Failed to run visualization")
        return False
    return True

if __name__ == "__main__":
    print("Setting up {filename}...")
    
    if install_dependencies():
        print("Dependencies installed successfully!")
        
        response = input("Do you want to run the visualization now? (y/n): ")
        if response.lower() in ['y', 'yes']:
            run_visualization()
    else:
        print("Failed to install some dependencies. Please install them manually.")
'''
    
    async def _create_sample_data(self, package_dir: Path):
        """Create sample data file"""
        import pandas as pd
        import numpy as np
        
        # Generate sample data
        n_points = 100
        data = {
            'x': np.random.randn(n_points),
            'y': np.random.randn(n_points),
            'z': np.random.randn(n_points),
            'value': np.random.randn(n_points),
            'category': np.random.choice(['A', 'B', 'C'], n_points)
        }
        
        df = pd.DataFrame(data)
        sample_file = package_dir / "sample_data.csv"
        df.to_csv(sample_file, index=False)
    
    async def get_download_file(self, file_path: str) -> Optional[Path]:
        """Get download file if it exists"""
        full_path = Path(file_path)
        if full_path.exists() and full_path.parent == self.downloads_dir:
            return full_path
        return None
    
    async def cleanup_old_downloads(self, max_age_hours: int = 24):
        """Clean up old download files"""
        import time
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for file_path in self.downloads_dir.glob("*.zip"):
            if current_time - file_path.stat().st_mtime > max_age_seconds:
                try:
                    file_path.unlink()
                    print(f"Cleaned up old download: {file_path.name}")
                except Exception as e:
                    print(f"Failed to clean up {file_path.name}: {e}")
    
    async def get_download_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get download history"""
        downloads = []
        
        for file_path in sorted(
            self.downloads_dir.glob("*.zip"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )[:limit]:
            stat = file_path.stat()
            downloads.append({
                "filename": file_path.name,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "download_url": f"/api/download/{file_path.name}"
            })
        
        return downloads
    
    def get_file_size_mb(self, file_path: Path) -> float:
        """Get file size in MB"""
        return file_path.stat().st_size / (1024 * 1024)
    
    def _enhance_dependencies(self, dependencies: List[str], python_version: str) -> List[str]:
        """Enhance dependencies with version constraints and additional packages"""
        enhanced_deps = []
        
        # Version mapping for different Python versions
        version_mapping = {
            "3.8": {
                "plotly": "plotly>=5.17.0",
                "numpy": "numpy>=1.24.0",
                "pandas": "pandas>=2.0.0",
                "matplotlib": "matplotlib>=3.7.0",
                "scipy": "scipy>=1.10.0",
                "dash": "dash>=2.14.0",
                "jupyter": "jupyter>=1.0.0",
                "ipywidgets": "ipywidgets>=8.0.0"
            },
            "3.9": {
                "plotly": "plotly>=5.17.0",
                "numpy": "numpy>=1.25.0",
                "pandas": "pandas>=2.1.0",
                "matplotlib": "matplotlib>=3.8.0",
                "scipy": "scipy>=1.11.0",
                "dash": "dash>=2.14.0",
                "jupyter": "jupyter>=1.0.0",
                "ipywidgets": "ipywidgets>=8.0.0"
            },
            "3.10": {
                "plotly": "plotly>=5.17.0",
                "numpy": "numpy>=1.26.0",
                "pandas": "pandas>=2.1.0",
                "matplotlib": "matplotlib>=3.8.0",
                "scipy": "scipy>=1.11.0",
                "dash": "dash>=2.14.0",
                "jupyter": "jupyter>=1.0.0",
                "ipywidgets": "ipywidgets>=8.0.0"
            }
        }
        
        mapping = version_mapping.get(python_version, version_mapping["3.8"])
        
        for dep in dependencies:
            # Remove version constraints if present
            dep_name = dep.split('>=')[0].split('==')[0].split('<=')[0].strip()
            
            # Use enhanced version if available
            if dep_name in mapping:
                enhanced_deps.append(mapping[dep_name])
            else:
                enhanced_deps.append(dep)
        
        # Add common utility packages
        common_packages = [
            "kaleido>=0.2.1",  # For static image export
            "psutil>=5.9.0",   # For system monitoring
        ]
        
        for pkg in common_packages:
            pkg_name = pkg.split('>=')[0]
            if not any(pkg_name in dep for dep in enhanced_deps):
                enhanced_deps.append(pkg)
        
        return enhanced_deps
    
    async def _create_dockerfile(self, package_dir: Path, filename: str, dependencies: List[str], python_version: str):
        """Create Dockerfile for containerized deployment"""
        dockerfile_content = f'''# Use official Python runtime as base image
FROM python:{python_version}-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY {filename}.py .
COPY sample_data.csv .

# Expose port for web applications
EXPOSE 8050

# Run the application
CMD ["python", "{filename}.py"]
'''
        
        dockerfile_path = package_dir / "Dockerfile"
        with open(dockerfile_path, 'w', encoding='utf-8') as f:
            f.write(dockerfile_content)
        
        # Create docker-compose.yml
        compose_content = f'''version: '3.8'

services:
  {filename}:
    build: .
    ports:
      - "8050:8050"
    volumes:
      - ./data:/app/data
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

volumes:
  data:
'''
        
        compose_path = package_dir / "docker-compose.yml"
        with open(compose_path, 'w', encoding='utf-8') as f:
            f.write(compose_content)
    
    async def _create_jupyter_notebook(self, package_dir: Path, filename: str, code: str):
        """Create Jupyter notebook version of the code"""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# {filename.replace('_', ' ').title()}\\n",
                        "\\n",
                        "This notebook contains the generated 3D visualization code.\\n",
                        "\\n",
                        "## Setup\\n",
                        "\\n",
                        "First, make sure you have all required dependencies installed:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Install required packages\\n",
                        "# !pip install -r requirements.txt"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Import Libraries\\n",
                        "\\n",
                        "Import all necessary libraries for the visualization:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "import plotly.graph_objects as go\\n",
                        "import plotly.express as px\\n",
                        "import numpy as np\\n",
                        "import pandas as pd\\n",
                        "from plotly.offline import plot, iplot\\n",
                        "import plotly.io as pio\\n",
                        "\\n",
                        "# Set default renderer for Jupyter\\n",
                        "pio.renderers.default = 'notebook'"
                    ]
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "## Visualization Code\\n",
                        "\\n",
                        "The main visualization code:"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": code.split('\\n')
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "codemirror_mode": {
                        "name": "ipython",
                        "version": 3
                    },
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.8.0"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        notebook_path = package_dir / f"{filename}.ipynb"
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2)
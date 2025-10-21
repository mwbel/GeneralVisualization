import ast
import re
from typing import List, Dict, Set, Optional, Tuple
from pathlib import Path
import json

class DependencyAnalyzer:
    """Service for intelligent dependency detection and version management"""
    
    def __init__(self):
        self.package_mappings = self._load_package_mappings()
        self.version_constraints = self._load_version_constraints()
        self.common_imports = self._load_common_imports()
    
    def analyze_code_dependencies(self, code: str) -> Dict[str, any]:
        """Analyze Python code to extract dependencies and their information"""
        try:
            # Parse the code into AST
            tree = ast.parse(code)
            
            # Extract imports
            imports = self._extract_imports_from_ast(tree)
            
            # Extract function calls that might indicate dependencies
            function_calls = self._extract_function_calls(tree)
            
            # Detect implicit dependencies
            implicit_deps = self._detect_implicit_dependencies(code)
            
            # Combine and resolve dependencies
            all_deps = imports.union(implicit_deps)
            resolved_deps = self._resolve_dependencies(all_deps)
            
            # Get version recommendations
            versioned_deps = self._get_version_recommendations(resolved_deps)
            
            # Analyze complexity and suggest additional packages
            complexity_analysis = self._analyze_complexity(code, tree)
            suggested_deps = self._suggest_additional_packages(resolved_deps, complexity_analysis)
            
            return {
                'core_dependencies': list(versioned_deps),
                'suggested_dependencies': suggested_deps,
                'import_statements': list(imports),
                'function_calls': function_calls,
                'complexity_analysis': complexity_analysis,
                'python_version_requirement': self._determine_python_version(tree)
            }
            
        except SyntaxError as e:
            # If code can't be parsed, fall back to regex analysis
            return self._fallback_regex_analysis(code)
    
    def _extract_imports_from_ast(self, tree: ast.AST) -> Set[str]:
        """Extract import statements from AST"""
        imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
        
        return imports
    
    def _extract_function_calls(self, tree: ast.AST) -> List[str]:
        """Extract function calls that might indicate dependencies"""
        function_calls = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        function_calls.append(f"{node.func.value.id}.{node.func.attr}")
                elif isinstance(node.func, ast.Name):
                    function_calls.append(node.func.id)
        
        return function_calls
    
    def _detect_implicit_dependencies(self, code: str) -> Set[str]:
        """Detect dependencies that might not be explicitly imported"""
        implicit_deps = set()
        
        # Common patterns that indicate specific libraries
        patterns = {
            r'\.show\(\)': 'plotly',
            r'\.plot\(\)': 'matplotlib',
            r'\.scatter\(\)': 'matplotlib',
            r'\.figure\(\)': 'matplotlib',
            r'px\.': 'plotly',
            r'go\.': 'plotly',
            r'sns\.': 'seaborn',
            r'plt\.': 'matplotlib',
            r'np\.': 'numpy',
            r'pd\.': 'pandas',
            r'tf\.': 'tensorflow',
            r'torch\.': 'torch',
            r'cv2\.': 'opencv-python',
            r'sklearn\.': 'scikit-learn',
            r'scipy\.': 'scipy',
            r'requests\.': 'requests',
            r'json\.': None,  # Built-in
            r'os\.': None,    # Built-in
            r'sys\.': None,   # Built-in
        }
        
        for pattern, package in patterns.items():
            if package and re.search(pattern, code):
                implicit_deps.add(package)
        
        return implicit_deps
    
    def _resolve_dependencies(self, deps: Set[str]) -> Set[str]:
        """Resolve package names to their correct PyPI names"""
        resolved = set()
        
        for dep in deps:
            if dep in self.package_mappings:
                resolved.add(self.package_mappings[dep])
            else:
                resolved.add(dep)
        
        return resolved
    
    def _get_version_recommendations(self, deps: Set[str]) -> List[str]:
        """Get version recommendations for dependencies"""
        versioned_deps = []
        
        for dep in deps:
            if dep in self.version_constraints:
                versioned_deps.append(f"{dep}>={self.version_constraints[dep]}")
            else:
                versioned_deps.append(dep)
        
        return sorted(versioned_deps)
    
    def _analyze_complexity(self, code: str, tree: ast.AST) -> Dict[str, any]:
        """Analyze code complexity and characteristics"""
        lines = len(code.split('\n'))
        functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
        classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        imports = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
        
        # Detect visualization types
        viz_indicators = {
            'plotly': bool(re.search(r'plotly|go\.|px\.', code)),
            'matplotlib': bool(re.search(r'matplotlib|plt\.', code)),
            'seaborn': bool(re.search(r'seaborn|sns\.', code)),
            '3d_visualization': bool(re.search(r'3d|scatter3d|surface|mesh3d', code, re.IGNORECASE)),
            'interactive': bool(re.search(r'widget|interact|ipywidgets', code)),
            'animation': bool(re.search(r'animation|animate|frames', code)),
            'statistical': bool(re.search(r'distribution|histogram|boxplot|violin', code)),
        }
        
        complexity_score = (lines / 10) + (functions * 2) + (classes * 3) + (imports * 0.5)
        
        if complexity_score < 10:
            complexity_level = "simple"
        elif complexity_score < 30:
            complexity_level = "medium"
        else:
            complexity_level = "complex"
        
        return {
            'lines_of_code': lines,
            'functions': functions,
            'classes': classes,
            'imports': imports,
            'complexity_score': complexity_score,
            'complexity_level': complexity_level,
            'visualization_indicators': viz_indicators
        }
    
    def _suggest_additional_packages(self, deps: Set[str], complexity: Dict[str, any]) -> List[str]:
        """Suggest additional packages based on code analysis"""
        suggestions = []
        
        # Suggest based on visualization type
        if complexity['visualization_indicators']['plotly']:
            suggestions.extend(['kaleido', 'psutil'])  # For image export and performance
        
        if complexity['visualization_indicators']['matplotlib']:
            suggestions.extend(['pillow', 'imageio'])  # For image handling
        
        if complexity['visualization_indicators']['3d_visualization']:
            suggestions.extend(['trimesh', 'pyvista'])  # For advanced 3D operations
        
        if complexity['visualization_indicators']['interactive']:
            suggestions.extend(['ipywidgets', 'jupyter'])  # For interactive features
        
        if complexity['visualization_indicators']['animation']:
            suggestions.extend(['imageio', 'ffmpeg-python'])  # For animation export
        
        if complexity['visualization_indicators']['statistical']:
            suggestions.extend(['scipy', 'statsmodels'])  # For statistical analysis
        
        # Suggest based on complexity
        if complexity['complexity_level'] == 'complex':
            suggestions.extend(['tqdm', 'joblib'])  # For progress bars and parallel processing
        
        # Remove duplicates and already included dependencies
        suggestions = [pkg for pkg in set(suggestions) if pkg not in deps]
        
        return suggestions
    
    def _determine_python_version(self, tree: ast.AST) -> str:
        """Determine minimum Python version requirement"""
        # Check for Python 3.8+ features
        has_walrus = any(isinstance(node, ast.NamedExpr) for node in ast.walk(tree))
        has_positional_only = any(
            isinstance(node, ast.FunctionDef) and any(arg.arg for arg in node.args.posonlyargs)
            for node in ast.walk(tree)
        )
        
        if has_walrus or has_positional_only:
            return "3.8"
        
        # Check for f-strings (Python 3.6+)
        has_fstring = any(isinstance(node, ast.JoinedStr) for node in ast.walk(tree))
        if has_fstring:
            return "3.6"
        
        return "3.6"  # Default minimum
    
    def _fallback_regex_analysis(self, code: str) -> Dict[str, any]:
        """Fallback analysis using regex when AST parsing fails"""
        # Extract imports using regex
        import_pattern = r'(?:from\s+(\w+)|import\s+(\w+))'
        imports = set()
        
        for match in re.finditer(import_pattern, code):
            module = match.group(1) or match.group(2)
            if module:
                imports.add(module.split('.')[0])
        
        # Detect implicit dependencies
        implicit_deps = self._detect_implicit_dependencies(code)
        
        all_deps = imports.union(implicit_deps)
        resolved_deps = self._resolve_dependencies(all_deps)
        versioned_deps = self._get_version_recommendations(resolved_deps)
        
        return {
            'core_dependencies': versioned_deps,
            'suggested_dependencies': [],
            'import_statements': list(imports),
            'function_calls': [],
            'complexity_analysis': {
                'lines_of_code': len(code.split('\n')),
                'complexity_level': 'unknown',
                'visualization_indicators': {}
            },
            'python_version_requirement': '3.6'
        }
    
    def _load_package_mappings(self) -> Dict[str, str]:
        """Load mappings from import names to PyPI package names"""
        return {
            'cv2': 'opencv-python',
            'sklearn': 'scikit-learn',
            'PIL': 'pillow',
            'yaml': 'pyyaml',
            'dateutil': 'python-dateutil',
            'serial': 'pyserial',
            'crypto': 'pycryptodome',
            'jwt': 'pyjwt',
            'bs4': 'beautifulsoup4',
            'requests_oauthlib': 'requests-oauthlib',
            'google': 'google-api-python-client',
        }
    
    def _load_version_constraints(self) -> Dict[str, str]:
        """Load recommended version constraints for packages"""
        return {
            'plotly': '5.17.0',
            'numpy': '1.21.0',
            'pandas': '1.3.0',
            'matplotlib': '3.5.0',
            'seaborn': '0.11.0',
            'scipy': '1.7.0',
            'scikit-learn': '1.0.0',
            'tensorflow': '2.8.0',
            'torch': '1.12.0',
            'opencv-python': '4.5.0',
            'pillow': '8.3.0',
            'requests': '2.25.0',
            'beautifulsoup4': '4.9.0',
            'jupyter': '1.0.0',
            'ipywidgets': '7.6.0',
            'kaleido': '0.2.1',
            'psutil': '5.8.0',
            'tqdm': '4.62.0',
            'joblib': '1.1.0',
        }
    
    def _load_common_imports(self) -> Dict[str, List[str]]:
        """Load common import patterns for different use cases"""
        return {
            'data_science': ['numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy'],
            'visualization': ['plotly', 'matplotlib', 'seaborn', 'bokeh'],
            'machine_learning': ['scikit-learn', 'tensorflow', 'torch', 'xgboost'],
            'web_scraping': ['requests', 'beautifulsoup4', 'selenium', 'scrapy'],
            'image_processing': ['opencv-python', 'pillow', 'imageio', 'skimage'],
            'api_development': ['fastapi', 'flask', 'requests', 'pydantic'],
        }

# Global instance
dependency_analyzer = DependencyAnalyzer()
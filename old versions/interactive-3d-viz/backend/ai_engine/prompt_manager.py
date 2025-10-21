import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

class PromptManager:
    """Prompt模板管理器 - 负责模板的加载、优化和管理"""
    
    def __init__(self):
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
        self.logger = self._setup_logger()
        self.template_cache = {}
        self.template_metadata = {}
        self.usage_statistics = {}
        
        # 初始化时加载所有模板
        self._load_all_templates()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger("PromptManager")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_all_templates(self):
        """加载所有Prompt模板"""
        
        if not os.path.exists(self.prompts_dir):
            self.logger.warning(f"Prompts目录不存在: {self.prompts_dir}")
            return
        
        template_files = [f for f in os.listdir(self.prompts_dir) if f.endswith('.txt')]
        
        for template_file in template_files:
            template_name = template_file.replace('.txt', '')
            template_path = os.path.join(self.prompts_dir, template_file)
            
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.template_cache[template_name] = content
                self.template_metadata[template_name] = {
                    "file_path": template_path,
                    "loaded_at": datetime.now().isoformat(),
                    "size": len(content),
                    "word_count": len(content.split()),
                    "line_count": len(content.split('\n'))
                }
                
                self.logger.info(f"已加载模板: {template_name}")
                
            except Exception as e:
                self.logger.error(f"加载模板失败 {template_file}: {str(e)}")
    
    def get_template(self, template_name: str) -> Optional[str]:
        """获取指定的模板内容"""
        
        # 移除.txt后缀（如果有）
        template_name = template_name.replace('.txt', '')
        
        if template_name in self.template_cache:
            # 记录使用统计
            self._record_usage(template_name)
            return self.template_cache[template_name]
        else:
            self.logger.warning(f"模板未找到: {template_name}")
            return None
    
    def _record_usage(self, template_name: str):
        """记录模板使用统计"""
        if template_name not in self.usage_statistics:
            self.usage_statistics[template_name] = {
                "usage_count": 0,
                "last_used": None,
                "first_used": datetime.now().isoformat()
            }
        
        self.usage_statistics[template_name]["usage_count"] += 1
        self.usage_statistics[template_name]["last_used"] = datetime.now().isoformat()
    
    def optimize_prompt(self, template_name: str, user_input: str, 
                       context: Optional[Dict] = None) -> str:
        """优化Prompt模板，根据用户输入和上下文进行个性化调整"""
        
        base_template = self.get_template(template_name)
        if not base_template:
            return "模板未找到，请使用通用模板。"
        
        # 分析用户输入特征
        input_analysis = self._analyze_user_input(user_input)
        
        # 根据分析结果优化模板
        optimized_template = self._apply_optimizations(
            base_template, input_analysis, context or {}
        )
        
        return optimized_template
    
    def _analyze_user_input(self, user_input: str) -> Dict:
        """分析用户输入的特征"""
        
        analysis = {
            "length": len(user_input),
            "word_count": len(user_input.split()),
            "has_numbers": bool(re.search(r'\d+', user_input)),
            "has_math_symbols": bool(re.search(r'[+\-*/=<>∫∑∏√]', user_input)),
            "has_chinese": bool(re.search(r'[\u4e00-\u9fff]', user_input)),
            "has_english": bool(re.search(r'[a-zA-Z]', user_input)),
            "complexity_indicators": [],
            "specific_requirements": [],
            "visualization_type": "unknown"
        }
        
        # 检测复杂度指标
        complexity_keywords = {
            "3d": ["3d", "三维", "立体", "空间"],
            "interactive": ["交互", "动态", "可控", "参数"],
            "animation": ["动画", "运动", "变化", "演示"],
            "real_time": ["实时", "在线", "动态更新"],
            "multi_data": ["多数据", "对比", "比较", "多个"]
        }
        
        for category, keywords in complexity_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                analysis["complexity_indicators"].append(category)
        
        # 检测具体需求
        requirement_patterns = {
            "color_scheme": r"颜色|配色|色彩",
            "data_format": r"数据格式|csv|json|excel",
            "export_function": r"导出|保存|下载",
            "responsive": r"响应式|自适应|移动端",
            "performance": r"性能|优化|快速|效率"
        }
        
        for req_type, pattern in requirement_patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                analysis["specific_requirements"].append(req_type)
        
        # 检测可视化类型
        viz_types = {
            "scatter": ["散点", "scatter", "点图"],
            "line": ["线图", "曲线", "line", "趋势"],
            "bar": ["柱状", "条形", "bar", "直方"],
            "surface": ["曲面", "surface", "3d表面"],
            "heatmap": ["热力", "heatmap", "密度"],
            "network": ["网络", "关系", "graph", "节点"]
        }
        
        for viz_type, keywords in viz_types.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                analysis["visualization_type"] = viz_type
                break
        
        return analysis
    
    def _apply_optimizations(self, template: str, analysis: Dict, context: Dict) -> str:
        """根据分析结果应用优化"""
        
        optimized = template
        
        # 1. 根据复杂度调整要求
        if "3d" in analysis["complexity_indicators"]:
            optimized += "\n\n特别强调：\n- 重点突出3D效果和立体感\n- 添加多角度视图控制\n- 优化3D渲染性能"
        
        if "interactive" in analysis["complexity_indicators"]:
            optimized += "\n\n交互功能要求：\n- 添加丰富的交互控件\n- 支持参数实时调整\n- 提供用户友好的操作界面"
        
        if "animation" in analysis["complexity_indicators"]:
            optimized += "\n\n动画效果要求：\n- 添加流畅的动画过渡\n- 支持播放控制（播放/暂停/重置）\n- 优化动画性能和流畅度"
        
        # 2. 根据具体需求添加指导
        if "color_scheme" in analysis["specific_requirements"]:
            optimized += "\n\n颜色设计要求：\n- 使用专业的配色方案\n- 考虑色盲友好性\n- 提供多种颜色主题选择"
        
        if "export_function" in analysis["specific_requirements"]:
            optimized += "\n\n导出功能要求：\n- 支持多种格式导出（PNG、SVG、PDF）\n- 提供高分辨率输出选项\n- 包含数据导出功能"
        
        if "performance" in analysis["specific_requirements"]:
            optimized += "\n\n性能优化要求：\n- 优化大数据集处理\n- 使用高效的渲染算法\n- 添加加载进度指示器"
        
        # 3. 根据可视化类型添加专门指导
        viz_guidance = {
            "scatter": "- 优化点的大小和透明度\n- 添加颜色映射和图例\n- 支持数据点选择和高亮",
            "line": "- 优化线条样式和粗细\n- 添加数据点标记\n- 支持多条线的对比显示",
            "surface": "- 优化曲面的光照效果\n- 添加等高线显示\n- 支持曲面的透明度调节",
            "heatmap": "- 选择合适的颜色映射\n- 添加数值标注\n- 支持区域选择和缩放",
            "network": "- 优化节点和边的布局\n- 添加力导向布局算法\n- 支持节点的交互选择"
        }
        
        if analysis["visualization_type"] in viz_guidance:
            optimized += f"\n\n{analysis['visualization_type'].upper()}图表专门要求：\n{viz_guidance[analysis['visualization_type']]}"
        
        # 4. 根据语言偏好调整
        if analysis["has_chinese"] and not analysis["has_english"]:
            optimized += "\n\n语言要求：\n- 所有标签和注释使用中文\n- 提供中文的使用说明\n- 确保中文字体正确显示"
        
        # 5. 添加上下文信息
        if context:
            if "user_level" in context:
                level_guidance = {
                    "beginner": "- 添加详细的代码注释\n- 提供基础概念解释\n- 使用简单易懂的示例",
                    "intermediate": "- 平衡代码复杂度和功能\n- 提供扩展建议\n- 包含最佳实践说明",
                    "advanced": "- 使用高级特性和优化\n- 提供性能调优建议\n- 包含扩展性设计"
                }
                if context["user_level"] in level_guidance:
                    optimized += f"\n\n用户水平适配（{context['user_level']}）：\n{level_guidance[context['user_level']]}"
        
        return optimized
    
    def create_custom_template(self, template_name: str, content: str, 
                             metadata: Optional[Dict] = None) -> bool:
        """创建自定义模板"""
        
        try:
            # 保存到文件
            template_path = os.path.join(self.prompts_dir, f"{template_name}.txt")
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 更新缓存
            self.template_cache[template_name] = content
            self.template_metadata[template_name] = {
                "file_path": template_path,
                "created_at": datetime.now().isoformat(),
                "custom": True,
                "size": len(content),
                "word_count": len(content.split()),
                "line_count": len(content.split('\n')),
                **(metadata or {})
            }
            
            self.logger.info(f"已创建自定义模板: {template_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"创建自定义模板失败: {str(e)}")
            return False
    
    def update_template(self, template_name: str, content: str) -> bool:
        """更新现有模板"""
        
        if template_name not in self.template_cache:
            self.logger.warning(f"模板不存在，无法更新: {template_name}")
            return False
        
        try:
            # 备份原模板
            backup_content = self.template_cache[template_name]
            backup_path = os.path.join(self.prompts_dir, f"{template_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            # 更新模板
            template_path = self.template_metadata[template_name]["file_path"]
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 更新缓存
            self.template_cache[template_name] = content
            self.template_metadata[template_name].update({
                "updated_at": datetime.now().isoformat(),
                "size": len(content),
                "word_count": len(content.split()),
                "line_count": len(content.split('\n')),
                "backup_path": backup_path
            })
            
            self.logger.info(f"已更新模板: {template_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"更新模板失败: {str(e)}")
            return False
    
    def get_template_list(self) -> List[Dict]:
        """获取所有模板的列表和元数据"""
        
        template_list = []
        for name, metadata in self.template_metadata.items():
            usage_stats = self.usage_statistics.get(name, {})
            
            template_info = {
                "name": name,
                "size": metadata.get("size", 0),
                "word_count": metadata.get("word_count", 0),
                "line_count": metadata.get("line_count", 0),
                "created_at": metadata.get("created_at") or metadata.get("loaded_at"),
                "updated_at": metadata.get("updated_at"),
                "custom": metadata.get("custom", False),
                "usage_count": usage_stats.get("usage_count", 0),
                "last_used": usage_stats.get("last_used"),
                "category": self._categorize_template(name)
            }
            
            template_list.append(template_info)
        
        return sorted(template_list, key=lambda x: x["usage_count"], reverse=True)
    
    def _categorize_template(self, template_name: str) -> str:
        """根据模板名称分类"""
        
        if "math" in template_name:
            return "Mathematics"
        elif "stats" in template_name:
            return "Statistics"
        elif "physics" in template_name:
            return "Physics"
        elif "bio" in template_name:
            return "Biology"
        elif "chem" in template_name:
            return "Chemistry"
        elif "eng" in template_name:
            return "Engineering"
        elif "ds" in template_name or "ml" in template_name:
            return "DataScience"
        elif "general" in template_name:
            return "General"
        else:
            return "Other"
    
    def get_usage_statistics(self) -> Dict:
        """获取模板使用统计"""
        
        total_usage = sum(stats["usage_count"] for stats in self.usage_statistics.values())
        
        category_stats = {}
        for template_name, stats in self.usage_statistics.items():
            category = self._categorize_template(template_name)
            if category not in category_stats:
                category_stats[category] = {"count": 0, "usage": 0}
            category_stats[category]["count"] += 1
            category_stats[category]["usage"] += stats["usage_count"]
        
        return {
            "total_templates": len(self.template_cache),
            "total_usage": total_usage,
            "category_distribution": category_stats,
            "most_used": max(self.usage_statistics.items(), 
                           key=lambda x: x[1]["usage_count"]) if self.usage_statistics else None,
            "least_used": min(self.usage_statistics.items(), 
                            key=lambda x: x[1]["usage_count"]) if self.usage_statistics else None
        }
    
    def search_templates(self, query: str) -> List[Dict]:
        """搜索模板"""
        
        results = []
        query_lower = query.lower()
        
        for name, content in self.template_cache.items():
            score = 0
            
            # 名称匹配
            if query_lower in name.lower():
                score += 10
            
            # 内容匹配
            content_lower = content.lower()
            if query_lower in content_lower:
                score += 5
            
            # 关键词匹配
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in content_lower:
                    score += 2
            
            if score > 0:
                results.append({
                    "name": name,
                    "score": score,
                    "category": self._categorize_template(name),
                    "metadata": self.template_metadata.get(name, {})
                })
        
        return sorted(results, key=lambda x: x["score"], reverse=True)

# 全局Prompt管理器实例
prompt_manager = PromptManager()

def get_optimized_prompt(template_name: str, user_input: str, context: Dict = None) -> str:
    """便捷函数：获取优化的Prompt"""
    return prompt_manager.optimize_prompt(template_name, user_input, context)

def get_template_content(template_name: str) -> str:
    """便捷函数：获取模板内容"""
    return prompt_manager.get_template(template_name) or "模板未找到"
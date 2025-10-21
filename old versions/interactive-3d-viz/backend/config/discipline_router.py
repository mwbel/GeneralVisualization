import json
import os
import re
from typing import Dict, List, Optional

class DisciplineRouter:
    """学科分类路由器，用于根据用户输入自动选择合适的学科模板和模型"""
    
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "discipline_map.json")
        self.disciplines = self._load_disciplines()
    
    def _load_disciplines(self) -> Dict:
        """加载学科配置文件"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"配置文件未找到: {self.config_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"配置文件格式错误: {e}")
            return {}
    
    def classify_prompt(self, user_input: str) -> Dict:
        """
        根据用户输入分类学科并返回路由信息
        
        Args:
            user_input: 用户输入的文本
            
        Returns:
            包含学科、子领域、模板和推荐模型的字典
        """
        user_input_lower = user_input.lower()
        
        # 计算每个学科的匹配分数
        discipline_scores = {}
        
        for discipline, data in self.disciplines.items():
            score = 0
            matched_keywords = []
            
            # 检查主学科关键词
            for keyword in data["keywords"]:
                if keyword.lower() in user_input_lower:
                    score += 2  # 主学科关键词权重更高
                    matched_keywords.append(keyword)
            
            # 检查子领域关键词
            subfield_matches = {}
            for subfield, info in data["subfields"].items():
                subfield_score = 0
                subfield_keywords = []
                
                for sub_keyword in info["keywords"]:
                    if sub_keyword.lower() in user_input_lower:
                        subfield_score += 3  # 子领域关键词权重最高
                        subfield_keywords.append(sub_keyword)
                
                if subfield_score > 0:
                    subfield_matches[subfield] = {
                        "score": subfield_score,
                        "keywords": subfield_keywords,
                        "info": info
                    }
                    score += subfield_score
            
            if score > 0:
                discipline_scores[discipline] = {
                    "score": score,
                    "keywords": matched_keywords,
                    "subfields": subfield_matches
                }
        
        # 如果没有匹配，返回通用分类
        if not discipline_scores:
            return self._get_general_classification()
        
        # 选择得分最高的学科
        best_discipline = max(discipline_scores.keys(), key=lambda x: discipline_scores[x]["score"])
        best_data = discipline_scores[best_discipline]
        
        # 在最佳学科中选择最佳子领域
        if best_data["subfields"]:
            best_subfield = max(best_data["subfields"].keys(), 
                              key=lambda x: best_data["subfields"][x]["score"])
            subfield_info = best_data["subfields"][best_subfield]["info"]
            
            return {
                "discipline": best_discipline,
                "subfield": best_subfield,
                "template": subfield_info["template"],
                "models": subfield_info["models"],
                "confidence": min(best_data["score"] / 10.0, 1.0),  # 置信度评分
                "matched_keywords": best_data["keywords"] + best_data["subfields"][best_subfield]["keywords"]
            }
        else:
            # 如果没有子领域匹配，使用第一个子领域
            first_subfield = list(self.disciplines[best_discipline]["subfields"].keys())[0]
            first_info = self.disciplines[best_discipline]["subfields"][first_subfield]
            
            return {
                "discipline": best_discipline,
                "subfield": first_subfield,
                "template": first_info["template"],
                "models": first_info["models"],
                "confidence": min(best_data["score"] / 10.0, 1.0),
                "matched_keywords": best_data["keywords"]
            }
    
    def _get_general_classification(self) -> Dict:
        """返回通用分类"""
        general_info = self.disciplines["General"]["subfields"]["GenericVisualization"]
        return {
            "discipline": "General",
            "subfield": "GenericVisualization",
            "template": general_info["template"],
            "models": general_info["models"],
            "confidence": 0.1,
            "matched_keywords": []
        }
    
    def get_available_disciplines(self) -> List[str]:
        """获取所有可用的学科列表"""
        return list(self.disciplines.keys())
    
    def get_subfields(self, discipline: str) -> List[str]:
        """获取指定学科的所有子领域"""
        if discipline in self.disciplines:
            return list(self.disciplines[discipline]["subfields"].keys())
        return []
    
    def get_template_path(self, template_name: str) -> str:
        """获取模板文件的完整路径"""
        prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
        return os.path.join(prompts_dir, template_name)
    
    def analyze_input_complexity(self, user_input: str) -> Dict:
        """分析输入的复杂度和特征"""
        analysis = {
            "length": len(user_input),
            "has_numbers": bool(re.search(r'\d+', user_input)),
            "has_math_symbols": bool(re.search(r'[+\-*/=<>∫∑∏√]', user_input)),
            "has_3d_keywords": any(keyword in user_input.lower() for keyword in ['3d', '三维', '立体', '空间']),
            "has_interactive_keywords": any(keyword in user_input.lower() for keyword in ['交互', '动态', '可控', '参数']),
            "complexity_score": 0
        }
        
        # 计算复杂度分数
        if analysis["length"] > 50:
            analysis["complexity_score"] += 1
        if analysis["has_numbers"]:
            analysis["complexity_score"] += 1
        if analysis["has_math_symbols"]:
            analysis["complexity_score"] += 2
        if analysis["has_3d_keywords"]:
            analysis["complexity_score"] += 1
        if analysis["has_interactive_keywords"]:
            analysis["complexity_score"] += 1
            
        return analysis

# 全局路由器实例
router = DisciplineRouter()

def classify_prompt(user_input: str) -> Dict:
    """
    便捷函数：根据用户输入分类学科
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        包含学科、子领域、模板和推荐模型的字典
    """
    return router.classify_prompt(user_input)

def get_template_content(template_name: str) -> str:
    """
    获取模板文件内容
    
    Args:
        template_name: 模板文件名
        
    Returns:
        模板内容字符串
    """
    template_path = router.get_template_path(template_name)
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "模板文件未找到，请使用通用可视化模板。"
    except Exception as e:
        return f"读取模板文件时出错: {e}"

def analyze_and_route(user_input: str) -> Dict:
    """
    综合分析用户输入并返回完整的路由信息
    
    Args:
        user_input: 用户输入的文本
        
    Returns:
        包含分类结果、复杂度分析和模板内容的完整信息
    """
    classification = router.classify_prompt(user_input)
    complexity = router.analyze_input_complexity(user_input)
    template_content = get_template_content(classification["template"])
    
    return {
        "classification": classification,
        "complexity": complexity,
        "template_content": template_content,
        "recommended_approach": _get_recommended_approach(classification, complexity)
    }

def _get_recommended_approach(classification: Dict, complexity: Dict) -> str:
    """根据分类和复杂度推荐处理方法"""
    if complexity["complexity_score"] >= 4:
        return "high_complexity"
    elif complexity["complexity_score"] >= 2:
        return "medium_complexity"
    else:
        return "simple_visualization"
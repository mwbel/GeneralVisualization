#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统功能测试脚本
测试学科分类、路由和模板加载功能
"""

import sys
import os
import json
from typing import Dict, List

# 添加项目路径
sys.path.append(os.path.dirname(__file__))

def test_config_loading():
    """测试配置文件加载"""
    print("🔧 测试配置文件加载...")
    
    try:
        from config.discipline_router import classify_prompt
        print("✅ discipline_router.py 导入成功")
        
        # 测试配置文件是否存在
        config_path = os.path.join(os.path.dirname(__file__), "config", "discipline_map.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ discipline_map.json 加载成功，包含 {len(config)} 个学科")
            return True
        else:
            print("❌ discipline_map.json 文件不存在")
            return False
            
    except Exception as e:
        print(f"❌ 配置加载失败: {str(e)}")
        return False

def test_prompt_templates():
    """测试Prompt模板加载"""
    print("\n📝 测试Prompt模板加载...")
    
    try:
        from ai_engine.prompt_manager import prompt_manager
        
        # 获取模板列表
        templates = prompt_manager.get_template_list()
        print(f"✅ 成功加载 {len(templates)} 个模板")
        
        # 显示模板信息
        for template in templates:
            print(f"  - {template['name']} ({template['category']}) - {template['word_count']} 词")
        
        return len(templates) > 0
        
    except Exception as e:
        print(f"❌ 模板加载失败: {str(e)}")
        return False

def test_classification_routing():
    """测试学科分类和路由功能"""
    print("\n🎯 测试学科分类和路由功能...")
    
    try:
        from config.discipline_router import classify_prompt
        
        # 测试用例
        test_cases = [
            {
                "input": "请生成一个展示行列式几何意义的3D可视化",
                "expected_discipline": "Mathematics",
                "expected_subfield": "LinearAlgebra"
            },
            {
                "input": "我想看正态分布和泊松分布的对比图",
                "expected_discipline": "Statistics",
                "expected_subfield": "Distributions"
            },
            {
                "input": "生成太阳地球月球的轨道演示",
                "expected_discipline": "Physics",
                "expected_subfield": "Astronomy"
            },
            {
                "input": "显示人体循环系统的3D结构",
                "expected_discipline": "Biology",
                "expected_subfield": "Anatomy"
            },
            {
                "input": "创建一个通用的数据可视化图表",
                "expected_discipline": "General",
                "expected_subfield": "GenericVisualization"
            }
        ]
        
        success_count = 0
        for i, case in enumerate(test_cases, 1):
            result = classify_prompt(case["input"])
            
            print(f"\n测试用例 {i}: {case['input'][:30]}...")
            print(f"  预期: {case['expected_discipline']} -> {case['expected_subfield']}")
            print(f"  实际: {result['discipline']} -> {result['subfield']}")
            print(f"  模板: {result['template']}")
            print(f"  推荐模型: {result['models']}")
            
            if (result['discipline'] == case['expected_discipline'] and 
                result['subfield'] == case['expected_subfield']):
                print("  ✅ 分类正确")
                success_count += 1
            else:
                print("  ⚠️ 分类不完全匹配")
        
        print(f"\n分类准确率: {success_count}/{len(test_cases)} ({success_count/len(test_cases)*100:.1f}%)")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ 分类路由测试失败: {str(e)}")
        return False

def test_template_optimization():
    """测试模板优化功能"""
    print("\n⚡ 测试模板优化功能...")
    
    try:
        from ai_engine.prompt_manager import get_optimized_prompt
        
        # 测试模板优化
        user_input = "生成一个3D交互式的行列式几何可视化，要求有动画效果和颜色配色"
        template_name = "visual_math_linear_algebra_prompt"
        
        optimized_prompt = get_optimized_prompt(template_name, user_input)
        
        if optimized_prompt and optimized_prompt != "模板未找到":
            print("✅ 模板优化成功")
            print(f"优化后的Prompt长度: {len(optimized_prompt)} 字符")
            
            # 检查是否包含优化内容
            optimization_indicators = ["3D效果", "交互功能", "动画效果", "颜色设计"]
            found_optimizations = [ind for ind in optimization_indicators if ind in optimized_prompt]
            
            if found_optimizations:
                print(f"✅ 检测到优化内容: {', '.join(found_optimizations)}")
                return True
            else:
                print("⚠️ 未检测到明显的优化内容")
                return False
        else:
            print("❌ 模板优化失败")
            return False
            
    except Exception as e:
        print(f"❌ 模板优化测试失败: {str(e)}")
        return False

def test_code_generation():
    """测试代码生成功能"""
    print("\n🚀 测试代码生成功能...")
    
    try:
        from ai_engine.code_generator import generate_code
        
        # 测试代码生成
        user_input = "生成一个简单的3D散点图"
        
        result = generate_code(
            user_input=user_input,
            preferred_model="gpt-4",
            complexity_override="medium"
        )
        
        if result and result.get("success"):
            print("✅ 代码生成成功")
            print(f"生成的代码长度: {len(result.get('code', ''))} 字符")
            print(f"使用的学科: {result.get('discipline', 'Unknown')}")
            print(f"使用的模板: {result.get('template', 'Unknown')}")
            print(f"推荐模型: {result.get('recommended_models', [])}")
            
            # 检查代码是否包含基本元素
            code = result.get('code', '')
            if 'import' in code and 'plotly' in code.lower():
                print("✅ 代码包含必要的导入语句")
                return True
            else:
                print("⚠️ 代码可能不完整")
                return False
        else:
            print("❌ 代码生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 代码生成测试失败: {str(e)}")
        return False

def test_system_integration():
    """测试系统集成"""
    print("\n🔗 测试系统集成...")
    
    try:
        # 测试完整的工作流程
        from config.discipline_router import classify_prompt
        from ai_engine.prompt_manager import get_optimized_prompt
        from ai_engine.code_generator import AICodeGenerator
        
        # 创建代码生成器实例
        generator = AICodeGenerator()
        
        # 模拟完整流程
        user_input = "创建一个展示正态分布概率密度函数的交互式图表"
        
        # 1. 分类路由
        classification = classify_prompt(user_input)
        print(f"✅ 分类结果: {classification['discipline']} -> {classification['subfield']}")
        
        # 2. 模板优化
        optimized_prompt = get_optimized_prompt(classification['template'], user_input)
        print(f"✅ 模板优化完成，长度: {len(optimized_prompt)} 字符")
        
        # 3. 模型选择
        selected_model = generator._select_optimal_model(
            routing_result=classification,
            preferred_model="gpt-4",
            complexity_override="medium"
        )
        print(f"✅ 选择模型: {selected_model}")
        
        # 4. 代码生成（模拟）
        routing_result = {"classification": classification}
        generated_code = generator._simulate_ai_generation(
            optimized_prompt, 
            selected_model,
            routing_result
        )
        print(f"✅ 代码生成完成，长度: {len(generated_code)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 系统集成测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始系统功能测试")
    print("=" * 50)
    
    tests = [
        ("配置文件加载", test_config_loading),
        ("Prompt模板加载", test_prompt_templates),
        ("学科分类路由", test_classification_routing),
        ("模板优化", test_template_optimization),
        ("代码生成", test_code_generation),
        ("系统集成", test_system_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {str(e)}")
            results.append((test_name, False))
    
    # 输出测试总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体通过率: {passed}/{len(results)} ({passed/len(results)*100:.1f}%)")
    
    if passed == len(results):
        print("\n🎉 所有测试通过！系统部署成功！")
    elif passed >= len(results) * 0.8:
        print("\n✅ 大部分测试通过，系统基本可用")
    else:
        print("\n⚠️ 多个测试失败，需要检查系统配置")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
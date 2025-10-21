#!/usr/bin/env python3
"""
交互式3D可视化应用系统测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查"""
    print("🔍 测试健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ 健康检查通过")
        return True
    else:
        print("❌ 健康检查失败")
        return False

def test_code_templates():
    """测试代码模板API"""
    print("🔍 测试代码模板API...")
    response = requests.get(f"{BASE_URL}/api/v1/code/templates")
    if response.status_code == 200:
        templates = response.json()
        print(f"✅ 获取到 {len(templates)} 个代码模板")
        return True
    else:
        print("❌ 代码模板API失败")
        return False

def test_visualization_examples():
    """测试可视化示例API"""
    print("🔍 测试可视化示例API...")
    response = requests.get(f"{BASE_URL}/api/v1/visualization/examples")
    if response.status_code == 200:
        examples = response.json()
        print(f"✅ 获取到 {len(examples)} 个可视化示例")
        return True
    else:
        print("❌ 可视化示例API失败")
        return False

def test_code_generation():
    """测试代码生成API"""
    print("🔍 测试代码生成API...")
    data = {
        "prompt": "创建一个3D散点图显示股票价格数据",
        "visualization_type": "scatter_3d"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/code/generate",
        headers={"Content-Type": "application/json"},
        json=data
    )
    if response.status_code == 200:
        result = response.json()
        print("✅ 代码生成成功")
        print(f"   生成的代码长度: {len(result['python_code'])} 字符")
        return True
    else:
        print("❌ 代码生成失败")
        return False

def test_visualization_generation():
    """测试可视化生成API"""
    print("🔍 测试可视化生成API...")
    data = {
        "title": "测试3D图表",
        "visualization_type": "scatter_3d",
        "data": {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 20, 30, 40, 50],
            "z": [100, 200, 300, 400, 500]
        },
        "parameters": {"color": "blue"}
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/visualization/generate",
        headers={"Content-Type": "application/json"},
        json=data
    )
    if response.status_code == 200:
        result = response.json()
        print("✅ 可视化生成成功")
        print(f"   生成的HTML长度: {len(result['html_output'])} 字符")
        return True
    else:
        print("❌ 可视化生成失败")
        return False

def test_file_upload():
    """测试文件上传API"""
    print("🔍 测试文件上传API...")
    
    # 创建测试CSV文件
    test_data = "x,y,z\n1,4,7\n2,5,8\n3,6,9\n"
    
    files = {'file': ('test.csv', test_data, 'text/csv')}
    response = requests.post(f"{BASE_URL}/api/v1/upload/", files=files)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 文件上传成功")
        print(f"   文件ID: {result['file_info']['file_id']}")
        print(f"   数据行数: {result['file_info']['rows']}")
        return True
    else:
        print("❌ 文件上传失败")
        return False

def main():
    """运行所有测试"""
    print("🚀 开始系统测试...\n")
    
    tests = [
        test_health_check,
        test_code_templates,
        test_visualization_examples,
        test_code_generation,
        test_visualization_generation,
        test_file_upload
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ 测试异常: {e}\n")
    
    print("=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
    else:
        print("⚠️  部分测试失败，请检查系统状态。")

if __name__ == "__main__":
    main()
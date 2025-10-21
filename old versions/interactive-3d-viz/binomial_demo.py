#!/usr/bin/env python3
"""
二项分布B(n,p)可视化示例 - 通过API生成
"""

import requests
import json

def test_binomial_visualization():
    """测试二项分布可视化生成"""
    
    # API端点
    base_url = "http://localhost:8000/api/v1"
    
    # 1. 固定n，变化p的可视化
    print("🎲 生成固定n=20，p变化的二项分布可视化...")
    
    prompt_fixed_n = """
请创建一个二项分布B(n,p)的可视化，其中：
1. 固定n=20，让p在[0.1, 0.3, 0.5, 0.7, 0.9]中变化
2. 绘制每个p值对应的概率质量函数
3. 使用不同颜色的线条和标记点
4. 添加图例说明每条线对应的p值
5. x轴为成功次数k (0到20)，y轴为概率P(X=k)
6. 标题为"二项分布B(20,p) - 固定n=20，p变化"
"""
    
    response1 = requests.post(
        f"{base_url}/code/generate",
        json={
            "prompt": prompt_fixed_n,
            "visualization_type": "custom"
        }
    )
    
    if response1.status_code == 200:
        result1 = response1.json()
        print("✅ 固定n的可视化代码生成成功")
        
        # 保存代码
        with open("binomial_fixed_n.py", "w", encoding="utf-8") as f:
            f.write(result1["python_code"])
        print("📁 代码已保存到: binomial_fixed_n.py")
    else:
        print(f"❌ 请求失败: {response1.status_code}")
        return
    
    # 2. 固定p，变化n的可视化
    print("\n🎲 生成固定p=0.3，n变化的二项分布可视化...")
    
    prompt_fixed_p = """
请创建一个二项分布B(n,p)的可视化，其中：
1. 固定p=0.3，让n在[5, 10, 20, 30, 50]中变化
2. 绘制每个n值对应的概率质量函数
3. 使用不同颜色的线条和标记点
4. 添加图例说明每条线对应的n值
5. x轴为成功次数k，y轴为概率P(X=k)
6. 标题为"二项分布B(n,0.3) - 固定p=0.3，n变化"
7. 注意不同n值的x轴范围不同，可以限制显示范围到合理区间
"""
    
    response2 = requests.post(
        f"{base_url}/code/generate",
        json={
            "prompt": prompt_fixed_p,
            "visualization_type": "custom"
        }
    )
    
    if response2.status_code == 200:
        result2 = response2.json()
        print("✅ 固定p的可视化代码生成成功")
        
        # 保存代码
        with open("binomial_fixed_p.py", "w", encoding="utf-8") as f:
            f.write(result2["python_code"])
        print("📁 代码已保存到: binomial_fixed_p.py")
    else:
        print(f"❌ 请求失败: {response2.status_code}")
        return
    
    # 3. 3D可视化 - n和p同时变化
    print("\n🎲 生成3D二项分布可视化...")
    
    prompt_3d = """
请创建一个3D二项分布可视化，展示参数n和p同时变化的效果：
1. 创建一个3D表面图，x轴为n (5到30)，y轴为p (0.1到0.9)
2. z轴显示二项分布的期望值 E[X] = n*p
3. 使用颜色映射显示数值大小
4. 添加另一个子图显示方差 Var[X] = n*p*(1-p) 的热力图
5. 标题为"二项分布B(n,p)参数影响 - 期望值和方差"
6. 使用plotly创建交互式图表
"""
    
    response3 = requests.post(
        f"{base_url}/code/generate",
        json={
            "prompt": prompt_3d,
            "visualization_type": "surface_3d"
        }
    )
    
    if response3.status_code == 200:
        result3 = response3.json()
        print("✅ 3D可视化代码生成成功")
        
        # 保存代码
        with open("binomial_3d.py", "w", encoding="utf-8") as f:
            f.write(result3["python_code"])
        print("📁 代码已保存到: binomial_3d.py")
    else:
        print(f"❌ 请求失败: {response3.status_code}")
        return
    
    # 4. 使用visualization API生成示例
    print("\n🎲 使用visualization API生成二项分布示例...")
    
    # 生成一些示例数据
    sample_data = {
        "n_values": [10, 20, 30],
        "p_values": [0.2, 0.5, 0.8],
        "k_range": list(range(0, 31))
    }
    
    viz_response = requests.post(
        f"{base_url}/visualization/generate",
        json={
            "title": "二项分布B(n,p)参数影响可视化",
            "visualization_type": "scatter_3d",
            "data": sample_data,
            "parameters": {
                "x_axis": "k_range",
                "y_axis": "p_values", 
                "z_axis": "n_values",
                "color_by": "probability",
                "size_by": "probability"
            }
        }
    )
    
    if viz_response.status_code == 200:
        viz_result = viz_response.json()
        print("✅ Visualization API调用成功")
        print(f"📊 预览URL: {viz_result.get('preview_url', 'N/A')}")
        print(f"📥 下载URL: {viz_result.get('download_url', 'N/A')}")
    else:
        print(f"❌ Visualization API请求失败: {viz_response.status_code}")
    
    print("\n🎯 二项分布可视化示例生成完成！")
    print("📚 生成的文件:")
    print("  - binomial_fixed_n.py: 固定n=20，p变化")
    print("  - binomial_fixed_p.py: 固定p=0.3，n变化") 
    print("  - binomial_3d.py: 3D参数影响可视化")
    
    print("\n📖 二项分布B(n,p)特性总结:")
    print("  • 期望值: E[X] = n × p")
    print("  • 方差: Var[X] = n × p × (1-p)")
    print("  • 当p=0.5时分布最对称")
    print("  • n增大时趋向正态分布")
    print("  • p接近0或1时分布明显偏斜")

if __name__ == "__main__":
    test_binomial_visualization()
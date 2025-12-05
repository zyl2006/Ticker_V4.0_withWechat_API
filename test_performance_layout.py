#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试性能和布局修复效果
"""

import requests
import json
import time

def test_performance_optimization():
    """测试性能优化效果"""
    print("测试性能优化效果...")
    
    # 测试数据
    test_data = {
        "style": "red15",
        "user_data": {
            "出发站": "北京",
            "到达站": "上海",
            "车次": "G1",
            "日期": "2024-01-01",
            "时间": "08:00",
            "座位号": "01车01A",
            "票价": "553元"
        },
        "format": "base64"
    }
    
    try:
        print("发送生成请求...")
        start_time = time.time()
        
        response = requests.post(
            'http://127.0.0.1:5001/api/generate',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"响应时间: {response_time:.2f}秒")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                base64_size = len(data.get('data', {}).get('image_base64', ''))
                print(f"生成的图片大小: {base64_size} 字符")
                print(f"图片大小: {base64_size / 1024:.1f} KB")
                
                # 性能评估
                if response_time < 3.0:
                    print("性能评估: 优秀")
                elif response_time < 5.0:
                    print("性能评估: 良好")
                else:
                    print("性能评估: 需要优化")
                
                return True
            else:
                print(f"生成失败: {data.get('error')}")
                return False
        else:
            print(f"请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"测试异常: {e}")
        return False

def test_api_server_status():
    """测试API服务器状态"""
    print("检查API服务器状态...")
    
    try:
        response = requests.get('http://127.0.0.1:5001/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"API服务器正常运行")
            print(f"   状态: {data.get('status')}")
            print(f"   可用样式: {data.get('available_styles')}")
            return True
        else:
            print(f"API服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"API服务器连接失败: {e}")
        return False

def test_multiple_styles():
    """测试多种样式"""
    print("\n测试多种样式...")
    
    styles = ['red15', 'blue15', 'red05_longride', 'red05_shortride', 'red1997']
    success_count = 0
    
    for style in styles:
        try:
            print(f"测试样式: {style}")
            
            test_data = {
                "style": style,
                "user_data": {
                    "出发站": "北京",
                    "到达站": "上海"
                },
                "format": "base64"
            }
            
            response = requests.post(
                'http://127.0.0.1:5001/api/generate',
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"  样式 {style} 生成成功")
                    success_count += 1
                else:
                    print(f"  样式 {style} 生成失败: {data.get('error')}")
            else:
                print(f"  样式 {style} 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"  样式 {style} 异常: {e}")
    
    print(f"样式测试结果: {success_count}/{len(styles)} 成功")
    return success_count > 0

def main():
    """主测试函数"""
    print("开始测试性能和布局修复效果")
    print("=" * 50)
    
    # 检查API服务器
    if not test_api_server_status():
        print("API服务器不可用，无法进行测试")
        return False
    
    # 测试性能优化
    print("\n" + "=" * 30)
    if test_performance_optimization():
        print("性能优化测试通过")
    else:
        print("性能优化测试失败")
    
    # 测试多种样式
    print("\n" + "=" * 30)
    if test_multiple_styles():
        print("多样式测试通过")
    else:
        print("多样式测试失败")
    
    print("\n" + "=" * 50)
    print("修复说明:")
    print("1. 性能优化:")
    print("   - 将base64图片数据保存为临时文件")
    print("   - 减少setData传输的数据量")
    print("   - 避免2557KB数据传输性能问题")
    print()
    print("2. 布局优化:")
    print("   - 预览窗格固定在顶部")
    print("   - 下方内容区域可滚动")
    print("   - 优化样式选择布局")
    print("   - 改进表单字段间距")
    print("   - 响应式设计优化")
    print()
    print("3. 用户体验改进:")
    print("   - 预览始终可见")
    print("   - 输入和预览同时进行")
    print("   - 更紧凑的界面布局")
    print("   - 更好的视觉层次")
    
    return True

if __name__ == "__main__":
    main()

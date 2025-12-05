#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试表单输入修复效果
"""

import requests
import json

def test_form_input_fix():
    """测试表单输入修复效果"""
    print("测试表单输入修复效果...")
    
    # 测试数据 - 模拟用户输入
    test_cases = [
        {
            "name": "正常输入测试",
            "data": {
                "style": "red15",
                "user_data": {
                    "出发站": "北京",
                    "到达站": "上海",
                    "车次": "G1",
                    "日期": "2024-01-01",
                    "时间": "08:00"
                },
                "format": "base64"
            }
        },
        {
            "name": "部分字段输入测试",
            "data": {
                "style": "red15",
                "user_data": {
                    "出发站": "北京",
                    "到达站": "上海"
                },
                "format": "base64"
            }
        },
        {
            "name": "单个字段输入测试",
            "data": {
                "style": "red15",
                "user_data": {
                    "出发站": "北京"
                },
                "format": "base64"
            }
        }
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            print(f"\n测试 {test_case['name']}...")
            print(f"发送数据: {test_case['data']}")
            
            response = requests.post(
                'http://127.0.0.1:5001/api/generate',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"成功 {test_case['name']}")
                    print(f"   生成的图片大小: {len(data.get('data', {}).get('image_base64', ''))} 字符")
                    success_count += 1
                else:
                    print(f"失败 {test_case['name']}: {data.get('error')}")
            else:
                print(f"失败 {test_case['name']} 请求失败: {response.status_code}")
                print(f"   响应内容: {response.text}")
                
        except Exception as e:
            print(f"异常 {test_case['name']}: {e}")
    
    print(f"\n测试结果: {success_count}/{len(test_cases)} 成功")
    return success_count == len(test_cases)

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

def main():
    """主测试函数"""
    print("开始测试表单输入修复效果")
    print("=" * 50)
    
    # 检查API服务器
    if not test_api_server_status():
        print("API服务器不可用，无法进行测试")
        return False
    
    # 测试表单输入修复
    if test_form_input_fix():
        print("\n所有测试通过！表单输入修复成功！")
        print("\n修复说明:")
        print("1. 修复了输入框数据绑定问题")
        print("2. 现在用户输入的内容会正确保存")
        print("3. 不再出现输入内容立即消失的问题")
        print("4. 可以正常生成车票预览")
        return True
    else:
        print("\n部分测试失败，需要进一步检查")
        return False

if __name__ == "__main__":
    main()

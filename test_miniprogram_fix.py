#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小程序修复效果
"""

import requests
import json
import time

def test_api_server():
    """测试API服务器是否正常运行"""
    print("测试API服务器...")
    
    try:
        # 测试健康检查
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

def test_generate_ticket():
    """测试生成车票功能"""
    print("\n测试生成车票功能...")
    
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
        response = requests.post(
            'http://127.0.0.1:5001/api/generate',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("车票生成成功")
                print(f"   样式: {data.get('data', {}).get('style')}")
                print(f"   图片格式: {data.get('data', {}).get('format')}")
                print(f"   图片大小: {len(data.get('data', {}).get('image_base64', ''))} 字符")
                return True
            else:
                print(f"车票生成失败: {data.get('error')}")
                return False
        else:
            print(f"请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"生成车票请求失败: {e}")
        return False

def test_multiple_formats():
    """测试多种数据格式"""
    print("\n📝 测试多种数据格式...")
    
    # 测试不同的请求格式
    test_cases = [
        {
            "name": "标准JSON格式",
            "data": {
                "style": "red15",
                "user_data": {"出发站": "北京", "到达站": "上海"},
                "format": "base64"
            },
            "headers": {"Content-Type": "application/json"}
        },
        {
            "name": "表单格式",
            "data": "style=red15&user_data[出发站]=北京&user_data[到达站]=上海&format=base64",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"}
        }
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            print(f"   测试 {test_case['name']}...")
            
            if test_case['headers']['Content-Type'] == 'application/json':
                response = requests.post(
                    'http://127.0.0.1:5001/api/generate',
                    json=test_case['data'],
                    headers=test_case['headers'],
                    timeout=5
                )
            else:
                response = requests.post(
                    'http://127.0.0.1:5001/api/generate',
                    data=test_case['data'],
                    headers=test_case['headers'],
                    timeout=5
                )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ {test_case['name']} 成功")
                    success_count += 1
                else:
                    print(f"   ❌ {test_case['name']} 失败: {data.get('error')}")
            else:
                print(f"   ❌ {test_case['name']} 请求失败: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {test_case['name']} 异常: {e}")
    
    print(f"   多格式测试完成: {success_count}/{len(test_cases)} 成功")
    return success_count > 0

def test_error_handling():
    """测试错误处理"""
    print("\n⚠️ 测试错误处理...")
    
    error_cases = [
        {
            "name": "空数据",
            "data": None,
            "expected_status": 400
        },
        {
            "name": "无效样式",
            "data": {
                "style": "invalid_style",
                "user_data": {"出发站": "北京"},
                "format": "base64"
            },
            "expected_status": 400
        },
        {
            "name": "空用户数据",
            "data": {
                "style": "red15",
                "user_data": {},
                "format": "base64"
            },
            "expected_status": 400
        }
    ]
    
    success_count = 0
    for test_case in error_cases:
        try:
            print(f"   测试 {test_case['name']}...")
            
            response = requests.post(
                'http://127.0.0.1:5001/api/generate',
                json=test_case['data'],
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == test_case['expected_status']:
                print(f"   ✅ {test_case['name']} 错误处理正确")
                success_count += 1
            else:
                print(f"   ❌ {test_case['name']} 错误处理异常: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {test_case['name']} 异常: {e}")
    
    print(f"   错误处理测试完成: {success_count}/{len(error_cases)} 成功")
    return success_count > 0

def main():
    """主测试函数"""
    print("开始测试小程序修复效果")
    print("=" * 50)
    
    # 等待API服务器启动
    print("等待API服务器启动...")
    time.sleep(2)
    
    # 执行测试
    tests = [
        ("API服务器", test_api_server),
        ("生成车票", test_generate_ticket),
        ("多格式支持", test_multiple_formats),
        ("错误处理", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"错误 {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    
    success_count = 0
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"   {test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("所有测试通过！小程序修复成功！")
    else:
        print("部分测试失败，需要进一步检查")
    
    return success_count == len(results)

if __name__ == "__main__":
    main()
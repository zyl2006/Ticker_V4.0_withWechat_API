#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小程序修复效果 - 简化版
"""

import requests
import json
import time

def test_api_server():
    """测试API服务器是否正常运行"""
    print("测试API服务器...")
    
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

def test_generate_ticket():
    """测试生成车票功能"""
    print("\n测试生成车票功能...")
    
    test_data = {
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
                return True
            else:
                print(f"车票生成失败: {data.get('error')}")
                return False
        else:
            print(f"请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"生成车票请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试小程序修复效果")
    print("=" * 50)
    
    time.sleep(2)
    
    tests = [
        ("API服务器", test_api_server),
        ("生成车票", test_generate_ticket)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"错误 {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
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

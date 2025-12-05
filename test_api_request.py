#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API请求格式
"""

import requests
import json

def test_api_request():
    """测试API请求格式"""
    print("测试API请求格式...")
    
    # 测试数据
    test_data = {
        'style': 'red15',
        'user_data': {
            '姓名': '测试用户',
            '车次号': 'G1234',
            '座位号': '01A',
            '出发站': '北京',
            '到达站': '上海'
        },
        'format': 'base64'
    }
    
    try:
        response = requests.post(
            'http://api.sgsky.tech/api/generate',
            json=test_data,
            timeout=10
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应结果: {result}")
            
            if result.get('success'):
                print("SUCCESS API请求成功！")
                return True
            else:
                print(f"FAIL API返回错误: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"FAIL HTTP错误: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL 请求异常: {e}")
        return False

def test_health_check():
    """测试健康检查"""
    print("\n测试健康检查...")
    
    try:
        response = requests.get('http://api.sgsky.tech/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"健康检查成功: {data.get('status', 'unknown')}")
            return True
        else:
            print(f"健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"健康检查异常: {e}")
        return False

def main():
    """主函数"""
    print("API请求格式测试")
    print("=" * 40)
    
    # 测试健康检查
    health_ok = test_health_check()
    
    # 测试API请求
    api_ok = test_api_request()
    
    print("\n" + "=" * 40)
    print("测试结果:")
    print(f"健康检查: {'正常' if health_ok else '异常'}")
    print(f"API请求: {'正常' if api_ok else '异常'}")
    
    if health_ok and api_ok:
        print("\nSUCCESS 所有测试通过！")
        print("现在小程序应该能正常生成预览了")
    else:
        print("\nFAIL 存在问题需要解决")
        if not health_ok:
            print("- API服务器连接问题")
        if not api_ok:
            print("- API请求格式问题")

if __name__ == "__main__":
    main()

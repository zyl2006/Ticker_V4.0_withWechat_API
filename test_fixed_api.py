#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的API请求
"""

import requests
import json

def test_fixed_request():
    """测试修复后的请求"""
    print("测试修复后的API请求...")
    
    # 包含所有必要字段的测试数据
    test_data = {
        'style': 'red15',
        'user_data': {
            '姓名': '测试用户',
            '车次号': 'G1234',
            '座位号': '01A',
            '出发站': '北京',
            '到达站': '上海',
            '车次类型': '高铁',
            '票价': '553.0',
            '票号': 'E123456789'
        },
        'format': 'base64'
    }
    
    try:
        response = requests.post(
            'http://api.sgsky.tech/api/generate',
            json=test_data,
            timeout=15
        )
        
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应结果: {result}")
            
            if result.get('success'):
                print("SUCCESS API请求成功！")
                print(f"生成了图片数据，长度: {len(result.get('data', {}).get('image_base64', ''))}")
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

def main():
    """主函数"""
    print("修复后的API请求测试")
    print("=" * 40)
    
    success = test_fixed_request()
    
    print("\n" + "=" * 40)
    if success:
        print("SUCCESS 修复成功！")
        print("现在小程序应该能正常生成预览了")
        print("\n请在微信开发者工具中:")
        print("1. 重新编译小程序")
        print("2. 填写完整的表单信息")
        print("3. 点击'生成预览'按钮")
    else:
        print("FAIL 仍有问题需要解决")

if __name__ == "__main__":
    main()

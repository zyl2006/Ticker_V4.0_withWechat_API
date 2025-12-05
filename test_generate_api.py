#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API生成请求
"""

import requests
import json

def test_generate_api():
    """测试生成API"""
    print("测试生成API")
    print("=" * 30)
    
    # 测试数据
    test_data = {
        "style": "red15",
        "user_data": {
            "姓名": "测试用户",
            "车次号": "G1234",
            "出发站": "北京",
            "到达站": "上海",
            "席位号": "01A",
            "车次类型": "高铁",
            "票价1": "553",
            "年": "2024",
            "月": "01",
            "日": "15",
            "时": "14",
            "分": "30",
            "席别": "二等座",
            "票种": "成人票",
            "身份证号1": "123456789012345678",
            "身份证号2": "123456789012345678",
            "证件类型": "身份证",
            "发售站": "北京站"
        },
        "format": "base64"
    }
    
    try:
        response = requests.post('http://127.0.0.1:5001/api/generate', json=test_data)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS API调用成功!")
                print(f"图片数据大小: {len(result.get('data', {}).get('image_base64', ''))} 字符")
                return True
            else:
                print(f"FAIL API返回错误: {result.get('error')}")
                return False
        else:
            print(f"FAIL HTTP错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL 请求异常: {e}")
        return False

def test_minimal_data():
    """测试最小数据"""
    print("\n测试最小数据")
    print("=" * 30)
    
    # 最小测试数据
    minimal_data = {
        "style": "red15",
        "user_data": {
            "姓名": "测试",
            "车次号": "G1234",
            "出发站": "北京",
            "到达站": "上海",
            "席位号": "01A"
        },
        "format": "base64"
    }
    
    try:
        response = requests.post('http://127.0.0.1:5001/api/generate', json=minimal_data)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS 最小数据测试成功!")
                return True
            else:
                print(f"FAIL 最小数据测试失败: {result.get('error')}")
                return False
        else:
            print(f"FAIL HTTP错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("API生成请求测试")
    print("=" * 40)
    
    # 测试完整数据
    success1 = test_generate_api()
    
    # 测试最小数据
    success2 = test_minimal_data()
    
    print("\n" + "=" * 40)
    if success1 or success2:
        print("SUCCESS API测试通过!")
        print("问题可能在小程序的数据格式")
    else:
        print("FAIL API测试失败")
        print("需要检查API服务器")

if __name__ == "__main__":
    main()

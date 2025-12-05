#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小程序数据格式修复
"""

import requests
import json

def test_miniprogram_data_format():
    """测试小程序数据格式"""
    print("测试小程序数据格式")
    print("=" * 30)
    
    # 模拟小程序发送的数据格式
    miniprogram_data = {
        "style": "red15",
        "user_data": {
            # 必填字段（小程序现在会确保这些字段存在）
            "姓名": "测试用户",
            "车次号": "G1234", 
            "席位号": "01A",
            "出发站": "北京",
            "到达站": "上海",
            # 其他字段（用户填写的）
            "车次类型": "高铁",
            "票价1": "553",
            "年": "2024",
            "月": "01",
            "日": "15",
            "时": "14",
            "分": "30"
        },
        "format": "base64"
    }
    
    try:
        response = requests.post('http://127.0.0.1:5001/api/generate', json=miniprogram_data)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS 小程序数据格式测试成功!")
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

def test_missing_required_fields():
    """测试缺少必填字段的情况"""
    print("\n测试缺少必填字段")
    print("=" * 30)
    
    # 缺少必填字段的数据
    incomplete_data = {
        "style": "red15",
        "user_data": {
            "姓名": "测试用户",
            "车次号": "G1234"
            # 缺少: 席位号, 出发站, 到达站
        },
        "format": "base64"
    }
    
    try:
        response = requests.post('http://127.0.0.1:5001/api/generate', json=incomplete_data)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print(f"EXPECTED 400错误: {result.get('error')}")
            return True
        else:
            print(f"UNEXPECTED 状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"FAIL 请求异常: {e}")
        return False

def main():
    """主函数"""
    print("小程序数据格式修复测试")
    print("=" * 40)
    
    # 测试修复后的数据格式
    success1 = test_miniprogram_data_format()
    
    # 测试缺少必填字段的情况
    success2 = test_missing_required_fields()
    
    print("\n" + "=" * 40)
    if success1 and success2:
        print("SUCCESS 数据格式修复成功!")
        print("小程序现在应该可以正常生成预览了")
        print("\n请在微信开发者工具中:")
        print("  1. 重新编译小程序")
        print("  2. 填写一些字段信息")
        print("  3. 点击生成预览")
        print("  4. 应该不再有400错误")
    else:
        print("FAIL 数据格式仍有问题")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试重构后的小程序API流程
"""

import requests
import json

def test_complete_flow():
    """测试完整的API流程"""
    print("测试重构后的完整API流程")
    print("=" * 50)
    
    # 1. 健康检查
    print("1. 健康检查...")
    try:
        response = requests.get('http://api.sgsky.tech/api/health')
        if response.status_code == 200:
            result = response.json()
            print(f"   OK 健康检查成功: {result.get('status')}")
            print(f"   可用样式: {result.get('available_styles', [])}")
        else:
            print(f"   FAIL 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL 健康检查异常: {e}")
        return False
    
    # 2. 获取样式列表
    print("\n2. 获取样式列表...")
    try:
        response = requests.get('http://api.sgsky.tech/api/styles')
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                styles = result.get('styles', [])
                print(f"   OK 样式列表获取成功: {len(styles)} 个样式")
                print(f"   样式: {styles}")
            else:
                print(f"   FAIL 样式列表获取失败: {result.get('error')}")
                return False
        else:
            print(f"   FAIL 样式列表请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL 样式列表异常: {e}")
        return False
    
    # 3. 获取模板信息
    print("\n3. 获取模板信息...")
    try:
        response = requests.get('http://api.sgsky.tech/api/template/red15')
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                fields = result.get('fields', {})
                text_fields = {k: v for k, v in fields.items() if v.get('type') == 'text'}
                print(f"   OK 模板信息获取成功")
                print(f"   总字段数: {len(fields)}")
                print(f"   文本字段数: {len(text_fields)}")
                print(f"   文本字段: {list(text_fields.keys())}")
            else:
                print(f"   FAIL 模板信息获取失败: {result.get('error')}")
                return False
        else:
            print(f"   FAIL 模板信息请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"   FAIL 模板信息异常: {e}")
        return False
    
    # 4. 测试生成
    print("\n4. 测试生成...")
    try:
        # 使用从模板获取的字段构建请求
        user_data = {
            '姓名': '测试用户',
            '车次号': 'G1234',
            '座位号': '01A',
            '出发站': '北京',
            '到达站': '上海',
            '车次类型': '高铁',
            '票价': '553.0',
            '票号': 'E123456789'
        }
        
        request_data = {
            'style': 'red15',
            'user_data': user_data,
            'format': 'base64'
        }
        
        response = requests.post('http://api.sgsky.tech/api/generate', json=request_data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                image_data = result.get('data', {}).get('image_base64', '')
                print(f"   OK 生成成功!")
                print(f"   图片数据长度: {len(image_data)} 字节")
                return True
            else:
                print(f"   FAIL 生成失败: {result.get('error')}")
                return False
        else:
            print(f"   FAIL 生成请求失败: {response.status_code}")
            print(f"   响应内容: {response.text}")
            return False
    except Exception as e:
        print(f"   FAIL 生成异常: {e}")
        return False

def main():
    """主函数"""
    print("重构后的小程序API流程测试")
    print("=" * 60)
    
    success = test_complete_flow()
    
    print("\n" + "=" * 60)
    if success:
        print("SUCCESS 所有测试通过！")
        print("小程序现在应该能正常工作了")
        print("\n请在微信开发者工具中:")
        print("   1. 重新编译小程序")
        print("   2. 等待页面加载完成")
        print("   3. 查看动态加载的字段")
        print("   4. 填写信息并生成预览")
    else:
        print("FAIL 测试失败，需要进一步调试")

if __name__ == "__main__":
    main()

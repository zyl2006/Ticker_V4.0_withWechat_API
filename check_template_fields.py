#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API模板字段结构
"""

import requests
import json

def check_template_fields():
    """检查模板字段结构"""
    print("检查API模板字段结构...")
    
    try:
        response = requests.get('http://api.sgsky.tech/api/template/red15')
        if response.status_code == 200:
            result = response.json()
            print("模板信息获取成功")
            print("字段数量:", len(result.get('fields', {})))
            
            # 显示所有字段
            fields = result.get('fields', {})
            for field_name, field_info in fields.items():
                print(f"字段: {field_name}")
                print(f"  类型: {field_info.get('type', 'unknown')}")
                print(f"  必需: {field_info.get('required', False)}")
                print(f"  描述: {field_info.get('description', '')}")
                print()
            
            return fields
        else:
            print(f"API请求失败: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"请求异常: {e}")
        return None

def test_generate_with_correct_fields():
    """使用正确字段测试生成"""
    print("\n测试生成API...")
    
    # 基于模板字段构建正确的请求数据
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
        response = requests.post('http://api.sgsky.tech/api/generate', json=test_data)
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("生成成功!")
                return True
            else:
                print(f"生成失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"HTTP错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"请求异常: {e}")
        return False

def main():
    """主函数"""
    print("API模板字段检查")
    print("=" * 50)
    
    # 检查模板字段
    fields = check_template_fields()
    
    if fields:
        # 测试生成
        test_generate_with_correct_fields()
    
    print("\n" + "=" * 50)
    print("检查完成")

if __name__ == "__main__":
    main()

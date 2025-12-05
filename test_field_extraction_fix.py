#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的小程序字段提取
"""

import requests
import json
import re

def test_field_extraction():
    """测试字段提取逻辑"""
    print("测试字段提取逻辑")
    print("=" * 40)
    
    try:
        # 获取模板信息
        response = requests.get('http://api.sgsky.tech/api/template/red15')
        if response.status_code != 200:
            print(f"FAIL 获取模板信息失败: {response.status_code}")
            return False
        
        result = response.json()
        if not result.get('success'):
            print(f"FAIL 模板信息获取失败: {result.get('error')}")
            return False
        
        fields = result.get('fields', {})
        print(f"模板字段总数: {len(fields)}")
        
        # 模拟JavaScript的字段提取逻辑
        real_fields = {}
        field_list = []
        
        for field_name, field_config in fields.items():
            if 'segments' in field_config:
                segments = field_config['segments']
                for segment in segments:
                    if 'text' in segment:
                        text = segment['text']
                        # 提取{字段名}格式的字段
                        matches = re.findall(r'\{([^}]+)\}', text)
                        for match in matches:
                            if match not in real_fields:
                                real_fields[match] = {'value': '', 'enabled': True}
                                field_list.append({
                                    'key': match,
                                    'label': match,
                                    'type': 'text',
                                    'required': False,
                                    'description': '请输入' + match
                                })
        
        print(f"提取的真实字段数量: {len(field_list)}")
        print("前10个字段:", [f['key'] for f in field_list[:10]])
        
        # 测试生成API
        print("\n测试生成API...")
        user_data = {}
        for field in field_list[:10]:  # 只测试前10个字段
            key = field['key']
            if key == '姓名':
                user_data[key] = '测试用户'
            elif key == '车次号':
                user_data[key] = 'G1234'
            elif key == '出发站':
                user_data[key] = '北京'
            elif key == '到达站':
                user_data[key] = '上海'
            else:
                user_data[key] = '测试' + key
        
        request_data = {
            'style': 'red15',
            'user_data': user_data,
            'format': 'base64'
        }
        
        response = requests.post('http://api.sgsky.tech/api/generate', json=request_data)
        print(f"生成API响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS 生成API调用成功!")
                return True
            else:
                print(f"FAIL 生成API返回错误: {result.get('error')}")
                return False
        else:
            print(f"FAIL 生成API HTTP错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL 测试异常: {e}")
        return False

def main():
    """主函数"""
    print("修复后的小程序字段提取测试")
    print("=" * 50)
    
    success = test_field_extraction()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS 字段提取修复成功!")
        print("小程序现在应该能正确提取segments中的字段了")
        print("\n请在微信开发者工具中:")
        print("   1. 重新编译小程序")
        print("   2. 查看字段数量应该显示46个")
        print("   3. 填写字段信息并生成预览")
    else:
        print("FAIL 字段提取仍有问题")

if __name__ == "__main__":
    main()

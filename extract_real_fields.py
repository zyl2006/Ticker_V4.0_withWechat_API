#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取模板中的真实字段
"""

import json
import re

def extract_fields_from_template():
    """从模板中提取真实字段"""
    print("提取模板中的真实字段")
    print("=" * 40)
    
    try:
        with open('templates/ticket_template_red15.json', 'r', encoding='utf-8') as f:
            template = json.load(f)
        
        fields = template.get('fields', {})
        real_fields = set()
        
        print("扫描所有segments中的字段...")
        
        for field_name, field_config in fields.items():
            if 'segments' in field_config:
                segments = field_config['segments']
                for segment in segments:
                    if 'text' in segment:
                        text = segment['text']
                        # 提取{字段名}格式的字段
                        matches = re.findall(r'\{([^}]+)\}', text)
                        for match in matches:
                            real_fields.add(match)
        
        real_fields_list = sorted(list(real_fields))
        
        print(f"发现 {len(real_fields_list)} 个真实字段:")
        for i, field in enumerate(real_fields_list, 1):
            print(f"{i:2d}. {field}")
        
        return real_fields_list
        
    except Exception as e:
        print(f"提取字段失败: {e}")
        return []

def test_api_with_real_fields():
    """使用真实字段测试API"""
    print("\n使用真实字段测试API...")
    
    real_fields = extract_fields_from_template()
    
    if not real_fields:
        print("没有找到字段，无法测试")
        return
    
    # 构建测试数据
    user_data = {}
    for field in real_fields:
        if field == '姓名':
            user_data[field] = '测试用户'
        elif field == '车次号':
            user_data[field] = 'G1234'
        elif field == '出发站':
            user_data[field] = '北京'
        elif field == '到达站':
            user_data[field] = '上海'
        elif field == '车次类型':
            user_data[field] = '高铁'
        elif field == '票价1':
            user_data[field] = '553'
        elif field == '年':
            user_data[field] = '2024'
        elif field == '月':
            user_data[field] = '01'
        elif field == '日':
            user_data[field] = '15'
        elif field == '时':
            user_data[field] = '14'
        elif field == '分':
            user_data[field] = '30'
        else:
            user_data[field] = '测试' + field
    
    print(f"构建了 {len(user_data)} 个字段的测试数据")
    
    # 测试API
    import requests
    
    request_data = {
        'style': 'red15',
        'user_data': user_data,
        'format': 'base64'
    }
    
    try:
        response = requests.post('http://api.sgsky.tech/api/generate', json=request_data)
        print(f"API响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS API调用成功!")
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

def main():
    """主函数"""
    print("模板字段分析")
    print("=" * 50)
    
    # 提取字段
    real_fields = extract_fields_from_template()
    
    if real_fields:
        # 测试API
        test_api_with_real_fields()
    
    print("\n" + "=" * 50)
    print("分析完成")

if __name__ == "__main__":
    main()

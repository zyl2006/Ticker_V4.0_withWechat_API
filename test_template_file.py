#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试模板文件读取
"""

import json
import os

def test_template_file():
    """测试模板文件读取"""
    print("测试模板文件读取")
    print("=" * 30)
    
    template_path = "templates/ticket_template_red15.json"
    
    if not os.path.exists(template_path):
        print(f"FAIL 模板文件不存在: {template_path}")
        return
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        fields = template_data.get('fields', {})
        print(f"模板字段总数: {len(fields)}")
        
        # 检查第一个字段
        first_field_name = list(fields.keys())[0]
        first_field = fields[first_field_name]
        
        print(f"第一个字段: {first_field_name}")
        print(f"字段类型: {first_field.get('type', 'unknown')}")
        print(f"包含segments: {'segments' in first_field}")
        
        if 'segments' in first_field:
            segments = first_field['segments']
            print(f"segments数量: {len(segments)}")
            if segments:
                print(f"第一个segment: {segments[0]}")
        
        # 统计有segments的字段
        fields_with_segments = 0
        for field_name, field_config in fields.items():
            if 'segments' in field_config and field_config['segments']:
                fields_with_segments += 1
        
        print(f"包含segments的字段数量: {fields_with_segments}")
        
        # 提取所有真实字段
        real_fields = set()
        for field_name, field_config in fields.items():
            if 'segments' in field_config:
                for segment in field_config['segments']:
                    if 'text' in segment:
                        text = segment['text']
                        import re
                        matches = re.findall(r'\{([^}]+)\}', text)
                        for match in matches:
                            real_fields.add(match)
        
        print(f"提取的真实字段数量: {len(real_fields)}")
        print("前10个真实字段:", sorted(list(real_fields))[:10])
        
    except Exception as e:
        print(f"FAIL 读取模板文件失败: {e}")

if __name__ == "__main__":
    test_template_file()

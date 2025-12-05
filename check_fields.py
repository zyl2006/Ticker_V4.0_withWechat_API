#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查字段列表
"""

import json

def check_fields():
    """检查字段列表"""
    with open('fields.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fields = data.get('fields', [])
    print(f"总字段数: {len(fields)}")
    
    # 查找包含"座"的字段
    seat_fields = [f['key'] for f in fields if '座' in f['key']]
    print(f"包含'座'的字段: {seat_fields}")
    
    # 查找包含"位"的字段
    position_fields = [f['key'] for f in fields if '位' in f['key']]
    print(f"包含'位'的字段: {position_fields}")
    
    # 查找包含"号"的字段
    number_fields = [f['key'] for f in fields if '号' in f['key']]
    print(f"包含'号'的字段: {number_fields}")
    
    # 显示所有字段
    print("\n所有字段:")
    for i, field in enumerate(fields):
        print(f"{i+1:2d}. {field['key']}")

if __name__ == "__main__":
    check_fields()

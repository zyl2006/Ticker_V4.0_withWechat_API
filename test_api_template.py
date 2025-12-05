#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试API模板信息
"""

import requests
import json

def test_api_template():
    """测试API模板信息"""
    print("测试API模板信息")
    print("=" * 30)
    
    try:
        response = requests.get('http://api.sgsky.tech/api/template/red15')
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('success')}")
            
            fields = result.get('fields', {})
            print(f"字段数量: {len(fields)}")
            
            # 检查第一个字段是否有segments
            first_field = list(fields.values())[0] if fields else {}
            print(f"第一个字段: {list(fields.keys())[0] if fields else 'None'}")
            print(f"包含segments: {'segments' in first_field}")
            
            if 'segments' in first_field:
                segments = first_field['segments']
                print(f"segments数量: {len(segments)}")
                if segments:
                    print(f"第一个segment: {segments[0]}")
            
            # 保存完整响应到文件
            with open('api_template_response.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("完整响应已保存到 api_template_response.json")
            
        else:
            print(f"请求失败: {response.text}")
            
    except Exception as e:
        print(f"异常: {e}")

if __name__ == "__main__":
    test_api_template()

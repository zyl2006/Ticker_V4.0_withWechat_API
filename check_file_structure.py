#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API文件结构
"""

import os
import re

def check_file_structure():
    """检查文件结构"""
    print("检查API文件结构")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查类定义
        if 'class ApiService' in content:
            print("✓ 类定义正确")
        else:
            print("✗ 缺少类定义")
        
        # 检查方法定义
        methods = [
            'constructor()',
            'request(options)',
            'healthCheck()',
            'getStyles()',
            'getTemplateFields(style)',
            'getTemplateInfo(style)',
            'generateTicket(data)',
            'batchGenerateTickets(data)'
        ]
        
        print("\n方法定义检查:")
        for method in methods:
            if method in content:
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method}")
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        print(f"\n括号匹配: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查逗号问题
        lines = content.split('\n')
        print("\n逗号检查:")
        for i, line in enumerate(lines):
            line_num = i + 1
            stripped = line.strip()
            if stripped.endswith(',') and line_num < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('//') or next_line == '':
                    continue
                if next_line.startswith('}') and not next_line.startswith('},'):
                    print(f"  第{line_num}行: 多余的逗号")
        
        # 检查module.exports
        if 'module.exports' in content:
            print("\n✓ module.exports存在")
        else:
            print("\n✗ 缺少module.exports")
        
        return True
        
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("API文件结构检查")
    print("=" * 40)
    
    check_file_structure()
    
    print("\n" + "=" * 40)
    print("检查完成!")

if __name__ == "__main__":
    main()

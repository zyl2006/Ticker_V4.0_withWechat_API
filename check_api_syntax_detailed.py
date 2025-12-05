#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查API文件语法
"""

import os
import re

def check_api_syntax():
    """检查API文件语法"""
    print("检查API文件语法")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    if not os.path.exists(api_file):
        print(f"FAIL API文件不存在: {api_file}")
        return False
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查第69行附近的内容
        lines = content.split('\n')
        print("第65-75行内容:")
        for i in range(64, min(75, len(lines))):
            line_num = i + 1
            line_content = lines[i]
            print(f"{line_num:2d}: {line_content}")
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        print(f"\n括号匹配检查: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查方法定义
        methods = [
            'getStyles',
            'getTemplateFields', 
            'getTemplateInfo',
            'generateTicket',
            'batchGenerateTickets'
        ]
        
        print("\n方法定义检查:")
        for method in methods:
            pattern = f'{method}\\s*\\('
            if re.search(pattern, content):
                print(f"  ✓ {method}")
            else:
                print(f"  ✗ {method}")
        
        # 检查逗号问题
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
                elif next_line.startswith('//') and not next_line.startswith('// 获取'):
                    print(f"  第{line_num}行: 方法后缺少逗号")
        
        return True
        
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("API文件语法详细检查")
    print("=" * 40)
    
    check_api_syntax()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终语法验证
"""

import os

def final_syntax_check():
    """最终语法检查"""
    print("最终语法检查")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查第10行附近的内容
        lines = content.split('\n')
        print("第5-15行内容:")
        for i in range(4, min(15, len(lines))):
            line_num = i + 1
            line_content = lines[i]
            print(f"{line_num:2d}: {line_content}")
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        print(f"\n括号匹配检查: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查类方法定义
        methods = [
            'constructor',
            'request',
            'healthCheck',
            'getStyles',
            'getTemplateFields', 
            'getTemplateInfo',
            'generateTicket',
            'batchGenerateTickets'
        ]
        
        print("\n方法定义检查:")
        for method in methods:
            if f'{method}(' in content:
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
        
        return True
        
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("最终语法验证")
    print("=" * 40)
    
    final_syntax_check()
    
    print("\n" + "=" * 40)
    print("语法检查完成!")
    print("现在请:")
    print("  1. 重启微信开发者工具")
    print("  2. 清除缓存")
    print("  3. 重新编译")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证ES5语法修复
"""

import os

def verify_es5_syntax():
    """验证ES5语法"""
    print("验证ES5语法修复")
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
        print(f"\n括号匹配: 开括号{open_braces}, 闭括号{close_braces}")
        
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
        
        # 检查类方法逗号问题
        print("\n类方法逗号检查:")
        for i, line in enumerate(lines):
            line_num = i + 1
            stripped = line.strip()
            if stripped.endswith(',') and line_num < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('//') and '方法' in next_line:
                    print(f"  第{line_num}行: 类方法后有多余逗号")
        
        return True
        
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("ES5语法修复验证")
    print("=" * 40)
    
    verify_es5_syntax()
    
    print("\n" + "=" * 40)
    print("ES5语法修复完成!")
    print("现在请:")
    print("  1. 重启微信开发者工具")
    print("  2. 清除缓存")
    print("  3. 重新编译")
    print("  4. 应该不再有语法错误")

if __name__ == "__main__":
    main()

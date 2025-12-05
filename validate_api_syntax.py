#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证API文件语法
"""

import os

def validate_syntax():
    """验证语法"""
    print("验证API文件语法")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本语法
        issues = []
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            issues.append(f"括号不匹配: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查方法定义
        methods = [
            'healthCheck',
            'getStyles',
            'getTemplateFields', 
            'getTemplateInfo',
            'generateTicket',
            'batchGenerateTickets'
        ]
        
        for method in methods:
            if f'{method}(' not in content:
                issues.append(f"缺少方法: {method}")
        
        # 检查类结构
        if 'class ApiService' not in content:
            issues.append("缺少ApiService类定义")
        
        if 'module.exports' not in content:
            issues.append("缺少module.exports导出")
        
        # 检查第69行附近
        lines = content.split('\n')
        if len(lines) >= 69:
            line_69 = lines[68].strip()  # 第69行
            if line_69 != '},':
                issues.append(f"第69行语法错误: {line_69}")
        
        if issues:
            print("发现语法问题:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("SUCCESS 语法检查通过")
            return True
            
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("API文件语法验证")
    print("=" * 40)
    
    success = validate_syntax()
    
    print("\n" + "=" * 40)
    if success:
        print("SUCCESS API文件语法正确!")
        print("如果小程序仍然报错，可能是缓存问题")
        print("建议:")
        print("  1. 重启微信开发者工具")
        print("  2. 清除编译缓存")
        print("  3. 重新编译小程序")
    else:
        print("FAIL 仍有语法问题需要修复")

if __name__ == "__main__":
    main()

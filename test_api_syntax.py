#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API文件语法
"""

import os

def test_api_syntax():
    """测试API文件语法"""
    print("测试API文件语法")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    if not os.path.exists(api_file):
        print(f"FAIL API文件不存在: {api_file}")
        return False
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本的语法问题
        issues = []
        
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
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            issues.append(f"括号不匹配: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查逗号问题
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.endswith(',') and i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith('//') or next_line == '':
                    continue
                if next_line.startswith('}') and not next_line.startswith('},'):
                    issues.append(f"第{i}行: 多余的逗号")
        
        if issues:
            print("发现语法问题:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("SUCCESS 语法检查通过")
            return True
            
    except Exception as e:
        print(f"FAIL 读取文件失败: {e}")
        return False

def main():
    """主函数"""
    print("API文件语法检查")
    print("=" * 40)
    
    success = test_api_syntax()
    
    print("\n" + "=" * 40)
    if success:
        print("SUCCESS API文件语法正确!")
        print("小程序应该可以正常编译了")
    else:
        print("FAIL 仍有语法问题需要修复")

if __name__ == "__main__":
    main()

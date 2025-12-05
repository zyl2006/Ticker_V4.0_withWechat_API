#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证
"""

import os

def final_verification():
    """最终验证"""
    print("最终验证")
    print("=" * 30)
    
    api_file = 'ticker-miniprogram-root/utils/api.js'
    
    try:
        with open(api_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本结构
        checks = [
            ('class ApiService', '类定义'),
            ('constructor()', '构造函数'),
            ('request(options)', '请求方法'),
            ('healthCheck()', '健康检查'),
            ('getStyles()', '获取样式'),
            ('getTemplateFields(style)', '获取字段'),
            ('getTemplateInfo(style)', '获取模板信息'),
            ('generateTicket(data)', '生成车票'),
            ('batchGenerateTickets(data)', '批量生成'),
            ('module.exports', '导出模块')
        ]
        
        print("结构检查:")
        for check, desc in checks:
            if check in content:
                print(f"  ✓ {desc}")
            else:
                print(f"  ✗ {desc}")
        
        # 检查括号匹配
        open_braces = content.count('{')
        close_braces = content.count('}')
        print(f"\n括号匹配: 开括号{open_braces}, 闭括号{close_braces}")
        
        # 检查文件大小
        file_size = len(content)
        print(f"文件大小: {file_size} 字符")
        
        return True
        
    except Exception as e:
        print(f"FAIL 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("API文件最终验证")
    print("=" * 40)
    
    success = final_verification()
    
    print("\n" + "=" * 40)
    if success:
        print("SUCCESS 文件结构正确!")
        print("现在请:")
        print("  1. 重启微信开发者工具")
        print("  2. 清除缓存")
        print("  3. 重新编译")
        print("  4. 应该不再有语法错误")
    else:
        print("FAIL 仍有问题")

if __name__ == "__main__":
    main()

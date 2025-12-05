#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决微信开发者工具错误
"""

import os

def check_miniprogram_files():
    """检查小程序文件"""
    print("检查小程序文件")
    print("=" * 30)
    
    files_to_check = [
        'ticker-miniprogram-root/app.js',
        'ticker-miniprogram-root/app.json',
        'ticker-miniprogram-root/pages/index/index.js',
        'ticker-miniprogram-root/pages/index/index.wxml',
        'ticker-miniprogram-root/pages/index/index.wxss',
        'ticker-miniprogram-root/utils/api.js'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - 文件不存在")
    
    # 检查app.json内容
    app_json_path = 'ticker-miniprogram-root/app.json'
    if os.path.exists(app_json_path):
        try:
            with open(app_json_path, 'r', encoding='utf-8') as f:
                content = f.read()
            print(f"\napp.json文件大小: {len(content)} 字符")
            if '"pages"' in content:
                print("✓ app.json包含pages配置")
            else:
                print("✗ app.json缺少pages配置")
        except Exception as e:
            print(f"✗ 读取app.json失败: {e}")

def main():
    """主函数"""
    print("微信开发者工具错误诊断")
    print("=" * 40)
    
    check_miniprogram_files()
    
    print("\n" + "=" * 40)
    print("解决方案:")
    print("1. 完全关闭微信开发者工具")
    print("2. 删除项目文件夹中的以下文件:")
    print("   - .vscode/ 文件夹")
    print("   - node_modules/ 文件夹")
    print("   - 任何临时文件")
    print("3. 重新打开微信开发者工具")
    print("4. 重新导入项目")
    print("5. 清除缓存并重新编译")

if __name__ == "__main__":
    main()

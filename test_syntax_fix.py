#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序语法修复测试脚本
验证修复后的代码是否能正常编译
"""

import os
import json

def check_syntax_fixes():
    """检查语法修复"""
    print("检查语法修复...")
    
    try:
        # 检查index.js文件
        with open("ticker-miniprogram-root/pages/index/index.js", "r", encoding="utf-8") as f:
            content = f.read()
            
            # 检查关键修复点
            fixes = [
                ("function()", "使用function()语法"),
                ("var ", "使用var声明变量"),
                ("e.detail.value", "正确的表单输入处理"),
                ("e.currentTarget.dataset", "正确的数据获取"),
                ("api.healthCheck().then", "Promise处理"),
                ("wx.saveImageToPhotosAlbum({", "正确的API调用"),
                ("success: function()", "回调函数语法"),
                ("fail: function(error)", "错误处理语法")
            ]
            
            all_fixed = True
            for fix, description in fixes:
                if fix in content:
                    print(f"修复存在: {description}")
                else:
                    print(f"修复缺失: {description}")
                    all_fixed = False
            
            # 检查是否移除了问题语法
            problems = [
                ("async ", "移除了async语法"),
                ("await ", "移除了await语法"),
                ("const ", "移除了const语法"),
                ("let ", "移除了let语法"),
                ("=>", "移除了箭头函数")
            ]
            
            for problem, description in problems:
                if problem not in content:
                    print(f"问题已解决: {description}")
                else:
                    print(f"问题仍存在: {description}")
                    all_fixed = False
            
            return all_fixed
            
    except Exception as e:
        print(f"检查语法修复失败: {e}")
        return False

def check_file_structure():
    """检查文件结构"""
    print("\n检查文件结构...")
    
    required_files = [
        "ticker-miniprogram-root/app.js",
        "ticker-miniprogram-root/app.json",
        "ticker-miniprogram-root/app.wxss",
        "ticker-miniprogram-root/pages/index/index.js",
        "ticker-miniprogram-root/pages/index/index.wxml",
        "ticker-miniprogram-root/pages/index/index.wxss",
        "ticker-miniprogram-root/utils/api.js",
        "ticker-miniprogram-root/utils/storage.js",
        "ticker-miniprogram-root/styles/variables.wxss"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"文件存在: {file_path}")
        else:
            print(f"文件缺失: {file_path}")
            all_exist = False
    
    return all_exist

def check_app_config():
    """检查app配置"""
    print("\n检查app配置...")
    
    try:
        with open("ticker-miniprogram-root/app.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            
            # 检查必要字段
            required_fields = ["pages", "window"]
            for field in required_fields:
                if field in config:
                    print(f"配置存在: {field}")
                else:
                    print(f"配置缺失: {field}")
                    return False
            
            # 检查页面配置
            pages = config.get("pages", [])
            if len(pages) >= 3:
                print(f"页面配置正确: {len(pages)} 个页面")
            else:
                print(f"页面配置不完整: {pages}")
                return False
            
            # 检查是否移除了问题配置
            if "tabBar" not in config:
                print("已移除tabBar配置")
            else:
                print("仍包含tabBar配置")
                return False
            
            return True
            
    except Exception as e:
        print(f"检查app配置失败: {e}")
        return False

def main():
    """主函数"""
    print("小程序语法修复测试")
    print("=" * 40)
    
    # 检查语法修复
    syntax_ok = check_syntax_fixes()
    
    # 检查文件结构
    files_ok = check_file_structure()
    
    # 检查app配置
    config_ok = check_app_config()
    
    print("\n" + "=" * 40)
    print("测试结果:")
    print(f"语法修复: {'正常' if syntax_ok else '异常'}")
    print(f"文件结构: {'正常' if files_ok else '异常'}")
    print(f"App配置: {'正常' if config_ok else '异常'}")
    
    all_ok = syntax_ok and files_ok and config_ok
    
    if all_ok:
        print("\n语法修复测试通过！")
        print("\n主要修复:")
        print("1. 移除了async/await语法")
        print("2. 使用function()替代箭头函数")
        print("3. 使用var替代const/let")
        print("4. 修复了表单输入处理")
        print("5. 使用Promise.then()处理异步")
        print("6. 修复了API调用语法")
        print("\n现在请在微信开发者工具中:")
        print("1. 重新编译小程序")
        print("2. 检查是否还有编译错误")
        print("3. 测试基本功能")
    else:
        print("\n存在问题，请检查上述错误")
    
    return all_ok

if __name__ == "__main__":
    main()

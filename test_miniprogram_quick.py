#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序快速测试脚本
验证修复后的小程序是否能正常显示
"""

import requests
import json
import os

def test_api_connection():
    """测试API连接"""
    print("测试API连接...")
    
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=3)
        if response.status_code == 200:
            print("API服务器连接正常")
            return True
        else:
            print(f"API服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"API服务器连接失败: {e}")
        return False

def test_miniprogram_files():
    """测试小程序文件"""
    print("\n测试小程序文件...")
    
    files_to_check = [
        "ticker-miniprogram-root/app.js",
        "ticker-miniprogram-root/app.json",
        "ticker-miniprogram-root/app.wxss",
        "ticker-miniprogram-root/pages/index/index.js",
        "ticker-miniprogram-root/pages/index/index.wxml",
        "ticker-miniprogram-root/pages/index/index.wxss",
        "ticker-miniprogram-root/utils/api.js",
        "ticker-miniprogram-root/utils/storage.js",
        "ticker-miniprogram-root/utils/validator.js",
        "ticker-miniprogram-root/styles/variables.wxss"
    ]
    
    all_exist = True
    for file_path in files_to_check:
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
        # 检查app.js
        with open("ticker-miniprogram-root/app.js", "r", encoding="utf-8") as f:
            app_js_content = f.read()
            if "http://localhost:5001" in app_js_content:
                print("app.js API地址配置正确")
            else:
                print("app.js API地址配置错误")
                return False
        
        # 检查app.json
        with open("ticker-miniprogram-root/app.json", "r", encoding="utf-8") as f:
            app_config = json.load(f)
            
            if "pages" in app_config and len(app_config["pages"]) >= 3:
                print("app.json页面配置正确")
            else:
                print("app.json页面配置错误")
                return False
            
            if "tabBar" not in app_config:
                print("app.json已移除tabBar配置")
            else:
                print("app.json仍包含tabBar配置")
                return False
        
        return True
        
    except Exception as e:
        print(f"检查app配置失败: {e}")
        return False

def check_index_page():
    """检查首页配置"""
    print("\n检查首页配置...")
    
    try:
        # 检查index.js
        with open("ticker-miniprogram-root/pages/index/index.js", "r", encoding="utf-8") as f:
            index_js_content = f.read()
            if "loading: false" in index_js_content:
                print("index.js loading状态已修复")
            else:
                print("index.js loading状态未修复")
                return False
            
            if "styles: ['red15'" in index_js_content:
                print("index.js 包含默认样式数据")
            else:
                print("index.js 缺少默认样式数据")
                return False
        
        # 检查index.wxml
        with open("ticker-miniprogram-root/pages/index/index.wxml", "r", encoding="utf-8") as f:
            index_wxml_content = f.read()
            if "Ticker-车票儿" in index_wxml_content:
                print("index.wxml 包含标题")
            else:
                print("index.wxml 缺少标题")
                return False
            
            if "调试信息" in index_wxml_content:
                print("index.wxml 包含调试信息")
            else:
                print("index.wxml 缺少调试信息")
                return False
        
        return True
        
    except Exception as e:
        print(f"检查首页配置失败: {e}")
        return False

def main():
    """主函数"""
    print("小程序快速测试")
    print("=" * 40)
    
    # 测试API连接
    api_ok = test_api_connection()
    
    # 测试小程序文件
    files_ok = test_miniprogram_files()
    
    # 检查app配置
    config_ok = check_app_config()
    
    # 检查首页配置
    page_ok = check_index_page()
    
    print("\n" + "=" * 40)
    print("测试结果:")
    print(f"API连接: {'正常' if api_ok else '异常'}")
    print(f"文件完整性: {'正常' if files_ok else '异常'}")
    print(f"App配置: {'正常' if config_ok else '异常'}")
    print(f"首页配置: {'正常' if page_ok else '异常'}")
    
    all_ok = api_ok and files_ok and config_ok and page_ok
    
    if all_ok:
        print("\n所有测试通过！")
        print("\n现在请在微信开发者工具中:")
        print("1. 重新编译小程序")
        print("2. 查看是否显示界面内容")
        print("3. 检查调试信息区域")
        print("4. 测试样式选择和表单填写")
    else:
        print("\n存在问题，请检查上述错误")
    
    return all_ok

if __name__ == "__main__":
    main()

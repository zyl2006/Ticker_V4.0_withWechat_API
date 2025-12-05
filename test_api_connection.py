#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API连接测试脚本
验证小程序API连接问题
"""

import requests
import json
import os

def test_api_server():
    """测试API服务器"""
    print("测试API服务器...")
    
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"API服务器正常: {data.get('status', 'unknown')}")
            print(f"可用样式: {data.get('available_styles', [])}")
            return True
        else:
            print(f"API服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"API服务器连接失败: {e}")
        return False

def check_miniprogram_config():
    """检查小程序配置"""
    print("\n检查小程序配置...")
    
    try:
        # 检查app.js中的API配置
        with open("ticker-miniprogram-root/app.js", "r", encoding="utf-8") as f:
            app_js_content = f.read()
            
            if "apiBaseUrl: 'http://localhost:5001'" in app_js_content:
                print("OK API基础URL配置正确")
            else:
                print("FAIL API基础URL配置错误")
                return False
        
        # 检查api.js中的语法
        with open("ticker-miniprogram-root/utils/api.js", "r", encoding="utf-8") as f:
            api_js_content = f.read()
            
            # 检查是否移除了async/await
            if "async " not in api_js_content and "await " not in api_js_content:
                print("OK API工具文件语法正确")
            else:
                print("FAIL API工具文件仍有async/await语法")
                return False
            
            # 检查Promise使用
            if "return new Promise(function(resolve, reject)" in api_js_content:
                print("OK API工具文件使用Promise语法")
            else:
                print("FAIL API工具文件Promise语法有问题")
                return False
        
        return True
        
    except Exception as e:
        print(f"检查小程序配置失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n测试API端点...")
    
    endpoints = [
        ("/api/health", "健康检查"),
        ("/api/styles", "样式列表"),
        ("/api/template/red15", "模板信息")
    ]
    
    all_ok = True
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:5001{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"OK {description}: {endpoint}")
            else:
                print(f"FAIL {description}: {endpoint} (状态码: {response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"FAIL {description}: {endpoint} (错误: {e})")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("API连接问题诊断")
    print("=" * 40)
    
    # 测试API服务器
    api_ok = test_api_server()
    
    # 检查小程序配置
    config_ok = check_miniprogram_config()
    
    # 测试API端点
    endpoints_ok = test_api_endpoints()
    
    print("\n" + "=" * 40)
    print("诊断结果:")
    print(f"API服务器: {'正常' if api_ok else '异常'}")
    print(f"小程序配置: {'正常' if config_ok else '异常'}")
    print(f"API端点: {'正常' if endpoints_ok else '异常'}")
    
    all_ok = api_ok and config_ok and endpoints_ok
    
    if all_ok:
        print("\nSUCCESS 所有检查通过！")
        print("\n问题已修复:")
        print("1. API服务器正常运行")
        print("2. 小程序API基础URL已修正为 http://localhost:5001")
        print("3. API工具文件语法已修复")
        print("\n现在请在微信开发者工具中:")
        print("1. 重新编译小程序")
        print("2. 服务器状态应该显示为在线")
        print("3. 可以正常生成预览")
    else:
        print("\nFAIL 仍有问题需要解决")
        if not api_ok:
            print("- 请确保API服务器正在运行: python api_server.py")
        if not config_ok:
            print("- 请检查小程序配置文件")
        if not endpoints_ok:
            print("- 请检查API端点是否正常")
    
    return all_ok

if __name__ == "__main__":
    main()

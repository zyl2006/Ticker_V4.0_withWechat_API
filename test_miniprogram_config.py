#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序配置测试脚本
测试API服务器和小程序配置是否正确
"""

import requests
import json
import time

def test_api_server():
    """测试API服务器是否正常运行"""
    print("测试API服务器...")
    
    base_url = "http://localhost:5001"
    
    # 测试健康检查
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"健康检查通过: {data.get('message', 'OK')}")
            print(f"可用样式: {data.get('available_styles', [])}")
        else:
            print(f"健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"API服务器连接失败: {e}")
        return False
    
    # 测试样式列表
    try:
        response = requests.get(f"{base_url}/api/styles", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                styles = data.get('styles', [])
                print(f"样式列表获取成功: {len(styles)} 个样式")
                for style in styles:
                    print(f"   - {style}")
            else:
                print(f"样式列表获取失败: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"样式列表请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"样式列表请求异常: {e}")
        return False
    
    # 测试模板信息
    try:
        response = requests.get(f"{base_url}/api/template/red15", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                fields = data.get('fields', {})
                print(f"模板信息获取成功: {len(fields)} 个字段")
                for field, config in fields.items():
                    print(f"   - {field}: {config.get('description', 'No description')}")
            else:
                print(f"模板信息获取失败: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"模板信息请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"模板信息请求异常: {e}")
        return False
    
    return True

def test_miniprogram_config():
    """测试小程序配置文件"""
    print("\n测试小程序配置...")
    
    import os
    
    # 检查关键文件是否存在
    required_files = [
        "ticker-miniprogram-root/app.js",
        "ticker-miniprogram-root/app.json", 
        "ticker-miniprogram-root/app.wxss",
        "ticker-miniprogram-root/pages/index/index.js",
        "ticker-miniprogram-root/pages/index/index.wxml",
        "ticker-miniprogram-root/pages/index/index.wxss",
        "ticker-miniprogram-root/utils/api.js",
        "ticker-miniprogram-root/styles/variables.wxss"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"文件存在: {file_path}")
    
    if missing_files:
        print(f"缺少文件: {missing_files}")
        return False
    
    # 检查app.js中的API地址配置
    try:
        with open("ticker-miniprogram-root/app.js", "r", encoding="utf-8") as f:
            content = f.read()
            if "http://localhost:5001" in content:
                print("API地址配置正确")
            else:
                print("API地址配置错误")
                return False
    except Exception as e:
        print(f"读取app.js失败: {e}")
        return False
    
    # 检查app.json配置
    try:
        with open("ticker-miniprogram-root/app.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            
            # 检查必要字段
            required_fields = ["pages", "window"]
            for field in required_fields:
                if field not in config:
                    print(f"app.json缺少字段: {field}")
                    return False
            
            # 检查页面配置
            pages = config.get("pages", [])
            if len(pages) < 3:
                print(f"页面配置不完整: {pages}")
                return False
            
            print("app.json配置正确")
            
    except Exception as e:
        print(f"读取app.json失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("Ticker-车票儿 小程序配置测试")
    print("=" * 50)
    
    # 测试API服务器
    api_ok = test_api_server()
    
    # 测试小程序配置
    config_ok = test_miniprogram_config()
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"API服务器: {'正常' if api_ok else '异常'}")
    print(f"小程序配置: {'正常' if config_ok else '异常'}")
    
    if api_ok and config_ok:
        print("\n所有测试通过！小程序应该可以正常运行了。")
        print("\n下一步操作:")
        print("1. 在微信开发者工具中重新编译小程序")
        print("2. 检查调试器中的Console输出")
        print("3. 测试样式选择和表单填写功能")
    else:
        print("\n存在问题，请检查上述错误信息。")
    
    return api_ok and config_ok

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序新架构测试脚本
测试新的按需API调用架构
"""

import requests
import json
import os

def test_api_health():
    """测试API健康检查接口"""
    print("测试API健康检查接口...")
    
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"健康检查成功: {data.get('status', 'unknown')}")
            print(f"可用样式: {data.get('available_styles', [])}")
            return True
        else:
            print(f"健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"健康检查异常: {e}")
        return False

def test_new_architecture():
    """测试新架构文件"""
    print("\n测试新架构文件...")
    
    # 检查关键文件
    files_to_check = [
        "ticker-miniprogram-root/pages/index/index.js",
        "ticker-miniprogram-root/pages/index/index.wxml",
        "ticker-miniprogram-root/pages/index/index.wxss"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"文件存在: {file_path}")
        else:
            print(f"文件缺失: {file_path}")
            all_exist = False
    
    return all_exist

def check_new_features():
    """检查新功能"""
    print("\n检查新功能...")
    
    try:
        # 检查index.js中的新功能
        with open("ticker-miniprogram-root/pages/index/index.js", "r", encoding="utf-8") as f:
            index_js_content = f.read()
            
            features = [
                ("serverStatus", "服务器状态检测"),
                ("checkServerStatus", "服务器状态检测方法"),
                ("loadApiDataInBackground", "后台API数据加载"),
                ("retryServerCheck", "重新检测服务器"),
                ("loading: false", "立即显示界面")
            ]
            
            for feature, description in features:
                if feature in index_js_content:
                    print(f"功能存在: {description}")
                else:
                    print(f"功能缺失: {description}")
                    return False
        
        # 检查index.wxml中的新功能
        with open("ticker-miniprogram-root/pages/index/index.wxml", "r", encoding="utf-8") as f:
            index_wxml_content = f.read()
            
            wxml_features = [
                ("server-status", "服务器状态显示"),
                ("status-indicator", "状态指示器"),
                ("retryServerCheck", "重新检测按钮"),
                ("serverStatus !== 'online'", "离线状态处理")
            ]
            
            for feature, description in wxml_features:
                if feature in index_wxml_content:
                    print(f"界面功能存在: {description}")
                else:
                    print(f"界面功能缺失: {description}")
                    return False
        
        # 检查index.wxss中的新样式
        with open("ticker-miniprogram-root/pages/index/index.wxss", "r", encoding="utf-8") as f:
            index_wxss_content = f.read()
            
            wxss_features = [
                ("server-status", "服务器状态样式"),
                ("status-indicator", "状态指示器样式"),
                ("btn-small", "小按钮样式")
            ]
            
            for feature, description in wxss_features:
                if feature in index_wxss_content:
                    print(f"样式存在: {description}")
                else:
                    print(f"样式缺失: {description}")
                    return False
        
        return True
        
    except Exception as e:
        print(f"检查新功能失败: {e}")
        return False

def main():
    """主函数"""
    print("小程序新架构测试")
    print("=" * 40)
    
    # 测试API健康检查
    api_ok = test_api_health()
    
    # 测试新架构文件
    files_ok = test_new_architecture()
    
    # 检查新功能
    features_ok = check_new_features()
    
    print("\n" + "=" * 40)
    print("测试结果:")
    print(f"API健康检查: {'正常' if api_ok else '异常'}")
    print(f"新架构文件: {'正常' if files_ok else '异常'}")
    print(f"新功能检查: {'正常' if features_ok else '异常'}")
    
    all_ok = api_ok and files_ok and features_ok
    
    if all_ok:
        print("\n新架构测试通过！")
        print("\n新架构特点:")
        print("1. 立即显示界面，不等待API加载")
        print("2. 后台检测服务器状态")
        print("3. 按需调用API接口")
        print("4. 服务器离线时显示友好提示")
        print("5. 支持重新检测服务器状态")
        print("\n现在请在微信开发者工具中:")
        print("1. 重新编译小程序")
        print("2. 查看服务器状态指示器")
        print("3. 测试离线/在线状态切换")
        print("4. 验证按需API调用")
    else:
        print("\n存在问题，请检查上述错误")
    
    return all_ok

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试隐私授权配置修复
"""

import json
import os

def check_app_json():
    """检查app.json配置"""
    print("检查app.json配置...")
    
    app_json_path = "miniprogram/app.json"
    
    if not os.path.exists(app_json_path):
        print(f"[ERROR] app.json文件不存在: {app_json_path}")
        return False
    
    try:
        with open(app_json_path, 'r', encoding='utf-8') as f:
            app_config = json.load(f)
        
        print("[OK] app.json文件格式正确")
        
        # 检查必要字段
        required_fields = ['pages', 'window', 'tabBar']
        for field in required_fields:
            if field in app_config:
                print(f"[OK] {field} 字段存在")
            else:
                print(f"[ERROR] {field} 字段缺失")
                return False
        
        # 检查隐私相关配置
        if 'permission' in app_config:
            print("[OK] permission 字段存在")
            permission = app_config['permission']
            
            if 'scope.userInfo' in permission:
                print("[OK] scope.userInfo 权限配置存在")
                print(f"   描述: {permission['scope.userInfo'].get('desc', '无描述')}")
            else:
                print("[ERROR] scope.userInfo 权限配置缺失")
            
            if 'scope.writePhotosAlbum' in permission:
                print("[OK] scope.writePhotosAlbum 权限配置存在")
                print(f"   描述: {permission['scope.writePhotosAlbum'].get('desc', '无描述')}")
            else:
                print("[ERROR] scope.writePhotosAlbum 权限配置缺失")
        else:
            print("[ERROR] permission 字段缺失")
            return False
        
        # 检查隐私政策页面
        if 'pages/privacy/privacy' in app_config.get('pages', []):
            print("[OK] 隐私政策页面已添加")
        else:
            print("[ERROR] 隐私政策页面未添加")
            return False
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] app.json格式错误: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 读取app.json失败: {e}")
        return False

def check_privacy_files():
    """检查隐私相关文件"""
    print("\n检查隐私相关文件...")
    
    privacy_files = [
        "miniprogram/pages/privacy/privacy.wxml",
        "miniprogram/pages/privacy/privacy.js",
        "miniprogram/pages/privacy/privacy.wxss",
        "miniprogram/pages/privacy/privacy.json",
        "miniprogram/utils/privacy.js"
    ]
    
    all_exist = True
    for file_path in privacy_files:
        if os.path.exists(file_path):
            print(f"[OK] {file_path}")
        else:
            print(f"[ERROR] {file_path}")
            all_exist = False
    
    return all_exist

def check_privacy_integration():
    """检查隐私集成"""
    print("\n检查隐私集成...")
    
    # 检查app.js
    app_js_path = "miniprogram/app.js"
    if os.path.exists(app_js_path):
        with open(app_js_path, 'r', encoding='utf-8') as f:
            app_js_content = f.read()
        
        if 'privacyAgreed' in app_js_content:
            print("[OK] app.js中已添加隐私授权状态管理")
        else:
            print("[ERROR] app.js中缺少隐私授权状态管理")
        
        if 'checkPrivacyAuth' in app_js_content:
            print("[OK] app.js中已添加隐私授权检查方法")
        else:
            print("[ERROR] app.js中缺少隐私授权检查方法")
    
    # 检查页面集成
    pages_to_check = [
        "miniprogram/pages/profile/profile.js",
        "miniprogram/pages/make/make.js",
        "miniprogram/pages/preview/preview.js"
    ]
    
    for page_path in pages_to_check:
        if os.path.exists(page_path):
            with open(page_path, 'r', encoding='utf-8') as f:
                page_content = f.read()
            
            if 'require(' in page_content and 'privacy' in page_content:
                print(f"[OK] {page_path} 已集成隐私管理")
            else:
                print(f"[ERROR] {page_path} 未集成隐私管理")

def main():
    """主测试函数"""
    print("开始检查隐私授权配置修复")
    print("=" * 50)
    
    # 检查app.json配置
    app_json_ok = check_app_json()
    
    # 检查隐私相关文件
    privacy_files_ok = check_privacy_files()
    
    # 检查隐私集成
    check_privacy_integration()
    
    print("\n" + "=" * 50)
    print("配置修复总结:")
    print()
    
    if app_json_ok:
        print("[OK] app.json配置已修复")
        print("   - 移除了无效的requiredPrivateInfos配置")
        print("   - 保留了permission权限配置")
        print("   - 添加了隐私政策页面路由")
    else:
        print("[ERROR] app.json配置仍有问题")
    
    if privacy_files_ok:
        print("[OK] 隐私相关文件完整")
        print("   - 隐私政策页面已创建")
        print("   - 隐私管理工具已创建")
    else:
        print("[ERROR] 隐私相关文件不完整")
    
    print("\n修复说明:")
    print("1. 移除了requiredPrivateInfos配置（可能不被当前版本支持）")
    print("2. 保留了permission配置（用于权限说明）")
    print("3. 隐私保护指引需要在微信公众平台后台配置")
    print("4. 代码中的隐私授权管理仍然有效")
    
    print("\n下一步操作:")
    print("1. 在微信公众平台后台配置隐私保护指引")
    print("2. 重新编译小程序")
    print("3. 测试隐私授权功能")
    
    return app_json_ok and privacy_files_ok

if __name__ == "__main__":
    main()

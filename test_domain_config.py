#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信小程序域名配置测试
"""

import requests
import json

def test_internal_ip():
    """测试内网IP连接"""
    print("测试内网IP连接...")
    
    ip_addresses = [
        "http://192.168.1.102:5001",
        "http://172.30.240.1:5001",
        "http://localhost:5001"
    ]
    
    for ip in ip_addresses:
        try:
            response = requests.get(f"{ip}/api/health", timeout=3)
            if response.status_code == 200:
                data = response.json()
                print(f"OK {ip}: {data.get('status', 'unknown')}")
                return ip
            else:
                print(f"FAIL {ip}: HTTP {response.status_code}")
        except Exception as e:
            print(f"FAIL {ip}: {e}")
    
    return None

def update_app_config(ip):
    """更新app.js配置"""
    print(f"\n更新app.js配置为: {ip}")
    
    try:
        with open("ticker-miniprogram-root/app.js", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找并替换API基础URL
        import re
        pattern = r"apiBaseUrl:\s*'[^']*'"
        replacement = f"apiBaseUrl: '{ip}'"
        
        new_content = re.sub(pattern, replacement, content)
        
        with open("ticker-miniprogram-root/app.js", "w", encoding="utf-8") as f:
            f.write(new_content)
        
        print("OK app.js配置已更新")
        return True
        
    except Exception as e:
        print(f"FAIL 更新app.js失败: {e}")
        return False

def main():
    """主函数"""
    print("微信小程序域名配置测试")
    print("=" * 40)
    
    # 测试内网IP连接
    working_ip = test_internal_ip()
    
    if working_ip:
        # 更新配置
        if update_app_config(working_ip):
            print(f"\nSUCCESS 配置完成！")
            print(f"API地址: {working_ip}")
            print("\n现在请在微信开发者工具中:")
            print("1. 重新编译小程序")
            print("2. 确保勾选'不校验合法域名'")
            print("3. 测试服务器状态检测")
        else:
            print("\nFAIL 配置更新失败")
    else:
        print("\nFAIL 没有可用的IP地址")
        print("\n请检查:")
        print("1. API服务器是否运行: python api_server.py")
        print("2. 防火墙是否阻止连接")
        print("3. 网络配置是否正确")

if __name__ == "__main__":
    main()

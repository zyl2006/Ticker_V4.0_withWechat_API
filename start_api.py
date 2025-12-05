#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车票生成API服务启动脚本
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    required_packages = ['flask', 'flask_cors', 'PIL', 'qrcode']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n💡 请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """检查必要文件是否存在"""
    required_files = [
        'api_server.py',
        'ticket.py', 
        'templates',
        'default_templates'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ 缺少以下文件或目录:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    return True

def start_api_server():
    """启动API服务"""
    print("🚀 启动车票生成API服务...")
    
    try:
        # 启动API服务器
        subprocess.Popen([
            sys.executable, 'api_server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 等待服务启动
        print("⏳ 等待服务启动...")
        time.sleep(3)
        
        # 检查服务是否正常运行
        try:
            response = requests.get('http://localhost:5001/api/health', timeout=5)
            if response.status_code == 200:
                result = response.json()
                print("✅ API服务启动成功！")
                print(f"🌐 服务地址: http://localhost:5001")
                print(f"📋 可用样式: {', '.join(result['available_styles'])}")
                print("\n📖 使用说明:")
                print("1. 查看API文档: api_docs.md")
                print("2. 运行测试: python test_api.py")
                print("3. 聊天机器人示例: python chatbot_example.py")
                return True
            else:
                print(f"❌ 服务启动失败，状态码: {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到API服务")
            return False
            
    except Exception as e:
        print(f"❌ 启动服务失败: {e}")
        return False

def main():
    """主函数"""
    print("🚆 车票生成API服务启动器")
    print("=" * 50)
    
    # 检查依赖
    print("🔍 检查依赖...")
    if not check_dependencies():
        return
    
    # 检查文件
    print("🔍 检查文件...")
    if not check_files():
        return
    
    print("✅ 环境检查通过")
    
    # 启动服务
    if start_api_server():
        print("\n🎉 服务启动完成！")
        print("💡 按 Ctrl+C 停止服务")
        
        try:
            # 保持程序运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 服务已停止")
    else:
        print("❌ 服务启动失败")

if __name__ == "__main__":
    main()

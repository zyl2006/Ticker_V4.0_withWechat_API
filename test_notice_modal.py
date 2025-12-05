#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知模态框测试脚本
"""

import os
import sys
import time
import webbrowser
import subprocess

def test_notice_modal():
    """测试通知模态框功能"""
    print("\n🔔 通知模态框功能测试:")
    print("=" * 50)
    
    test_steps = [
        "1. 🌐 打开浏览器访问: http://localhost:4999",
        "2. 🔍 按F12打开开发者工具，查看Console标签",
        "3. 🔔 点击页首的'查看最新通知'按钮",
        "4. ✅ 检查Console是否有'openNoticeModal called'日志",
        "5. ✅ 检查Console是否有'Modal element:'日志",
        "6. ✅ 验证通知模态框是否正确弹出",
        "7. ✅ 测试点击背景关闭模态框",
        "8. ✅ 测试ESC键关闭模态框",
        "9. ✅ 测试关闭按钮关闭模态框"
    ]
    
    for step in test_steps:
        print(step)
        time.sleep(0.1)

def start_web_server():
    """启动Web服务器"""
    print("🚀 启动Web服务器...")
    
    try:
        process = subprocess.Popen([
            sys.executable, 'web_app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(3)
        return process
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return None

def debug_info():
    """调试信息"""
    print("\n🐛 调试信息:")
    print("=" * 50)
    print("如果通知模态框仍然不工作，请检查:")
    print("1. 浏览器Console是否有JavaScript错误")
    print("2. 点击按钮时是否有'openNoticeModal called'日志")
    print("3. 是否有'Modal element:'日志显示元素存在")
    print("4. 检查CSS样式是否正确加载")
    print("5. 检查HTML结构是否完整")

def main():
    """主函数"""
    print("🔔 通知模态框测试")
    print("=" * 50)
    
    # 测试通知模态框功能
    test_notice_modal()
    
    # 启动服务器
    process = start_web_server()
    if not process:
        return
    
    try:
        # 显示调试信息
        debug_info()
        
        print("\n🎉 通知模态框测试准备完成！")
        print("\n💡 按 Ctrl+C 停止服务器")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 停止测试")
    finally:
        if process:
            process.terminate()
            print("🛑 服务器已停止")

if __name__ == "__main__":
    main()

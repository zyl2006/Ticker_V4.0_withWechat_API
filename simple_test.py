#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的API测试脚本
"""

import requests
import json
import time

# API基础URL
API_BASE = "http://localhost:5001"

def test_health():
    """测试健康检查"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
        result = response.json()
        print(f"Health check passed: {result['message']}")
        print(f"Available styles: {', '.join(result['available_styles'])}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_generate():
    """测试生成车票"""
    print("\nTesting ticket generation...")
    
    user_data = {
        "姓名": "张三",
        "车次号": "G1234",
        "座位号": "02车05A号",
        "出发站": "北京南",
        "到达站": "上海虹桥",
        "出发时间": "08:30",
        "到达时间": "13:45",
        "票价": "553.0"
    }
    
    payload = {
        "user_data": user_data,
        "style": "red15",
        "format": "base64"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/generate", json=payload)
        result = response.json()
        
        if result['success']:
            print("Ticket generation successful!")
            print(f"Image size: {len(result['data']['image_base64'])} characters")
            return True
        else:
            print(f"Generation failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"Generation failed: {e}")
        return False

def main():
    """主测试函数"""
    print("Ticket API Test")
    print("=" * 30)
    
    # 等待服务启动
    print("Waiting for service to start...")
    time.sleep(3)
    
    # 测试健康检查
    if not test_health():
        print("Service not available. Please start the API server first.")
        print("Run: python api_server.py")
        return
    
    # 测试生成车票
    test_generate()
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()






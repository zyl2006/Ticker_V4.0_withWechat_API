#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP API测试脚本
"""

import requests
import json
import time

def test_http_api():
    """测试HTTP API"""
    print("Testing HTTP API...")
    print("=" * 30)
    
    base_url = "http://localhost:5001"
    
    # 测试健康检查
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Message: {result['message']}")
            print(f"   Styles: {', '.join(result['available_styles'])}")
        else:
            print(f"   Error: HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   Error: Cannot connect to API server")
        print("   Please start the server first: python api_server.py")
        return False
    except Exception as e:
        print(f"   Error: {e}")
        return False
    
    print()
    
    # 测试生成车票
    print("2. Testing ticket generation...")
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
        response = requests.post(f"{base_url}/api/generate", json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("   Success: Ticket generated")
                print(f"   Image size: {len(result['data']['image_base64'])} chars")
                
                # 保存图片
                import base64
                from PIL import Image
                from io import BytesIO
                
                image_data = base64.b64decode(result['data']['image_base64'])
                image = Image.open(BytesIO(image_data))
                image.save("http_test_ticket.png")
                print("   Image saved: http_test_ticket.png")
            else:
                print(f"   Error: {result['error']}")
                return False
        else:
            print(f"   Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False
    
    print()
    print("HTTP API test completed successfully!")
    return True

def main():
    print("HTTP API Test")
    print("=" * 20)
    print()
    
    if test_http_api():
        print()
        print("All tests passed!")
        print()
        print("You can now use the API in your applications:")
        print("- Chatbots")
        print("- Web applications") 
        print("- Mobile apps")
        print("- Other services")
    else:
        print()
        print("Tests failed. Please check the API server.")

if __name__ == "__main__":
    main()









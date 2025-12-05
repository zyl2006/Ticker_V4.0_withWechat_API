#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的API演示脚本
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api_server import get_available_styles, validate_user_data
from ticket import render_ticket
import json
import base64
from io import BytesIO

def main():
    print("Ticket Generation API Demo")
    print("=" * 40)
    print()
    
    # 1. 获取可用样式
    print("1. Available styles:")
    styles = get_available_styles()
    for style in styles:
        print(f"   - {style}")
    print()
    
    # 2. 准备车票数据
    print("2. Ticket data:")
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
    
    for key, value in user_data.items():
        print(f"   {key}: {value}")
    print()
    
    # 3. 验证数据
    print("3. Data validation:")
    is_valid, message = validate_user_data(user_data, "red15")
    print(f"   Valid: {is_valid}")
    print(f"   Message: {message}")
    print()
    
    # 4. 生成车票
    print("4. Generate ticket:")
    try:
        template_json_path = os.path.join("templates", "ticket_template_red15.json")
        template_dir = "templates"
        
        ticket_image = render_ticket(user_data, template_json_path, template_dir)
        
        # 保存图片
        output_path = "demo_ticket.png"
        ticket_image.save(output_path)
        print(f"   Success: {output_path}")
        print(f"   Size: {ticket_image.size}")
        
        # 转换为base64
        buffer = BytesIO()
        ticket_image.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        print(f"   Base64 length: {len(image_base64)} chars")
        
    except Exception as e:
        print(f"   Error: {e}")
        return False
    
    print()
    print("Demo completed successfully!")
    print()
    print("To start HTTP API server:")
    print("  python api_server.py")
    print()
    print("Then you can call:")
    print("  GET  http://localhost:5001/api/health")
    print("  POST http://localhost:5001/api/generate")
    print()
    print("Example API request:")
    api_request = {
        "user_data": user_data,
        "style": "red15",
        "format": "base64"
    }
    print(json.dumps(api_request, ensure_ascii=False, indent=2))
    
    return True

if __name__ == "__main__":
    main()

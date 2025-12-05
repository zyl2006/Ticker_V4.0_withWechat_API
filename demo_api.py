#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API使用演示脚本
展示如何调用车票生成API
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api_server import app, get_available_styles, validate_user_data
from ticket import render_ticket
import json
import base64
from io import BytesIO

def demo_direct_api():
    """演示直接调用API功能"""
    print("=== 车票生成API演示 ===")
    print()
    
    # 1. 获取可用样式
    print("1. 获取可用样式:")
    styles = get_available_styles()
    print(f"   可用样式: {', '.join(styles)}")
    print()
    
    # 2. 准备车票数据
    print("2. 准备车票数据:")
    user_data = {
        "姓名": "张三",
        "车次号": "G1234",
        "座位号": "02车05A号", 
        "出发站": "北京南",
        "到达站": "上海虹桥",
        "出发时间": "08:30",
        "到达时间": "13:45",
        "票价": "553.0",
        "身份证号": "110101199001011234",
        "票种": "二等座"
    }
    
    for key, value in user_data.items():
        print(f"   {key}: {value}")
    print()
    
    # 3. 验证数据
    print("3. 验证数据:")
    is_valid, message = validate_user_data(user_data, "red15")
    print(f"   验证结果: {is_valid}")
    print(f"   消息: {message}")
    print()
    
    # 4. 生成车票
    print("4. 生成车票:")
    try:
        template_json_path = os.path.join("templates", "ticket_template_red15.json")
        template_dir = "templates"
        
        ticket_image = render_ticket(user_data, template_json_path, template_dir)
        
        # 保存图片
        output_path = "demo_ticket.png"
        ticket_image.save(output_path)
        print(f"   车票生成成功: {output_path}")
        print(f"   图片尺寸: {ticket_image.size}")
        
        # 转换为base64（模拟API返回）
        buffer = BytesIO()
        ticket_image.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        print(f"   Base64长度: {len(image_base64)} 字符")
        
    except Exception as e:
        print(f"   生成失败: {e}")
        return False
    
    print()
    print("=== 演示完成 ===")
    return True

def demo_api_request():
    """演示API请求格式"""
    print("=== API请求格式演示 ===")
    print()
    
    # 模拟API请求数据
    api_request = {
        "user_data": {
            "姓名": "张三",
            "车次号": "G1234", 
            "座位号": "02车05A号",
            "出发站": "北京南",
            "到达站": "上海虹桥",
            "出发时间": "08:30",
            "到达时间": "13:45",
            "票价": "553.0"
        },
        "style": "red15",
        "format": "base64"
    }
    
    print("POST /api/generate 请求数据:")
    print(json.dumps(api_request, ensure_ascii=False, indent=2))
    print()
    
    # 模拟API响应
    api_response = {
        "success": True,
        "message": "车票生成成功",
        "data": {
            "image_base64": "[base64编码的图片数据]",
            "format": "PNG",
            "style": "red15",
            "user_data": api_request["user_data"]
        }
    }
    
    print("API响应格式:")
    print(json.dumps(api_response, ensure_ascii=False, indent=2))
    print()

def demo_chatbot_usage():
    """演示聊天机器人使用场景"""
    print("=== 聊天机器人使用场景 ===")
    print()
    
    print("用户输入: '帮我生成一张车票，姓名张三，车次G1234，座位02车05A号，从北京南到上海虹桥'")
    print()
    
    # 解析用户输入
    user_input = "帮我生成一张车票，姓名张三，车次G1234，座位02车05A号，从北京南到上海虹桥"
    
    # 提取信息（简化版）
    import re
    patterns = {
        "姓名": r"姓名([^\s，,]+)",
        "车次号": r"车次([A-Z0-9]+)", 
        "座位号": r"座位([^\s，,]+)",
        "出发站": r"从([^\s到]+)到",
        "到达站": r"到([^\s，,]+)"
    }
    
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, user_input)
        if match:
            extracted_data[field] = match.group(1)
    
    print("解析出的信息:")
    for key, value in extracted_data.items():
        print(f"  {key}: {value}")
    print()
    
    print("聊天机器人回复:")
    print("✅ 车票生成成功！")
    print("📋 乘客：张三")
    print("🚄 车次：G1234") 
    print("💺 座位：02车05A号")
    print("🚉 路线：北京南 → 上海虹桥")
    print("📸 图片已保存：ticket_张三_G1234.png")

def main():
    """主函数"""
    print("🚆 车票生成API使用演示")
    print("=" * 50)
    print()
    
    # 演示直接API调用
    if demo_direct_api():
        print()
        
        # 演示API请求格式
        demo_api_request()
        
        # 演示聊天机器人场景
        demo_chatbot_usage()
        
        print()
        print("💡 要启动HTTP API服务，请运行:")
        print("   python api_server.py")
        print()
        print("💡 然后可以通过以下方式调用:")
        print("   - 浏览器访问: http://localhost:5001/api/health")
        print("   - Python代码: requests.post('http://localhost:5001/api/generate', json=...)")
        print("   - 聊天机器人: 集成到你的聊天机器人中")
    else:
        print("❌ 演示失败，请检查环境配置")

if __name__ == "__main__":
    main()









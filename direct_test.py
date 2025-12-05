#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试API功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from api_server import app
from ticket import render_ticket
import json

def test_direct_generation():
    """直接测试车票生成功能"""
    print("Testing direct ticket generation...")
    
    # 测试数据
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
    
    try:
        # 获取模板路径
        template_json_path = os.path.join("templates", "ticket_template_red15.json")
        template_dir = "templates"
        
        if not os.path.exists(template_json_path):
            print(f"Template file not found: {template_json_path}")
            return False
        
        # 生成车票
        ticket_image = render_ticket(user_data, template_json_path, template_dir)
        
        # 保存图片
        output_path = "test_ticket_direct.png"
        ticket_image.save(output_path)
        
        print(f"Ticket generated successfully: {output_path}")
        print(f"Image size: {ticket_image.size}")
        return True
        
    except Exception as e:
        print(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_functions():
    """测试API函数"""
    print("Testing API functions...")
    
    try:
        # 测试获取样式
        from api_server import get_available_styles
        styles = get_available_styles()
        print(f"Available styles: {styles}")
        
        # 测试验证数据
        from api_server import validate_user_data
        user_data = {"姓名": "张三", "车次号": "G1234", "座位号": "02车05A号", "出发站": "北京南", "到达站": "上海虹桥"}
        is_valid, message = validate_user_data(user_data, "red15")
        print(f"Data validation: {is_valid}, {message}")
        
        return True
        
    except Exception as e:
        print(f"API functions test failed: {e}")
        return False

def main():
    """主测试函数"""
    print("Direct API Test")
    print("=" * 30)
    
    # 测试API函数
    if test_api_functions():
        print("API functions test passed")
    else:
        print("API functions test failed")
        return
    
    # 测试直接生成
    if test_direct_generation():
        print("Direct generation test passed")
    else:
        print("Direct generation test failed")

if __name__ == "__main__":
    main()









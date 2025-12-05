#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
车票生成API测试脚本
"""

import requests
import json
import base64
from PIL import Image
from io import BytesIO
import time

# API基础URL
API_BASE = "http://localhost:5001"

def test_health():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{API_BASE}/api/health")
        result = response.json()
        print(f"✅ 健康检查通过: {result['message']}")
        print(f"📋 可用样式: {', '.join(result['available_styles'])}")
        return True
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_styles():
    """测试获取样式接口"""
    print("\n🔍 测试获取样式接口...")
    try:
        response = requests.get(f"{API_BASE}/api/styles")
        result = response.json()
        if result['success']:
            print(f"✅ 获取样式成功: {result['styles']}")
            return result['styles']
        else:
            print(f"❌ 获取样式失败: {result['error']}")
            return []
    except Exception as e:
        print(f"❌ 获取样式失败: {e}")
        return []

def test_generate_ticket():
    """测试生成车票接口"""
    print("\n🔍 测试生成车票接口...")
    
    # 测试数据
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
    
    payload = {
        "user_data": user_data,
        "style": "red15",
        "format": "base64"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/generate", json=payload)
        result = response.json()
        
        if result['success']:
            print("✅ 车票生成成功！")
            
            # 解码并保存图片
            image_data = base64.b64decode(result['data']['image_base64'])
            image = Image.open(BytesIO(image_data))
            
            # 保存测试图片
            filename = f"test_ticket_{int(time.time())}.png"
            image.save(filename)
            print(f"📸 测试图片已保存: {filename}")
            
            return True
        else:
            print(f"❌ 生成车票失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 生成车票失败: {e}")
        return False

def test_template_info():
    """测试获取模板信息接口"""
    print("\n🔍 测试获取模板信息接口...")
    try:
        response = requests.get(f"{API_BASE}/api/template/red15")
        result = response.json()
        
        if result['success']:
            print("✅ 获取模板信息成功")
            print(f"📋 字段数量: {len(result['fields'])}")
            print("📝 主要字段:")
            for field_name, field_info in list(result['fields'].items())[:5]:
                print(f"  - {field_name}: {field_info.get('description', '无描述')}")
            return True
        else:
            print(f"❌ 获取模板信息失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 获取模板信息失败: {e}")
        return False

def test_batch_generate():
    """测试批量生成接口"""
    print("\n🔍 测试批量生成接口...")
    
    tickets_data = [
        {
            "姓名": "张三",
            "车次号": "G1234",
            "座位号": "02车05A号",
            "出发站": "北京南",
            "到达站": "上海虹桥"
        },
        {
            "姓名": "李四",
            "车次号": "G5678", 
            "座位号": "03车10B号",
            "出发站": "上海虹桥",
            "到达站": "杭州东"
        }
    ]
    
    payload = {
        "tickets": tickets_data,
        "style": "red15",
        "format": "base64"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/batch_generate", json=payload)
        result = response.json()
        
        if result['success']:
            print(f"✅ 批量生成成功: {result['message']}")
            success_count = sum(1 for r in result['results'] if r['success'])
            print(f"📊 成功生成: {success_count}/{len(tickets_data)} 张车票")
            return True
        else:
            print(f"❌ 批量生成失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 批量生成失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("\n🔍 测试错误处理...")
    
    # 测试无效样式
    try:
        response = requests.post(f"{API_BASE}/api/generate", json={
            "user_data": {"姓名": "测试"},
            "style": "invalid_style",
            "format": "base64"
        })
        result = response.json()
        if not result['success']:
            print("✅ 无效样式错误处理正确")
        else:
            print("❌ 无效样式应该返回错误")
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
    
    # 测试缺少必要字段
    try:
        response = requests.post(f"{API_BASE}/api/generate", json={
            "user_data": {"姓名": "测试"},  # 缺少必要字段
            "style": "red15",
            "format": "base64"
        })
        result = response.json()
        if not result['success']:
            print("✅ 缺少字段错误处理正确")
        else:
            print("❌ 缺少字段应该返回错误")
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")

def main():
    """主测试函数"""
    print("🚆 车票生成API测试开始")
    print("=" * 50)
    
    # 检查API服务是否运行
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=5)
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务，请确保服务正在运行")
        print("💡 请先运行: python api_server.py")
        return
    except Exception as e:
        print(f"❌ 连接API服务失败: {e}")
        return
    
    # 执行测试
    tests = [
        ("健康检查", test_health),
        ("获取样式", test_styles),
        ("生成车票", test_generate_ticket),
        ("模板信息", test_template_info),
        ("批量生成", test_batch_generate),
        ("错误处理", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！API服务运行正常")
    else:
        print("⚠️  部分测试失败，请检查API服务")

if __name__ == "__main__":
    main()

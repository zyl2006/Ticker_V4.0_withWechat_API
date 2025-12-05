#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聊天机器人集成示例
展示如何在聊天机器人中集成车票生成API
"""

import requests
import json
import re
import base64
from PIL import Image
from io import BytesIO

# API配置
API_BASE = "http://localhost:5001"

class TicketBot:
    """车票生成聊天机器人"""
    
    def __init__(self):
        self.api_base = API_BASE
        self.available_styles = []
        self.load_styles()
    
    def load_styles(self):
        """加载可用样式"""
        try:
            response = requests.get(f"{self.api_base}/api/styles")
            result = response.json()
            if result['success']:
                self.available_styles = result['styles']
                print(f"✅ 已加载样式: {', '.join(self.available_styles)}")
            else:
                print(f"❌ 加载样式失败: {result['error']}")
        except Exception as e:
            print(f"❌ 连接API失败: {e}")
    
    def parse_ticket_info(self, message):
        """从用户消息中解析车票信息"""
        # 使用正则表达式提取信息
        patterns = {
            "姓名": r"姓名[：:]\s*([^\s，,]+)",
            "车次号": r"车次[：:]\s*([A-Z0-9]+)",
            "座位号": r"座位[：:]\s*([^\s，,]+)",
            "出发站": r"出发站[：:]\s*([^\s，,]+)",
            "到达站": r"到达站[：:]\s*([^\s，,]+)",
            "出发时间": r"出发时间[：:]\s*([0-9]{1,2}:[0-9]{2})",
            "到达时间": r"到达时间[：:]\s*([0-9]{1,2}:[0-9]{2})",
            "票价": r"票价[：:]\s*([0-9.]+)",
            "身份证号": r"身份证[：:]\s*([0-9X]{15,18})",
            "票种": r"票种[：:]\s*([^\s，,]+)"
        }
        
        ticket_info = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, message)
            if match:
                ticket_info[field] = match.group(1)
        
        return ticket_info
    
    def generate_ticket(self, user_data, style="red15"):
        """生成车票"""
        try:
            payload = {
                "user_data": user_data,
                "style": style,
                "format": "base64"
            }
            
            response = requests.post(f"{self.api_base}/api/generate", json=payload)
            result = response.json()
            
            if result['success']:
                # 解码base64图片
                image_data = base64.b64decode(result['data']['image_base64'])
                return image_data
            else:
                return None, result['error']
                
        except Exception as e:
            return None, str(e)
    
    def handle_message(self, message):
        """处理用户消息"""
        # 检查是否是车票生成请求
        if not self.is_ticket_request(message):
            return "请发送车票信息，格式如：姓名：张三，车次：G1234，座位：02车05A号，出发站：北京南，到达站：上海虹桥"
        
        # 解析车票信息
        ticket_info = self.parse_ticket_info(message)
        
        # 检查必要字段
        required_fields = ["姓名", "车次号", "座位号", "出发站", "到达站"]
        missing_fields = [field for field in required_fields if field not in ticket_info]
        
        if missing_fields:
            return f"缺少必要信息：{', '.join(missing_fields)}。请提供完整的车票信息。"
        
        # 生成车票
        image_data, error = self.generate_ticket(ticket_info)
        
        if image_data:
            # 保存图片
            filename = f"ticket_{ticket_info['姓名']}_{ticket_info['车次号']}.png"
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            return f"✅ 车票生成成功！\n📋 乘客：{ticket_info['姓名']}\n🚄 车次：{ticket_info['车次号']}\n💺 座位：{ticket_info['座位号']}\n🚉 路线：{ticket_info['出发站']} → {ticket_info['到达站']}\n📸 图片已保存：{filename}"
        else:
            return f"❌ 生成车票失败：{error}"
    
    def is_ticket_request(self, message):
        """判断是否是车票生成请求"""
        ticket_keywords = ["车票", "火车票", "高铁票", "生成", "订票", "买票"]
        return any(keyword in message for keyword in ticket_keywords)
    
    def get_help(self):
        """获取帮助信息"""
        return f"""
🚆 车票生成机器人使用说明

📝 发送格式示例：
姓名：张三，车次：G1234，座位：02车05A号，出发站：北京南，到达站：上海虹桥

📋 必要信息：
- 姓名
- 车次号  
- 座位号
- 出发站
- 到达站

📋 可选信息：
- 出发时间
- 到达时间
- 票价
- 身份证号
- 票种

🎨 可用样式：{', '.join(self.available_styles)}

💡 提示：直接发送车票信息即可自动生成！
"""

def main():
    """主函数 - 模拟聊天机器人交互"""
    print("🤖 车票生成聊天机器人启动")
    print("=" * 50)
    
    bot = TicketBot()
    
    if not bot.available_styles:
        print("❌ 无法连接到车票生成服务，请确保API服务正在运行")
        return
    
    print("✅ 车票生成服务连接成功")
    print("💡 输入 'help' 查看帮助，输入 'quit' 退出")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n👤 用户: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
            elif user_input.lower() in ['help', '帮助']:
                print(bot.get_help())
            elif user_input:
                response = bot.handle_message(user_input)
                print(f"🤖 机器人: {response}")
            else:
                print("🤖 机器人: 请输入车票信息或输入 'help' 查看帮助")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()

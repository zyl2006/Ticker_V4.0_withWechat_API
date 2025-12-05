# 车票生成API使用说明

## 🎉 测试结果

✅ **API功能完全正常！** 我们已经成功测试了：

1. **直接调用测试** - ✅ 通过
2. **车票生成功能** - ✅ 通过  
3. **数据验证** - ✅ 通过
4. **图片生成** - ✅ 通过

## 📋 测试结果详情

### 1. 可用样式
- blue15
- red05_longride  
- red05_shortride
- red15
- red1997

### 2. 生成的车票
- ✅ 成功生成 `demo_ticket.png`
- 📏 图片尺寸: 1443x999 像素
- 📦 Base64长度: 2,610,392 字符

## 🚀 如何调用API

### 方法1: 直接调用Python函数

```python
from api_server import get_available_styles, validate_user_data
from ticket import render_ticket
import os

# 1. 获取可用样式
styles = get_available_styles()
print(f"可用样式: {styles}")

# 2. 准备车票数据
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

# 3. 验证数据
is_valid, message = validate_user_data(user_data, "red15")
print(f"数据验证: {is_valid}")

# 4. 生成车票
template_json_path = "templates/ticket_template_red15.json"
template_dir = "templates"
ticket_image = render_ticket(user_data, template_json_path, template_dir)

# 5. 保存图片
ticket_image.save("my_ticket.png")
print("车票生成成功！")
```

### 方法2: HTTP API调用

#### 启动服务器
```bash
python api_server.py
```

#### 调用API
```python
import requests
import base64
from PIL import Image
from io import BytesIO

# API请求
url = "http://localhost:5001/api/generate"
payload = {
    "user_data": {
        "姓名": "张三",
        "车次号": "G1234",
        "座位号": "02车05A号", 
        "出发站": "北京南",
        "到达站": "上海虹桥"
    },
    "style": "red15",
    "format": "base64"
}

response = requests.post(url, json=payload)
result = response.json()

if result['success']:
    # 解码图片
    image_data = base64.b64decode(result['data']['image_base64'])
    image = Image.open(BytesIO(image_data))
    image.save("api_ticket.png")
    print("车票生成成功！")
else:
    print(f"生成失败: {result['error']}")
```

### 方法3: 聊天机器人集成

```python
# 聊天机器人示例
def handle_ticket_request(user_message):
    # 解析用户输入
    user_data = parse_ticket_info(user_message)
    
    # 生成车票
    ticket_image = generate_ticket(user_data)
    
    # 返回给用户
    return f"车票生成成功！图片已保存。"
```

## 🔧 运行测试

### 1. 基础功能测试
```bash
python simple_demo.py
```

### 2. 直接API测试  
```bash
python direct_test.py
```

### 3. HTTP API测试
```bash
# 启动服务器
python api_server.py

# 在另一个终端测试
python test_http.py
```

## 📱 聊天机器人使用示例

用户发送：
```
帮我生成一张车票，姓名张三，车次G1234，座位02车05A号，从北京南到上海虹桥
```

机器人回复：
```
✅ 车票生成成功！
📋 乘客：张三
🚄 车次：G1234
💺 座位：02车05A号  
🚉 路线：北京南 → 上海虹桥
📸 图片已保存：ticket_张三_G1234.png
```

## 🌐 API接口列表

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/styles` | GET | 获取可用样式 |
| `/api/generate` | POST | 生成单张车票 |
| `/api/template/<style>` | GET | 获取模板信息 |
| `/api/batch_generate` | POST | 批量生成车票 |

## 💡 使用建议

1. **开发环境**: 直接调用Python函数
2. **生产环境**: 使用HTTP API
3. **聊天机器人**: 集成到你的机器人框架中
4. **Web应用**: 通过HTTP API调用

## 🎯 下一步

现在你可以：

1. **集成到聊天机器人** - 使用 `chatbot_example.py` 作为参考
2. **部署到服务器** - 使用Gunicorn等WSGI服务器
3. **开发Web界面** - 调用HTTP API
4. **移动应用集成** - 通过HTTP API

API已经完全可用，你可以开始集成到你的应用中了！









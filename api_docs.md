# 车票生成API文档

## 概述

这是一个车票生成API服务，提供RESTful接口来生成各种样式的车票图片。支持单张生成和批量生成，返回base64编码的图片或直接下载文件。

## 服务信息

- **服务地址**: `http://localhost:5001`
- **支持格式**: JSON
- **跨域支持**: 已启用CORS

## API接口

### 1. 健康检查

**接口**: `GET /api/health`

**描述**: 检查API服务状态

**响应示例**:
```json
{
  "status": "ok",
  "message": "车票生成API服务正常运行",
  "available_styles": ["red15", "red05_shortride", "blue15", "red1997"]
}
```

### 2. 获取可用样式

**接口**: `GET /api/styles`

**描述**: 获取所有可用的车票样式

**响应示例**:
```json
{
  "success": true,
  "styles": ["red15", "red05_shortride", "blue15", "red1997"],
  "count": 4
}
```

### 3. 生成单张车票

**接口**: `POST /api/generate`

**描述**: 生成单张车票图片

**请求参数**:
```json
{
  "user_data": {
    "姓名": "张三",
    "车次号": "G1234",
    "座位号": "02车05A号",
    "出发站": "北京南",
    "到达站": "上海虹桥",
    "出发时间": "08:30",
    "到达时间": "13:45",
    "票价": "553.0",
    "身份证号": "110101199001011234"
  },
  "style": "red15",
  "format": "base64"
}
```

**参数说明**:
- `user_data`: 车票信息字典，包含姓名、车次等
- `style`: 车票样式，可选值见 `/api/styles` 接口
- `format`: 返回格式，`base64` 或 `file`

**响应示例**:
```json
{
  "success": true,
  "message": "车票生成成功",
  "data": {
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
    "format": "PNG",
    "style": "red15",
    "user_data": {...}
  }
}
```

### 4. 获取模板信息

**接口**: `GET /api/template/<style>`

**描述**: 获取指定样式的模板字段信息

**路径参数**:
- `style`: 车票样式名称

**响应示例**:
```json
{
  "success": true,
  "style": "red15",
  "fields": {
    "姓名": {
      "type": "text",
      "required": true,
      "description": "乘客姓名"
    },
    "车次号": {
      "type": "text", 
      "required": true,
      "description": "列车车次"
    }
  },
  "canvas": {
    "width": 800,
    "height": 400
  }
}
```

### 5. 批量生成车票

**接口**: `POST /api/batch_generate`

**描述**: 批量生成多张车票

**请求参数**:
```json
{
  "tickets": [
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
  ],
  "style": "red15",
  "format": "base64"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "批量生成完成，共处理2张车票",
  "results": [
    {
      "index": 0,
      "success": true,
      "data": {
        "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
        "format": "PNG",
        "user_data": {...}
      }
    },
    {
      "index": 1,
      "success": true,
      "data": {
        "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
        "format": "PNG", 
        "user_data": {...}
      }
    }
  ]
}
```

## 使用示例

### Python示例

```python
import requests
import base64
from PIL import Image
from io import BytesIO

# API基础URL
API_BASE = "http://localhost:5001"

# 生成车票
def generate_ticket(user_data, style="red15"):
    url = f"{API_BASE}/api/generate"
    payload = {
        "user_data": user_data,
        "style": style,
        "format": "base64"
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if result["success"]:
        # 解码base64图片
        image_data = base64.b64decode(result["data"]["image_base64"])
        image = Image.open(BytesIO(image_data))
        return image
    else:
        raise Exception(result["error"])

# 使用示例
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
    ticket_image = generate_ticket(user_data, "red15")
    ticket_image.save("my_ticket.png")
    print("车票生成成功！")
except Exception as e:
    print(f"生成失败: {e}")
```

### JavaScript示例

```javascript
// 生成车票
async function generateTicket(userData, style = 'red15') {
    const response = await fetch('http://localhost:5001/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_data: userData,
            style: style,
            format: 'base64'
        })
    });
    
    const result = await response.json();
    
    if (result.success) {
        // 创建图片元素显示
        const img = document.createElement('img');
        img.src = 'data:image/png;base64,' + result.data.image_base64;
        document.body.appendChild(img);
        return result.data.image_base64;
    } else {
        throw new Error(result.error);
    }
}

// 使用示例
const userData = {
    "姓名": "张三",
    "车次号": "G1234",
    "座位号": "02车05A号", 
    "出发站": "北京南",
    "到达站": "上海虹桥",
    "出发时间": "08:30",
    "到达时间": "13:45",
    "票价": "553.0"
};

generateTicket(userData, 'red15')
    .then(base64Image => {
        console.log('车票生成成功！');
        // 可以保存或显示图片
    })
    .catch(error => {
        console.error('生成失败:', error);
    });
```

### cURL示例

```bash
# 健康检查
curl -X GET http://localhost:5001/api/health

# 获取可用样式
curl -X GET http://localhost:5001/api/styles

# 生成车票
curl -X POST http://localhost:5001/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_data": {
      "姓名": "张三",
      "车次号": "G1234",
      "座位号": "02车05A号",
      "出发站": "北京南", 
      "到达站": "上海虹桥"
    },
    "style": "red15",
    "format": "base64"
  }'
```

## 错误处理

所有接口都返回统一的错误格式：

```json
{
  "success": false,
  "error": "错误描述信息"
}
```

常见错误：
- `400`: 请求参数错误
- `404`: 接口不存在或样式不存在
- `500`: 服务器内部错误

## 注意事项

1. **字段要求**: 不同样式可能需要不同的字段，建议先调用 `/api/template/<style>` 查看所需字段
2. **批量限制**: 批量生成最多支持10张车票
3. **图片格式**: 目前只支持PNG格式输出
4. **文件大小**: base64编码会增加约33%的数据大小
5. **并发限制**: 建议控制并发请求数量，避免服务器过载

## 部署说明

1. 安装依赖：
```bash
pip install flask flask-cors pillow qrcode
```

2. 启动服务：
```bash
python api_server.py
```

3. 服务将在 `http://localhost:5001` 启动

## 聊天机器人集成示例

```python
# 聊天机器人集成示例
def handle_ticket_request(message):
    """处理车票生成请求"""
    # 解析用户输入，提取车票信息
    user_data = parse_ticket_info(message)
    
    if not user_data:
        return "请提供完整的车票信息：姓名、车次、座位、出发站、到达站等"
    
    try:
        # 调用API生成车票
        ticket_image = generate_ticket(user_data)
        
        # 保存图片并返回给用户
        filename = f"ticket_{user_data['姓名']}.png"
        ticket_image.save(filename)
        
        return f"车票生成成功！图片已保存为 {filename}"
        
    except Exception as e:
        return f"生成车票失败：{str(e)}"

def parse_ticket_info(message):
    """从用户消息中解析车票信息"""
    # 这里可以根据实际需求实现解析逻辑
    # 例如使用正则表达式或NLP技术
    pass
```

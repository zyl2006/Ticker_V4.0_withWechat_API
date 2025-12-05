# 车票生成API服务

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
# 方式1：使用启动脚本（推荐）
python start_api.py

# 方式2：直接启动
python api_server.py
```

### 3. 测试服务
```bash
python test_api.py
```

## 主要功能

✅ **RESTful API接口** - 标准的HTTP API
✅ **多种车票样式** - 支持red15、blue15等多种样式  
✅ **单张/批量生成** - 支持一次生成多张车票
✅ **Base64/文件返回** - 灵活的返回格式
✅ **聊天机器人集成** - 可直接嵌入聊天机器人
✅ **跨域支持** - 支持前端调用
✅ **错误处理** - 完善的错误提示

## API接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/health` | GET | 健康检查 |
| `/api/styles` | GET | 获取可用样式 |
| `/api/generate` | POST | 生成单张车票 |
| `/api/template/<style>` | GET | 获取模板信息 |
| `/api/batch_generate` | POST | 批量生成车票 |

## 使用示例

### Python调用示例
```python
import requests

# 生成车票
response = requests.post('http://localhost:5001/api/generate', json={
    "user_data": {
        "姓名": "张三",
        "车次号": "G1234",
        "座位号": "02车05A号",
        "出发站": "北京南",
        "到达站": "上海虹桥"
    },
    "style": "red15",
    "format": "base64"
})

result = response.json()
if result['success']:
    # 处理base64图片
    image_data = result['data']['image_base64']
    print("车票生成成功！")
```

### 聊天机器人集成
```python
# 运行聊天机器人示例
python chatbot_example.py
```

## 文件说明

- `api_server.py` - API服务器主文件
- `test_api.py` - API功能测试脚本
- `chatbot_example.py` - 聊天机器人集成示例
- `start_api.py` - 服务启动脚本
- `api_docs.md` - 详细API文档
- `requirements.txt` - 依赖包列表

## 部署到生产环境

### 使用Gunicorn部署
```bash
# 安装gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:5001 api_server:app
```

### 使用Docker部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5001

CMD ["python", "api_server.py"]
```

## 常见问题

**Q: 如何添加新的车票样式？**
A: 在`templates/`目录下添加新的模板JSON文件，在`default_templates/`目录下添加对应的用户数据模板。

**Q: 如何自定义字段验证？**
A: 修改`api_server.py`中的`validate_user_data`函数。

**Q: 如何提高生成速度？**
A: 使用Gunicorn多进程部署，或考虑使用Redis缓存。

**Q: 支持哪些图片格式？**
A: 目前只支持PNG格式输出。

## 技术支持

如有问题，请查看：
1. `api_docs.md` - 详细API文档
2. `test_api.py` - 运行测试检查问题
3. 检查控制台错误信息

## 更新日志

- **v1.0.0** - 初始版本，支持基础车票生成API
- 支持单张和批量生成
- 支持多种返回格式
- 完善的错误处理
- 聊天机器人集成示例

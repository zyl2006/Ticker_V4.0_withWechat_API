from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_ticket():
    """简化的生成车票图片API"""
    try:
        print(f"收到请求: {request.method} {request.url}")
        
        data = request.get_json()
        print(f"解析的JSON数据: {data}")
        
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据不能为空"
            }), 400
        
        # 提取参数
        user_data = data.get('user_data', {})
        style = data.get('style', 'red15')
        
        print(f"用户数据: {user_data}")
        print(f"样式: {style}")
        
        # 创建简单的测试图片
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # 使用默认字体
        font = ImageFont.load_default()
        
        # 绘制车票信息
        y = 20
        for key, value in user_data.items():
            if value and str(value).strip():
                text = f"{key}: {value}"
                draw.text((10, y), text, fill='black', font=font)
                y += 30
        
        # 添加样式信息
        draw.text((10, y), f"样式: {style}", fill='blue', font=font)
        
        # 转换为base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        print("图片生成成功")
        
        return jsonify({
            "success": True,
            "message": "车票生成成功",
            "data": {
                "image_base64": image_base64,
                "format": "PNG",
                "style": style,
                "user_data": user_data
            }
        })
        
    except Exception as e:
        print(f"生成车票时发生错误: {str(e)}")
        import traceback
        print(f"错误详情: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "error": f"生成车票时发生错误: {str(e)}"
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "车票生成API服务正常运行"
    })

if __name__ == '__main__':
    print("简化车票生成API服务启动...")
    print("可用接口:")
    print("  GET  /api/health - 健康检查")
    print("  POST /api/generate - 生成车票")
    print("服务地址: http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)

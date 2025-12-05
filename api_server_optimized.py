# API服务器优化配置
# 针对微信小程序的API优化

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ticket import render_ticket
import os
import json
import uuid
import tempfile
import base64
from io import BytesIO
import traceback
from datetime import datetime
import hashlib

app = Flask(__name__)
CORS(app, origins=['https://servicewechat.com'])  # 允许微信小程序域名

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

# 请求频率限制
REQUEST_LIMITS = {}
MAX_REQUESTS_PER_MINUTE = 60

def check_rate_limit(client_ip):
    """检查请求频率限制"""
    now = datetime.now()
    minute_key = now.strftime('%Y-%m-%d %H:%M')
    
    if client_ip not in REQUEST_LIMITS:
        REQUEST_LIMITS[client_ip] = {}
    
    if minute_key not in REQUEST_LIMITS[client_ip]:
        REQUEST_LIMITS[client_ip][minute_key] = 0
    
    REQUEST_LIMITS[client_ip][minute_key] += 1
    
    if REQUEST_LIMITS[client_ip][minute_key] > MAX_REQUESTS_PER_MINUTE:
        return False
    
    return True

def get_client_ip():
    """获取客户端IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def generate_response(success=True, data=None, message="", error_code=None):
    """生成统一响应格式"""
    response = {
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "message": message
    }
    
    if success:
        response["data"] = data
    else:
        response["error"] = data
        if error_code:
            response["error_code"] = error_code
    
    return response

def get_available_styles():
    """获取可用的车票样式"""
    styles = []
    default_templates_dir = os.path.join(BASE_DIR, "default_templates")
    if os.path.exists(default_templates_dir):
        for f in os.listdir(default_templates_dir):
            if f.startswith("user_") and f.endswith(".json"):
                styles.append(f[5:-5])
    return styles

def get_template_json(style):
    """获取模板JSON文件路径"""
    return os.path.join(TEMPLATE_DIR, f"ticket_template_{style}.json")

def validate_user_data(user_data, style):
    """验证用户数据格式"""
    if not isinstance(user_data, dict):
        return False, "用户数据必须是字典格式"
    
    # 检查必要的字段
    required_fields = ["姓名", "车次号", "座位号", "出发站", "到达站"]
    missing_fields = [field for field in required_fields if not user_data.get(field)]
    
    if missing_fields:
        return False, f"缺少必要字段: {', '.join(missing_fields)}"
    
    return True, "数据验证通过"

@app.before_request
def before_request():
    """请求前处理"""
    # 检查请求频率
    client_ip = get_client_ip()
    if not check_rate_limit(client_ip):
        return jsonify(generate_response(
            success=False,
            data="请求过于频繁，请稍后再试",
            error_code="RATE_LIMIT_EXCEEDED"
        )), 429

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify(generate_response(
        success=True,
        data={
            "status": "ok",
            "message": "车票生成API服务正常运行",
            "available_styles": get_available_styles(),
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    ))

@app.route('/api/styles', methods=['GET'])
def get_styles():
    """获取可用的车票样式列表"""
    try:
        styles = get_available_styles()
        return jsonify(generate_response(
            success=True,
            data={
                "styles": styles,
                "count": len(styles)
            }
        ))
    except Exception as e:
        return jsonify(generate_response(
            success=False,
            data=str(e),
            error_code="STYLES_FETCH_ERROR"
        )), 500

@app.route('/api/template/<style>', methods=['GET'])
def get_template_info(style):
    """获取指定样式的模板信息"""
    try:
        template_json_path = get_template_json(style)
        if not os.path.exists(template_json_path):
            return jsonify(generate_response(
                success=False,
                data=f"模板文件不存在: {style}",
                error_code="TEMPLATE_NOT_FOUND"
            )), 404
        
        with open(template_json_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        # 提取字段信息
        fields = template_data.get('fields', {})
        field_info = {}
        for field_name, field_config in fields.items():
            field_info[field_name] = {
                "type": field_config.get("type", "text"),
                "required": field_config.get("required", False),
                "description": field_config.get("description", ""),
                "placeholder": field_config.get("placeholder", f"请输入{field_name}")
            }
        
        return jsonify(generate_response(
            success=True,
            data={
                "style": style,
                "fields": field_info,
                "canvas": template_data.get('canvas', {}),
                "metadata": template_data.get('metadata', {})
            }
        ))
    
    except Exception as e:
        return jsonify(generate_response(
            success=False,
            data=str(e),
            error_code="TEMPLATE_FETCH_ERROR"
        )), 500

@app.route('/api/generate', methods=['POST'])
def generate_ticket():
    """生成车票图片API"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify(generate_response(
                success=False,
                data="请求数据不能为空",
                error_code="EMPTY_REQUEST"
            )), 400
        
        # 提取参数
        user_data = data.get('user_data', {})
        style = data.get('style', 'red15')
        return_format = data.get('format', 'base64')
        
        # 验证样式是否存在
        available_styles = get_available_styles()
        if style not in available_styles:
            return jsonify(generate_response(
                success=False,
                data=f"不支持的样式: {style}。可用样式: {', '.join(available_styles)}",
                error_code="INVALID_STYLE"
            )), 400
        
        # 验证用户数据
        is_valid, message = validate_user_data(user_data, style)
        if not is_valid:
            return jsonify(generate_response(
                success=False,
                data=message,
                error_code="INVALID_DATA"
            )), 400
        
        # 生成车票
        template_json_path = get_template_json(style)
        if not os.path.exists(template_json_path):
            return jsonify(generate_response(
                success=False,
                data=f"模板文件不存在: {template_json_path}",
                error_code="TEMPLATE_NOT_FOUND"
            )), 500
        
        # 渲染车票
        ticket_image = render_ticket(user_data, template_json_path, TEMPLATE_DIR)
        
        if return_format == 'base64':
            # 返回base64编码的图片
            buffer = BytesIO()
            ticket_image.save(buffer, format='PNG', optimize=True)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return jsonify(generate_response(
                success=True,
                data={
                    "image_base64": image_base64,
                    "format": "PNG",
                    "style": style,
                    "user_data": user_data,
                    "size": len(buffer.getvalue()),
                    "generated_at": datetime.now().isoformat()
                }
            ))
        
        else:
            # 返回临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            ticket_image.save(temp_file.name, format='PNG', optimize=True)
            temp_file.close()
            
            return send_file(
                temp_file.name,
                mimetype='image/png',
                as_attachment=True,
                download_name=f'ticket_{style}_{uuid.uuid4().hex[:8]}.png'
            )
    
    except Exception as e:
        error_msg = f"生成车票时发生错误: {str(e)}"
        print(f"API错误: {error_msg}")
        print(f"错误详情: {traceback.format_exc()}")
        
        return jsonify(generate_response(
            success=False,
            data=error_msg,
            error_code="GENERATION_ERROR"
        )), 500

@app.route('/api/batch_generate', methods=['POST'])
def batch_generate():
    """批量生成车票API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify(generate_response(
                success=False,
                data="请求数据不能为空",
                error_code="EMPTY_REQUEST"
            )), 400
        
        tickets_data = data.get('tickets', [])
        style = data.get('style', 'red15')
        return_format = data.get('format', 'base64')
        
        if not isinstance(tickets_data, list) or len(tickets_data) == 0:
            return jsonify(generate_response(
                success=False,
                data="tickets数据必须是包含车票信息的数组",
                error_code="INVALID_TICKETS_DATA"
            )), 400
        
        if len(tickets_data) > 10:  # 限制批量生成数量
            return jsonify(generate_response(
                success=False,
                data="批量生成数量不能超过10张",
                error_code="BATCH_LIMIT_EXCEEDED"
            )), 400
        
        results = []
        template_json_path = get_template_json(style)
        
        for i, ticket_data in enumerate(tickets_data):
            try:
                # 验证单个车票数据
                is_valid, message = validate_user_data(ticket_data, style)
                if not is_valid:
                    results.append({
                        "index": i,
                        "success": False,
                        "error": message,
                        "error_code": "INVALID_DATA"
                    })
                    continue
                
                # 生成车票
                ticket_image = render_ticket(ticket_data, template_json_path, TEMPLATE_DIR)
                
                if return_format == 'base64':
                    buffer = BytesIO()
                    ticket_image.save(buffer, format='PNG', optimize=True)
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    results.append({
                        "index": i,
                        "success": True,
                        "data": {
                            "image_base64": image_base64,
                            "format": "PNG",
                            "user_data": ticket_data,
                            "size": len(buffer.getvalue())
                        }
                    })
                else:
                    results.append({
                        "index": i,
                        "success": False,
                        "error": "批量生成不支持文件格式，请使用base64格式",
                        "error_code": "UNSUPPORTED_FORMAT"
                    })
            
            except Exception as e:
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e),
                    "error_code": "GENERATION_ERROR"
                })
        
        return jsonify(generate_response(
            success=True,
            data={
                "results": results,
                "total": len(tickets_data),
                "success_count": len([r for r in results if r["success"]]),
                "generated_at": datetime.now().isoformat()
            }
        ))
    
    except Exception as e:
        return jsonify(generate_response(
            success=False,
            data=str(e),
            error_code="BATCH_GENERATION_ERROR"
        )), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify(generate_response(
        success=False,
        data="接口不存在",
        error_code="NOT_FOUND"
    )), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(generate_response(
        success=False,
        data="服务器内部错误",
        error_code="INTERNAL_ERROR"
    )), 500

if __name__ == '__main__':
    print("🚆 Ticker-车票儿 API服务启动中...")
    print("📋 可用接口:")
    print("  GET  /api/health - 健康检查")
    print("  GET  /api/styles - 获取可用样式")
    print("  POST /api/generate - 生成单张车票")
    print("  GET  /api/template/<style> - 获取模板信息")
    print("  POST /api/batch_generate - 批量生成车票")
    print("\n🌐 服务地址: http://localhost:5001")
    print("📱 小程序优化: 已启用")
    print("🔒 安全特性: 请求频率限制、统一错误处理")
    
    app.run(host='0.0.0.0', port=5001, debug=False)

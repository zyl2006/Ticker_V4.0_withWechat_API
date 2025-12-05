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

app = Flask(__name__)
CORS(app)  # 允许跨域请求

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

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
    
    # 检查是否有任何非空字段
    has_content = any(value and str(value).strip() for value in user_data.values())
    
    if not has_content:
        return False, "至少需要填写一个字段"
    
    return True, "数据验证通过"

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        "status": "ok",
        "message": "车票生成API服务正常运行",
        "available_styles": get_available_styles()
    })

@app.route('/api/styles', methods=['GET'])
def get_styles():
    """获取可用的车票样式列表"""
    try:
        styles = get_available_styles()
        return jsonify({
            "success": True,
            "styles": styles,
            "count": len(styles)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate_ticket():
    """生成车票图片API"""
    try:
        # 获取请求数据
        print(f"收到请求: {request.method} {request.url}")
        print(f"请求头: {dict(request.headers)}")
        print(f"请求来源: {request.headers.get('User-Agent', 'Unknown')}")
        print(f"请求内容类型: {request.headers.get('Content-Type', 'Unknown')}")
        
        # 尝试多种方式获取数据
        data = None
        
        # 首先尝试JSON
        try:
            data = request.get_json()
            print(f"JSON数据: {data}")
        except Exception as json_error:
            print(f"JSON解析失败: {json_error}")
        
        # 如果JSON失败，尝试表单数据
        if not data:
            try:
                data = request.form.to_dict()
                print(f"表单数据: {data}")
            except Exception as form_error:
                print(f"表单解析失败: {form_error}")
        
        # 如果还是失败，尝试原始数据
        if not data:
            try:
                raw_data = request.get_data(as_text=True)
                print(f"原始数据: {raw_data}")
                if raw_data:
                    data = json.loads(raw_data)
                    print(f"解析后的原始数据: {data}")
            except Exception as raw_error:
                print(f"原始数据解析失败: {raw_error}")
        
        if not data:
            print("错误: 无法解析请求数据")
            return jsonify({
                "success": False,
                "error": "请求数据格式错误，无法解析"
            }), 400
        
        # 提取参数
        user_data = data.get('user_data', {})
        style = data.get('style', 'red15')  # 默认样式
        return_format = data.get('format', 'base64')  # base64 或 file
        
        # 验证样式是否存在
        available_styles = get_available_styles()
        if style not in available_styles:
            return jsonify({
                "success": False,
                "error": f"不支持的样式: {style}。可用样式: {', '.join(available_styles)}"
            }), 400
        
        # 验证用户数据
        is_valid, message = validate_user_data(user_data, style)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": message
            }), 400
        
        # 生成车票
        template_json_path = get_template_json(style)
        if not os.path.exists(template_json_path):
            return jsonify({
                "success": False,
                "error": f"模板文件不存在: {template_json_path}"
            }), 500
        
        # 渲染车票
        try:
            ticket_image = render_ticket(user_data, template_json_path, TEMPLATE_DIR)
        except Exception as render_error:
            print(f"渲染错误: {render_error}")
            print(f"渲染错误详情: {traceback.format_exc()}")
            return jsonify({
                "success": False,
                "error": f"渲染车票失败: {str(render_error)}"
            }), 500
        
        if return_format == 'base64':
            # 返回base64编码的图片
            buffer = BytesIO()
            ticket_image.save(buffer, format='PNG')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
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
        
        else:
            # 返回临时文件
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            ticket_image.save(temp_file.name, format='PNG')
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
        
        return jsonify({
            "success": False,
            "error": error_msg
        }), 500

@app.route('/api/template/<style>', methods=['GET'])
def get_template_info(style):
    """获取指定样式的模板信息"""
    try:
        template_json_path = get_template_json(style)
        if not os.path.exists(template_json_path):
            return jsonify({
                "success": False,
                "error": f"模板文件不存在: {style}"
            }), 404
        
        with open(template_json_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        # 提取字段信息 - 包含完整的字段配置
        fields = template_data.get('fields', {})
        field_info = {}
        print(f"DEBUG: Processing {len(fields)} fields")
        for field_name, field_config in fields.items():
            field_info[field_name] = {
                "type": field_config.get("type", "text"),
                "required": field_config.get("required", False),
                "description": field_config.get("description", ""),
                "segments": field_config.get("segments", []),  # 包含segments信息
                "x": field_config.get("x"),
                "y": field_config.get("y"),
                "anchor": field_config.get("anchor")
            }
            if field_config.get("segments"):
                print(f"DEBUG: Field {field_name} has {len(field_config.get('segments', []))} segments")
        
        return jsonify({
            "success": True,
            "style": style,
            "fields": field_info,
            "canvas": template_data.get('canvas', {})
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/template/<style>/fields', methods=['GET'])
def get_template_fields(style):
    """获取指定样式的真实字段列表（从segments中提取）"""
    try:
        template_json_path = get_template_json(style)
        if not os.path.exists(template_json_path):
            return jsonify({
                "success": False,
                "error": f"模板文件不存在: {style}"
            }), 404
        
        with open(template_json_path, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        # 从segments中提取真实字段
        import re
        real_fields = set()
        fields = template_data.get('fields', {})
        
        for field_name, field_config in fields.items():
            if 'segments' in field_config:
                for segment in field_config['segments']:
                    if 'text' in segment:
                        text = segment['text']
                        # 提取{字段名}格式的字段
                        matches = re.findall(r'\{([^}]+)\}', text)
                        for match in matches:
                            real_fields.add(match)
        
        # 构建字段信息
        field_list = []
        for field_name in sorted(real_fields):
            field_list.append({
                "key": field_name,
                "label": field_name,
                "type": "text",
                "required": False,
                "description": f"请输入{field_name}"
            })
        
        return jsonify({
            "success": True,
            "style": style,
            "fields": field_list,
            "field_count": len(field_list)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/batch_generate', methods=['POST'])
def batch_generate():
    """批量生成车票API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "请求数据不能为空"
            }), 400
        
        tickets_data = data.get('tickets', [])
        style = data.get('style', 'red15')
        return_format = data.get('format', 'base64')
        
        if not isinstance(tickets_data, list) or len(tickets_data) == 0:
            return jsonify({
                "success": False,
                "error": "tickets数据必须是包含车票信息的数组"
            }), 400
        
        if len(tickets_data) > 10:  # 限制批量生成数量
            return jsonify({
                "success": False,
                "error": "批量生成数量不能超过10张"
            }), 400
        
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
                        "error": message
                    })
                    continue
                
                # 生成车票
                ticket_image = render_ticket(ticket_data, template_json_path, TEMPLATE_DIR)
                
                if return_format == 'base64':
                    buffer = BytesIO()
                    ticket_image.save(buffer, format='PNG')
                    buffer.seek(0)
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    
                    results.append({
                        "index": i,
                        "success": True,
                        "data": {
                            "image_base64": image_base64,
                            "format": "PNG",
                            "user_data": ticket_data
                        }
                    })
                else:
                    # 对于文件格式，这里返回错误，因为批量生成文件比较复杂
                    results.append({
                        "index": i,
                        "success": False,
                        "error": "批量生成不支持文件格式，请使用base64格式"
                    })
            
            except Exception as e:
                results.append({
                    "index": i,
                    "success": False,
                    "error": str(e)
                })
        
        return jsonify({
            "success": True,
            "message": f"批量生成完成，共处理{len(tickets_data)}张车票",
            "results": results
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "接口不存在"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "服务器内部错误"
    }), 500

if __name__ == '__main__':
    print("车票生成API服务启动中...")
    print("可用接口:")
    print("  GET  /api/health - 健康检查")
    print("  GET  /api/styles - 获取可用样式")
    print("  POST /api/generate - 生成单张车票")
    print("  GET  /api/template/<style> - 获取模板信息")
    print("  POST /api/batch_generate - 批量生成车票")
    print("\n服务地址: http://localhost:5001")
    print("API文档: 请查看 api_docs.md")
    
    app.run(host='0.0.0.0', port=5001, debug=False)

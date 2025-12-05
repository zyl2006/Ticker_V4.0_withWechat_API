from flask import Flask, render_template_string, request, send_file, url_for, session, jsonify
from ticket import render_ticket
import os, json
from io import BytesIO
import base64
import uuid
import shutil

app = Flask(__name__)
app.secret_key = "replace_with_random_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
PREVIEW_DIR = os.path.join(BASE_DIR, "static", "previews")  # 样式示例图片

# Ensure preview folder and bg.png
os.makedirs(PREVIEW_DIR, exist_ok=True)
bg_path = os.path.join(PREVIEW_DIR, 'bg.png')
if not os.path.exists(bg_path):
    for candidate in os.listdir(PREVIEW_DIR):
        if candidate.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                shutil.copy2(os.path.join(PREVIEW_DIR, candidate), bg_path)
                break
            except Exception:
                pass

RECOMMEND_SITES = [
    {"name":"蜀科院&爱杰之家微信公众号","url":"https://mp.weixin.qq.com/s/lqU5oQZ8eln7Xm_zJ-KIkA","desc":"欢迎关注","logo":"site1.png"},
    {"name":"蜀科院博客","url":"https://blog.sgsky.tech","desc":"信息整合分享平台","logo":"site2.png"},
    {"name":"中国铁路12306","url":"https:/12306.cn","desc":"了解铁路官方资讯","logo":"site3.png"}
]

NOTICES = [
    "重要提示：①本站仅用于学习与演示用途，请勿用于非法用途。\n ②尚未开发完全，建议仅使用较新的票面版本",
    "更新日志：V3.0 内测全新升级：优化票种渲染、支持自定义上票号、适配了一些特性、修改了一些问题。",
]


def get_available_styles():
    out = []
    default_templates_dir = os.path.join(BASE_DIR, "default_templates")
    if os.path.exists(default_templates_dir):
        for f in os.listdir(default_templates_dir):
            if f.startswith("user_") and f.endswith(".json"):
                out.append(f[5:-5])
    return out


def get_or_create_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']


def get_user_json(style, user_id):
    user_dir = os.path.join(BASE_DIR, "user_data", user_id)
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, f"user_{style}.json")


def get_user_ticket_path(user_id):
    user_dir = os.path.join(BASE_DIR, "user_data", user_id)
    os.makedirs(user_dir, exist_ok=True)
    return os.path.join(user_dir, "ticket.png")


def get_template_json(style):
    return os.path.join(TEMPLATE_DIR, f"ticket_template_{style}.json")


def load_user_data(style, user_id):
    path = get_user_json(style, user_id)
    if not os.path.exists(path):
        default_path = os.path.join(BASE_DIR, "default_templates", f"user_{style}.json")
        if os.path.exists(default_path):
            shutil.copy2(default_path, path)
        else:
            return {}
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    norm = {}
    for k, v in raw.items():
        if isinstance(v, dict):
            val = v.get("value", "") if "value" in v or "enabled" in v else v
            if isinstance(val, dict):
                val = str(val)
            enabled = bool(v.get("enabled", True))
            norm[k] = {"value": val, "enabled": enabled}
        else:
            norm[k] = {"value": v if v is not None else "", "enabled": True}
    return norm


def save_user_data(data, style, user_id):
    with open(get_user_json(style, user_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>🚆 Ticker-智能纪念票制作工具</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="description" content="Ticker-车票儿，精细化纪念车票智能生成助手~">
<meta name="keywords" content="车票,火车票,模拟器,生成器">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root {
  --primary-color: #3b82f6;
  --primary-hover: #2563eb;
  --secondary-color: #8b5cf6;
  --success-color: #10b981;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-tertiary: #f1f5f9;
  --border-color: #e2e8f0;
  --border-hover: #cbd5e1;
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
  min-height: 100vh;
  overflow-x: hidden;
}

/* 背景装饰 */
.page-bg {
  position: fixed;
  inset: 0;
  background: 
    radial-gradient(circle at 20% 20%, rgba(59, 130, 246, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 60%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 60% 40%, rgba(99, 102, 241, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* 主容器 */
.app-shell {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
}

/* 顶部导航栏 */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: var(--radius-xl);
  padding: 16px 24px;
  box-shadow: var(--shadow-lg);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand .logo {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 700;
  font-size: 18px;
  box-shadow: var(--shadow-md);
  transition: var(--transition);
}

.brand .logo:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-xl);
}

.brand h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.notice-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border-radius: var(--radius-lg);
  border: 1px solid #f59e0b;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.notice-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(236, 72, 153, 0.1));
  opacity: 0;
  transition: var(--transition);
}

.notice-bar:hover::before {
  opacity: 1;
}

.notice-bar:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-color);
}

.notice-toggle {
  font-size: 14px;
  font-weight: 500;
  color: #92400e;
  position: relative;
  z-index: 1;
}

/* 主布局 */
.layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 24px;
  align-items: start;
}

/* 面板样式 */
.panel {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.panel:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.panel h3 {
  margin: 0 0 20px 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel h3 i {
  color: var(--primary-color);
}

/* 表单区域 */
.form-area {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 样式选择网格 */
.style-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
}

.style-card {
  border-radius: var(--radius-lg);
  padding: 16px;
  text-align: center;
  cursor: pointer;
  background: var(--bg-primary);
  border: 2px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.style-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  opacity: 0;
  transition: var(--transition);
}

.style-card:hover::before {
  opacity: 0.05;
}

.style-card.selected {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  transform: translateY(-2px);
}

.style-card.selected::before {
  opacity: 0.1;
}

.style-preview {
  width: 100%;
  height: 90px;
  object-fit: cover;
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  transition: var(--transition);
}

.style-card:hover .style-preview {
  transform: scale(1.05);
}

.style-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  position: relative;
  z-index: 1;
}

/* 表单字段 */
.field-row {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 16px;
  padding: 12px;
  border-radius: var(--radius-lg);
  background: var(--bg-secondary);
  transition: var(--transition);
}

.field-row:hover {
  background: var(--bg-tertiary);
}

.key-label {
  min-width: 120px;
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 14px;
}

.key-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--primary-color);
}

.field-input {
  flex: 1;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-color);
  background: var(--bg-primary);
  font-size: 14px;
  transition: var(--transition);
  font-family: inherit;
}

.field-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.field-input.disabled {
  background: var(--bg-tertiary);
  color: var(--text-muted);
  cursor: not-allowed;
}

/* 按钮样式 */
.controls {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 20px;
  border-radius: var(--radius-lg);
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: var(--transition);
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-family: inherit;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-secondary {
  background: var(--bg-primary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--bg-secondary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: 2px solid var(--border-color);
}

.btn-ghost:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
  transform: translateY(-2px);
}

/* 预览区域 */
.preview-area {
  position: sticky;
  top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-box {
  text-align: center;
  padding: 20px;
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, var(--bg-primary), var(--bg-secondary));
  border: 2px solid var(--border-color);
}

.preview-img {
  width: 100%;
  height: auto;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  transition: var(--transition);
}

.preview-img:hover {
  transform: scale(1.02);
}

/* 推荐网站 */
.site-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.site-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: 16px;
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid var(--border-color);
  text-align: center;
}

.site-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
  border-color: var(--primary-color);
}

.site-logo {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  margin: 0 auto 12px;
  display: block;
}

.site-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.site-desc {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 通知面板 */
.notice-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notice-item {
  font-size: 14px;
  color: var(--text-secondary);
  background: var(--bg-secondary);
  padding: 16px;
  border-radius: var(--radius-lg);
  border-left: 4px solid var(--primary-color);
  line-height: 1.6;
}

/* 移动端悬浮预览 */
.mobile-preview-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  box-shadow: var(--shadow-xl);
  cursor: pointer;
  z-index: 1000;
  display: none;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  transition: var(--transition);
}

.mobile-preview-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 25px 50px rgba(59, 130, 246, 0.3);
}

.mobile-preview-toggle.active {
  background: linear-gradient(135deg, var(--success-color), #059669);
}

.mobile-preview-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  z-index: 1500;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mobile-preview-overlay.show {
  opacity: 1;
}

.mobile-preview-container {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  padding: 20px;
  max-width: 90vw;
  max-height: 80vh;
  box-shadow: var(--shadow-xl);
  transform: scale(0.9);
  transition: transform 0.3s ease;
  position: relative;
}

.mobile-preview-overlay.show .mobile-preview-container {
  transform: scale(1);
}

.mobile-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.mobile-preview-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.mobile-preview-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--bg-secondary);
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.mobile-preview-close:hover {
  background: var(--error-color);
  color: white;
}

.mobile-preview-content {
  text-align: center;
  max-height: 60vh;
  overflow-y: auto;
}

.mobile-preview-img {
  width: 100%;
  max-width: 300px;
  height: auto;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  margin-bottom: 16px;
}

.mobile-preview-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.mobile-preview-actions .btn {
  flex: 1;
  min-width: 120px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .layout {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .preview-area {
    position: relative;
    top: 0;
  }
}

@media (max-width: 768px) {
  .app-shell {
    padding: 16px;
    padding-bottom: 100px; /* 为悬浮按钮留出空间 */
  }
  
  .topbar {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .brand h1 {
    font-size: 20px;
  }
  
  .style-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px;
  }
  
  .field-row {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .key-label {
    min-width: auto;
  }
  
  .controls {
    flex-direction: column;
  }
  
  .btn {
    justify-content: center;
  }
  
  .site-grid {
    grid-template-columns: 1fr;
  }
  
  /* 移动端隐藏右侧预览区域 */
  .preview-area {
    display: none;
  }
  
  /* 显示悬浮预览按钮 */
  .mobile-preview-toggle {
    display: flex;
  }
  
  /* 优化表单字段在移动端的显示 */
  .field-row {
    padding: 16px;
    margin-bottom: 12px;
  }
  
  .field-input {
    font-size: 16px; /* 防止iOS缩放 */
  }
}

@media (max-width: 480px) {
  .app-shell {
    padding: 12px;
    padding-bottom: 100px;
  }
  
  .panel {
    padding: 16px;
  }
  
  .style-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .brand .logo {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
  
  .brand h1 {
    font-size: 18px;
  }
  
  .mobile-preview-toggle {
    width: 56px;
    height: 56px;
    bottom: 16px;
    right: 16px;
    font-size: 20px;
  }
  
  .mobile-preview-container {
    padding: 16px;
    max-width: 95vw;
  }
  
  .mobile-preview-actions {
    flex-direction: column;
  }
  
  .mobile-preview-actions .btn {
    min-width: auto;
  }
}

/* 加载动画 */
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 成功/错误状态 */
.success-message {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  border: 1px solid #10b981;
  margin: 16px 0;
}

.error-message {
  background: linear-gradient(135deg, #fee2e2, #fecaca);
  color: #991b1b;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  border: 1px solid #ef4444;
  margin: 16px 0;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--bg-secondary);
  border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb {
  background: var(--border-hover);
  border-radius: var(--radius-sm);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--text-muted);
}
</style>
</head>
<body>
<div class="page-bg"></div>

<div class="app-shell">
  <!-- 顶部导航栏 -->
  <div class="topbar">
    <div class="brand">
      <div class="logo">
        <i class="fa-solid fa-ticket"></i>
    </div>
      <h1>Ticker-车票儿    精细化纪念车票智能生成工具</h1>
    </div>
    <div class="notice-bar" id="noticeToggleTop" onclick="openNoticeModal()">
      <i class="fas fa-bell"></i>
      <span class="notice-toggle">使用前请点击以查看最新通知</span>
    </div>
  </div>

  <!-- 主布局 -->
  <div class="layout">
    <!-- 左侧表单区域 -->
    <div class="form-area">
      <!-- 样式选择面板 -->
      <div class="panel">
        <h3><i class="fas fa-palette"></i> 选择车票样式</h3>
        <form method="GET" id="styleForm">
          <div class="style-grid">
            {% for s in styles %}
            <label class="style-card {% if s==selected_style %}selected{% endif %}" title="{{s}}">
              <input type="radio" name="style" value="{{s}}" onchange="document.getElementById('styleForm').submit()" {% if s==selected_style %}checked{% endif %} hidden>
              <img src="{{ url_for('static', filename='previews/' + s + '.png') }}" class="style-preview" alt="{{s}}">
              <div class="style-name">{{s}}</div>
            </label>
            {% endfor %}
          </div>
        </form>
      </div>

      <!-- 车票信息填写面板 -->
      <div class="panel">
        <h3><i class="fas fa-edit"></i> 填写车票信息</h3>
        <div style="margin-bottom: 16px; padding: 12px; background: var(--bg-secondary); border-radius: var(--radius-lg); border-left: 4px solid var(--primary-color);">
          <strong>当前样式：</strong><span style="color: var(--primary-color);">{{selected_style}}</span>
        </div>
        <form method="POST" id="dataForm">
          <input type="hidden" name="style" value="{{selected_style}}">
          <div>
            {% for key, info in user_data.items() %}
            <div class="field-row" data-index="{{loop.index0}}">
              <label class="key-label">
                <input type="checkbox" name="field_enabled_{{loop.index0}}" id="enabled_{{loop.index0}}" {% if info.enabled %}checked{% endif %} onchange="toggleField({{loop.index0}})">
                <span>{{key}}</span>
              </label>
              <input type="hidden" name="field_key_{{loop.index0}}" value="{{key|replace('\\n',' ')}}">
              <input class="field-input" type="text" name="field_value_{{loop.index0}}" id="value_{{loop.index0}}" value="{{info.value|e}}" {% if not info.enabled %}class="disabled" disabled{% endif %}>
            </div>
            {% endfor %}
          </div>

          <div class="controls">
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-magic"></i>
              点击预览窗格“下载预览”以下载结果
            </button>
            <button type="button" onclick="saveLocally()" class="btn btn-secondary">
              <i class="fas fa-save"></i>
              保存草稿至缓存
            </button>
            <button type="button" onclick="resetForm()" class="btn btn-ghost">
              <i class="fas fa-undo"></i>
              重置输入内容
            </button>
          </div>
        </form>
      </div>

      <!-- 推荐网站面板 -->
      <div class="panel">
        <h3><i class="fas fa-globe"></i> 推荐网站</h3>
        <div class="site-grid">
          {% for site in recommend_sites %}
            <div class="site-card" onclick="window.open('{{site.url}}','_blank')">
              <img src="{{ url_for('static', filename='previews/' + site.logo) }}" class="site-logo" alt="{{site.name}}">
              <div class="site-name">{{site.name}}</div>
              <div class="site-desc">{{site.desc}}</div>
            </div>
          {% endfor %}
        </div>
      </div>
    </div>

    <!-- 右侧预览区域 -->
    <aside class="preview-area">
      <!-- 实时预览面板 -->
      <div class="panel preview-box">
        <h3><i class="fas fa-eye"></i> 实时预览</h3>
        <div id="previewContainer">
        <img id="livePreview" class="preview-img" src="" alt="实时预览">
          <div id="previewPlaceholder" style="display: none; text-align: center; padding: 40px; color: var(--text-muted);">
            <i class="fas fa-image" style="font-size: 48px; margin-bottom: 16px; opacity: 0.3;"></i>
            <p>填写内容后将显示实时预览</p>
        </div>
        </div>
        <div class="controls" style="justify-content: center; margin-top: 16px;">
          <a id="downloadPreview" class="btn btn-primary" href="#" download="preview.png" style="display: none;">
            <i class="fas fa-download"></i>
            下载预览
          </a>
          <button type="button" id="refreshPreview" onclick="forcePreview()" class="btn btn-secondary">
            <i class="fas fa-sync-alt"></i>
            刷新预览
          </button>
        </div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 12px; text-align: center;">
          <i class="fas fa-info-circle"></i>
          填写内容以预览。若预览空白，请点击"刷新预览"。
        </div>
      </div>

      <!-- 通知公告面板 -->
      <div class="panel">
        <h3><i class="fas fa-bullhorn"></i> 通知公告</h3>
        <div class="notice-panel" id="noticePanel">
          {% for n in notices %}
          <div class="notice-item">{{n}}</div>
          {% endfor %}
        </div>
      </div>
    </aside>
  </div>
  </div>

<!-- 通知模态框 -->
<div id="noticeModalBackdrop" class="modal-backdrop">
  <div class="modal" role="dialog" aria-modal="true">
    <h4><i class="fas fa-bullhorn"></i> 系统通知</h4>
    <div class="modal-body" id="modalNotices">
      {% for n in notices %}
        <div class="notice-item">{{n}}</div>
      {% endfor %}
    </div>
    <div class="modal-actions">
      <button class="btn-close" onclick="closeNoticeModal()">
        <i class="fas fa-times"></i>
        关闭
      </button>
    </div>
  </div>
</div>

<!-- 移动端悬浮预览按钮 -->
<button class="mobile-preview-toggle" id="mobilePreviewToggle" onclick="toggleMobilePreview()">
  <i class="fas fa-eye"></i>
</button>

<!-- 移动端预览覆盖层 -->
<div class="mobile-preview-overlay" id="mobilePreviewOverlay">
  <div class="mobile-preview-container">
    <div class="mobile-preview-header">
      <div class="mobile-preview-title">
        <i class="fas fa-eye"></i>
        实时预览
      </div>
      <button class="mobile-preview-close" onclick="closeMobilePreview()">
        <i class="fas fa-times"></i>
      </button>
    </div>
    <div class="mobile-preview-content">
      <img id="mobilePreviewImg" class="mobile-preview-img" src="" alt="实时预览" style="display: none;">
      <div id="mobilePreviewPlaceholder" style="text-align: center; padding: 40px; color: var(--text-muted);">
        <i class="fas fa-image" style="font-size: 48px; margin-bottom: 16px; opacity: 0.3;"></i>
        <p>填写内容后将显示实时预览</p>
      </div>
      <div class="mobile-preview-actions">
        <a id="mobileDownloadPreview" class="btn btn-primary" href="#" download="preview.png" style="display: none;">
          <i class="fas fa-download"></i>
          下载预览
        </a>
        <button type="button" onclick="refreshMobilePreview()" class="btn btn-secondary">
          <i class="fas fa-sync-alt"></i>
          刷新预览
        </button>
      </div>
    </div>
  </div>
</div>

<script>
// 防抖函数
function debounce(fn, wait) {
  let t;
  return function(...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), wait);
  }
}

// 切换字段启用状态
function toggleField(i) {
  const cb = document.getElementById("enabled_" + i);
  const input = document.getElementById("value_" + i);
  if (cb.checked) {
    input.disabled = false;
    input.classList.remove("disabled");
  } else {
    input.disabled = true;
    input.classList.add("disabled");
  }
  schedulePreview();
}

// 收集表单数据
function collectFormData() {
  const form = document.getElementById('dataForm');
  const inputs = form.querySelectorAll('[name^="field_key_"]');
  const data = {};
  inputs.forEach(k => {
    const idx = k.name.split('_').pop();
    const key = k.value;
    const val = document.getElementById('value_' + idx).value || '';
    const enabled = document.getElementById('enabled_' + idx).checked;
    data[key] = { value: val, enabled: enabled };
  });
  return data;
}

// 显示加载状态
function showLoading(element) {
  const originalText = element.innerHTML;
  element.innerHTML = '<span class="loading"></span> 生成中...';
  element.disabled = true;
  return originalText;
}

// 恢复按钮状态
function restoreButton(element, originalText) {
  element.innerHTML = originalText;
  element.disabled = false;
}

// 移动端预览功能
let mobilePreviewData = null;

function toggleMobilePreview() {
  const overlay = document.getElementById('mobilePreviewOverlay');
  const toggle = document.getElementById('mobilePreviewToggle');
  
  if (overlay.style.display === 'flex') {
    closeMobilePreview();
  } else {
    openMobilePreview();
  }
}

function openMobilePreview() {
  const overlay = document.getElementById('mobilePreviewOverlay');
  const toggle = document.getElementById('mobilePreviewToggle');
  
  overlay.style.display = 'flex';
  toggle.classList.add('active');
  
  setTimeout(() => {
    overlay.classList.add('show');
  }, 10);
  
  // 更新移动端预览内容
  updateMobilePreview();
}

function closeMobilePreview() {
  const overlay = document.getElementById('mobilePreviewOverlay');
  const toggle = document.getElementById('mobilePreviewToggle');
  
  overlay.classList.remove('show');
  toggle.classList.remove('active');
  
  setTimeout(() => {
    overlay.style.display = 'none';
  }, 300);
}

function updateMobilePreview() {
  const img = document.getElementById('mobilePreviewImg');
  const downloadBtn = document.getElementById('mobileDownloadPreview');
  const placeholder = document.getElementById('mobilePreviewPlaceholder');
  
  if (mobilePreviewData) {
    img.src = mobilePreviewData;
    img.style.display = 'block';
    downloadBtn.href = mobilePreviewData;
    downloadBtn.style.display = 'inline-flex';
    placeholder.style.display = 'none';
  } else {
    img.style.display = 'none';
    downloadBtn.style.display = 'none';
    placeholder.style.display = 'block';
  }
}

function refreshMobilePreview() {
  const refreshBtn = document.querySelector('.mobile-preview-actions .btn-secondary');
  const originalText = showLoading(refreshBtn);
  
  doPreview().finally(() => {
    restoreButton(refreshBtn, originalText);
  });
}

// 更新预览功能以支持移动端
async function doPreview() {
  try {
    const style = '{{selected_style}}';
    const user_data = collectFormData();
    
    // 检查是否有有效数据
    const hasData = Object.values(user_data).some(item => item.enabled && item.value.trim());
    
    if (!hasData) {
      showPreviewPlaceholder();
      mobilePreviewData = null;
      updateMobilePreview();
      return;
    }
    
    const resp = await fetch(window.location.pathname + '?preview=1', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ style, user_data })
    });
    
    const j = await resp.json();
    if (j.success) {
      const imgSrc = 'data:image/png;base64,' + j.image_base64;
      
      // 更新桌面端预览
      const img = document.getElementById('livePreview');
      const downloadBtn = document.getElementById('downloadPreview');
      const placeholder = document.getElementById('previewPlaceholder');
      
      img.src = imgSrc;
      img.style.display = 'block';
      downloadBtn.href = imgSrc;
      downloadBtn.style.display = 'inline-flex';
      placeholder.style.display = 'none';
      
      // 更新移动端预览数据
      mobilePreviewData = imgSrc;
      updateMobilePreview();
      
      // 添加成功动画
      img.style.transform = 'scale(1.05)';
      setTimeout(() => {
        img.style.transform = 'scale(1)';
      }, 200);
      
      // 更新悬浮按钮状态
      const toggle = document.getElementById('mobilePreviewToggle');
      if (toggle && window.innerWidth <= 768) {
        toggle.classList.add('active');
      }
    } else {
      showError('预览生成失败: ' + (j.error || '未知错误'));
    }
  } catch (e) {
    console.warn('预览失败', e);
    showError('预览生成失败，请检查网络连接');
  }
}

// 显示预览占位符
function showPreviewPlaceholder() {
  const img = document.getElementById('livePreview');
  const downloadBtn = document.getElementById('downloadPreview');
  const placeholder = document.getElementById('previewPlaceholder');
  
  img.style.display = 'none';
  downloadBtn.style.display = 'none';
  placeholder.style.display = 'block';
}

// 显示错误消息
function showError(message) {
  // 创建错误提示
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
  
  // 插入到页面顶部
  const appShell = document.querySelector('.app-shell');
  appShell.insertBefore(errorDiv, appShell.firstChild);
  
  // 3秒后自动移除
  setTimeout(() => {
    errorDiv.remove();
  }, 3000);
}

// 显示成功消息
function showSuccess(message) {
  const successDiv = document.createElement('div');
  successDiv.className = 'success-message';
  successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
  
  const appShell = document.querySelector('.app-shell');
  appShell.insertBefore(successDiv, appShell.firstChild);
  
  setTimeout(() => {
    successDiv.remove();
  }, 3000);
}

const schedulePreview = debounce(doPreview, 600);

function forcePreview() {
  const refreshBtn = document.getElementById('refreshPreview');
  const originalText = showLoading(refreshBtn);
  
  doPreview().finally(() => {
    restoreButton(refreshBtn, originalText);
  });
}

// 保存到本地存储
function saveLocally() {
  const key = 'cr_ticket_draft_{{selected_style}}';
  localStorage.setItem(key, JSON.stringify(collectFormData()));
  showSuccess('草稿已保存到本地浏览器存储');
}

// 重置表单
function resetForm() {
  if (!confirm('确认重置为模板默认值？')) return;
  window.location.href = window.location.pathname + '?style={{selected_style}}';
}

// 恢复草稿
function tryRestoreDraft() {
  const key = 'cr_ticket_draft_{{selected_style}}';
  const raw = localStorage.getItem(key);
  if (!raw) return;
  
  try {
    const data = JSON.parse(raw);
    Object.keys(data).forEach((k, idx) => {
      const hidden = Array.from(document.querySelectorAll('[name^="field_key_"]')).find(h => h.value === k);
      if (hidden) {
        const index = hidden.name.split('_').pop();
        const info = data[k];
        const input = document.getElementById('value_' + index);
        const cb = document.getElementById('enabled_' + index);
        
        if (input) {
          input.value = info.value;
          if (!info.enabled) {
            input.disabled = true;
            input.classList.add('disabled');
          } else {
            input.disabled = false;
            input.classList.remove('disabled');
          }
        }
        if (cb) cb.checked = !!info.enabled;
      }
    });
    schedulePreview();
    showSuccess('已恢复本地草稿');
  } catch (e) {
    console.warn('恢复草稿失败', e);
  }
}

// 通知模态框
function openNoticeModal() {
  console.log('🔔 openNoticeModal called'); // 调试信息
  const modal = document.getElementById('noticeModalBackdrop');
  console.log('🔍 Modal element:', modal); // 调试信息
  
  if (modal) {
    console.log('✅ Modal found, showing...');
    modal.style.display = 'flex';
    modal.style.opacity = '0';
    setTimeout(() => {
      modal.style.opacity = '1';
      modal.classList.add('show');
    }, 10);
  } else {
    console.error('❌ Modal element not found!');
    alert('通知模态框元素未找到！请检查HTML结构。');
  }
}

function closeNoticeModal() {
  const modal = document.getElementById('noticeModalBackdrop');
  if (modal) {
    modal.classList.remove('show');
    setTimeout(() => {
      modal.style.display = 'none';
    }, 300);
  }
}

// 移动端触摸优化
function initTouchOptimizations() {
  // 为移动端优化点击区域
  if ('ontouchstart' in window) {
    document.querySelectorAll('.btn, .style-card, .site-card').forEach(element => {
      element.style.minHeight = '44px';
      element.style.minWidth = '44px';
    });
  }
}

// 键盘快捷键
function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter 生成车票
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      document.getElementById('dataForm').submit();
    }
    
    // Ctrl/Cmd + S 保存草稿
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      saveLocally();
    }
  });
}

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', () => {
  // 初始化预览
  showPreviewPlaceholder();
  
  // 绑定输入事件监听器
  document.querySelectorAll('[id^="value_"]').forEach(el => {
    el.addEventListener('input', schedulePreview);
  });
  
  document.querySelectorAll('[id^="enabled_"]').forEach(el => {
    el.addEventListener('change', schedulePreview);
  });
  
  // 恢复草稿
  tryRestoreDraft();
  
  // 初始化其他功能
  initTouchOptimizations();
  initKeyboardShortcuts();
  
  // 初始化移动端预览
  initMobilePreview();
  
  // 延迟显示通知模态框
  setTimeout(() => {
    openNoticeModal();
  }, 1000);
  
  // 绑定通知按钮事件
  const noticeToggleTop = document.getElementById('noticeToggleTop');
  if (noticeToggleTop) {
    noticeToggleTop.addEventListener('click', openNoticeModal);
  }
  
  // 绑定所有通知切换按钮
  document.querySelectorAll('.notice-toggle').forEach(toggle => {
    toggle.addEventListener('click', openNoticeModal);
  });
  
  // 绑定模态框事件
  const modalBackdrop = document.getElementById('noticeModalBackdrop');
  if (modalBackdrop) {
    // 点击背景关闭模态框
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === e.currentTarget) {
        closeNoticeModal();
      }
    });
  }
  
  // ESC键关闭模态框
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeNoticeModal();
    }
  });
});

// 初始化移动端预览功能
function initMobilePreview() {
  // 检查是否为移动端
  const isMobile = window.innerWidth <= 768;
  
  if (isMobile) {
    // 初始化移动端预览状态
    updateMobilePreview();
    
    // 添加触摸手势支持
    let startY = 0;
    let currentY = 0;
    let isDragging = false;
    
    const overlay = document.getElementById('mobilePreviewOverlay');
    const container = document.querySelector('.mobile-preview-container');
    
    // 触摸开始
    overlay.addEventListener('touchstart', (e) => {
      if (e.target === overlay) {
        startY = e.touches[0].clientY;
        isDragging = true;
      }
    });
    
    // 触摸移动
    overlay.addEventListener('touchmove', (e) => {
      if (isDragging && e.target === overlay) {
        currentY = e.touches[0].clientY;
        const deltaY = currentY - startY;
        
        if (deltaY > 50) {
          closeMobilePreview();
          isDragging = false;
        }
      }
    });
    
    // 触摸结束
    overlay.addEventListener('touchend', () => {
      isDragging = false;
    });
  }
}

// 页面可见性变化时的处理
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // 页面重新可见时刷新预览
  schedulePreview();
  }
});

// 窗口大小变化处理
window.addEventListener('resize', () => {
  const isMobile = window.innerWidth <= 768;
  const toggle = document.getElementById('mobilePreviewToggle');
  const overlay = document.getElementById('mobilePreviewOverlay');
  
  if (isMobile) {
    // 切换到移动端模式
    if (toggle) toggle.style.display = 'flex';
  } else {
    // 切换到桌面端模式
    if (toggle) toggle.style.display = 'none';
    if (overlay) {
      overlay.style.display = 'none';
      overlay.classList.remove('show');
    }
  }
});

// 点击背景关闭移动端预览
document.getElementById('mobilePreviewOverlay').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) {
    closeMobilePreview();
  }
});
</script>
<!-- 通知模态框 -->
<style>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modal {
  background: var(--bg-primary);
  width: 90%;
  max-width: 600px;
  border-radius: var(--radius-xl);
  padding: 24px;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--border-color);
  transform: scale(0.9);
  transition: transform 0.3s ease;
}

.modal-backdrop.show .modal {
  transform: scale(1);
}

.modal h4 {
  margin: 0 0 16px 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal h4 i {
  color: var(--primary-color);
}

.modal .modal-body {
  max-height: 60vh;
  overflow-y: auto;
  margin-top: 16px;
}

.modal .modal-actions {
  margin-top: 20px;
  text-align: right;
}

.modal .btn-close {
  padding: 10px 20px;
  border-radius: var(--radius-lg);
  border: 2px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  font-weight: 500;
  transition: var(--transition);
}

.modal .btn-close:hover {
  background: var(--bg-secondary);
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.notice-item {
  padding: 12px 0;
  border-bottom: 1px dashed var(--border-color);
  line-height: 1.6;
  color: var(--text-secondary);
}

.notice-item:last-child {
  border-bottom: none;
}
</style>

<script>
// 这些事件绑定将在DOMContentLoaded中处理
</script>
</body>
</html>
"""


@app.route("/", methods=["GET","POST"])
def index():
    user_id = get_or_create_user_id()
    styles = get_available_styles()
    if not styles:
        return "❌ 没有找到任何 user_*.json 文件"
    selected_style = request.values.get("style", styles[0])
    ticket_url = None

    # Inline preview handling: if client POSTs JSON to this endpoint with ?preview=1, return base64 PNG
    if request.method == 'POST' and request.args.get('preview') == '1':
        try:
            data = request.get_json(force=True)
            style = data.get('style', selected_style)
            user_data = data.get('user_data', {})
            img = render_ticket(user_data, get_template_json(style), TEMPLATE_DIR)
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            b64 = base64.b64encode(buf.read()).decode('ascii')
            return jsonify({'success': True, 'image_base64': b64})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    # Normal POST (form submit) -> generate and save ticket file
    if request.method == "POST":
        field_keys = [k for k in request.form.keys() if k.startswith("field_key_")]
        indices = sorted([int(k.split("_")[-1]) for k in field_keys])
        user_data = {}
        for i in indices:
            key_name = request.form.get(f"field_key_{i}", "").strip()
            enabled = True if request.form.get(f"field_enabled_{i}") is not None else False
            value = request.form.get(f"field_value_{i}", "")
            if key_name:
                user_data[key_name] = {"value": value, "enabled": enabled}
        save_user_data(user_data, selected_style, user_id)
        try:
            img = render_ticket(user_data, get_template_json(selected_style), TEMPLATE_DIR)
            ticket_path = get_user_ticket_path(user_id)
            img.save(ticket_path, format="PNG")
            ticket_url = url_for("get_user_ticket", user_id=user_id)
        except Exception as e:
            return f"生成失败: {e}"
    else:
        user_data = load_user_data(selected_style, user_id)

    return render_template_string(HTML_TEMPLATE,
                                  styles=styles,
                                  selected_style=selected_style,
                                  user_data=user_data,
                                  ticket_url=ticket_url,
                                  recommend_sites=RECOMMEND_SITES,
                                  notices=NOTICES,
                                  bg_url=url_for('static', filename='previews/bg.png'))


@app.route("/ticket/<filename>")
def get_ticket(filename):
    return send_file(os.path.join(BASE_DIR, filename), mimetype="image/png")


@app.route("/user_ticket/<user_id>")
def get_user_ticket(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return "Unauthorized", 403
    ticket_path = get_user_ticket_path(user_id)
    if not os.path.exists(ticket_path):
        return "Ticket not found", 404
    return send_file(ticket_path, mimetype="image/png")


if __name__=="__main__":
    app.run(host="0.0.0.0", port=4999, debug=False)

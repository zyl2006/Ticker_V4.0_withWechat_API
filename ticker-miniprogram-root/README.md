# 🚀 Ticker-车票儿 微信小程序

## 📋 项目说明

Ticker-车票儿是一个基于微信小程序的纪念车票生成工具，利用Python API服务作为后端，提供便捷的纪念车票制作体验。

## 🚀 快速开始

### 1. 导入项目到微信开发者工具

1. **打开微信开发者工具**
2. **选择"导入项目"**
3. **选择项目目录**：选择 `ticker-miniprogram-root` 文件夹
4. **填写项目信息**：
   - AppID：填写您的小程序AppID（或选择测试号）
   - 项目名称：Ticker-车票儿
   - 开发模式：小程序
5. **点击"导入"**

### 2. 配置API地址

编辑 `app.js` 文件，修改API地址：

```javascript
globalData: {
  apiBaseUrl: 'https://your-api-domain.com', // 替换为您的API域名
  // 本地测试可以使用：http://localhost:5001
}
```

### 3. 启动API服务器

在项目根目录运行：

```bash
python api_server_optimized.py
```

### 4. 预览和调试

- 在微信开发者工具中点击"预览"
- 使用真机调试功能测试
- 检查控制台是否有错误信息

## 📁 项目结构

```
ticker-miniprogram-root/
├── app.js                 # 小程序入口文件
├── app.json              # 小程序全局配置
├── app.wxss              # 小程序全局样式
├── project.config.json   # 项目配置文件
├── sitemap.json          # 站点地图配置
├── pages/                # 页面目录
│   ├── index/            # 首页
│   ├── preview/          # 预览页
│   └── about/            # 关于页
├── utils/                # 工具函数
│   ├── api.js           # API调用封装
│   ├── storage.js       # 本地存储工具
│   └── validator.js      # 数据验证工具
└── styles/              # 样式文件
    └── variables.wxss   # 样式变量
```

## 🔧 功能特性

- ✅ **样式选择**：多种车票样式可选
- ✅ **表单填写**：动态表单，智能验证
- ✅ **实时预览**：即时生成预览效果
- ✅ **图片保存**：支持保存到相册
- ✅ **草稿管理**：本地存储和恢复
- ✅ **历史记录**：查看生成历史
- ✅ **响应式设计**：适配不同设备

## 🛠️ 开发说明

### API接口

小程序通过以下API接口与后端通信：

- `GET /api/health` - 健康检查
- `GET /api/styles` - 获取样式列表
- `GET /api/template/<style>` - 获取模板信息
- `POST /api/generate` - 生成车票
- `POST /api/batch_generate` - 批量生成

### 本地存储

使用微信小程序的本地存储API：

- 草稿数据：`wx.setStorageSync('ticker_draft', data)`
- 历史记录：`wx.setStorageSync('ticker_history', data)`
- 用户设置：`wx.setStorageSync('ticker_settings', data)`

### 权限申请

小程序需要以下权限：

- 相册权限：保存图片到相册
- 网络权限：调用API接口

## 🚀 部署发布

### 1. 代码上传

1. 在微信开发者工具中点击"上传"
2. 填写版本号和项目备注
3. 上传到微信后台

### 2. 提交审核

1. 在微信公众平台完善小程序信息
2. 上传小程序图标和截图
3. 设置服务类目
4. 提交审核

### 3. 发布上线

1. 审核通过后点击"发布"
2. 用户即可在微信中搜索使用

## 🐛 常见问题

### Q: 编译错误 "app.json 未找到"
A: 确保在微信开发者工具中导入的是 `ticker-miniprogram-root` 文件夹，而不是整个项目文件夹。

### Q: API请求失败
A: 检查API服务器是否正常运行，以及API地址是否正确配置。

### Q: 图片保存失败
A: 检查是否已授权相册权限，可以在设置中手动开启。

### Q: 预览生成失败
A: 检查网络连接和API服务状态，确保后端服务正常运行。

## 📞 技术支持

如有问题，请通过以下方式联系：

- 邮箱：support@ticker.com
- 微信：TickerSupport

## 📄 许可证

© 2024 Ticker-车票儿. All rights reserved.

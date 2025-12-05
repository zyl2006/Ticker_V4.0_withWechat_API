// pages/home/home.js
// 首页 - 项目介绍和车票样式展示

const api = require('../../utils/api')

Page({
  data: {
    // 页面状态
    loading: true,
    error: null,
    
    // 样式相关
    styles: [],
    
    // 项目信息
    projectInfo: {
      name: 'Ticker-车票儿',
      description: '专业的车票生成工具，支持多种样式，让您的车票更加个性化',
      version: '1.0.0',
      features: [
        '多种车票样式选择',
        '实时预览功能',
        '云端同步保存',
        '一键保存到相册'
      ]
    }
  },

  onLoad() {
    console.log('首页加载')
    this.initPage()
  },

  onShow() {
    console.log('首页显示')
  },

  onReady() {
    console.log('首页准备完成')
  },

  // 初始化页面
  async initPage() {
    try {
      this.setData({ loading: true, error: null })
      
      // 获取样式列表
      await this.loadStyles()
      
      this.setData({ loading: false })
    } catch (error) {
      console.error('初始化页面失败:', error)
      this.setData({ 
        loading: false, 
        error: '初始化失败，请检查网络连接' 
      })
    }
  },

  // 加载样式列表
  async loadStyles() {
    try {
      const result = await api.getStyles()
      if (result.success) {
        this.setData({ styles: result.styles })
      } else {
        throw new Error(result.error || '获取样式列表失败')
      }
    } catch (error) {
      console.error('加载样式列表失败:', error)
      // 使用默认样式列表
      this.setData({ 
        styles: ['red15', 'blue15', 'red05_longride', 'red05_shortride', 'red1997']
      })
    }
  },

  // 选择样式跳转到制作页面
  onStyleSelect(e) {
    const style = e.currentTarget.dataset.style
    console.log('选择样式:', style)
    
    // 跳转到制作页面并传递样式参数
    wx.switchTab({
      url: `/pages/make/make?style=${style}`
    })
  },

  // 开始制作
  startMaking() {
    wx.switchTab({
      url: '/pages/make/make'
    })
  },

  // 查看历史
  viewHistory() {
    wx.switchTab({
      url: '/pages/history/history'
    })
  },

  // 错误重试
  retry() {
    this.initPage()
  }
})
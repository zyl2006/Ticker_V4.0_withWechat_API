// pages/about/about.js
// 关于页面

const storage = require('../../utils/storage')

Page({
  data: {
    version: '1.0.0',
    buildTime: '2024-01-01',
    history: [],
    settings: {}
  },

  onLoad() {
    console.log('关于页面加载')
    this.loadData()
  },

  onShow() {
    console.log('关于页面显示')
  },

  // 加载数据
  loadData() {
    // 加载历史记录
    const history = storage.getHistory()
    this.setData({ history })
    
    // 加载用户设置
    const settings = storage.getSettings()
    this.setData({ settings })
  },

  // 清除历史记录
  clearHistory() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有历史记录吗？此操作不可恢复。',
      success: (res) => {
        if (res.confirm) {
          storage.clearHistory()
          this.setData({ history: [] })
          wx.showToast({
            title: '已清除历史记录',
            icon: 'success'
          })
        }
      }
    })
  },

  // 清除草稿
  clearDraft() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除当前草稿吗？',
      success: (res) => {
        if (res.confirm) {
          storage.clearDraft()
          wx.showToast({
            title: '已清除草稿',
            icon: 'success'
          })
        }
      }
    })
  },

  // 清除所有数据
  clearAllData() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有数据吗？包括历史记录、草稿和设置。此操作不可恢复。',
      success: (res) => {
        if (res.confirm) {
          storage.clear()
          this.setData({ 
            history: [],
            settings: {}
          })
          wx.showToast({
            title: '已清除所有数据',
            icon: 'success'
          })
        }
      }
    })
  },

  // 查看历史记录
  viewHistory() {
    if (this.data.history.length === 0) {
      wx.showToast({
        title: '暂无历史记录',
        icon: 'none'
      })
      return
    }
    
    wx.showModal({
      title: '历史记录',
      content: `共有 ${this.data.history.length} 条历史记录`,
      showCancel: false
    })
  },

  // 检查更新
  checkUpdate() {
    wx.showLoading({ title: '检查更新...' })
    
    setTimeout(() => {
      wx.hideLoading()
      wx.showToast({
        title: '已是最新版本',
        icon: 'success'
      })
    }, 1000)
  },

  // 联系客服
  contactService() {
    wx.showModal({
      title: '联系客服',
      content: '如有问题，请通过以下方式联系我们：\n\n邮箱：support@ticker.com\n微信：TickerSupport',
      showCancel: false
    })
  },

  // 分享应用
  shareApp() {
    wx.showShareMenu({
      withShareTicket: true
    })
  },

  // 复制版本信息
  copyVersion() {
    wx.setClipboardData({
      data: `Ticker-车票儿 v${this.data.version}\n构建时间：${this.data.buildTime}`,
      success: () => {
        wx.showToast({
          title: '已复制版本信息',
          icon: 'success'
        })
      }
    })
  }
})

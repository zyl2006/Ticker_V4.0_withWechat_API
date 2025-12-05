// app.js
App({
  globalData: {
    userInfo: null,
    apiBaseUrl: 'http://api.sgsky.tech', // 本地API服务器地址
    currentStyle: 'red15',
    draftData: null,
    history: []
  },

  onLaunch() {
    console.log('Ticker-车票儿 小程序启动')
    
    // 检查更新
    this.checkForUpdate()
    
    // 初始化本地数据
    this.initLocalData()
  },

  onShow() {
    console.log('小程序显示')
  },

  onHide() {
    console.log('小程序隐藏')
  },

  onError(error) {
    console.error('小程序错误:', error)
  },

  // 检查小程序更新
  checkForUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      updateManager.onCheckForUpdate((res) => {
        console.log('检查更新结果:', res.hasUpdate)
      })

      updateManager.onUpdateReady(() => {
        wx.showModal({
          title: '更新提示',
          content: '新版本已经准备好，是否重启应用？',
          success: (res) => {
            if (res.confirm) {
              updateManager.applyUpdate()
            }
          }
        })
      })

      updateManager.onUpdateFailed(() => {
        console.log('更新失败')
      })
    }
  },

  // 初始化本地数据
  initLocalData() {
    try {
      // 获取草稿数据
      const draftData = wx.getStorageSync('ticker_draft')
      if (draftData) {
        this.globalData.draftData = draftData
      }

      // 获取历史记录
      const history = wx.getStorageSync('ticker_history')
      if (history) {
        this.globalData.history = history
      }
    } catch (error) {
      console.error('初始化本地数据失败:', error)
    }
  },

  // 保存草稿
  saveDraft(data) {
    try {
      wx.setStorageSync('ticker_draft', data)
      this.globalData.draftData = data
      return true
    } catch (error) {
      console.error('保存草稿失败:', error)
      return false
    }
  },

  // 获取草稿
  getDraft() {
    return this.globalData.draftData
  },

  // 清除草稿
  clearDraft() {
    try {
      wx.removeStorageSync('ticker_draft')
      this.globalData.draftData = null
      return true
    } catch (error) {
      console.error('清除草稿失败:', error)
      return false
    }
  },

  // 添加历史记录
  addHistory(item) {
    try {
      const history = this.globalData.history || []
      history.unshift({
        id: Date.now(),
        timestamp: new Date().toISOString(),
        style: item.style,
        data: item.data,
        preview: item.preview
      })
      
      // 只保留最近20条记录
      if (history.length > 20) {
        history.splice(20)
      }
      
      wx.setStorageSync('ticker_history', history)
      this.globalData.history = history
      return true
    } catch (error) {
      console.error('添加历史记录失败:', error)
      return false
    }
  },

  // 获取历史记录
  getHistory() {
    return this.globalData.history || []
  },

  // 清除历史记录
  clearHistory() {
    try {
      wx.removeStorageSync('ticker_history')
      this.globalData.history = []
      return true
    } catch (error) {
      console.error('清除历史记录失败:', error)
      return false
    }
  }
})

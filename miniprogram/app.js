// app.js
App({
  globalData: {
    userInfo: null,
    userId: null, // 用户唯一标识
    apiBaseUrl: 'https://api.sgsky.online', // 修复端口号
    currentStyle: 'blue15',
    draftData: null,
    history: [],
    loadHistoryData: null, // 用于从历史记录加载数据到制作页面
    privacyAgreed: true // 隐私授权状态
  },

  onLaunch() {
    console.log('Ticker-车票儿 小程序启动')

    // 检查更新
    this.checkForUpdate()

    // 初始化本地数据
    this.initLocalData()

    // 延迟检查隐私授权状态，确保框架完全初始化
    setTimeout(() => {
      this.checkPrivacyAuth()
    }, 100)
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

  // 检查更新
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
        console.error('更新失败')
      })
    }
  },

  // 初始化本地数据
  initLocalData() {
    try {
      // 加载用户ID
      const userId = wx.getStorageSync('ticker_user_id')
      if (userId) {
        this.globalData.userId = userId
        console.log('用户ID已加载:', userId)
      }

      // 加载用户信息
      const userInfo = wx.getStorageSync('ticker_user_info')
      if (userInfo) {
        this.globalData.userInfo = userInfo
        console.log('用户信息已加载:', userInfo.nickName)
      }

      // 加载历史记录（仅作为缓存，用于离线查看）
      const history = wx.getStorageSync('ticker_history') || []
      this.globalData.history = history

      // 加载草稿数据
      const draftData = wx.getStorageSync('ticker_draft') || null
      this.globalData.draftData = draftData

      console.log('本地数据初始化完成')
    } catch (error) {
      console.error('初始化本地数据失败:', error)
    }
  },

  // 获取历史记录
  getHistory() {
    return this.globalData.history || []
  },

  // 添加历史记录
  addHistory(item) {
    try {
      const history = this.getHistory()
      const newItem = {
        id: Date.now().toString(),
        ...item,
        timestamp: new Date().toISOString()
      }
      
      history.unshift(newItem)
      
      // 限制历史记录数量
      if (history.length > 100) {
        history.splice(100)
      }
      
      this.globalData.history = history
      wx.setStorageSync('ticker_history', history)
      
      console.log('历史记录已添加:', newItem)
    } catch (error) {
      console.error('添加历史记录失败:', error)
    }
  },

  // 清除历史记录
  clearHistory() {
    try {
      this.globalData.history = []
      wx.removeStorageSync('ticker_history')
      console.log('历史记录已清除')
    } catch (error) {
      console.error('清除历史记录失败:', error)
    }
  },

  // 保存草稿
  saveDraft(data) {
    try {
      this.globalData.draftData = data
      wx.setStorageSync('ticker_draft', data)
      console.log('草稿已保存')
    } catch (error) {
      console.error('保存草稿失败:', error)
    }
  },

  // 获取草稿
  getDraft() {
    return this.globalData.draftData
  },

  // 清除草稿
  clearDraft() {
    try {
      this.globalData.draftData = null
      wx.removeStorageSync('ticker_draft')
      console.log('草稿已清除')
    } catch (error) {
      console.error('清除草稿失败:', error)
    }
  },

  // 设置API基础URL
  setApiBaseUrl(url) {
    this.globalData.apiBaseUrl = url
    console.log('API基础URL已设置:', url)
  },

  // 获取API基础URL
  getApiBaseUrl() {
    return this.globalData.apiBaseUrl
  },

  // 设置当前样式
  setCurrentStyle(style) {
    this.globalData.currentStyle = style
    console.log('当前样式已设置:', style)
  },

  // 获取当前样式
  getCurrentStyle() {
    return this.globalData.currentStyle
  },

  // 检查隐私授权状态
  checkPrivacyAuth() {
    try {
      const privacyAgreed = wx.getStorageSync('privacy_agreed') || false
      this.globalData.privacyAgreed = privacyAgreed
      console.log('隐私授权状态:', privacyAgreed)

      if (!privacyAgreed) {
        console.log('用户尚未同意隐私政策，跳转到隐私政策页面')
        // 强制跳转到隐私政策页面
        wx.redirectTo({
          url: '/pages/privacy/privacy?required=true'
        })
        return false
      }
      return true
    } catch (error) {
      console.error('检查隐私授权状态失败:', error)
      this.globalData.privacyAgreed = false
      // 出错时也强制跳转到隐私政策页面
      wx.redirectTo({
        url: '/pages/privacy/privacy?required=true'
      })
      return false
    }
  },

  // 设置隐私授权状态
  setPrivacyAgreed(agreed) {
    this.globalData.privacyAgreed = agreed
    try {
      wx.setStorageSync('privacy_agreed', agreed)
      if (agreed) {
        wx.setStorageSync('privacy_agree_time', new Date().toISOString())
      }
      console.log('隐私授权状态已更新:', agreed)
    } catch (error) {
      console.error('保存隐私授权状态失败:', error)
    }
  },

  // 设置用户ID
  setUserId(userId) {
    this.globalData.userId = userId
    try {
      wx.setStorageSync('ticker_user_id', userId)
      console.log('用户ID已设置:', userId)
    } catch (error) {
      console.error('保存用户ID失败:', error)
    }
  },

  // 获取用户ID
  getUserId() {
    return this.globalData.userId
  },

  // 设置用户信息
  setUserInfo(userInfo) {
    this.globalData.userInfo = userInfo
    try {
      wx.setStorageSync('ticker_user_info', userInfo)
      console.log('用户信息已保存:', userInfo.nickName)
    } catch (error) {
      console.error('保存用户信息失败:', error)
    }
  },

  // 获取用户信息
  getUserInfo() {
    return this.globalData.userInfo
  },

  // 清除用户数据（登出）
  clearUserData() {
    this.globalData.userId = null
    this.globalData.userInfo = null
    this.globalData.history = []

    try {
      wx.removeStorageSync('ticker_user_id')
      wx.removeStorageSync('ticker_user_info')
      wx.removeStorageSync('ticker_history')
      wx.removeStorageSync('ticker_draft')
      console.log('用户数据已清除')
    } catch (error) {
      console.error('清除用户数据失败:', error)
    }
  }
})
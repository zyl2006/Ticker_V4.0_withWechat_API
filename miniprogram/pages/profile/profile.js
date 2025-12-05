// pages/profile/profile.js
// 用户中心页面 - 用户信息和小程序信息

const privacy = require('../../utils/privacy')
const api = require('../../utils/api')

Page({
  data: {
    // 用户信息
    userInfo: null,
    hasUserInfo: false,
    
    // 小程序信息
    appInfo: {
      name: 'Ticker-车票儿',
      version: '1.0.0',
      description: '专业的车票生成工具',
      developer: 'Ticker Team',
      contact: 'support@ticker.com'
    },
    
    // 统计数据
    stats: {
      totalGenerated: 0,
      favoriteStyle: 'red15',
      joinDate: '2024-01-01'
    },
    
    // 设置选项
    settings: [
      {
        key: 'autoPreview',
        title: '自动预览',
        desc: '输入内容时自动生成预览',
        type: 'switch',
        value: true
      },
      {
        key: 'saveDraft',
        title: '自动保存草稿',
        desc: '自动保存未完成的制作',
        type: 'switch',
        value: true
      },
      {
        key: 'notifications',
        title: '推送通知',
        desc: '接收制作完成通知',
        type: 'switch',
        value: false
      }
    ]
  },

  onLoad() {
    console.log('用户中心页面加载')
    this.initPage()
  },

  onShow() {
    console.log('用户中心页面显示')
    this.loadUserInfo()
    this.loadStats()
  },

  onReady() {
    console.log('用户中心页面准备完成')
  },

  // 初始化页面
  initPage() {
    this.loadUserInfo()
    this.loadStats()
    this.loadSettings()
  },

  // 加载用户信息
  loadUserInfo() {
    const app = getApp()
    const userInfo = app.getUserInfo()
    const userId = app.getUserId()

    if (userInfo && userId) {
      this.setData({
        userInfo: userInfo,
        hasUserInfo: true
      })
    } else {
      this.setData({
        userInfo: {
          nickName: '未登录用户',
          avatarUrl: '/images/default-avatar.png'
        },
        hasUserInfo: false
      })
    }
  },

  // 加载统计数据
  loadStats() {
    try {
      const app = getApp()
      const history = app.getHistory()
      
      // 计算统计数据
      const totalGenerated = history.length
      const styleCounts = {}
      history.forEach(item => {
        styleCounts[item.style] = (styleCounts[item.style] || 0) + 1
      })
      
      const favoriteStyle = Object.keys(styleCounts).reduce((a, b) => 
        styleCounts[a] > styleCounts[b] ? a : b, 'red15'
      )
      
      this.setData({
        'stats.totalGenerated': totalGenerated,
        'stats.favoriteStyle': favoriteStyle
      })
    } catch (error) {
      console.error('加载统计数据失败:', error)
    }
  },

  // 加载设置
  loadSettings() {
    try {
      const settings = wx.getStorageSync('ticker_settings') || this.data.settings
      this.setData({ settings })
    } catch (error) {
      console.error('加载设置失败:', error)
    }
  },

  // 获取用户信息（真正的登录/注册）
  getUserProfile(e) {
    console.log('获取用户信息事件:', e)

    if (e.detail.userInfo) {
      // 用户同意授权
      const rawUserInfo = e.detail.userInfo
      console.log('获取微信用户信息成功:', rawUserInfo)

      wx.showLoading({ title: '登录中...' })

      // 尝试登录或注册用户
      this.loginOrRegisterUser(rawUserInfo)
    } else {
      // 用户拒绝授权
      console.log('用户拒绝授权')
      wx.showToast({
        title: '需要授权才能登录',
        icon: 'none'
      })
    }
  },

  // 登录或注册用户
  async loginOrRegisterUser(rawUserInfo) {
    try {
      const app = getApp()

      // 构造用户数据（去除敏感信息，只保留基本信息）
      const userData = {
        nickName: rawUserInfo.nickName,
        avatarUrl: rawUserInfo.avatarUrl,
        gender: rawUserInfo.gender,
        // 使用微信的匿名标识作为用户标识符的一部分
        openId: rawUserInfo.openId || this.generateUserIdentifier(rawUserInfo)
      }

      console.log('准备登录/注册用户:', userData)

      // 首先尝试登录
      try {
        const loginResult = await api.loginUser(userData)
        if (loginResult.success) {
          console.log('用户登录成功:', loginResult)

          // 保存用户ID和信息
          app.setUserId(loginResult.user.user_id)
          app.setUserInfo({
            ...userData,
            user_id: loginResult.user.user_id,
            register_time: loginResult.user.register_time
          })

          this.setData({
            userInfo: app.getUserInfo(),
            hasUserInfo: true
          })

          wx.hideLoading()
          wx.showToast({
            title: '登录成功',
            icon: 'success'
          })

          // 重新加载统计数据
          this.loadStats()
          return
        }
      } catch (loginError) {
        console.log('用户未注册，准备注册:', loginError.message)
      }

      // 登录失败，尝试注册
      try {
        const registerResult = await api.registerUser(userData)
        if (registerResult.success) {
          console.log('用户注册成功:', registerResult)

          // 保存用户ID和信息
          app.setUserId(registerResult.user.user_id)
          app.setUserInfo({
            ...userData,
            user_id: registerResult.user.user_id,
            register_time: registerResult.user.register_time
          })

          this.setData({
            userInfo: app.getUserInfo(),
            hasUserInfo: true
          })

          wx.hideLoading()
          wx.showToast({
            title: '注册成功',
            icon: 'success'
          })

          // 重新加载统计数据
          this.loadStats()
        } else {
          throw new Error('注册失败')
        }
      } catch (registerError) {
        console.error('注册失败:', registerError)
        wx.hideLoading()
        wx.showToast({
          title: '登录失败，请重试',
          icon: 'error'
        })
      }

    } catch (error) {
      console.error('登录/注册过程出错:', error)
      wx.hideLoading()
      wx.showToast({
        title: '登录失败',
        icon: 'error'
      })
    }
  },

  // 生成用户标识符（用于没有openId的情况）
  generateUserIdentifier(userInfo) {
    // 使用昵称、头像和时间戳生成唯一标识符
    const timestamp = Date.now()
    const identifier = `${userInfo.nickName}_${userInfo.avatarUrl}_${timestamp}`
    return this.hashString(identifier)
  },

  // 简单的字符串哈希函数
  hashString(str) {
    let hash = 0
    if (str.length === 0) return hash.toString()
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i)
      hash = ((hash << 5) - hash) + char
      hash = hash & hash // 转换为32位整数
    }
    return Math.abs(hash).toString()
  },

  // 设置项切换
  onSettingChange(e) {
    const { key, value } = e.currentTarget.dataset
    const settings = [...this.data.settings]
    const setting = settings.find(s => s.key === key)
    
    if (setting) {
      setting.value = value
      this.setData({ settings })
      
      // 保存设置
      try {
        wx.setStorageSync('ticker_settings', settings)
        wx.showToast({
          title: '设置已保存',
          icon: 'success'
        })
      } catch (error) {
        console.error('保存设置失败:', error)
      }
    }
  },

  // 登出
  logout() {
    const app = getApp()
    if (!app.getUserId()) {
      wx.showToast({
        title: '当前未登录',
        icon: 'none'
      })
      return
    }

    wx.showModal({
      title: '确认登出',
      content: '确定要登出当前账号吗？这将清除本地数据。',
      success: (res) => {
        if (res.confirm) {
          try {
            // 清除用户数据
            app.clearUserData()

            // 重置界面
            this.setData({
              userInfo: {
                nickName: '未登录用户',
                avatarUrl: '/images/default-avatar.png'
              },
              hasUserInfo: false,
              'stats.totalGenerated': 0,
              'stats.favoriteStyle': 'red15'
            })

            wx.showToast({
              title: '已登出',
              icon: 'success'
            })
          } catch (error) {
            console.error('登出失败:', error)
            wx.showToast({
              title: '登出失败',
              icon: 'error'
            })
          }
        }
      }
    })
  },

  // 清除缓存
  clearCache() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有缓存数据吗？这将删除草稿和本地历史记录，但不会影响服务器数据。',
      success: (res) => {
        if (res.confirm) {
          try {
            // 只清除非用户数据的缓存
            wx.removeStorageSync('ticker_draft')
            wx.removeStorageSync('ticker_history') // 本地缓存的历史记录

            // 重置应用数据
            const app = getApp()
            app.globalData.draftData = null
            app.globalData.history = []

            // 重新加载统计数据（如果已登录）
            if (app.getUserId()) {
              this.loadStats()
            } else {
              this.setData({
                'stats.totalGenerated': 0,
                'stats.favoriteStyle': 'red15'
              })
            }

            wx.showToast({
              title: '缓存已清除',
              icon: 'success'
            })
          } catch (error) {
            console.error('清除缓存失败:', error)
            wx.showToast({
              title: '清除失败',
              icon: 'error'
            })
          }
        }
      }
    })
  },

  // 检查更新
  checkUpdate() {
    if (wx.canIUse('getUpdateManager')) {
      const updateManager = wx.getUpdateManager()
      
      updateManager.onCheckForUpdate((res) => {
        if (res.hasUpdate) {
          wx.showModal({
            title: '发现新版本',
            content: '是否立即更新？',
            success: (res) => {
              if (res.confirm) {
                updateManager.applyUpdate()
              }
            }
          })
        } else {
          wx.showToast({
            title: '已是最新版本',
            icon: 'success'
          })
        }
      })
    } else {
      wx.showToast({
        title: '当前版本不支持自动更新',
        icon: 'none'
      })
    }
  },

  // 意见反馈
  feedback() {
    wx.showModal({
      title: '意见反馈',
      content: '如有问题或建议，请联系：' + this.data.appInfo.contact,
      showCancel: false
    })
  },

  // 关于我们
  about() {
    wx.showModal({
      title: '关于我们',
      content: `${this.data.appInfo.name}\n版本：${this.data.appInfo.version}\n\n${this.data.appInfo.description}\n\n开发者：${this.data.appInfo.developer}`,
      showCancel: false
    })
  },

  // 隐私政策
  privacy() {
    wx.showModal({
      title: '隐私政策',
      content: '我们重视您的隐私保护。本应用仅在本地存储您的制作数据，不会上传到服务器。',
      showCancel: false
    })
  },

  // 使用条款
  terms() {
    wx.showModal({
      title: '使用条款',
      content: '使用本应用即表示您同意相关使用条款。请合理使用本应用，不得用于违法违规用途。',
      showCancel: false
    })
  }
})
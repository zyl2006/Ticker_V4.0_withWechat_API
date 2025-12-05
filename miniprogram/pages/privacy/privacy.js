// pages/privacy/privacy.js
// 隐私政策页面

Page({
  data: {
    hasAgreed: false,
    isRequired: false
  },

  onLoad(options) {
    console.log('隐私政策页面加载', options)

    // 检查是否已经同意过隐私政策
    const hasAgreed = wx.getStorageSync('privacy_agreed') || false
    const isRequired = options.required === 'true'

    this.setData({
      hasAgreed,
      isRequired
    })

    // 如果已经同意且不是强制要求的，直接返回
    if (hasAgreed && !isRequired) {
      this.goBack()
    }
  },

  onShow() {
    console.log('隐私政策页面显示')
  },

  // 同意隐私政策
  agreePrivacy() {
    try {
      // 保存用户同意状态
      wx.setStorageSync('privacy_agreed', true)
      wx.setStorageSync('privacy_agree_time', new Date().toISOString())

      wx.showToast({
        title: '感谢您的信任',
        icon: 'success'
      })

      // 延迟返回或跳转到首页
      setTimeout(() => {
        if (this.data.isRequired) {
          // 如果是强制要求的，跳转到首页
          wx.switchTab({
            url: '/pages/home/home',
            fail: (error) => {
              console.error('跳转到首页失败:', error)
              // 如果跳转失败，尝试重新加载当前页面
              wx.reLaunch({
                url: '/pages/home/home'
              })
            }
          })
        } else {
          this.goBack()
        }
      }, 1500)

    } catch (error) {
      console.error('保存隐私同意状态失败:', error)
      wx.showToast({
        title: '保存失败',
        icon: 'error'
      })
    }
  },

  // 不同意隐私政策
  disagreePrivacy() {
    if (this.data.isRequired) {
      wx.showModal({
        title: '必须同意',
        content: '您必须同意隐私政策才能使用本应用',
        showCancel: false
      })
    } else {
      wx.showModal({
        title: '提示',
        content: '不同意隐私政策将无法使用部分功能',
        showCancel: false,
        success: () => {
          wx.navigateBack()
        }
      })
    }
  },

  // 返回上一页
  goBack() {
    const pages = getCurrentPages()
    if (pages.length > 1) {
      wx.navigateBack()
    } else {
      // 如果是第一个页面，跳转到首页
      wx.switchTab({
        url: '/pages/home/home'
      })
    }
  }
})

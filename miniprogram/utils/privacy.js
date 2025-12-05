// utils/privacy.js
// 隐私授权管理工具

class PrivacyManager {
  constructor() {
    this.privacyAgreed = false
    this.init()
  }

  // 初始化
  init() {
    try {
      this.privacyAgreed = wx.getStorageSync('privacy_agreed') || false
      console.log('隐私授权状态:', this.privacyAgreed)
    } catch (error) {
      console.error('初始化隐私授权状态失败:', error)
      this.privacyAgreed = false
    }
  }

  // 检查隐私授权状态
  checkPrivacyAuth() {
    return this.privacyAgreed
  }

  // 显示隐私授权弹窗
  showPrivacyAuth(callback) {
    if (this.privacyAgreed) {
      // 已经同意，直接执行回调
      if (callback) callback(true)
      return
    }

    // 显示隐私授权弹窗
    wx.showModal({
      title: '隐私授权',
      content: '为了给您提供更好的服务，我们需要获取您的个人信息。请阅读并同意我们的隐私政策。',
      confirmText: '查看隐私政策',
      cancelText: '暂不同意',
      success: (res) => {
        if (res.confirm) {
          // 用户点击查看隐私政策
          this.showPrivacyPolicy(callback)
        } else {
          // 用户暂不同意
          if (callback) callback(false)
        }
      },
      fail: () => {
        if (callback) callback(false)
      }
    })
  }

  // 显示隐私政策页面
  showPrivacyPolicy(callback) {
    wx.navigateTo({
      url: '/pages/privacy/privacy',
      success: () => {
        // 监听隐私政策页面返回
        this.waitForPrivacyResult(callback)
      },
      fail: () => {
        if (callback) callback(false)
      }
    })
  }

  // 等待隐私政策结果
  waitForPrivacyResult(callback) {
    const checkInterval = setInterval(() => {
      const agreed = wx.getStorageSync('privacy_agreed') || false
      if (agreed) {
        clearInterval(checkInterval)
        this.privacyAgreed = true
        if (callback) callback(true)
      }
    }, 500)

    // 10秒后超时
    setTimeout(() => {
      clearInterval(checkInterval)
      if (callback) callback(false)
    }, 10000)
  }

  // 请求用户信息权限
  requestUserInfo(callback) {
    this.showPrivacyAuth((agreed) => {
      if (agreed) {
        wx.getUserProfile({
          desc: '用于完善用户资料和个性化服务',
          success: (res) => {
            console.log('获取用户信息成功:', res.userInfo)
            if (callback) callback(true, res.userInfo)
          },
          fail: (error) => {
            console.error('获取用户信息失败:', error)
            if (callback) callback(false, error)
          }
        })
      } else {
        if (callback) callback(false, '用户未同意隐私政策')
      }
    })
  }

  // 请求相册权限
  requestPhotosAlbum(callback) {
    this.showPrivacyAuth((agreed) => {
      if (agreed) {
        wx.authorize({
          scope: 'scope.writePhotosAlbum',
          success: () => {
            console.log('相册权限授权成功')
            if (callback) callback(true)
          },
          fail: (error) => {
            console.error('相册权限授权失败:', error)
            // 引导用户手动开启权限
            wx.showModal({
              title: '权限提示',
              content: '需要相册权限才能保存图片，请在设置中开启',
              showCancel: false
            })
            if (callback) callback(false, error)
          }
        })
      } else {
        if (callback) callback(false, '用户未同意隐私政策')
      }
    })
  }

  // 保存图片到相册（带权限检查）
  saveImageToPhotosAlbum(filePath, callback) {
    wx.saveImageToPhotosAlbum({
      filePath: filePath,
      success: () => {
        console.log('保存图片成功')
        if (callback) callback(true)
      },
      fail: (error) => {
        console.error('保存图片失败:', error)

        // 如果是权限问题，引导用户开启权限
        if (error.errMsg && error.errMsg.includes('auth deny')) {
          wx.showModal({
            title: '权限提示',
            content: '需要相册权限才能保存图片，是否前往设置开启？',
            confirmText: '去设置',
            success: (res) => {
              if (res.confirm) {
                wx.openSetting({
                  success: (settingRes) => {
                    if (settingRes.authSetting['scope.writePhotosAlbum']) {
                      // 用户开启了权限，重新尝试保存
                      wx.saveImageToPhotosAlbum({
                        filePath: filePath,
                        success: () => {
                          console.log('重新保存图片成功')
                          if (callback) callback(true)
                        },
                        fail: (retryError) => {
                          console.error('重新保存图片失败:', retryError)
                          if (callback) callback(false, retryError)
                        }
                      })
                    } else {
                      if (callback) callback(false, '用户未开启相册权限')
                    }
                  }
                })
              } else {
                if (callback) callback(false, '用户取消开启权限')
              }
            }
          })
        } else {
          if (callback) callback(false, error)
        }
      }
    })
  }

  // 重置隐私授权状态（用于测试）
  resetPrivacyAuth() {
    try {
      wx.removeStorageSync('privacy_agreed')
      wx.removeStorageSync('privacy_agree_time')
      this.privacyAgreed = false
      console.log('隐私授权状态已重置')
    } catch (error) {
      console.error('重置隐私授权状态失败:', error)
    }
  }
}

// 创建全局实例
const privacyManager = new PrivacyManager()

// 导出方法
module.exports = {
  // 基础方法
  checkPrivacyAuth: () => privacyManager.checkPrivacyAuth(),
  showPrivacyAuth: (callback) => privacyManager.showPrivacyAuth(callback),
  
  // 权限请求方法
  requestUserInfo: (callback) => privacyManager.requestUserInfo(callback),
  requestPhotosAlbum: (callback) => privacyManager.requestPhotosAlbum(callback),
  
  // 功能方法
  saveImageToPhotosAlbum: (filePath, callback) => privacyManager.saveImageToPhotosAlbum(filePath, callback),
  
  // 工具方法
  resetPrivacyAuth: () => privacyManager.resetPrivacyAuth()
}

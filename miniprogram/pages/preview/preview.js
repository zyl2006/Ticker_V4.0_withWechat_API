// pages/preview/preview.js
// 预览页面 - 查看车票预览

const privacy = require('../../utils/privacy')

Page({
  data: {
    previewImage: null
  },

  onLoad(options) {
    console.log('预览页面加载', options)
    
    if (options.image) {
      this.setData({
        previewImage: decodeURIComponent(options.image)
      })
    }
  },

  onShow() {
    console.log('预览页面显示')
  },

  // 保存到相册
  async saveToAlbum() {
    if (!this.data.previewImage) {
      wx.showToast({
        title: '没有图片可保存',
        icon: 'none'
      })
      return
    }

    try {
      wx.showLoading({ title: '保存中...' })

      // 检查图片数据格式
      let filePath = this.data.previewImage

      // 如果是base64数据，需要先转换为临时文件
      if (this.data.previewImage.startsWith('data:image')) {
        console.log('检测到base64图片数据，转换为临时文件')
        const base64Data = this.data.previewImage.split(',')[1] // 移除data:image/png;base64,前缀
        const fs = wx.getFileSystemManager()
        const tempFilePath = `${wx.env.USER_DATA_PATH}/preview_${Date.now()}.png`

        fs.writeFileSync(tempFilePath, base64Data, 'base64')
        filePath = tempFilePath
        console.log('base64转换为临时文件:', tempFilePath)
      }

      // 使用隐私授权管理保存图片
      privacy.saveImageToPhotosAlbum(filePath, (success, error) => {
        wx.hideLoading()

        if (success) {
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          })
        } else {
          console.error('保存到相册失败:', error)

          if (error && error.errMsg && error.errMsg.includes('auth deny')) {
            wx.showModal({
              title: '权限提示',
              content: '需要相册权限才能保存图片，请在设置中开启',
              showCancel: false
            })
          } else {
            wx.showToast({
              title: '保存失败',
              icon: 'error'
            })
          }
        }
      })

    } catch (error) {
      wx.hideLoading()
      console.error('保存到相册异常:', error)
      wx.showToast({
        title: '保存失败',
        icon: 'error'
      })
    }
  },

  // 返回
  goBack() {
    const pages = getCurrentPages()
    if (pages.length > 1) {
      // 有上一页，可以正常返回
      wx.navigateBack({
        fail: (error) => {
          console.error('返回上一页失败:', error)
          // 如果返回失败，跳转到首页
          wx.switchTab({
            url: '/pages/home/home'
          })
        }
      })
    } else {
      // 没有上一页，跳转到首页
      wx.switchTab({
        url: '/pages/home/home',
        fail: (error) => {
          console.error('跳转到首页失败:', error)
          // 如果跳转失败，尝试重新启动应用
          wx.reLaunch({
            url: '/pages/home/home'
          })
        }
      })
    }
  }
})

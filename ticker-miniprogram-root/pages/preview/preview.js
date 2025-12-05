// pages/preview/preview.js
// 预览页面

const storage = require('../../utils/storage')

Page({
  data: {
    imageUrl: '',
    loading: true,
    error: null,
    canSave: false
  },

  onLoad(options) {
    console.log('预览页面加载', options)
    
    if (options.image) {
      this.setData({ 
        imageUrl: decodeURIComponent(options.image),
        loading: false 
      })
      this.checkSavePermission()
    } else {
      this.setData({ 
        loading: false, 
        error: '没有预览图片' 
      })
    }
  },

  onShow() {
    console.log('预览页面显示')
  },

  onReady() {
    console.log('预览页面准备完成')
  },

  // 检查保存权限
  checkSavePermission() {
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.writePhotosAlbum']) {
          this.setData({ canSave: true })
        } else {
          this.setData({ canSave: false })
        }
      }
    })
  },

  // 保存到相册
  async saveToAlbum() {
    if (!this.data.imageUrl) {
      wx.showToast({
        title: '没有可保存的图片',
        icon: 'none'
      })
      return
    }

    try {
      wx.showLoading({ title: '保存中...' })
      
      await wx.saveImageToPhotosAlbum({
        filePath: this.data.imageUrl
      })
      
      wx.hideLoading()
      wx.showToast({
        title: '保存成功',
        icon: 'success'
      })
    } catch (error) {
      wx.hideLoading()
      console.error('保存到相册失败:', error)
      
      if (error.errMsg.includes('auth deny')) {
        wx.showModal({
          title: '权限提示',
          content: '需要相册权限才能保存图片，是否前往设置开启？',
          success: (res) => {
            if (res.confirm) {
              wx.openSetting()
            }
          }
        })
      } else {
        wx.showToast({
          title: '保存失败',
          icon: 'error'
        })
      }
    }
  },

  // 分享图片
  shareImage() {
    wx.showActionSheet({
      itemList: ['保存到相册', '分享给朋友'],
      success: (res) => {
        if (res.tapIndex === 0) {
          this.saveToAlbum()
        } else if (res.tapIndex === 1) {
          this.shareToFriend()
        }
      }
    })
  },

  // 分享给朋友
  shareToFriend() {
    wx.showToast({
      title: '请使用右上角分享',
      icon: 'none'
    })
  },

  // 返回首页
  goBack() {
    wx.navigateBack()
  },

  // 重新制作
  remake() {
    wx.navigateBack()
  },

  // 图片加载完成
  onImageLoad() {
    console.log('图片加载完成')
  },

  // 图片加载失败
  onImageError() {
    console.error('图片加载失败')
    this.setData({ 
      error: '图片加载失败' 
    })
  },

  // 长按图片
  onImageLongPress() {
    wx.showActionSheet({
      itemList: ['保存到相册', '分享给朋友'],
      success: (res) => {
        if (res.tapIndex === 0) {
          this.saveToAlbum()
        } else if (res.tapIndex === 1) {
          this.shareToFriend()
        }
      }
    })
  }
})

// pages/index/index.js
// 首页 - 车票制作

const api = require('../../utils/api')
const storage = require('../../utils/storage')

Page({
  data: {
    // 页面状态
    loading: true,
    error: null,
    serverStatus: 'checking', // checking, online, offline
    
    // 样式相关
    styles: [],
    currentStyle: 'red15',
    
    // 表单数据 - 动态加载
    formData: {},
    formFields: [],
    fieldNames: '', // 字段名称列表，用于调试显示
    
    // 预览相关
    previewImage: null,
    previewLoading: false,
    
    // 草稿相关
    hasDraft: false
  },

  onLoad: function() {
    console.log('首页加载')
    this.initPage()
  },

  onShow: function() {
    console.log('首页显示')
    this.loadDraft()
  },

  onReady: function() {
    console.log('首页准备完成')
  },

  onHide: function() {
    console.log('首页隐藏')
    this.saveDraft()
  },

  onUnload: function() {
    console.log('首页卸载')
    this.saveDraft()
  },

  // 初始化页面
  initPage: function() {
    var that = this
    try {
      console.log('开始初始化页面')
      
      // 检测服务器状态并加载数据
      this.checkServerStatus().then(function() {
        if (that.data.serverStatus === 'online') {
          // 加载样式列表
          return that.loadStyles()
        } else {
          throw new Error('服务器离线')
        }
      }).then(function() {
        // 加载当前样式的模板信息
        return that.loadTemplateInfo(that.data.currentStyle)
      }).then(function() {
        // 初始化完成
        that.setData({ 
          loading: false, 
          error: null 
        })
        console.log('页面初始化完成')
      }).catch(function(error) {
        console.error('初始化失败:', error)
        that.setData({ 
          loading: false, 
          error: '初始化失败: ' + error.message 
        })
      })
      
    } catch (error) {
      console.error('初始化页面失败:', error)
      this.setData({ 
        loading: false, 
        error: '初始化失败，请检查网络连接' 
      })
    }
  },

  // 检测服务器状态
  checkServerStatus: function() {
    var that = this
    return new Promise(function(resolve, reject) {
      try {
        console.log('检测服务器状态...')
        that.setData({ serverStatus: 'checking' })
        
        api.healthCheck().then(function(result) {
          if (result.status === 'ok') {
            console.log('服务器在线')
            that.setData({ serverStatus: 'online' })
            resolve()
          } else {
            throw new Error('服务器响应异常')
          }
        }).catch(function(error) {
          console.log('服务器离线:', error)
          that.setData({ serverStatus: 'offline' })
          reject(error)
        })
        
      } catch (error) {
        console.log('服务器检测异常:', error)
        that.setData({ serverStatus: 'offline' })
        reject(error)
      }
    })
  },

  // 加载样式列表
  loadStyles: function() {
    var that = this
    return new Promise(function(resolve, reject) {
      console.log('加载样式列表...')
      
      api.getStyles().then(function(result) {
        if (result.success && result.styles) {
          console.log('样式列表加载成功:', result.styles)
          that.setData({ styles: result.styles })
          resolve()
        } else {
          throw new Error('样式列表加载失败')
        }
      }).catch(function(error) {
        console.error('加载样式列表失败:', error)
        // 使用默认样式列表
        that.setData({ styles: ['red15', 'blue15', 'red05_longride', 'red05_shortride', 'red1997'] })
        resolve() // 继续执行，使用默认样式
      })
    })
  },

  // 加载模板信息
  loadTemplateInfo: function(style) {
    var that = this
    return new Promise(function(resolve, reject) {
      console.log('加载模板信息:', style)
      
      // 使用新的API端点获取真实字段
      api.getTemplateFields(style).then(function(result) {
        if (result.success && result.fields) {
          console.log('模板字段加载成功')
          console.log('字段数量:', result.field_count)
          
          // 构建字段数据
          var realFields = {}
          var fieldList = result.fields
          
          for (var i = 0; i < fieldList.length; i++) {
            var field = fieldList[i]
            realFields[field.key] = { value: '', enabled: true }
          }
          
          console.log('字段列表:', fieldList.map(function(f) { return f.key }))
          
          // 计算字段名称列表
          var fieldNames = fieldList.map(function(f) { return f.key }).join(', ')
          
          that.setData({
            formData: realFields,
            formFields: fieldList,
            fieldNames: fieldNames
          })
          
          resolve()
        } else {
          throw new Error('模板字段加载失败: ' + (result.error || '未知错误'))
        }
      }).catch(function(error) {
        console.error('加载模板字段失败:', error)
        reject(error)
      })
    })
  },

  // 样式选择
  onStyleSelect: function(e) {
    var that = this
    var style = e.currentTarget.dataset.style
    if (style === this.data.currentStyle) return

    try {
      wx.showLoading({ title: '切换样式...' })
      
      this.setData({ currentStyle: style })
      
      // 加载新样式的模板信息
      this.loadTemplateInfo(style).then(function() {
        wx.hideLoading()
        wx.showToast({
          title: '样式切换成功',
          icon: 'success'
        })
        
        // 清除预览
        that.setData({ previewImage: null })
      }).catch(function(error) {
        wx.hideLoading()
        wx.showToast({
          title: '样式切换失败',
          icon: 'error'
        })
        console.error('切换样式失败:', error)
      })
      
    } catch (error) {
      wx.hideLoading()
      wx.showToast({
        title: '样式切换失败',
        icon: 'error'
      })
      console.error('切换样式异常:', error)
    }
  },

  // 表单输入
  onFormInput: function(e) {
    var field = e.currentTarget.dataset.field
    var value = e.detail.value
    var formData = this.data.formData
    formData[field].value = value
    this.setData({ formData: formData })
    
    // 自动保存草稿
    this.saveDraft()
  },

  // 字段启用/禁用
  onFieldToggle: function(e) {
    var field = e.currentTarget.dataset.field
    var formData = this.data.formData
    formData[field].enabled = !formData[field].enabled
    this.setData({ formData: formData })
    
    // 自动保存草稿
    this.saveDraft()
  },

  // 生成预览
  generatePreview: function() {
    var that = this
    if (this.data.serverStatus !== 'online') {
      wx.showModal({
        title: '服务器离线',
        content: '当前服务器离线，无法生成预览。请检查网络连接后重试。',
        showCancel: false
      })
      return
    }

    try {
      this.setData({ previewLoading: true })
      
      // 转换数据格式为API期望的格式
      var userData = {}
      var requiredFields = ['姓名', '车次号', '席位号', '出发站', '到达站']
      
      // 先添加必填字段
      for (var i = 0; i < requiredFields.length; i++) {
        var field = requiredFields[i]
        if (this.data.formData[field] && this.data.formData[field].enabled) {
          userData[field] = this.data.formData[field].value.trim() || '测试' + field
        } else {
          userData[field] = '测试' + field
        }
      }
      
      // 再添加其他有值的字段
      for (var key in this.data.formData) {
        if (!requiredFields.includes(key) && this.data.formData[key].enabled && this.data.formData[key].value.trim()) {
          userData[key] = this.data.formData[key].value.trim()
        }
      }
      
      console.log('发送的用户数据:', userData)
      
      var requestData = {
        style: this.data.currentStyle,
        user_data: userData,
        format: 'base64'
      }
      
      api.generateTicket(requestData).then(function(result) {
        if (result.success) {
          that.setData({ 
            previewImage: result.data.image_base64,
            previewLoading: false 
          })
          
          wx.showToast({
            title: '预览生成成功',
            icon: 'success'
          })
        } else {
          throw new Error(result.error || '生成预览失败')
        }
      }).catch(function(error) {
        console.error('生成预览失败:', error)
        that.setData({ previewLoading: false })
        wx.showToast({
          title: '预览生成失败',
          icon: 'error'
        })
      })
      
    } catch (error) {
      console.error('生成预览异常:', error)
      this.setData({ previewLoading: false })
      wx.showToast({
        title: '预览生成失败',
        icon: 'error'
      })
    }
  },

  // 保存到相册
  saveToAlbum: function() {
    var that = this
    if (!this.data.previewImage) {
      wx.showToast({
        title: '请先生成预览',
        icon: 'none'
      })
      return
    }

    try {
      wx.showLoading({ title: '保存中...' })
      
      // 保存到相册
      wx.saveImageToPhotosAlbum({
        filePath: this.data.previewImage,
        success: function() {
          wx.hideLoading()
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          })
          
          // 添加到历史记录
          that.addToHistory()
        },
        fail: function(error) {
          wx.hideLoading()
          console.error('保存到相册失败:', error)
          
          if (error.errMsg && error.errMsg.includes('auth deny')) {
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

  // 添加到历史记录
  addToHistory: function() {
    var historyItem = {
      style: this.data.currentStyle,
      data: this.data.formData,
      preview: this.data.previewImage,
      timestamp: new Date().toISOString()
    }
    
    var app = getApp()
    if (app && app.addHistory) {
      app.addHistory(historyItem)
    }
  },

  // 保存草稿
  saveDraft: function() {
    var draftData = {
      style: this.data.currentStyle,
      formData: this.data.formData,
      timestamp: new Date().toISOString()
    }
    
    try {
      storage.saveDraft(draftData)
      this.setData({ hasDraft: true })
    } catch (error) {
      console.error('保存草稿失败:', error)
    }
  },

  // 加载草稿
  loadDraft: function() {
    try {
      var draft = storage.getDraft()
      if (draft && draft.style === this.data.currentStyle) {
        this.setData({ 
          formData: draft.formData,
          hasDraft: true 
        })
        
        wx.showToast({
          title: '已恢复草稿',
          icon: 'success'
        })
      }
    } catch (error) {
      console.error('加载草稿失败:', error)
    }
  },

  // 清除草稿
  clearDraft: function() {
    try {
      storage.clearDraft()
      this.setData({ hasDraft: false })
      
      // 重置表单
      var formData = {}
      for (var key in this.data.formData) {
        formData[key] = { value: '', enabled: true }
      }
      this.setData({ formData: formData })
      
      wx.showToast({
        title: '草稿已清除',
        icon: 'success'
      })
    } catch (error) {
      console.error('清除草稿失败:', error)
    }
  },

  // 重置表单
  resetForm: function() {
    var that = this
    wx.showModal({
      title: '确认重置',
      content: '确定要重置所有输入内容吗？',
      success: function(res) {
        if (res.confirm) {
          var formData = {}
          for (var key in that.data.formData) {
            formData[key] = { value: '', enabled: true }
          }
          that.setData({ formData: formData })
          
          wx.showToast({
            title: '已重置',
            icon: 'success'
          })
        }
      }
    })
  },

  // 查看预览
  viewPreview: function() {
    if (!this.data.previewImage) {
      wx.showToast({
        title: '请先生成预览',
        icon: 'none'
      })
      return
    }
    
    wx.navigateTo({
      url: '/pages/preview/preview?image=' + encodeURIComponent(this.data.previewImage)
    })
  },

  // 重新检测服务器
  retryServerCheck: function() {
    this.initPage()
  },

  // 错误重试
  retry: function() {
    this.initPage()
  }
})
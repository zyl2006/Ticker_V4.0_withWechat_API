// pages/make/make.js
// 制作页面 - 车票制作和实时预览

const api = require('../../utils/api')
const storage = require('../../utils/storage')
const privacy = require('../../utils/privacy')

Page({
  data: {
    // 页面状态
    loading: true,
    error: null,
    
    // 样式相关
    styles: [],
    currentStyle: 'red15',
    styleInfo: null,
    
    // 表单数据
    formData: {},
    formFields: [],
    
    // 预览相关
    previewImage: null,
    previewLoading: false,
    autoPreview: true,
    
    // 服务器状态
    serverStatus: 'checking',
    
    // 草稿相关
    hasDraft: false
  },

  onLoad(options) {
    console.log('制作页面加载', options)
    // 如果从首页传入了样式参数
    if (options.style) {
      this.setData({ currentStyle: options.style })
    }
    this.initPage()
  },

  onShow() {
    console.log('制作页面显示')
    this.loadDraft()
    this.checkServerStatus()
    this.loadHistoryData()
  },

  onReady() {
    console.log('制作页面准备完成')
  },

  onHide() {
    console.log('制作页面隐藏')
    this.saveDraft()
  },

  onUnload() {
    console.log('制作页面卸载')
    this.saveDraft()
  },

  // 初始化页面
  async initPage() {
    try {
      this.setData({ loading: true, error: null })
      
      // 获取样式列表
      await this.loadStyles()
      
      // 加载当前样式信息
      await this.loadStyleInfo(this.data.currentStyle)
      
      this.setData({ loading: false })
    } catch (error) {
      console.error('初始化页面失败:', error)
      this.setData({ 
        loading: false, 
        error: '初始化失败，请检查网络连接' 
      })
    }
  },

  // 检查服务器状态
  async checkServerStatus() {
    try {
      const result = await api.checkServer()
      this.setData({ 
        serverStatus: result.success ? 'online' : 'offline' 
      })
    } catch (error) {
      console.error('检查服务器状态失败:', error)
      this.setData({ serverStatus: 'offline' })
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

  // 加载样式信息
  async loadStyleInfo(style) {
    try {
      const result = await api.getTemplateInfo(style)
      if (result.success) {
        const formFields = this.parseFormFields(result.fields)
        this.setData({ 
          currentStyle: style,
          styleInfo: result,
          formFields: formFields,
          formData: this.initFormData(formFields)
        })
        
        // 如果开启了自动预览，立即生成预览
        if (this.data.autoPreview) {
          this.generatePreview()
        }
      } else {
        throw new Error(result.error || '获取样式信息失败')
      }
    } catch (error) {
      console.error('加载样式信息失败:', error)
      // 使用默认字段
      const defaultFields = this.getDefaultFields()
      this.setData({ 
        currentStyle: style,
        styleInfo: { fields: {} },
        formFields: defaultFields,
        formData: this.initFormData(defaultFields)
      })
    }
  },

  // 获取默认字段
  getDefaultFields() {
    const defaultFields = [
      { key: '上票号', label: '上票号', type: 'text', required: false, description: '请输入上票号', value: '', enabled: true },
      { key: '检票口', label: '检票口', type: 'text', required: false, description: '请输入检票口', value: '', enabled: true },
      { key: '出发站', label: '出发站', type: 'text', required: true, description: '请输入出发站', value: '', enabled: true },
      { key: '到达站', label: '到达站', type: 'text', required: true, description: '请输入到达站', value: '', enabled: true },
      { key: '车次', label: '车次', type: 'text', required: true, description: '请输入车次', value: '', enabled: true },
      { key: '日期', label: '日期', type: 'text', required: true, description: '请输入日期', value: '', enabled: true },
      { key: '时间', label: '时间', type: 'text', required: true, description: '请输入时间', value: '', enabled: true },
      { key: '座位号', label: '座位号', type: 'text', required: false, description: '请输入座位号', value: '', enabled: true },
      { key: '票价', label: '票价', type: 'text', required: false, description: '请输入票价', value: '', enabled: true }
    ]
    return defaultFields
  },

  // 解析表单字段
  parseFormFields(fields) {
    const formFields = []
    const fieldMap = new Map()
    
    // 遍历所有字段，提取segments中的字段名
    for (const [key, config] of Object.entries(fields)) {
      if (config.segments && Array.isArray(config.segments)) {
        config.segments.forEach(segment => {
          if (segment.text && segment.text.includes('{') && segment.text.includes('}')) {
            // 提取字段名，如 {出发站} -> 出发站
            const fieldName = segment.text.match(/\{([^}]+)\}/)?.[1]
            if (fieldName && !fieldMap.has(fieldName)) {
              fieldMap.set(fieldName, {
                key: fieldName,
                label: fieldName,
                type: 'text',
                required: false,
                description: `请输入${fieldName}`,
                value: '',
                enabled: true
              })
            }
          }
        })
      }
    }
    
    // 转换为数组
    formFields.push(...fieldMap.values())
    
    // 如果没有找到字段，使用默认字段
    if (formFields.length === 0) {
      const defaultFields = this.getDefaultFields()
      formFields.push(...defaultFields)
    }
    
    return formFields
  },

  // 初始化表单数据
  initFormData(formFields) {
    const formData = {}
    formFields.forEach(field => {
      formData[field.key] = {
        value: '',
        enabled: field.enabled
      }
    })
    return formData
  },

  // 样式选择
  async onStyleSelect(e) {
    const style = e.currentTarget.dataset.style
    if (style === this.data.currentStyle) return

    try {
      wx.showLoading({ title: '切换样式...' })
      await this.loadStyleInfo(style)
      wx.hideLoading()
      
      wx.showToast({
        title: '样式切换成功',
        icon: 'success'
      })
    } catch (error) {
      wx.hideLoading()
      wx.showToast({
        title: '样式切换失败',
        icon: 'error'
      })
    }
  },

  // 表单输入
  onFormInput(e) {
    const field = e.currentTarget.dataset.field
    const value = e.detail.value  // 从e.detail.value获取用户输入的值
    const formData = { ...this.data.formData }
    formData[field].value = value
    this.setData({ formData })
    
    console.log('表单输入:', { field, value, formData })
    
    // 自动保存草稿
    this.saveDraft()
    
    // 如果开启了自动预览，延迟生成预览
    if (this.data.autoPreview) {
      this.debouncePreview()
    }
  },

  // 防抖预览
  debouncePreview() {
    if (this.previewTimer) {
      clearTimeout(this.previewTimer)
    }
    this.previewTimer = setTimeout(() => {
      this.generatePreview()
    }, 1000) // 1秒后生成预览
  },

  // 字段启用/禁用
  onFieldToggle(e) {
    const field = e.currentTarget.dataset.field
    const formData = { ...this.data.formData }
    formData[field].enabled = !formData[field].enabled
    this.setData({ formData })
    
    // 自动保存草稿
    this.saveDraft()
    
    // 如果开启了自动预览，立即生成预览
    if (this.data.autoPreview) {
      this.generatePreview()
    }
  },

  // 生成预览
  async generatePreview() {
    try {
      this.setData({ previewLoading: true })
      
      // 只发送用户填写的字段，未填写的字段不发送或发送空值
      const userData = {}
      Object.keys(this.data.formData).forEach(key => {
        const fieldData = this.data.formData[key]
        if (fieldData.enabled && fieldData.value && fieldData.value.trim() !== '') {
          userData[key] = fieldData.value.trim()
        } else {
          userData[key] = '' // 未填写或禁用的字段返回空值
        }
      })
      
      const requestData = {
        style: this.data.currentStyle,
        user_data: userData,
        format: 'base64'
      }
      
      console.log('发送生成请求:', requestData)
      
      const result = await api.generateTicket(requestData)
      console.log('生成结果:', result)
      console.log('结果类型:', typeof result)
      console.log('结果success:', result.success)
      
      if (result && result.success) {
        // 优化性能：不直接存储base64数据，而是存储临时文件路径
        const base64Data = result.data.image_base64
        
        // 将base64转换为临时文件
        const fs = wx.getFileSystemManager()
        const tempFilePath = `${wx.env.USER_DATA_PATH}/temp_preview_${Date.now()}.png`
        
        try {
          fs.writeFileSync(tempFilePath, base64Data, 'base64')
          
          this.setData({ 
            previewImage: tempFilePath,  // 存储文件路径而不是base64数据
            previewLoading: false 
          })
          
          console.log('预览图片已保存到临时文件:', tempFilePath)
          
          wx.showToast({
            title: '预览生成成功',
            icon: 'success'
          })
        } catch (fileError) {
          console.error('保存临时文件失败:', fileError)
          // 如果文件保存失败，回退到base64方式
          this.setData({ 
            previewImage: `data:image/png;base64,${base64Data}`,
            previewLoading: false 
          })
          
          wx.showToast({
            title: '预览生成成功',
            icon: 'success'
          })
        }
      } else {
        console.error('生成失败，结果:', result)
        throw new Error(result?.error || '生成预览失败')
      }
    } catch (error) {
      console.error('生成预览失败:', error)
      this.setData({ previewLoading: false })
      
      // 显示详细错误信息
      wx.showModal({
        title: '预览生成失败',
        content: `错误信息: ${error.message || error}`,
        showCancel: false
      })
    }
  },

  // 保存到相册
  async saveToAlbum() {
    if (!this.data.previewImage) {
      wx.showToast({
        title: '请先生成预览',
        icon: 'none'
      })
      return
    }

    try {
      wx.showLoading({ title: '保存中...' })
      
      // 使用隐私授权管理保存图片
      privacy.saveImageToPhotosAlbum(this.data.previewImage, (success, error) => {
        wx.hideLoading()
        
        if (success) {
          wx.showToast({
            title: '保存成功',
            icon: 'success'
          })
          
          // 添加到历史记录
          this.addToHistory()
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

  // 添加到历史记录
  async addToHistory() {
    try {
      const app = getApp()
      const userId = app.getUserId()

      if (!userId) {
        console.log('用户未登录，只保存到本地缓存')
        // 用户未登录，只保存到本地作为缓存
        this.saveToLocalHistory()
        return
      }

      // 将预览图片转换为base64格式
      const fs = wx.getFileSystemManager()
      const base64Data = fs.readFileSync(this.data.previewImage, 'base64')

      // 构造完整的历史记录数据
      const historyItem = {
        style: this.data.currentStyle,
        data: this.data.formData,
        preview_base64: base64Data,
        timestamp: new Date().toISOString(),
        // 生成唯一ID
        id: Date.now().toString() + '_' + Math.random().toString(36).substr(2, 9)
      }

      console.log('准备上传历史记录到服务器:', historyItem.id)

      // 上传到服务器
      const result = await api.uploadHistory(userId, [historyItem])

      if (result.success) {
        console.log('历史记录上传成功')

        // 同时保存到本地缓存（用于离线查看）
        app.addHistory(historyItem)

        wx.showToast({
          title: '保存成功',
          icon: 'success'
        })
      } else {
        throw new Error(result.error || '上传失败')
      }

    } catch (error) {
      console.error('添加到历史记录失败:', error)

      // 服务器上传失败，回退到本地保存
      console.log('服务器上传失败，回退到本地保存')
      this.saveToLocalHistory()

      wx.showToast({
        title: '已保存到本地',
        icon: 'none'
      })
    }
  },

  // 保存到本地历史记录（作为缓存或离线使用）
  saveToLocalHistory() {
    try {
      const app = getApp()

      // 将预览图片转换为base64格式存储
      const fs = wx.getFileSystemManager()
      const base64Data = fs.readFileSync(this.data.previewImage, 'base64')

      const historyItem = {
        id: Date.now().toString() + '_local',
        style: this.data.currentStyle,
        data: this.data.formData,
        preview: base64Data, // 本地使用base64
        timestamp: new Date().toISOString()
      }

      app.addHistory(historyItem)
      console.log('已保存到本地历史记录缓存')
    } catch (error) {
      console.error('保存到本地历史记录失败:', error)
    }
  },

  // 保存草稿
  saveDraft() {
    const draftData = {
      style: this.data.currentStyle,
      formData: this.data.formData,
      timestamp: new Date().toISOString()
    }
    
    storage.saveDraft(draftData)
    this.setData({ hasDraft: true })
  },

  // 加载草稿
  loadDraft() {
    const draft = storage.getDraft()
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
  },

  // 清除草稿
  clearDraft() {
    storage.clearDraft()
    this.setData({ hasDraft: false })
    
    // 重置表单
    const formData = this.initFormData(this.data.formFields)
    this.setData({ formData })
    
    wx.showToast({
      title: '草稿已清除',
      icon: 'success'
    })
  },

  // 重置表单
  resetForm() {
    wx.showModal({
      title: '确认重置',
      content: '确定要重置所有输入内容吗？',
      success: (res) => {
        if (res.confirm) {
          const formData = this.initFormData(this.data.formFields)
          this.setData({ formData })
          
          wx.showToast({
            title: '已重置',
            icon: 'success'
          })
        }
      }
    })
  },

  // 查看预览
  viewPreview() {
    if (!this.data.previewImage) {
      wx.showToast({
        title: '请先生成预览',
        icon: 'none'
      })
      return
    }
    
    wx.navigateTo({
      url: `/pages/preview/preview?image=${encodeURIComponent(this.data.previewImage)}`
    })
  },

  // 切换自动预览
  toggleAutoPreview() {
    this.setData({ autoPreview: !this.data.autoPreview })
    
    wx.showToast({
      title: this.data.autoPreview ? '已开启自动预览' : '已关闭自动预览',
      icon: 'success'
    })
  },

  // 加载历史数据
  loadHistoryData() {
    const app = getApp()
    const historyData = app.globalData.loadHistoryData
    
    if (historyData) {
      // 加载历史数据到表单
      this.setData({ formData: historyData })
      
      // 清除加载标记
      app.globalData.loadHistoryData = null
      
      // 如果开启了自动预览，立即生成预览
      if (this.data.autoPreview) {
        this.generatePreview()
      }
      
      wx.showToast({
        title: '已加载历史数据',
        icon: 'success'
      })
    }
  },

  // 错误重试
  retry() {
    this.initPage()
  }
})
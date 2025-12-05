// pages/history/history.js
// 历史结果页面 - 查看历史生成的车票

const storage = require('../../utils/storage')
const api = require('../../utils/api')

Page({
  data: {
    // 页面状态
    loading: false,
    error: null,

    // 历史数据
    history: [],
    filteredHistory: [],
    totalCount: 0,

    // 筛选相关
    filterStyle: 'all',
    filterDeparture: '',
    filterArrival: '',
    styles: [],
    departureStations: [],
    arrivalStations: [],

    // 排序相关
    sortBy: 'time_desc', // time_desc, time_asc
    showFilters: false
  },

  onLoad() {
    console.log('历史结果页面加载')
    this.initPage()
  },

  onShow() {
    console.log('历史结果页面显示')
    this.loadHistory()
  },

  onReady() {
    console.log('历史结果页面准备完成')
  },

  onPullDownRefresh() {
    console.log('下拉刷新')
    this.loadHistory()
    wx.stopPullDownRefresh()
  },

  // 初始化页面
  initPage() {
    this.loadHistory()
  },

  // 加载历史记录
  async loadHistory() {
    try {
      const app = getApp()
      const userId = app.getUserId()

      let history = []

      if (userId) {
        // 用户已登录，优先从服务器获取
        try {
          console.log('从服务器获取历史记录，用户ID:', userId)
          const result = await api.getHistory(userId)

          if (result.success && result.history) {
            history = result.history
            console.log('从服务器获取历史记录成功:', history.length, '条')

            // 保存到本地缓存
            app.globalData.history = history
            wx.setStorageSync('ticker_history', history)
          } else {
            throw new Error('服务器返回数据格式错误')
          }
        } catch (serverError) {
          console.error('从服务器获取历史记录失败:', serverError)
          console.log('回退到本地缓存')

          // 从服务器获取失败，使用本地缓存
          history = app.getHistory()
        }
      } else {
        // 用户未登录，只使用本地缓存
        console.log('用户未登录，使用本地历史记录缓存')
        history = app.getHistory()
      }

      // 处理历史数据，提取车票信息
      const processedHistory = history.map(item => ({
        ...item,
        departureStation: this.getFormValue(item.data, '出发站') || '',
        arrivalStation: this.getFormValue(item.data, '到达站') || '',
        ticketNumber: this.getFormValue(item.data, '车票号') || '',
        passengerName: this.getFormValue(item.data, '乘客姓名') || '',
        trainNumber: this.getFormValue(item.data, '车次') || '',
        seatInfo: this.getFormValue(item.data, '座位信息') || '',
        date: this.getFormValue(item.data, '日期') || '',
        // 确保预览图片字段统一
        preview: item.preview || item.preview_base64 || ''
      }))

      // 获取所有样式
      const styles = [...new Set(processedHistory.map(item => item.style))]

      // 获取所有出发站和到达站（去重）
      const departureStations = [...new Set(processedHistory.map(item => item.departureStation).filter(s => s))]
      const arrivalStations = [...new Set(processedHistory.map(item => item.arrivalStation).filter(s => s))]

      this.setData({
        history: processedHistory,
        totalCount: processedHistory.length,
        styles: styles,
        departureStations: departureStations,
        arrivalStations: arrivalStations
      })

      // 应用筛选和排序
      this.applyFiltersAndSort()
    } catch (error) {
      console.error('加载历史记录失败:', error)
      this.setData({
        error: '加载历史记录失败'
      })
    }
  },

  // 从表单数据中获取字段值
  getFormValue(formData, fieldKey) {
    if (!formData || !formData[fieldKey]) return ''
    return formData[fieldKey].value || ''
  },

  // 应用筛选和排序
  applyFiltersAndSort() {
    let filteredData = [...this.data.history]

    // 应用筛选条件
    if (this.data.filterStyle !== 'all') {
      filteredData = filteredData.filter(item => item.style === this.data.filterStyle)
    }

    if (this.data.filterDeparture) {
      filteredData = filteredData.filter(item =>
        item.departureStation.toLowerCase().includes(this.data.filterDeparture.toLowerCase())
      )
    }

    if (this.data.filterArrival) {
      filteredData = filteredData.filter(item =>
        item.arrivalStation.toLowerCase().includes(this.data.filterArrival.toLowerCase())
      )
    }

    // 应用排序
    filteredData.sort((a, b) => {
      const dateA = new Date(a.timestamp)
      const dateB = new Date(b.timestamp)

      if (this.data.sortBy === 'time_desc') {
        return dateB - dateA // 最新在前
      } else if (this.data.sortBy === 'time_asc') {
        return dateA - dateB // 最旧在前
      }
      return 0
    })

    this.setData({
      filteredHistory: filteredData
    })
  },

  // 筛选样式
  onStyleFilter(e) {
    const style = e.currentTarget.dataset.style
    this.setData({ filterStyle: style })
    this.applyFiltersAndSort()
  },

  // 筛选出发站
  onDepartureFilter(e) {
    const departure = e.detail.value
    this.setData({ filterDeparture: departure })
    this.applyFiltersAndSort()
  },

  // 筛选到达站
  onArrivalFilter(e) {
    const arrival = e.detail.value
    this.setData({ filterArrival: arrival })
    this.applyFiltersAndSort()
  },

  // 切换排序方式
  onSortChange(e) {
    const sortBy = e.currentTarget.dataset.sort
    this.setData({ sortBy: sortBy })
    this.applyFiltersAndSort()
  },

  // 切换筛选面板显示
  toggleFilters() {
    this.setData({
      showFilters: !this.data.showFilters
    })
  },

  // 清除所有筛选条件
  clearFilters() {
    this.setData({
      filterStyle: 'all',
      filterDeparture: '',
      filterArrival: '',
      sortBy: 'time_desc'
    })
    this.applyFiltersAndSort()
  },

  // 查看详情
  viewDetail(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.filteredHistory[index]

    if (!item) return

    // 确保图片数据格式正确
    let imageData = item.preview

    // 如果是base64数据但没有data:image前缀，添加前缀
    if (imageData && !imageData.startsWith('data:image') && imageData.length > 100) {
      imageData = `data:image/png;base64,${imageData}`
    }

    wx.navigateTo({
      url: `/pages/preview/preview?image=${encodeURIComponent(imageData)}&history=true&index=${index}`
    })
  },

  // 重新制作
  remake(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.filteredHistory[index]

    if (!item) return

    // 跳转到制作页面并传递数据
    wx.switchTab({
      url: `/pages/make/make?style=${item.style}&loadData=true`
    })

    // 通知制作页面加载数据
    const app = getApp()
    app.globalData.loadHistoryData = item.data
  },

  // 删除记录
  deleteItem(e) {
    const index = e.currentTarget.dataset.index
    const item = this.data.filteredHistory[index]

    if (!item) return

    wx.showModal({
      title: '确认删除',
      content: '确定要删除这条记录吗？',
      success: (res) => {
        if (res.confirm) {
          this.deleteHistoryItem(item.id)
        }
      }
    })
  },

  // 删除历史记录项
  async deleteHistoryItem(id) {
    try {
      const app = getApp()
      const userId = app.getUserId()

      if (userId) {
        // 用户已登录，先从服务器删除
        try {
          console.log('从服务器删除历史记录:', userId, id)
          const result = await api.deleteHistory(userId, id)

          if (result.success) {
            console.log('服务器删除成功')
          } else {
            throw new Error(result.error || '服务器删除失败')
          }
        } catch (serverError) {
          console.error('服务器删除失败:', serverError)
          wx.showToast({
            title: '服务器删除失败，已删除本地缓存',
            icon: 'none'
          })
        }
      }

      // 同时更新本地数据
      const history = app.getHistory()
      const newHistory = history.filter(item => item.id !== id)

      // 更新本地存储
      wx.setStorageSync('ticker_history', newHistory)
      app.globalData.history = newHistory

      // 重新加载数据
      this.loadHistory()

      wx.showToast({
        title: '删除成功',
        icon: 'success'
      })
    } catch (error) {
      console.error('删除记录失败:', error)
      wx.showToast({
        title: '删除失败',
        icon: 'error'
      })
    }
  },

  // 清空所有记录
  clearAllHistory() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有历史记录吗？此操作不可恢复！',
      success: (res) => {
        if (res.confirm) {
          this.doClearAllHistory()
        }
      }
    })
  },

  // 执行清空所有历史记录
  async doClearAllHistory() {
    try {
      const app = getApp()
      const userId = app.getUserId()

      if (userId && this.data.history.length > 0) {
        // 用户已登录，删除服务器上的所有历史记录
        try {
          const historyIds = this.data.history.map(item => item.id)
          console.log('批量删除服务器历史记录:', historyIds.length, '条')

          const result = await api.batchDeleteHistory(userId, historyIds)

          if (result.success) {
            console.log('服务器批量删除成功')
          } else {
            console.error('服务器批量删除失败:', result.error)
            wx.showToast({
              title: '服务器删除失败，仅清除本地缓存',
              icon: 'none'
            })
          }
        } catch (serverError) {
          console.error('服务器批量删除出错:', serverError)
          wx.showToast({
            title: '服务器删除失败，仅清除本地缓存',
            icon: 'none'
          })
        }
      }

      // 清除本地数据
      app.clearHistory()

      this.setData({
        history: [],
        filteredHistory: [],
        totalCount: 0,
        styles: [],
        departureStations: [],
        arrivalStations: []
      })

      wx.showToast({
        title: '清空成功',
        icon: 'success'
      })
    } catch (error) {
      console.error('清空历史记录失败:', error)
      wx.showToast({
        title: '清空失败',
        icon: 'error'
      })
    }
  },

  // 导出记录
  exportHistory() {
    if (this.data.filteredHistory.length === 0) {
      wx.showToast({
        title: '没有记录可导出',
        icon: 'none'
      })
      return
    }
    
    wx.showModal({
      title: '导出记录',
      content: '是否将历史记录导出为JSON文件？',
      success: (res) => {
        if (res.confirm) {
          this.downloadHistory()
        }
      }
    })
  },

  // 下载历史记录
  downloadHistory() {
    try {
      const historyData = JSON.stringify(this.data.filteredHistory, null, 2)
      const fileName = `ticker_history_${new Date().toISOString().split('T')[0]}.json`
      
      // 创建临时文件
      const fs = wx.getFileSystemManager()
      const filePath = `${wx.env.USER_DATA_PATH}/${fileName}`
      
      fs.writeFileSync(filePath, historyData, 'utf8')
      
      // 保存到相册或分享
      wx.showActionSheet({
        itemList: ['保存到文件', '分享给朋友'],
        success: (res) => {
          if (res.tapIndex === 0) {
            wx.showToast({
              title: '文件已保存',
              icon: 'success'
            })
          } else if (res.tapIndex === 1) {
            wx.showToast({
              title: '请使用文件管理器分享',
              icon: 'none'
            })
          }
        }
      })
    } catch (error) {
      console.error('导出失败:', error)
      wx.showToast({
        title: '导出失败',
        icon: 'error'
      })
    }
  },

  // 开始制作
  startMaking() {
    wx.switchTab({
      url: '/pages/make/make'
    })
  },

  // 格式化日期
  formatDate(timestamp) {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date
    
    if (diff < 60000) { // 1分钟内
      return '刚刚'
    } else if (diff < 3600000) { // 1小时内
      return `${Math.floor(diff / 60000)}分钟前`
    } else if (diff < 86400000) { // 1天内
      return `${Math.floor(diff / 3600000)}小时前`
    } else if (diff < 604800000) { // 1周内
      return `${Math.floor(diff / 86400000)}天前`
    } else {
      return date.toLocaleDateString()
    }
  }
})
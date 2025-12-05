// utils/api.js
// API调用封装

const app = getApp()

class ApiService {
  constructor() {
    this.baseUrl = app.globalData.apiBaseUrl
    this.timeout = 10000
  }

  // 通用请求方法
  request(options) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.baseUrl + options.url,
        method: options.method || 'GET',
        data: options.data || {},
        header: {
          'Content-Type': 'application/json',
          ...options.header
        },
        timeout: this.timeout,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            reject(new Error(`请求失败: ${res.statusCode}`))
          }
        },
        fail: (error) => {
          console.error('API请求失败:', error)
          reject(error)
        }
      })
    })
  }

  // 健康检查
  healthCheck() {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/health',
        method: 'GET'
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('健康检查失败:', error)
        reject(error)
      })
    })
  }

  // 获取样式列表
  getStyles() {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/styles',
        method: 'GET'
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('获取样式列表失败:', error)
        reject(error)
      })
    })
  }

  // 获取模板字段列表
  getTemplateFields(style) {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/template/' + style + '/fields',
        method: 'GET'
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('获取模板字段失败:', error)
        reject(error)
      })
    })
  }

  // 获取模板信息
  getTemplateInfo(style) {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/template/' + style,
        method: 'GET'
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('获取模板信息失败:', error)
        reject(error)
      })
    })
  }

  // 生成车票
  generateTicket(data) {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/generate',
        method: 'POST',
        data: data
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('生成车票失败:', error)
        reject(error)
      })
    })
  }

  // 批量生成车票
  batchGenerateTickets(data) {
    var that = this
    return new Promise(function(resolve, reject) {
      that.request({
        url: '/api/batch_generate',
        method: 'POST',
        data: data
      }).then(function(result) {
        resolve(result)
      }).catch(function(error) {
        console.error('批量生成车票失败:', error)
        reject(error)
      })
    })
  }
}

// 创建API服务实例
const apiService = new ApiService()

// 导出API方法
module.exports = {
  // 基础方法
  request: (options) => apiService.request(options),
  
  // 业务方法
  healthCheck: () => apiService.healthCheck(),
  getStyles: () => apiService.getStyles(),
  getTemplateInfo: (style) => apiService.getTemplateInfo(style),
  getTemplateFields: (style) => apiService.getTemplateFields(style),
  generateTicket: (data) => apiService.generateTicket(data),
  batchGenerateTickets: (data) => apiService.batchGenerateTickets(data),
  
  // 工具方法
  setBaseUrl: (url) => {
    apiService.baseUrl = url
    app.globalData.apiBaseUrl = url
  },
  
  getBaseUrl: () => apiService.baseUrl
}

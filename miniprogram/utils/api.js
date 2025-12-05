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
      // 检查是否在多端插件模式下
      const isPluginMode = wx.getSystemInfoSync().platform === 'devtools' && 
                          wx.getSystemInfoSync().environment === 'wxext'
      
      console.log('请求环境信息:', {
        platform: wx.getSystemInfoSync().platform,
        environment: wx.getSystemInfoSync().environment,
        isPluginMode: isPluginMode
      })
      
      // 构建请求数据
      let requestData = options.data || {}
      
      // 如果是POST请求且数据是对象，确保正确序列化
      if (options.method === 'POST' && typeof requestData === 'object') {
        // 对于多端插件模式，可能需要特殊处理
        if (isPluginMode) {
          // 确保数据格式正确
          requestData = JSON.parse(JSON.stringify(requestData))
        }
      }
      
      console.log('发送请求:', {
        url: this.baseUrl + options.url,
        method: options.method || 'GET',
        data: requestData,
        isPluginMode: isPluginMode
      })
      
      wx.request({
        url: this.baseUrl + options.url,
        method: options.method || 'GET',
        data: requestData,
        header: {
          'content-type': 'application/json',
          'Accept': 'application/json',
          ...options.header
        },
        timeout: this.timeout,
        success: (res) => {
          console.log('API响应:', res)
          console.log('响应状态码:', res.statusCode)
          console.log('响应数据:', res.data)
          console.log('响应头:', res.header)
          
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            console.error('请求失败，状态码:', res.statusCode)
            console.error('错误响应:', res.data)
            console.error('响应头:', res.header)
            
            // 提供更详细的错误信息
            let errorMessage = `请求失败: ${res.statusCode}`
            if (res.data && res.data.error) {
              errorMessage += ` - ${res.data.error}`
            } else if (res.data && typeof res.data === 'string') {
              errorMessage += ` - ${res.data}`
            }
            
            reject(new Error(errorMessage))
          }
        },
        fail: (error) => {
          console.error('API请求失败:', error)
          console.error('错误详情:', {
            errMsg: error.errMsg,
            errno: error.errno,
            errcode: error.errcode
          })
          reject(error)
        }
      })
    })
  }

  // 健康检查
  async healthCheck() {
    try {
      const result = await this.request({
        url: '/api/health',
        method: 'GET'
      })
      return result
    } catch (error) {
      console.error('健康检查失败:', error)
      throw error
    }
  }

  // 检查服务器状态
  async checkServer() {
    try {
      const result = await this.request({
        url: '/api/health',
        method: 'GET'
      })
      return { success: true, data: result }
    } catch (error) {
      console.error('检查服务器状态失败:', error)
      return { success: false, error: error.message }
    }
  }

  // 获取样式列表
  async getStyles() {
    try {
      const result = await this.request({
        url: '/api/styles',
        method: 'GET'
      })
      return result
    } catch (error) {
      console.error('获取样式列表失败:', error)
      throw error
    }
  }

  // 获取模板信息
  async getTemplateInfo(style) {
    try {
      const result = await this.request({
        url: `/api/template/${style}`,
        method: 'GET'
      })
      return result
    } catch (error) {
      console.error('获取模板信息失败:', error)
      throw error
    }
  }

  // 生成车票
  async generateTicket(data) {
    try {
      const result = await this.request({
        url: '/api/generate',
        method: 'POST',
        data: data
      })
      return result
    } catch (error) {
      console.error('生成车票失败:', error)
      throw error
    }
  }

  // 批量生成车票
  async batchGenerateTickets(data) {
    try {
      const result = await this.request({
        url: '/api/batch_generate',
        method: 'POST',
        data: data
      })
      return result
    } catch (error) {
      console.error('批量生成车票失败:', error)
      throw error
    }
  }

  // 用户注册
  async registerUser(userInfo) {
    try {
      const result = await this.request({
        url: '/api/user/register',
        method: 'POST',
        data: userInfo
      })
      return result
    } catch (error) {
      console.error('用户注册失败:', error)
      throw error
    }
  }

  // 用户登录
  async loginUser(userInfo) {
    try {
      const result = await this.request({
        url: '/api/user/login',
        method: 'POST',
        data: userInfo
      })
      return result
    } catch (error) {
      console.error('用户登录失败:', error)
      throw error
    }
  }

  // 获取用户信息
  async getUserInfo(userId) {
    try {
      const result = await this.request({
        url: `/api/user/${userId}`,
        method: 'GET'
      })
      return result
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  // 上传历史记录
  async uploadHistory(userId, historyData) {
    try {
      const result = await this.request({
        url: '/api/history/upload',
        method: 'POST',
        data: {
          user_id: userId,
          history: historyData
        }
      })
      return result
    } catch (error) {
      console.error('上传历史记录失败:', error)
      throw error
    }
  }

  // 获取历史记录
  async getHistory(userId) {
    try {
      const result = await this.request({
        url: `/api/history/${userId}`,
        method: 'GET'
      })
      return result
    } catch (error) {
      console.error('获取历史记录失败:', error)
      throw error
    }
  }

  // 删除历史记录
  async deleteHistory(userId, historyId) {
    try {
      const result = await this.request({
        url: `/api/history/${userId}/${historyId}`,
        method: 'DELETE'
      })
      return result
    } catch (error) {
      console.error('删除历史记录失败:', error)
      throw error
    }
  }

  // 批量删除历史记录
  async batchDeleteHistory(userId, historyIds) {
    try {
      const result = await this.request({
        url: '/api/history/batch_delete',
        method: 'POST',
        data: {
          user_id: userId,
          history_ids: historyIds
        }
      })
      return result
    } catch (error) {
      console.error('批量删除历史记录失败:', error)
      throw error
    }
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
  checkServer: () => apiService.checkServer(),
  getStyles: () => apiService.getStyles(),
  getTemplateInfo: (style) => apiService.getTemplateInfo(style),
  generateTicket: (data) => apiService.generateTicket(data),
  batchGenerateTickets: (data) => apiService.batchGenerateTickets(data),

  // 用户相关方法
  registerUser: (userInfo) => apiService.registerUser(userInfo),
  loginUser: (userInfo) => apiService.loginUser(userInfo),
  getUserInfo: (userId) => apiService.getUserInfo(userId),

  // 历史记录相关方法
  uploadHistory: (userId, historyData) => apiService.uploadHistory(userId, historyData),
  getHistory: (userId) => apiService.getHistory(userId),
  deleteHistory: (userId, historyId) => apiService.deleteHistory(userId, historyId),
  batchDeleteHistory: (userId, historyIds) => apiService.batchDeleteHistory(userId, historyIds),

  // 工具方法
  setBaseUrl: (url) => {
    apiService.baseUrl = url
    app.globalData.apiBaseUrl = url
  },

  getBaseUrl: () => apiService.baseUrl
}

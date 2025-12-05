// utils/storage.js
// 本地存储工具

const app = getApp()

class StorageService {
  constructor() {
    this.prefix = 'ticker_'
  }

  // 生成存储键名
  getKey(key) {
    return this.prefix + key
  }

  // 设置存储
  set(key, value) {
    try {
      const storageKey = this.getKey(key)
      wx.setStorageSync(storageKey, value)
      return true
    } catch (error) {
      console.error('存储失败:', error)
      return false
    }
  }

  // 获取存储
  get(key, defaultValue = null) {
    try {
      const storageKey = this.getKey(key)
      const value = wx.getStorageSync(storageKey)
      return value !== '' ? value : defaultValue
    } catch (error) {
      console.error('获取存储失败:', error)
      return defaultValue
    }
  }

  // 删除存储
  remove(key) {
    try {
      const storageKey = this.getKey(key)
      wx.removeStorageSync(storageKey)
      return true
    } catch (error) {
      console.error('删除存储失败:', error)
      return false
    }
  }

  // 清空所有存储
  clear() {
    try {
      wx.clearStorageSync()
      return true
    } catch (error) {
      console.error('清空存储失败:', error)
      return false
    }
  }

  // 获取存储信息
  getInfo() {
    try {
      return wx.getStorageInfoSync()
    } catch (error) {
      console.error('获取存储信息失败:', error)
      return null
    }
  }

  // 草稿相关方法
  saveDraft(data) {
    return this.set('draft', data)
  }

  getDraft() {
    return this.get('draft')
  }

  clearDraft() {
    return this.remove('draft')
  }

  // 历史记录相关方法
  saveHistory(history) {
    return this.set('history', history)
  }

  getHistory() {
    return this.get('history', [])
  }

  clearHistory() {
    return this.remove('history')
  }

  // 用户设置相关方法
  saveSettings(settings) {
    return this.set('settings', settings)
  }

  getSettings() {
    return this.get('settings', {
      autoSave: true,
      showTips: true,
      defaultStyle: 'red15'
    })
  }

  // 缓存相关方法
  setCache(key, value, expireTime = 3600000) { // 默认1小时过期
    const cacheData = {
      value: value,
      expireTime: Date.now() + expireTime
    }
    return this.set(`cache_${key}`, cacheData)
  }

  getCache(key) {
    const cacheData = this.get(`cache_${key}`)
    if (!cacheData) {
      return null
    }

    if (Date.now() > cacheData.expireTime) {
      this.remove(`cache_${key}`)
      return null
    }

    return cacheData.value
  }

  // 清除过期缓存
  clearExpiredCache() {
    try {
      const info = this.getInfo()
      if (!info) return

      const now = Date.now()
      info.keys.forEach(key => {
        if (key.startsWith(this.prefix + 'cache_')) {
          const cacheData = wx.getStorageSync(key)
          if (cacheData && cacheData.expireTime && now > cacheData.expireTime) {
            wx.removeStorageSync(key)
          }
        }
      })
    } catch (error) {
      console.error('清除过期缓存失败:', error)
    }
  }
}

// 创建存储服务实例
const storageService = new StorageService()

// 导出存储方法
module.exports = {
  // 基础方法
  set: (key, value) => storageService.set(key, value),
  get: (key, defaultValue) => storageService.get(key, defaultValue),
  remove: (key) => storageService.remove(key),
  clear: () => storageService.clear(),
  getInfo: () => storageService.getInfo(),

  // 草稿方法
  saveDraft: (data) => storageService.saveDraft(data),
  getDraft: () => storageService.getDraft(),
  clearDraft: () => storageService.clearDraft(),

  // 历史记录方法
  saveHistory: (history) => storageService.saveHistory(history),
  getHistory: () => storageService.getHistory(),
  clearHistory: () => storageService.clearHistory(),

  // 用户设置方法
  saveSettings: (settings) => storageService.saveSettings(settings),
  getSettings: () => storageService.getSettings(),

  // 缓存方法
  setCache: (key, value, expireTime) => storageService.setCache(key, value, expireTime),
  getCache: (key) => storageService.getCache(key),
  clearExpiredCache: () => storageService.clearExpiredCache()
}

// utils/validator.js
// 数据验证工具

class Validator {
  constructor() {
    this.rules = {
      // 姓名验证
      name: {
        required: true,
        minLength: 1,
        maxLength: 10,
        pattern: /^[\u4e00-\u9fa5a-zA-Z\s]+$/,
        message: '姓名只能包含中文、英文和空格，长度1-10个字符'
      },
      
      // 车次号验证
      trainNumber: {
        required: true,
        pattern: /^[A-Z]\d{1,4}$/,
        message: '车次号格式不正确，应为字母+数字（如G1234）'
      },
      
      // 座位号验证
      seatNumber: {
        required: true,
        pattern: /^\d{1,2}[A-F]$/,
        message: '座位号格式不正确，应为数字+字母（如12A）'
      },
      
      // 车站名验证
      station: {
        required: true,
        minLength: 2,
        maxLength: 20,
        pattern: /^[\u4e00-\u9fa5]+$/,
        message: '车站名只能包含中文，长度2-20个字符'
      },
      
      // 日期验证
      date: {
        required: true,
        pattern: /^\d{4}-\d{2}-\d{2}$/,
        message: '日期格式不正确，应为YYYY-MM-DD'
      },
      
      // 时间验证
      time: {
        required: true,
        pattern: /^\d{2}:\d{2}$/,
        message: '时间格式不正确，应为HH:MM'
      },
      
      // 价格验证
      price: {
        required: false,
        pattern: /^\d+(\.\d{1,2})?$/,
        message: '价格格式不正确，应为数字（如123.45）'
      }
    }
  }

  // 验证单个字段
  validateField(fieldName, value) {
    const rule = this.rules[fieldName]
    if (!rule) {
      return { valid: true, message: '' }
    }

    // 必填验证
    if (rule.required && (!value || value.trim() === '')) {
      return { valid: false, message: `${fieldName}不能为空` }
    }

    // 如果值为空且非必填，则通过验证
    if (!value || value.trim() === '') {
      return { valid: true, message: '' }
    }

    // 长度验证
    if (rule.minLength && value.length < rule.minLength) {
      return { valid: false, message: `${fieldName}长度不能少于${rule.minLength}个字符` }
    }

    if (rule.maxLength && value.length > rule.maxLength) {
      return { valid: false, message: `${fieldName}长度不能超过${rule.maxLength}个字符` }
    }

    // 正则验证
    if (rule.pattern && !rule.pattern.test(value)) {
      return { valid: false, message: rule.message }
    }

    return { valid: true, message: '' }
  }

  // 验证表单数据
  validateForm(formData, requiredFields = []) {
    const errors = []
    const warnings = []

    // 验证必填字段
    requiredFields.forEach(field => {
      const value = formData[field]?.value || ''
      const result = this.validateField(field, value)
      if (!result.valid) {
        errors.push({
          field: field,
          message: result.message
        })
      }
    })

    // 验证所有字段
    Object.keys(formData).forEach(field => {
      const value = formData[field]?.value || ''
      const result = this.validateField(field, value)
      if (!result.valid) {
        errors.push({
          field: field,
          message: result.message
        })
      }
    })

    return {
      valid: errors.length === 0,
      errors: errors,
      warnings: warnings
    }
  }

  // 验证车票数据
  validateTicketData(formData) {
    const requiredFields = ['姓名', '车次号', '座位号', '出发站', '到达站']
    return this.validateForm(formData, requiredFields)
  }

  // 清理数据
  cleanData(formData) {
    const cleanedData = {}
    
    Object.keys(formData).forEach(key => {
      const value = formData[key]?.value || ''
      cleanedData[key] = {
        value: value.trim(),
        enabled: formData[key]?.enabled || false
      }
    })
    
    return cleanedData
  }

  // 格式化数据用于API请求
  formatForAPI(formData) {
    const formattedData = {}
    
    Object.keys(formData).forEach(key => {
      if (formData[key].enabled && formData[key].value) {
        formattedData[key] = formData[key].value
      }
    })
    
    return formattedData
  }

  // 检查数据完整性
  checkCompleteness(formData) {
    const enabledFields = Object.keys(formData).filter(
      key => formData[key].enabled && formData[key].value
    )
    
    const totalFields = Object.keys(formData).length
    const completeness = (enabledFields.length / totalFields) * 100
    
    return {
      enabledFields: enabledFields.length,
      totalFields: totalFields,
      completeness: Math.round(completeness),
      isComplete: completeness >= 50 // 至少50%的字段有值
    }
  }

  // 获取字段建议
  getFieldSuggestions(fieldName) {
    const suggestions = {
      '姓名': ['张三', '李四', '王五'],
      '车次号': ['G1234', 'D5678', 'K9012', 'T3456'],
      '座位号': ['01A', '02B', '03C', '04D', '05F'],
      '出发站': ['北京南', '上海虹桥', '广州南', '深圳北'],
      '到达站': ['北京南', '上海虹桥', '广州南', '深圳北'],
      '日期': [new Date().toISOString().split('T')[0]],
      '时间': ['08:00', '10:30', '14:20', '18:45']
    }
    
    return suggestions[fieldName] || []
  }

  // 自动补全建议
  getAutoCompleteSuggestions(fieldName, inputValue) {
    const suggestions = this.getFieldSuggestions(fieldName)
    if (!inputValue) return suggestions
    
    return suggestions.filter(suggestion => 
      suggestion.toLowerCase().includes(inputValue.toLowerCase())
    )
  }
}

// 创建验证器实例
const validator = new Validator()

// 导出验证方法
module.exports = {
  // 基础验证
  validateField: (fieldName, value) => validator.validateField(fieldName, value),
  validateForm: (formData, requiredFields) => validator.validateForm(formData, requiredFields),
  
  // 业务验证
  validateTicketData: (formData) => validator.validateTicketData(formData),
  
  // 数据处理
  cleanData: (formData) => validator.cleanData(formData),
  formatForAPI: (formData) => validator.formatForAPI(formData),
  checkCompleteness: (formData) => validator.checkCompleteness(formData),
  
  // 建议功能
  getFieldSuggestions: (fieldName) => validator.getFieldSuggestions(fieldName),
  getAutoCompleteSuggestions: (fieldName, inputValue) => validator.getAutoCompleteSuggestions(fieldName, inputValue)
}

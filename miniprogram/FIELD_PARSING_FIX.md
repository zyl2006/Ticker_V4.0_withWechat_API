# 字段解析修复说明

## 🔧 问题描述

之前的字段解析逻辑有误，没有正确从API返回的模板数据中提取字段信息。API返回的数据结构中，字段定义在 `segments` 数组的 `text` 属性中，格式为 `{字段名}`。

## ✅ 修复内容

### 1. 修复了 `parseFormFields` 方法

**之前的错误逻辑：**
```javascript
// 错误：直接从fields的key获取字段名
for (const [key, config] of Object.entries(fields)) {
  formFields.push({
    key: key,  // 这里key是模板中的位置名称，不是字段名
    label: key,
    // ...
  })
}
```

**修复后的正确逻辑：**
```javascript
// 正确：从segments中提取字段名
for (const [key, config] of Object.entries(fields)) {
  if (config.segments && Array.isArray(config.segments)) {
    config.segments.forEach(segment => {
      if (segment.text && segment.text.includes('{') && segment.text.includes('}')) {
        // 提取字段名，如 {出发站} -> 出发站
        const fieldName = segment.text.match(/\{([^}]+)\}/)?.[1]
        if (fieldName && !fieldMap.has(fieldName)) {
          fieldMap.set(fieldName, {
            key: fieldName,  // 使用提取的字段名
            label: fieldName,
            // ...
          })
        }
      }
    })
  }
}
```

### 2. 修复了 `getDefaultFields` 方法

**之前的错误：**
```javascript
// 错误：返回对象格式
getDefaultFields(style) {
  const defaultFields = {
    'from': { type: 'text', required: true, description: '出发地' },
    // ...
  }
  return defaultFields
}
```

**修复后：**
```javascript
// 正确：返回数组格式，字段名使用中文
getDefaultFields() {
  const defaultFields = [
    { key: '出发站', label: '出发站', type: 'text', required: true, description: '请输入出发站', value: '', enabled: true },
    { key: '到达站', label: '到达站', type: 'text', required: true, description: '请输入到达站', value: '', enabled: true },
    // ...
  ]
  return defaultFields
}
```

## 📋 API数据结构说明

### 模板数据结构
```json
{
  "fields": {
    "出发站": {
      "x": 315,
      "y": 200,
      "anchor": "ma",
      "segments": [
        {"text": "{出发站}", "font_path": "fonts/simhei.ttf", "size":90, "fill": "#000000", "letter_spacing": 2},
        {"text": "站", "font_path": "fonts/simsun.ttc", "size": 60, "fill": "#000000", "letter_spacing": 2,"y_offset": 15}
      ]
    }
  }
}
```

### 字段提取逻辑
1. 遍历 `fields` 对象
2. 检查每个字段的 `segments` 数组
3. 从 `segments[].text` 中提取 `{字段名}` 格式的字段
4. 使用正则表达式 `/\{([^}]+)\}/` 提取字段名
5. 去重并创建表单字段配置

## 🎯 修复效果

- ✅ 正确解析API返回的字段信息
- ✅ 表单字段名称使用中文（出发站、到达站、车次等）
- ✅ 支持字段的启用/禁用功能
- ✅ 未填写字段返回空值
- ✅ 实时预览功能正常工作

## 🧪 测试验证

已通过测试脚本验证字段解析逻辑正确：
```javascript
// 测试数据
const testFields = {
  "出发站": {
    "segments": [{"text": "{出发站}", ...}]
  },
  "到达站": {
    "segments": [{"text": "{到达站}", ...}]
  }
}

// 解析结果
[
  { key: '出发站', label: '出发站', ... },
  { key: '到达站', label: '到达站', ... }
]
```

现在小程序应该能够正确解析字段并生成预览了！

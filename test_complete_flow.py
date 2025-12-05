#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整的小程序流程
"""

import requests
import json

def test_complete_flow():
    """测试完整流程"""
    print("测试完整的小程序流程")
    print("=" * 40)
    
    base_url = 'http://localhost:5001'
    
    try:
        # 1. 健康检查
        print("1. 健康检查...")
        response = requests.get(f'{base_url}/api/health')
        if response.status_code != 200:
            print("FAIL 健康检查失败")
            return False
        print("SUCCESS 健康检查通过")
        
        # 2. 获取样式列表
        print("\n2. 获取样式列表...")
        response = requests.get(f'{base_url}/api/styles')
        if response.status_code != 200:
            print("FAIL 获取样式列表失败")
            return False
        result = response.json()
        if not result.get('success'):
            print("FAIL 样式列表获取失败")
            return False
        print(f"SUCCESS 获取到 {len(result.get('styles', []))} 个样式")
        
        # 3. 获取字段列表
        print("\n3. 获取字段列表...")
        response = requests.get(f'{base_url}/api/template/red15/fields')
        if response.status_code != 200:
            print("FAIL 获取字段列表失败")
            return False
        result = response.json()
        if not result.get('success'):
            print("FAIL 字段列表获取失败")
            return False
        print(f"SUCCESS 获取到 {result.get('field_count')} 个字段")
        
        fields = result.get('fields', [])
        print("前10个字段:")
        for i, field in enumerate(fields[:10]):
            print(f"  {i+1}. {field['key']}")
        
        # 4. 构建测试数据
        print("\n4. 构建测试数据...")
        user_data = {}
        for field in fields:  # 使用所有字段
            key = field['key']
            if key == '姓名':
                user_data[key] = '测试用户'
            elif key == '车次号':
                user_data[key] = 'G1234'
            elif key == '出发站':
                user_data[key] = '北京'
            elif key == '到达站':
                user_data[key] = '上海'
            elif key == '车次类型':
                user_data[key] = '高铁'
            elif key == '票价1':
                user_data[key] = '553'
            elif key == '年':
                user_data[key] = '2024'
            elif key == '月':
                user_data[key] = '01'
            elif key == '日':
                user_data[key] = '15'
            elif key == '时':
                user_data[key] = '14'
            elif key == '分':
                user_data[key] = '30'
            elif key == '席位号':
                user_data[key] = '01A'
            elif key == '席别':
                user_data[key] = '二等座'
            elif key == '票种':
                user_data[key] = '成人票'
            elif key == '身份证号1':
                user_data[key] = '123456789012345678'
            elif key == '身份证号2':
                user_data[key] = '123456789012345678'
            elif key == '证件类型':
                user_data[key] = '身份证'
            elif key == '发售站':
                user_data[key] = '北京站'
            else:
                user_data[key] = '测试' + key
        
        print(f"SUCCESS 构建了 {len(user_data)} 个字段的测试数据")
        
        # 5. 生成预览
        print("\n5. 生成预览...")
        request_data = {
            'style': 'red15',
            'user_data': user_data,
            'format': 'base64'
        }
        
        response = requests.post(f'{base_url}/api/generate', json=request_data)
        if response.status_code != 200:
            print(f"FAIL 生成预览失败: {response.text}")
            return False
        
        result = response.json()
        if not result.get('success'):
            print(f"FAIL 生成预览失败: {result.get('error')}")
            return False
        
        print("SUCCESS 预览生成成功!")
        print(f"图片数据大小: {len(result.get('data', {}).get('image_base64', ''))} 字符")
        
        return True
        
    except Exception as e:
        print(f"FAIL 测试异常: {e}")
        return False

def main():
    """主函数"""
    print("小程序完整流程测试")
    print("=" * 50)
    
    success = test_complete_flow()
    
    print("\n" + "=" * 50)
    if success:
        print("SUCCESS 完整流程测试通过!")
        print("小程序现在可以:")
        print("  - 动态获取字段列表")
        print("  - 自动适应模板变化")
        print("  - 正确生成预览")
        print("\n请在微信开发者工具中:")
        print("   1. 重新编译小程序")
        print("   2. 查看字段数量应该显示46个")
        print("   3. 填写字段信息并生成预览")
    else:
        print("FAIL 流程测试失败")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的API端点
"""

import requests
import json

def test_new_api_endpoint():
    """测试新的API端点"""
    print("测试新的API端点")
    print("=" * 30)
    
    try:
        # 测试新的字段端点
        response = requests.get('http://api.sgsky.tech/api/template/red15/fields')
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"成功: {result.get('success')}")
            print(f"字段数量: {result.get('field_count')}")
            
            fields = result.get('fields', [])
            print(f"字段列表长度: {len(fields)}")
            
            if fields:
                print("前10个字段:")
                for i, field in enumerate(fields[:10]):
                    print(f"  {i+1}. {field['key']}")
            
            # 保存响应到文件
            with open('api_fields_response.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print("响应已保存到 api_fields_response.json")
            
            return True
        else:
            print(f"请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"异常: {e}")
        return False

def test_generate_with_new_fields():
    """使用新字段测试生成API"""
    print("\n测试生成API...")
    
    try:
        # 获取字段列表
        response = requests.get('http://api.sgsky.tech/api/template/red15/fields')
        if response.status_code != 200:
            print("FAIL 无法获取字段列表")
            return False
        
        result = response.json()
        if not result.get('success'):
            print("FAIL 字段列表获取失败")
            return False
        
        fields = result.get('fields', [])
        print(f"获取到 {len(fields)} 个字段")
        
        # 构建测试数据
        user_data = {}
        for field in fields[:10]:  # 只测试前10个字段
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
            else:
                user_data[key] = '测试' + key
        
        print(f"构建了 {len(user_data)} 个字段的测试数据")
        
        # 测试生成API
        request_data = {
            'style': 'red15',
            'user_data': user_data,
            'format': 'base64'
        }
        
        response = requests.post('http://api.sgsky.tech/api/generate', json=request_data)
        print(f"生成API响应状态: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("SUCCESS 生成API调用成功!")
                return True
            else:
                print(f"FAIL 生成API返回错误: {result.get('error')}")
                return False
        else:
            print(f"FAIL 生成API HTTP错误: {response.text}")
            return False
            
    except Exception as e:
        print(f"FAIL 测试异常: {e}")
        return False

def main():
    """主函数"""
    print("新API端点测试")
    print("=" * 40)
    
    # 测试新端点
    endpoint_success = test_new_api_endpoint()
    
    if endpoint_success:
        # 测试生成API
        generate_success = test_generate_with_new_fields()
        
        print("\n" + "=" * 40)
        if generate_success:
            print("SUCCESS 新API端点工作正常!")
            print("小程序现在可以动态获取字段了")
            print("\n请在微信开发者工具中:")
            print("   1. 重新编译小程序")
            print("   2. 查看字段数量应该显示46个")
            print("   3. 填写字段信息并生成预览")
        else:
            print("FAIL 生成API仍有问题")
    else:
        print("FAIL 新API端点有问题")

if __name__ == "__main__":
    main()

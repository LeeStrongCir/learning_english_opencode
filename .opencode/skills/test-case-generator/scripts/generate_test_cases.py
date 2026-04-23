#!/usr/bin/env python3
"""
Test Case CSV Generator
将 JSON 格式的测试用例数据生成为按类型分类的 CSV 文件
"""

import json
import csv
import argparse
import os
from datetime import datetime


# 列定义
COLUMNS = [
    '用例ID', '测试场景/模块', '用例标题', '前置条件',
    '测试步骤', '预期结果', '优先级', '测试类型',
    '实际结果', '状态', '测试数据', '备注'
]

# 文件映射
FILE_MAPPING = {
    '功能测试': 'functional_tests.csv',
    '边界测试': 'boundary_tests.csv',
    '异常测试': 'exception_tests.csv',
    '用户旅程': 'user_journey_tests.csv',
    'API测试': 'api_tests.csv',
}

TYPE_MAPPING = {
    '功能': '功能测试',
    'boundary': '边界测试',
    '边界': '边界测试',
    'exception': '异常测试',
    '异常': '异常测试',
    'user_journey': '用户旅程',
    '用户旅程': '用户旅程',
    'api': 'API测试',
    'API': 'API测试',
}


def write_csv(filepath, test_cases, case_id_counter):
    """写入单个 CSV 文件"""
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        
        for case in test_cases:
            module = case.get('模块', 'COMMON')
            if module not in case_id_counter:
                case_id_counter[module] = 1
            
            case_id = f"TC-{module}-{case_id_counter[module]:03d}"
            case_id_counter[module] += 1
            
            row = {
                '用例ID': case_id,
                '测试场景/模块': case.get('测试场景', ''),
                '用例标题': case.get('标题', ''),
                '前置条件': case.get('前置条件', ''),
                '测试步骤': case.get('测试步骤', ''),
                '预期结果': case.get('预期结果', ''),
                '优先级': case.get('优先级', 'P2'),
                '测试类型': case.get('测试类型', ''),
                '实际结果': '',
                '状态': 'Not Run',
                '测试数据': case.get('测试数据', ''),
                '备注': case.get('备注', ''),
            }
            writer.writerow(row)


def write_summary(filepath, cases_by_type):
    """生成汇总统计 CSV"""
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['统计项', '值'])
        writer.writerow(['生成时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        total = 0
        writer.writerow(['测试类型', '数量'])
        for type_name, cases in cases_by_type.items():
            count = len(cases)
            total += count
            writer.writerow([type_name, count])
        
        writer.writerow([])
        writer.writerow(['总计', total])
        writer.writerow([])
        
        # 按优先级统计
        writer.writerow(['优先级', '数量'])
        for priority in ['P0', 'P1', 'P2', 'P3']:
            count = sum(
                1 for cases in cases_by_type.values()
                for c in cases if c.get('优先级') == priority
            )
            writer.writerow([priority, count])


def generate_csv(test_cases_json, output_dir):
    """主函数：生成 CSV 文件"""
    
    with open(test_cases_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    test_cases = data.get('test_cases', [])
    
    # 按类型分组
    cases_by_type = {
        '功能测试': [],
        '边界测试': [],
        '异常测试': [],
        '用户旅程': [],
        'API测试': [],
    }
    
    for case in test_cases:
        test_type = case.get('测试类型', '功能')
        file_key = TYPE_MAPPING.get(test_type, '功能测试')
        if file_key in cases_by_type:
            cases_by_type[file_key].append(case)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成各类型 CSV
    case_id_counter = {}
    generated_files = []
    
    for type_name, cases in cases_by_type.items():
        if cases:
            filepath = os.path.join(output_dir, FILE_MAPPING[type_name])
            write_csv(filepath, cases, case_id_counter)
            generated_files.append((type_name, len(cases), filepath))
    
    # 生成汇总文件
    summary_path = os.path.join(output_dir, 'summary.csv')
    write_summary(summary_path, cases_by_type)
    
    # 打印统计
    total = sum(len(cases) for cases in cases_by_type.values())
    print(f"CSV 文件已生成到: {output_dir}")
    print(f"共生成 {total} 条测试用例")
    for type_name, count, filepath in generated_files:
        print(f"  - {type_name}: {count} 条 -> {os.path.basename(filepath)}")
    print(f"  - 汇总统计: {os.path.basename(summary_path)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成测试用例 CSV 文件')
    parser.add_argument('--test-cases', required=True, help='测试用例 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出目录路径')
    
    args = parser.parse_args()
    generate_csv(args.test_cases, args.output)

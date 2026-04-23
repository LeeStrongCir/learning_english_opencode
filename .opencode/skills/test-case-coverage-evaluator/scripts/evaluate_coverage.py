#!/usr/bin/env python3
"""
Test Case Coverage Evaluator
根据需求清单和测试用例集，评定测试用例覆盖率
"""

import json
import argparse
import os
from datetime import datetime


# 权重配置
WEIGHTS = {
    'requirements': 0.30,
    'feature_dimensions': 0.25,
    'scenario_paths': 0.20,
    'code_coverage': 0.15,
    'defect_regression': 0.10,
}

# 功能维度列表
FEATURE_DIMENSIONS = ['正向流程', '反向流程', '边界值', '权限/角色', '数据状态', '兼容性']

# 等级评定标准
def get_grade(score):
    if score >= 90:
        return '优秀', '可以发布'
    elif score >= 80:
        return '良好', '核心路径已覆盖，可发布'
    elif score >= 70:
        return '合格', '有漏测风险，谨慎发布'
    else:
        return '不足', '补充用例后再发布'


def evaluate_requirements_coverage(requirements, test_cases):
    """评定需求→用例覆盖率"""
    if not requirements:
        return 0, [], "未提供需求清单"
    
    req_ids = [r.get('id', r.get('需求ID', '')) for r in requirements]
    covered_reqs = set()
    uncovered_reqs = []
    req_case_mapping = {}
    
    for case in test_cases:
        # 假设用例中有 '关联需求' 或 'requirement_id' 字段
        linked_req = case.get('关联需求', case.get('requirement_id', ''))
        if linked_req:
            if isinstance(linked_req, list):
                covered_reqs.update(linked_req)
            else:
                covered_reqs.add(linked_req)
    
    for req_id in req_ids:
        if req_id in covered_reqs:
            req_case_mapping[req_id] = '已覆盖'
        else:
            req_case_mapping[req_id] = '未覆盖'
            uncovered_reqs.append(req_id)
    
    total = len(req_ids)
    covered = len(covered_reqs)
    rate = (covered / total * 100) if total > 0 else 0
    
    issues = []
    if uncovered_reqs:
        issues.append(f"以下需求未关联测试用例: {', '.join(uncovered_reqs)}")
    if rate < 100:
        issues.append(f"需求覆盖率未达到100%底线，当前为 {rate:.1f}%")
    
    return rate, issues, req_case_mapping


def evaluate_feature_coverage(features, test_cases):
    """评定功能点→用例覆盖（6维度）"""
    if not features:
        return 0, ["未提供功能点清单"], {}
    
    feature_scores = {}
    all_issues = []
    
    for feature in features:
        feature_name = feature.get('name', feature.get('功能名称', ''))
        feature_id = feature.get('id', feature.get('功能ID', feature_name))
        
        # 查找关联该功能的用例
        feature_cases = [
            c for c in test_cases
            if c.get('功能模块') == feature_name or c.get('feature_id') == feature_id
        ]
        
        # 检查6个维度
        covered_dims = []
        missing_dims = []
        
        for dim in FEATURE_DIMENSIONS:
            has_case = any(
                dim in c.get('测试类型', '') or dim in c.get('覆盖维度', '')
                for c in feature_cases
            )
            if has_case:
                covered_dims.append(dim)
            else:
                missing_dims.append(dim)
        
        dim_score = len(covered_dims) / len(FEATURE_DIMENSIONS) * 100
        feature_scores[feature_name] = {
            'score': dim_score,
            'covered': covered_dims,
            'missing': missing_dims,
        }
        
        if missing_dims:
            all_issues.append(f"功能 [{feature_name}] 缺少以下维度用例: {', '.join(missing_dims)}")
    
    avg_score = sum(f['score'] for f in feature_scores.values()) / len(feature_scores) if feature_scores else 0
    return avg_score, all_issues, feature_scores


def evaluate_scenario_coverage(scenarios, test_cases):
    """评定场景路径覆盖率"""
    if not scenarios:
        return 0, ["未提供场景路径清单"], {}
    
    total_paths = 0
    covered_paths = 0
    path_details = []
    issues = []
    
    for scenario in scenarios:
        scenario_name = scenario.get('name', scenario.get('场景名称', ''))
        paths = scenario.get('paths', scenario.get('路径', []))
        
        for path in paths:
            total_paths += 1
            path_type = path.get('type', '主流程')  # 主流程/分支/边缘
            path_desc = path.get('description', path)
            
            # 检查是否有对应用例
            has_case = any(
                scenario_name in c.get('测试场景', '') or path_desc in c.get('标题', '')
                for c in test_cases
            )
            
            if has_case:
                covered_paths += 1
                path_details.append({'path': path_desc, 'type': path_type, 'status': '已覆盖'})
            else:
                path_details.append({'path': path_desc, 'type': path_type, 'status': '未覆盖'})
                if path_type == '主流程':
                    issues.append(f"主流程场景未覆盖: {path_desc}")
                elif path_type == '分支':
                    issues.append(f"分支场景未覆盖: {path_desc}")
    
    rate = (covered_paths / total_paths * 100) if total_paths > 0 else 0
    return rate, issues, path_details


def evaluate_code_coverage(code_report):
    """评定代码覆盖率（从工具报告读取）"""
    if not code_report:
        return 0, ["未提供代码覆盖率报告"], {}
    
    # 假设 code_report 是包含覆盖率数据的字典
    line_rate = code_report.get('line_coverage', 0)
    branch_rate = code_report.get('branch_coverage', 0)
    
    details = {
        'line_coverage': line_rate,
        'branch_coverage': branch_rate,
    }
    
    issues = []
    if line_rate < 80:
        issues.append(f"代码行覆盖率较低 ({line_rate:.1f}%)，建议补充用例")
    if branch_rate < 70:
        issues.append(f"分支覆盖率较低 ({branch_rate:.1f}%)，建议补充边界和异常用例")
    
    # 综合取平均
    return (line_rate + branch_rate) / 2, issues, details


def evaluate_defect_coverage(defects, test_cases):
    """评定缺陷→用例覆盖（回归保护）"""
    if not defects:
        return 0, ["未提供缺陷清单"], {}
    
    total_defects = len(defects)
    covered_defects = 0
    uncovered_defects = []
    
    for defect in defects:
        defect_id = defect.get('id', defect.get('缺陷ID', ''))
        status = defect.get('status', defect.get('状态', ''))
        
        # 只检查已修复的缺陷
        if status not in ['已修复', 'fixed', 'closed', '已关闭']:
            continue
        
        # 检查是否有回归用例
        has_regression = any(
            defect_id in c.get('关联缺陷', '') or defect_id in c.get('defect_id', '')
            for c in test_cases
        )
        
        if has_regression:
            covered_defects += 1
        else:
            uncovered_defects.append(defect_id)
    
    fixed_total = total_defects  # 简化处理，实际应只统计已修复的
    rate = (covered_defects / fixed_total * 100) if fixed_total > 0 else 0
    
    issues = []
    if uncovered_defects:
        issues.append(f"以下已修复缺陷缺少回归用例: {', '.join(uncovered_defects)}")
    
    return rate, issues, {'covered': covered_defects, 'uncovered': uncovered_defects}


def evaluate_case_quality(test_cases):
    """评定测试用例自身质量"""
    if not test_cases:
        return 0, ["未提供测试用例"], {}
    
    quality_checks = {
        'has_precondition': 0,
        'has_steps': 0,
        'has_expected': 0,
        'has_specific_assertion': 0,
        'is_independent': 0,
    }
    
    total = len(test_cases)
    qualified_cases = 0
    case_quality = []
    
    for case in test_cases:
        checks = {}
        
        # 检查前置条件
        checks['has_precondition'] = bool(case.get('前置条件', case.get('preconditions', '')))
        
        # 检查测试步骤
        checks['has_steps'] = bool(case.get('测试步骤', case.get('steps', '')))
        
        # 检查预期结果
        expected = case.get('预期结果', case.get('expected_result', ''))
        checks['has_expected'] = bool(expected)
        
        # 检查预期结果是否具体（不是模糊描述）
        vague_words = ['应该正常', '应该可以', '正常', '没问题']
        checks['has_specific_assertion'] = bool(expected) and not any(
            word in expected for word in vague_words
        )
        
        # 检查独立性
        checks['is_independent'] = '不依赖' not in case.get('备注', '') or '独立' in case.get('备注', '')
        
        # 统计
        for key, value in checks.items():
            if value:
                quality_checks[key] += 1
        
        # 判断是否满足所有条件
        is_qualified = all(checks.values())
        if is_qualified:
            qualified_cases += 1
        
        case_quality.append({
            'case_id': case.get('用例ID', case.get('id', '')),
            'title': case.get('标题', case.get('title', '')),
            'qualified': is_qualified,
            'checks': checks,
        })
    
    rate = (qualified_cases / total * 100) if total > 0 else 0
    
    issues = []
    for key, count in quality_checks.items():
        if count < total:
            missing = total - count
            check_names = {
                'has_precondition': '缺少前置条件',
                'has_steps': '缺少测试步骤',
                'has_expected': '缺少预期结果',
                'has_specific_assertion': '预期结果描述模糊',
                'is_independent': '用例不独立',
            }
            issues.append(f"{check_names[key]}: {missing} 条用例")
    
    return rate, issues, case_quality


def generate_report(results, output_path):
    """生成覆盖率评定报告"""
    
    grade_name, grade_meaning = get_grade(results['total_score'])
    
    report = f"""# 测试用例覆盖率评定报告

## 概要
- 评定日期：{datetime.now().strftime('%Y-%m-%d %H:%M')}
- 综合评分：{results['total_score']:.1f}%
- 等级：{grade_name}
- 含义：{grade_meaning}

## 各维度得分

| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| 需求覆盖率 | {results['dimensions']['requirements']['score']:.1f}% | 30% | {results['dimensions']['requirements']['weighted']:.1f}% |
| 功能维度覆盖率 | {results['dimensions']['feature_dimensions']['score']:.1f}% | 25% | {results['dimensions']['feature_dimensions']['weighted']:.1f}% |
| 场景路径覆盖率 | {results['dimensions']['scenario_paths']['score']:.1f}% | 20% | {results['dimensions']['scenario_paths']['weighted']:.1f}% |
| 代码覆盖率 | {results['dimensions']['code_coverage']['score']:.1f}% | 15% | {results['dimensions']['code_coverage']['weighted']:.1f}% |
| 缺陷回归覆盖率 | {results['dimensions']['defect_regression']['score']:.1f}% | 10% | {results['dimensions']['defect_regression']['weighted']:.1f}% |

## 发现的问题

"""
    
    all_issues = []
    for dim_name, dim_data in results['dimensions'].items():
        for issue in dim_data.get('issues', []):
            all_issues.append(f"- [{dim_name}] {issue}")
    
    if all_issues:
        report += '\n'.join(all_issues)
    else:
        report += "未发现明显问题。"
    
    report += """

## 改进建议

"""
    
    # 根据问题生成建议
    suggestions = []
    if results['dimensions']['requirements']['score'] < 100:
        suggestions.append("1. **补充需求关联用例**：确保每个需求至少有 1 个正向用例和 1 个反向用例")
    if results['dimensions']['feature_dimensions']['score'] < 80:
        suggestions.append("2. **完善功能维度覆盖**：对每个功能点检查 6 个维度（正向、反向、边界、权限、数据、兼容）")
    if results['dimensions']['scenario_paths']['score'] < 80:
        suggestions.append("3. **补充场景路径用例**：识别主流程、分支和边缘场景，确保核心路径全覆盖")
    if results['dimensions']['code_coverage']['score'] < 80:
        suggestions.append("4. **提升代码覆盖率**：使用覆盖率工具识别未覆盖的代码分支，补充对应用例")
    if results['dimensions']['defect_regression']['score'] < 100:
        suggestions.append("5. **添加回归用例**：为每个已修复的 bug 创建回归测试用例")
    
    if suggestions:
        report += '\n'.join(suggestions)
    else:
        report += "当前覆盖率良好，建议定期重新评估。"
    
    report += """

## 详细分析

### 需求追踪矩阵

"""
    
    req_mapping = results['dimensions']['requirements'].get('details', {})
    if req_mapping:
        report += "| 需求ID | 覆盖状态 |\n|--------|----------|\n"
        for req_id, status in req_mapping.items():
            report += f"| {req_id} | {status} |\n"
    
    report += """

### 功能维度覆盖详情

"""
    
    feature_scores = results['dimensions']['feature_dimensions'].get('details', {})
    if feature_scores:
        report += "| 功能名称 | 得分 | 已覆盖维度 | 缺失维度 |\n|----------|------|------------|----------|\n"
        for name, data in feature_scores.items():
            covered = ', '.join(data.get('covered', [])) or '无'
            missing = ', '.join(data.get('missing', [])) or '无'
            report += f"| {name} | {data['score']:.0f}% | {covered} | {missing} |\n"
    
    report += """

---

*本报告由 test-case-coverage-evaluator 自动生成*
"""
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"评定报告已生成: {output_path}")
    print(f"综合评分: {results['total_score']:.1f}% ({grade_name})")


def main():
    parser = argparse.ArgumentParser(description='评定测试用例覆盖率')
    parser.add_argument('--requirements', help='需求清单 JSON 文件路径')
    parser.add_argument('--test-cases', required=True, help='测试用例 JSON 文件路径')
    parser.add_argument('--features', help='功能点清单 JSON 文件路径')
    parser.add_argument('--scenarios', help='场景路径清单 JSON 文件路径')
    parser.add_argument('--code-report', help='代码覆盖率报告 JSON 文件路径')
    parser.add_argument('--defects', help='缺陷清单 JSON 文件路径')
    parser.add_argument('--output', required=True, help='输出报告文件路径')
    
    args = parser.parse_args()
    
    # 加载数据
    with open(args.test_cases, 'r', encoding='utf-8') as f:
        test_cases_data = json.load(f)
    test_cases = test_cases_data.get('test_cases', [])
    
    requirements = []
    if args.requirements:
        with open(args.requirements, 'r', encoding='utf-8') as f:
            req_data = json.load(f)
        requirements = req_data.get('requirements', [])
    
    features = []
    if args.features:
        with open(args.features, 'r', encoding='utf-8') as f:
            feat_data = json.load(f)
        features = feat_data.get('features', [])
    
    scenarios = []
    if args.scenarios:
        with open(args.scenarios, 'r', encoding='utf-8') as f:
            scen_data = json.load(f)
        scenarios = scen_data.get('scenarios', [])
    
    code_report = {}
    if args.code_report:
        with open(args.code_report, 'r', encoding='utf-8') as f:
            code_report = json.load(f)
    
    defects = []
    if args.defects:
        with open(args.defects, 'r', encoding='utf-8') as f:
            defect_data = json.load(f)
        defects = defect_data.get('defects', [])
    
    # 逐维度评定
    dimensions = {}
    
    # 1. 需求覆盖率
    req_score, req_issues, req_details = evaluate_requirements_coverage(requirements, test_cases)
    dimensions['requirements'] = {
        'score': req_score,
        'weighted': req_score * WEIGHTS['requirements'],
        'issues': req_issues,
        'details': req_details,
    }
    
    # 2. 功能维度覆盖率
    feat_score, feat_issues, feat_details = evaluate_feature_coverage(features, test_cases)
    dimensions['feature_dimensions'] = {
        'score': feat_score,
        'weighted': feat_score * WEIGHTS['feature_dimensions'],
        'issues': feat_issues,
        'details': feat_details,
    }
    
    # 3. 场景路径覆盖率
    scen_score, scen_issues, scen_details = evaluate_scenario_coverage(scenarios, test_cases)
    dimensions['scenario_paths'] = {
        'score': scen_score,
        'weighted': scen_score * WEIGHTS['scenario_paths'],
        'issues': scen_issues,
        'details': scen_details,
    }
    
    # 4. 代码覆盖率
    code_score, code_issues, code_details = evaluate_code_coverage(code_report)
    dimensions['code_coverage'] = {
        'score': code_score,
        'weighted': code_score * WEIGHTS['code_coverage'],
        'issues': code_issues,
        'details': code_details,
    }
    
    # 5. 缺陷回归覆盖率
    defect_score, defect_issues, defect_details = evaluate_defect_coverage(defects, test_cases)
    dimensions['defect_regression'] = {
        'score': defect_score,
        'weighted': defect_score * WEIGHTS['defect_regression'],
        'issues': defect_issues,
        'details': defect_details,
    }
    
    # 6. 用例质量（作为参考，不计入综合评分）
    quality_score, quality_issues, quality_details = evaluate_case_quality(test_cases)
    dimensions['case_quality'] = {
        'score': quality_score,
        'weighted': 0,
        'issues': quality_issues,
        'details': quality_details,
    }
    
    # 计算综合评分（只计前5个维度）
    total_score = sum(
        dimensions[dim]['weighted']
        for dim in ['requirements', 'feature_dimensions', 'scenario_paths', 'code_coverage', 'defect_regression']
    )
    
    results = {
        'total_score': total_score,
        'dimensions': dimensions,
    }
    
    # 生成报告
    generate_report(results, args.output)


if __name__ == '__main__':
    main()

---
name: test-case-generator
description: >
  Generates comprehensive test cases from requirement documents. Use this skill whenever the user provides a requirement document (PRD, spec, user story, feature description) and wants to create test cases, test scenarios, or a test plan. Make sure to use this skill when the user mentions "test case", "test scenario", "test design", "test coverage", "QA plan", "testing strategy", or wants to analyze requirements for testing purposes. Also trigger when the user asks to identify edge cases, boundary conditions, or exception scenarios from a requirement. Outputs structured test cases in Excel/CSV format with multiple sheets for different test types.
---

# Test Case Generator

This skill helps you generate comprehensive test cases from requirement documents, outputting them as structured Excel files with multiple sheets.

## Workflow

### Step 1: 分析需求文档

读取用户提供的需求文档，提取：
- **功能需求**：系统应该做什么
- **非功能需求**：性能、安全、可用性约束
- **用户角色/权限**：不同访问级别
- **数据实体**：关键数据对象及关系
- **业务规则**：验证规则、计算逻辑、工作流
- **集成点**：API、外部系统、第三方服务

如果文档不清晰或缺少关键信息，在继续之前询问澄清问题。

### Step 2: 设计测试场景

基于分析结果，应用以下测试设计方法（选择所有适用的）：

1. **等价类划分**：识别有效和无效输入类别
2. **边界值分析**：覆盖输入边界处的边缘情况
3. **决策表测试**：适用于多条件组合的复杂业务逻辑
4. **状态转换测试**：适用于有明确状态变化的工作流
5. **用户旅程测试**：从用户视角的端到端流程
6. **异常场景**：网络失败、数据错误、权限拒绝、超时场景
7. **探索式测试启发**：异常组合、竞态条件、并发操作

按功能模块或用户旅程组织场景。

### Step 3: 生成详细测试用例

为每个场景生成测试用例，包含以下字段：

| 字段 | 说明 |
|------|------|
| 用例ID | 自动生成：TC-{模块}-{序号} (如 TC-LOGIN-001) |
| 测试场景/模块 | 所属场景或模块 |
| 用例标题 | 简洁描述测试内容 |
| 前置条件 | 执行前需满足的条件 |
| 测试步骤 | 编号的步骤说明 |
| 预期结果 | 每步或最终的预期结果 |
| 优先级 | P0(关键), P1(高), P2(中), P3(低) |
| 测试类型 | 功能/UI/API/边界/异常/性能/安全 |
| 实际结果 | 空 - 供测试执行时填写 |
| 状态 | 默认："Not Run" |
| 测试数据 | 具体使用的输入值 |

### Step 4: 生成 Excel 文件

使用内置脚本生成 Excel 文件：

```bash
python scripts/generate_test_cases.py \
  --test-cases <test-cases-json> \
  --template assets/test_case_template.xlsx \
  --output <output-path.xlsx>
```

脚本将：
- 创建按测试类型或模块组织的多 Sheet
- 应用一致的格式化和样式
- 自动生成用例 ID
- 包含统计摘要页

### Step 5: 交付给用户

提供生成的 Excel 文件和简要摘要，包括：
- 测试用例总数
- 按优先级分布 (P0/P1/P2/P3)
- 按测试类型分布
- 覆盖说明（已覆盖什么，可能需要手动补充什么）

## Excel 输出结构

Excel 文件包含以下 Sheet：

1. **Summary**：统计概览
2. **功能测试**：核心功能测试用例
3. **边界测试**：边界值测试用例
4. **异常测试**：错误处理和边缘场景
5. **用户旅程**：端到端工作流测试
6. **API测试**：接口级测试（如适用）
7. **测试数据**：测试执行参考数据

## 质量准则

- **完整性**：每个需求至少有一个正向和一个反向测试用例
- **独立性**：每个测试用例应可独立执行（尽可能）
- **可追溯性**：测试用例可追溯到具体需求
- **可维护性**：语言清晰简洁，任何测试人员都能理解
- **优先级划分**：P0 覆盖关键路径，P3 覆盖锦上添花场景

## 参考资料

有关测试设计技术的详细说明，请参阅 `references/test_design_methods.md`。

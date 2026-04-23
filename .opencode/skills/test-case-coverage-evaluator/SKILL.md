---
name: test-case-coverage-evaluator
description: >
  Evaluates test case coverage quality and completeness. Use this skill whenever the user wants to assess how well their test cases cover requirements, features, scenarios, or code. Make sure to use this skill when the user mentions "coverage", "test coverage", "coverage rate", "coverage analysis", "coverage evaluation", "test completeness", "漏测", "覆盖率", "测试覆盖", or wants to review if their test cases are comprehensive enough. Also trigger when the user asks to evaluate test quality, identify coverage gaps, calculate coverage metrics, or generate coverage reports. Supports multiple coverage dimensions: requirements-to-cases, feature dimensions, scenario paths, code coverage, defect regression, and test case quality.
---

# Test Case Coverage Evaluator

This skill provides a comprehensive framework for evaluating test case coverage across six dimensions, producing a weighted score and actionable recommendations.

## Coverage Dimensions

### 1. 需求→用例覆盖 (Requirements-to-Cases Coverage)

**衡量**：每个需求是否都有用例对应

**公式**：
```
需求用例覆盖率 = 已关联用例的需求数 / 总需求数 × 100%
```

**关键做法**：
- 建立需求追踪矩阵（需求 ↔ 用例的双向映射）
- 每个需求至少关联 1 个正向用例 + 1 个反向用例
- **100% 是底线**——有需求没用例，就是漏测风险

**检查清单**：
- [ ] 所有需求都有对应的用例
- [ ] 每个需求至少有 1 个正向用例
- [ ] 每个需求至少有 1 个反向/异常用例
- [ ] 需求变更已同步更新用例

---

### 2. 功能点→用例覆盖 (Feature Dimensions Coverage)

**衡量**：每个功能点的各个维度是否都被用例覆盖

**覆盖维度**：

| 维度 | 说明 |
|------|------|
| 正向流程 | 正常输入、正常操作 |
| 反向流程 | 异常输入、错误操作 |
| 边界值 | 最大值、最小值、临界点 |
| 权限/角色 | 不同角色的访问控制 |
| 数据状态 | 空数据、脏数据、并发 |
| 兼容性 | 浏览器、设备、系统 |

**评定方式**：对每个功能点打分，如 6 个维度覆盖了 5 个 = 83%

---

### 3. 场景路径覆盖 (Scenario Path Coverage)

**衡量**：用户实际使用路径是否都被用例覆盖

**公式**：
```
场景覆盖率 = 已覆盖的场景路径数 / 应覆盖的场景路径总数 × 100%
```

**场景路径识别**：
- **主流程路径**（必须覆盖）
- **分支/异常路径**（应该覆盖）
- **边缘场景路径**（评估后决定是否覆盖）

---

### 4. 代码→用例覆盖 (Code Coverage)

**衡量**：用例实际执行了多少代码

**公式**：
```
代码覆盖率 = 用例执行覆盖的代码行数 / 总可执行代码行数 × 100%
```

**注意**：
- 这是用工具跑出来的数据（如 JaCoCo、Istanbul、Coverage.py）
- 代码覆盖率低 → 说明用例集可能不够充分
- 代码覆盖率高 → 不代表用例质量好（可能执行了但没验证）
- **这是辅助指标，不能替代需求覆盖分析**

---

### 5. 缺陷→用例覆盖 (Defect Regression Coverage)

**衡量**：历史 bug 是否都有对应的回归用例

**公式**：
```
缺陷用例覆盖率 = 已有关联回归用例的缺陷数 / 总已修复缺陷数 × 100%
```

**关键**：每个修复的 bug 都应该有一条回归用例，这是防止回归的最有效手段。

---

### 6. 测试用例自身质量覆盖 (Test Case Quality)

**衡量**：用例本身是否具备有效性

**检查每个用例是否满足**：
- ✅ 有明确的前置条件
- ✅ 有清晰的测试步骤
- ✅ 有可验证的预期结果
- ✅ 预期结果包含具体断言（不是"应该正常"这种模糊描述）
- ✅ 用例独立可执行（不依赖其他用例的执行顺序）

**公式**：
```
质量覆盖率 = 满足所有条件的用例数 / 总用例数
```

---

## 综合评定框架

### 加权评分公式

```
综合评分 =
    需求覆盖率 × 30%  （权重最高，方向性指标）
  + 功能维度覆盖率 × 25%
  + 场景路径覆盖率 × 20%
  + 代码覆盖率 × 15%  （辅助指标）
  + 缺陷回归覆盖率 × 10%
```

### 分级标准

| 综合评分 | 等级 | 含义 |
|----------|------|------|
| ≥ 90% | 优秀 | 可以发布 |
| 80-89% | 良好 | 核心路径已覆盖，可发布 |
| 70-79% | 合格 | 有漏测风险，谨慎发布 |
| < 70% | 不足 | 补充用例后再发布 |

---

## Workflow

### Step 1: 收集输入数据

从用户处获取以下信息（根据实际情况，有些可能不可用）：

1. **需求清单**：功能需求列表或需求文档
2. **测试用例集**：现有的测试用例（Excel、CSV、或文档形式）
3. **功能点列表**：系统功能模块清单
4. **场景路径**：用户操作流程图或描述
5. **代码覆盖率报告**（可选）：来自 Coverage.py、JaCoCo 等工具
6. **缺陷列表**（可选）：历史 bug 清单及修复状态

### Step 2: 逐维度评定

对每个维度进行独立分析：

1. **需求→用例**：建立需求追踪矩阵，检查覆盖情况
2. **功能维度**：对每个功能点检查 6 个维度
3. **场景路径**：识别主流程、分支、边缘场景
4. **代码覆盖**：分析代码覆盖率报告（如提供）
5. **缺陷回归**：检查历史 bug 是否有回归用例
6. **用例质量**：抽查用例的有效性

### Step 3: 计算综合评分

使用加权公式计算综合评分，并给出等级评定。

### Step 4: 生成评定报告

输出包含以下内容的报告：

```
# 测试用例覆盖率评定报告

## 概要
- 评定日期：YYYY-MM-DD
- 综合评分：XX%
- 等级：优秀/良好/合格/不足

## 各维度得分
| 维度 | 得分 | 权重 | 加权分 |
|------|------|------|--------|
| 需求覆盖率 | XX% | 30% | XX% |
| 功能维度覆盖率 | XX% | 25% | XX% |
| 场景路径覆盖率 | XX% | 20% | XX% |
| 代码覆盖率 | XX% | 15% | XX% |
| 缺陷回归覆盖率 | XX% | 10% | XX% |

## 发现的问题
1. [问题描述] - [严重程度]
2. ...

## 改进建议
1. [具体建议]
2. ...

## 详细分析
### 需求追踪矩阵
...

### 功能维度覆盖详情
...

### 场景路径覆盖详情
...
```

---

## 常见误区提醒

在评定时注意以下误区：

1. **用例数量多 ≠ 覆盖率高** — 100 条重复测同一件事的用例，覆盖率为 0
2. **需求覆盖率 100% 是必须的** — 不是"越高越好"，是"必须达到"
3. **代码覆盖率是辅助** — 它告诉你用例执行了什么，但不能替代需求覆盖分析
4. **覆盖率是动态的** — 需求变了、功能加了，覆盖率也要重新评估

---

## 使用脚本辅助评定

可以使用内置脚本生成评定报告模板：

```bash
python scripts/evaluate_coverage.py \
  --requirements <requirements-file> \
  --test-cases <test-cases-file> \
  --output <report-output.md>
```

---

## 参考资料

- `references/coverage_best_practices.md` — 覆盖率评定最佳实践
- `assets/coverage_report_template.md` — 评定报告模板

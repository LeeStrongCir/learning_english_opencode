# 使用场景示例

## 场景 1：需求评审前快速分析

**背景**: 明天要开需求评审会，今天拿到需求文档

```bash
# 快速分析，带着问题参会
openclaw skill run test-requirement-analyzer \
  --document ./requirements/用户中心 v2.0.md \
  --output-format markdown \
  > analysis-report.md

# 打开报告，重点关注"需求问题清单"
cat analysis-report.md
```

**价值**: 
- 提前发现需求漏洞，评审会上提问
- 避免评审会后才发现问题，需要二次评审
- 展现测试的专业性

---

## 场景 2：批量分析多个需求

**背景**: 一个大版本有 10+ 个需求文档

```bash
# 写个脚本批量分析
for file in ./requirements/v2.0/*.md; do
  echo "分析 $file..."
  openclaw skill run test-requirement-analyzer \
    --document "$file" \
    --output-format json \
    > "analysis/$(basename $file .md).json"
done

# 汇总分析结果
node scripts/summarize.js analysis/
```

**价值**:
- 快速了解整个版本的测试工作量
- 识别跨需求的风险和依赖
- 为测试计划提供数据支持

---

## 场景 3：与 OpenCode 联动

**背景**: 在 OpenCode 中开发时，需要快速理解需求

```bash
# 在 OpenCode 终端中
/opencode run openclaw skill run test-requirement-analyzer \
  --document ./requirements/支付模块.md \
  --output-format markdown
```

**价值**:
- 开发过程中随时回顾测试要点
- 实现时注意高风险区域
- 减少返工

---

## 场景 4：测试计划输入

**背景**: 编写测试计划需要测试范围和优先级

```bash
# 分析需求
openclaw skill run test-requirement-analyzer \
  --document ./requirements/订单模块.md \
  --output-format json \
  > analysis.json

# 用脚本提取关键信息到测试计划
node scripts/extract-for-test-plan.js analysis.json > test-plan-input.md

# 基于输入编写测试计划
```

**价值**:
- 测试计划的范围定义有依据
- 优先级评估有数据支持
- 减少拍脑袋决策

---

## 场景 5：需求变更影响分析

**背景**: 需求有变更，需要评估对测试的影响

```bash
# 分析变更后的需求
openclaw skill run test-requirement-analyzer \
  --document ./requirements/订单模块 v1.2.md \
  --output-format json \
  > analysis-v1.2.json

# 对比前后版本（需要额外脚本）
node scripts/compare-analysis.js analysis-v1.1.json analysis-v1.2.json
```

**价值**:
- 快速识别变更影响的测试点
- 评估是否需要补充用例
- 为回归测试范围提供依据

---

## 场景 6：新人培训

**背景**: 新测试加入团队，学习如何分析需求

```bash
# 让新人先自己分析
# 然后用 skill 分析同一份需求
openclaw skill run test-requirement-analyzer \
  --document ./requirements/示例需求.md \
  --output-format markdown

# 对比差异，讨论为什么 skill 发现了某些问题
```

**价值**:
- 学习测试分析的思维方法
- 理解什么是"质疑思维"
- 快速提升需求分析能力

---

## 场景 7：跨团队对齐

**背景**: 产品、开发、测试对需求理解不一致

```bash
# 用 skill 分析需求，作为讨论基础
openclaw skill run test-requirement-analyzer \
  --document ./requirements/共享需求.md \
  --output-format markdown \
  > shared-analysis.md

# 在评审会上基于报告讨论
# "skill 识别了这些风险，大家看看有没有遗漏"
```

**价值**:
- 有客观的第三方视角
- 减少"我以为"的误解
- 提高评审效率

---

## 场景 8：测试复盘输入

**背景**: 项目结束后复盘，分析哪些漏测了

```bash
# 用 skill 重新分析需求
openclaw skill run test-requirement-analyzer \
  --document ./requirements/已上线功能.md \
  --output-format json \
  > post-mortem-analysis.json

# 对比实际 bug，看 skill 是否识别了相关风险
# 如果识别了但没测 → 测试执行问题
# 如果没识别 → 优化 skill 的 prompt
```

**价值**:
- 发现测试过程的改进点
- 优化 skill 的分析能力
- 形成正向循环

---

## 提示

1. **不要完全依赖 AI**: skill 的输出一定要人工 review
2. **重点关注问题清单**: 这是最有价值的部分
3. **持续优化**: 根据实际效果调整 skill 的 prompt
4. **结合上下文**: skill 不了解你们团队的特殊约定，需要人工补充

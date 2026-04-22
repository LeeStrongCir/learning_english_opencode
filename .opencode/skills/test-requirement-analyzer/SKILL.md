# test-requirement-analyzer

需求测试分析专家 - 基于 10+ 年测试经验沉淀的 AI 分析技能

## 功能

自动分析软件需求文档，输出：
- **测试目标**：明确要验证什么
- **测试范围**：测什么、不测什么
- **优先级评估**：P0/P1/P2 分级
- **风险识别**：潜在问题点
- **测试建议**：推荐的测试类型和方法

## 核心能力

1. **质疑思维**：发现需求本身的问题和漏洞
2. **场景化分析**：从用户视角还原完整使用场景
3. **风险嗅觉**：识别高风险区域，指导资源分配

## 使用方法

### OpenClaw 调用

```bash
# 基础用法
openclaw skill run test-requirement-analyzer --document ./requirements/v1.2.md

# 完整参数
openclaw skill run test-requirement-analyzer \
  --document ./requirements/v1.2.md \
  --project-name "我的项目" \
  --output-format markdown \
  --save-to-ontology false
```

### OpenCode 调用

在 OpenCode 终端中：

```bash
# 方式 1：通过 openclaw 命令
/opencode run openclaw skill run test-requirement-analyzer --document ./requirements.md

# 方式 2：直接调用脚本（如果配置了 PATH）
test-requirement-analyzer ./requirements.md

# 方式 3：在 OpenCode 对话中
"帮我分析这个需求文档：./requirements.md"
```

### 对话调用

直接在聊天中说：
- "帮我分析这个需求文档：./requirements/v1.2.md"
- "分析这个需求的测试范围：[粘贴需求内容]"

## 参数说明

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--document` | ✅ | 需求文档路径（本地文件或 URL） | - |
| `--project-name` | ❌ | 项目名称（用于 Ontology 存储） | 从文档提取 |
| `--output-format` | ❌ | 输出格式：markdown/json/both | markdown |
| `--save-to-ontology` | ❌ | 是否存储到 Ontology | false |
| `--include-prompt` | ❌ | 是否在输出中包含使用的 prompt | false |

## 输出结构

```markdown
# 需求测试分析报告

## 1. 需求概述
- 项目名称
- 需求版本
- 分析时间

## 2. 测试目标
- [OBJ-001] 目标描述（优先级：P0）
- [OBJ-002] 目标描述（优先级：P1）

## 3. 测试范围
### 3.1 范围内
- 功能点 A
- 功能点 B

### 3.2 范围外
- 明确不测试的内容

## 4. 优先级评估
### P0（必须测试）
- 核心功能列表

### P1（应该测试）
- 次要功能列表

### P2（可以测试）
- 边缘功能列表

## 5. 风险识别
- ⚠️ 高风险：xxx
- ⚠️ 中风险：xxx

## 6. 测试建议
- 推荐的测试类型
- 重点关注的场景

## 7. 需求问题清单
- ❓ 待澄清问题 1
- ❓ 待澄清问题 2
```

## 输出示例

```json
{
  "test_objectives": [
    {
      "id": "OBJ-001",
      "description": "验证用户登录功能的正确性",
      "priority": "P0",
      "related_requirements": ["REQ-001", "REQ-002"],
      "acceptance_criteria": ["..."]
    }
  ],
  "test_scope": {
    "in_scope": ["功能 A", "功能 B"],
    "out_of_scope": ["功能 X"]
  },
  "priorities": {
    "P0": ["核心登录流程"],
    "P1": ["次要功能"],
    "P2": ["UI 优化"]
  },
  "risks": [
    {
      "level": "high",
      "description": "依赖第三方短信服务",
      "mitigation": "准备 mock 服务"
    }
  ],
  "questions": ["需求问题 1", "需求问题 2"],
  "suggested_test_types": ["功能测试", "接口测试"]
}
```

## 依赖

- Node.js v18+
- OpenClaw runtime
- LLM Provider（已在 OpenClaw 中配置）

## 文件结构

```
test-requirement-analyzer/
├── SKILL.md           # 技能说明（本文件）
├── index.js           # 主程序入口
├── prompts/
│   ├── analyzer.js    # 分析 prompt 模板
│   └── critic.js      # 质疑 prompt 模板
├── lib/
│   ├── parser.js      # 文档解析器
│   ├── analyzer.js    # 分析引擎
│   └── formatter.js   # 输出格式化
└── examples/
    └── sample-output.md
```

## 核心分析逻辑

### 1. 需求理解
- 提取业务背景、目标用户、核心功能
- 识别输入输出、业务规则、依赖关系

### 2. 质疑分析
- 发现模糊描述（"大概""可能""尽量"）
- 识别矛盾点
- 发现缺失信息

### 3. 场景还原
- 正常流程（Happy Path）
- 异常流程（Exception）
- 边界场景（Boundary）

### 4. 风险评估
- 基于业务影响 × 发生概率
- 识别技术风险、依赖风险、变更风险

## 最佳实践

1. **人机协作**：Agent 分析 + 人工 review + 确认发布
2. **持续优化**：根据实际 bug 反馈优化分析 prompt
3. **知识沉淀**：将分析结果存储到 Ontology，支持追溯

## 版本

- v1.0.0 - 初始版本

## 作者

臭宝 (Chou Bao) - 基于 10+ 年测试经验沉淀

## License

MIT

# test-requirement-analyzer

需求测试分析专家 - 基于 10+ 年测试经验沉淀的 AI 分析技能

## 快速开始

### OpenClaw 调用

```bash
# 基础用法
openclaw skill run test-requirement-analyzer --document ./requirements/v1.2.md

# 输出 JSON 格式
openclaw skill run test-requirement-analyzer -d ./req.md -o json

# 保存到 Ontology
openclaw skill run test-requirement-analyzer -d ./req.md --save-to-ontology
```

### OpenCode 调用

在 OpenCode 终端中，有三种方式：

#### 方式 1：通过 openclaw 命令（推荐）

```bash
/opencode run openclaw skill run test-requirement-analyzer --document ./requirements.md
```

#### 方式 2：直接调用脚本

```bash
# 先安装到全局
cd ~/.openclaw/workspace/skills/test-requirement-analyzer
npm link

# 然后直接调用
test-requirement-analyzer ./requirements.md
```

#### 方式 3：在 OpenCode 对话中

```
/opencode 帮我分析这个需求文档：./requirements.md
```

OpenCode 会自动调用这个 skill 进行分析。

### 对话调用

在 OpenClaw 聊天中直接说：
- "帮我分析这个需求文档：./requirements/v1.2.md"
- "分析这个需求的测试范围：[粘贴需求内容]"

## 输出示例

```markdown
# 需求测试分析报告

## 1. 测试目标
- [OBJ-001] 验证用户登录功能的正确性（优先级：P0）
- [OBJ-002] 验证异常登录场景的处理（优先级：P0）

## 2. 测试范围
### 范围内
- 账号密码登录
- 手机验证码登录

### 范围外
- 注册功能
- 找回密码功能

## 3. 优先级评估
### P0（必须测试）
- 正确账号密码登录成功
- 密码错误提示

## 4. 风险识别
- 🔴 dependency: 依赖第三方短信服务

## 5. 需求问题清单
- [Q-001] ❓ 模糊描述：需求中说"登录响应时间要快"

## 6. 测试建议
- 推荐测试类型：功能测试、接口测试

## 7. 分析总结
...
```

## 核心能力

1. **质疑思维**：发现需求本身的问题和漏洞
2. **场景化分析**：从用户视角还原完整使用场景  
3. **风险嗅觉**：识别高风险区域，指导资源分配

## 分析维度

- 测试目标识别
- 测试范围界定
- 优先级评估（P0/P1/P2）
- 风险识别（技术/依赖/变更/数据）
- 需求问题清单
- 测试建议

## 文件结构

```
test-requirement-analyzer/
├── SKILL.md           # 技能说明
├── index.js           # 主程序
├── opencode.json      # OpenCode 配置
├── README.md          # 使用说明
├── examples/
│   └── sample-output.md
└── prompts/           # Prompt 模板（可扩展）
```

## 最佳实践

1. **人机协作**：Agent 分析 + 人工 review + 确认发布
2. **尽早使用**：需求评审前先用 skill 分析，带着问题参会
3. **持续优化**：根据实际 bug 反馈优化分析 prompt
4. **知识沉淀**：将分析结果归档，支持后续追溯

## 与 OpenCode 集成

本 skill 设计为同时兼容 OpenClaw 和 OpenCode：

- **OpenClaw**: 作为 skill 运行，支持完整的参数和输出格式
- **OpenCode**: 可通过命令调用或对话触发

未来可以扩展：
- OpenCode 插件形式集成
- 在 OpenCode 中直接显示分析结果
- 与 OpenCode 的代码分析能力联动

## 版本

- v1.0.0 - 初始版本

## 作者

臭宝 (Chou Bao) 😜

## License

MIT

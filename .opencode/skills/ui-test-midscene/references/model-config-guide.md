# 模型配置指南

Midscene.js 依赖视觉语言模型（VLM）来理解页面截图并执行操作。本 Skill **仅支持通过环境变量配置模型**。

## 配置方式

设置以下 4 个环境变量：

```bash
export MIDSCENE_MODEL_BASE_URL="你的模型 API 端点"
export MIDSCENE_MODEL_API_KEY="你的 API 密钥"
export MIDSCENE_MODEL_NAME="模型名称"
export MIDSCENE_MODEL_FAMILY="模型家族"
```

### 方式 A：终端直接设置

```bash
export MIDSCENE_MODEL_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MIDSCENE_MODEL_API_KEY="sk-xxx"
export MIDSCENE_MODEL_NAME="qwen3-vl-plus"
export MIDSCENE_MODEL_FAMILY="qwen3-vl"
```

### 方式 B：.env 文件（推荐）

在项目根目录创建 `.env` 文件：

```
MIDSCENE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MIDSCENE_MODEL_API_KEY=sk-xxx
MIDSCENE_MODEL_NAME=qwen3-vl-plus
MIDSCENE_MODEL_FAMILY=qwen3-vl
```

运行测试脚本时会自动加载 `.env` 文件中的配置。

---

## 常用模型配置示例

```
MIDSCENE_MODEL_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MIDSCENE_MODEL_API_KEY=sk-xxx
MIDSCENE_MODEL_NAME=qwen3-vl-plus
MIDSCENE_MODEL_FAMILY=qwen3-vl
```

---

## 环境变量说明

| 变量 | 说明 | 示例 |
|------|------|------|
| `MIDSCENE_MODEL_BASE_URL` | API 端点 URL | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `MIDSCENE_MODEL_API_KEY` | API 密钥 | `sk-xxx` |
| `MIDSCENE_MODEL_NAME` | 模型名称 | `qwen3-vl-plus` |
| `MIDSCENE_MODEL_FAMILY` | 模型家族（影响内部处理策略） | `qwen3-vl` |

---

## 排查问题

### 模型调用失败

1. 检查 `MIDSCENE_MODEL_BASE_URL` 是否正确
2. 检查 `MIDSCENE_MODEL_API_KEY` 是否有效
3. 确认模型名称拼写正确
4. 检查网络连通性

### 操作执行不准确

1. 尝试更换更强的模型
2. 使用 `deepLocate: true` 提高定位精度
3. 提供更详细的自然语言描述
4. 使用 `aiActContext` 提供背景知识

---
name: ui-test-midscene
description: 基于 Midscene.js 的 AI 视觉驱动 UI 自动化测试。支持 Web 浏览器自然语言操作、断言验证、数据提取和 HTML 报告生成。
version: 0.1.0
alwaysApply: false
keywords:
  - ui test
  - ui 测试
  - 自动化测试
  - midscene
  - web test
  - 浏览器测试
  - 视觉测试
  - ai test
  - playwright
  - puppeteer
  - 端到端测试
  - e2e
---

# UI 自动化测试 Skill (Midscene.js)

## 触发条件

当用户提出以下需求时自动触发：
- 要求进行 Web UI 自动化测试
- 需要测试网页功能、表单、交互流程
- 需要视觉验证和断言
- 需要生成 UI 测试报告
- 提到 "UI 测试"、"浏览器测试"、"自动化测试"、"端到端测试"

## 核心能力

| 能力 | API | 说明 |
|------|-----|------|
| 自然语言操作 | `aiAct()` | AI 自动规划并执行 UI 操作序列 |
| 原子操作 | `aiTap()` / `aiInput()` / `aiScroll()` | 精确定位并执行单一操作 |
| 断言验证 | `aiAssert()` | AI 判断页面状态是否符合预期 |
| 数据提取 | `aiQuery()` / `aiBoolean()` / `aiNumber()` / `aiString()` | 从页面提取结构化数据 |
| 元素定位 | `aiLocate()` | 用自然语言定位页面元素 |
| 等待条件 | `aiWaitFor()` | 等待页面状态满足条件 |
| 报告生成 | 自动 | 每次执行生成 HTML 可视化报告 |

## 快速开始

### 1. 环境检查

执行前必须确认：
- Node.js >= 18
- 已安装 Playwright 浏览器（`npx playwright install chromium`）
- 已配置 AI 模型环境变量（见下方模型配置）

### 2. 初始化测试项目

```bash
node <skill_dir>/scripts/init-test.js <project-name>
```

此脚本会：
- 在 `test-artifacts/{project-name}/06-ui-tests/v1/` 创建目录结构
- 生成 `package.json` 和 `playwright.config.js`
- 生成示例测试文件 `scenarios/login-test.js`

### 3. 编写测试脚本

测试脚本使用 Playwright + Midscene.js 编写，核心模式：

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('用户登录测试', async ({ page }) => {
  const agent = new PlaywrightAgent(page);

  // 导航到目标页面
  await page.goto('https://example.com/login');

  // 方式 A：AI 自动规划（适合简单线性流程）
  await agent.aiAct('输入用户名 testuser，输入密码 testpass，点击登录按钮');

  // 方式 B：手动分步（适合复杂逻辑和精确控制）
  await agent.aiInput('用户名输入框', { value: 'testuser' });
  await agent.aiInput('密码输入框', { value: 'testpass' });
  await agent.aiTap('登录按钮');

  // 断言验证
  await agent.aiAssert('页面显示欢迎信息或跳转到了首页');

  // 数据提取
  const userInfo = await agent.aiQuery('{username: string, role: string}');
  console.log('用户信息:', userInfo);
});
```

### 4. 执行测试

```bash
cd test-artifacts/{project-name}/06-ui-tests/v1/
npx playwright test
```

测试报告自动生成到 `midscene_run/report/` 目录。

## 两种测试模式

### 模式 A：Auto Planning（自动规划）

AI 自动拆分步骤并执行，适合简单线性流程。

```javascript
// 一条指令完成整个流程
await agent.aiAct('打开登录页面，填写用户名和密码，点击登录，验证登录成功');
```

**优点**：代码简洁，AI 自动处理细节
**缺点**：依赖模型质量，复杂流程可能出错
**适用**：3-5 步以内的简单流程

### 模式 B：Workflow（工作流）

手动分步控制，适合复杂逻辑。

```javascript
// 提取数据
const items = await agent.aiQuery('string[], 商品列表名称');

// 条件分支
for (const item of items) {
  const price = await agent.aiNumber(`"${item}" 的价格数字`);
  if (price > 100) {
    await agent.aiTap(`"${item}" 的加入购物车按钮`);
  }
}

// 断言验证
await agent.aiAssert('购物车中至少有 1 件商品');
```

**优点**：精确控制，支持循环和条件
**缺点**：代码量较大
**适用**：多步骤、有分支逻辑的复杂流程

## 模型配置

Midscene.js 依赖视觉语言模型（VLM），**仅支持通过环境变量配置**。

详细配置方法见 [模型配置指南](references/model-config-guide.md)。

快速配置（终端执行）：

```bash
export MIDSCENE_MODEL_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MIDSCENE_MODEL_API_KEY="sk-你的密钥"
export MIDSCENE_MODEL_NAME="qwen3-vl-plus"
export MIDSCENE_MODEL_FAMILY="qwen3-vl"
```

## 与测试流程集成

本 Skill 在测试流程中的定位：

```
阶段 3：@test-automation 自动化实现
    ↓
使用本 Skill 创建 UI 测试脚本
    ↓
保存到 test-artifacts/{project}/06-ui-tests/v{version}/
    ↓
阶段 4：@test-executor 测试执行
    ↓
运行 Playwright + Midscene 测试
    ↓
生成 HTML 报告到 midscene_run/report/
```

### 产物保存路径

| 产物 | 路径 |
|------|------|
| 测试脚本 | `06-ui-tests/v{version}/tests/*.spec.js` |
| 场景定义 | `06-ui-tests/v{version}/scenarios/*.yaml` |
| HTML 报告 | `06-ui-tests/v{version}/midscene_run/report/` |
| 执行日志 | `06-ui-tests/v{version}/midscene_run/` |
| 截图 | `06-ui-tests/v{version}/midscene_run/report/assets/` |

## 常见问题

### Q: 元素定位不准怎么办？
A: 使用 `deepLocate: true` 选项提高定位精度：
```javascript
await agent.aiTap('右上角的设置图标', { deepLocate: true });
```

### Q: 页面加载慢导致操作失败？
A: 使用 `aiWaitFor` 等待条件满足：
```javascript
await agent.aiWaitFor('页面加载完成，出现主要内容区域', { timeoutMs: 30000 });
```

### Q: 如何验证不可见的属性（如链接 URL）？
A: 使用 `domIncluded: true`：
```javascript
const link = await agent.aiString('登录按钮的链接地址', { domIncluded: true });
```

### Q: 跨页面跳转后测试中断？
A: Midscene.js 支持跨页导航，无需特殊处理。PlaywrightAgent 会自动跟踪页面变化。

## 参考文档

- [Midscene API 速查](references/midscene-api-reference.md)
- [模型配置指南](references/model-config-guide.md)
- [测试模式最佳实践](references/test-patterns.md)

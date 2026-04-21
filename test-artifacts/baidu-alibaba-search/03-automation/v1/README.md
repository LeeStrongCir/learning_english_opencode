# 百度搜索阿里巴巴 - UI 自动化测试

## 项目概述

本项目使用 **Playwright + Midscene.js** 框架，实现百度搜索"阿里巴巴"并进入阿里巴巴官网的端到端 UI 自动化测试。

### 测试目标

- 验证通过百度搜索"阿里巴巴"能够正确显示搜索结果
- 验证能够成功点击进入阿里巴巴官方网站
- 验证官网页面内容完整性
- 验证搜索建议、特殊字符输入、空搜索等边界场景

### 测试用例覆盖

| 用例编号 | 用例名称 | 优先级 | 状态 |
|----------|----------|--------|------|
| TC001 | 正常搜索流程（完整端到端） | P0 | ✅ 已实现 |
| TC002 | 回车键执行搜索 | P0 | ✅ 已实现 |
| TC003 | 官网链接识别验证 | P0 | ✅ 已实现 |
| TC004 | 官网链接点击跳转验证 | P0 | ✅ 已实现 |
| TC005 | 官网页面内容完整性验证 | P0 | ✅ 已实现 |
| TC006 | 搜索框中文输入验证 | P0 | ✅ 已实现 |
| TC007 | 搜索结果排序验证 | P1 | ✅ 已实现 |
| TC008 | 搜索建议/联想验证 | P2 | ✅ 已实现 |
| TC021 | 搜索框清空重搜验证 | P2 | ✅ 已实现 |
| TC022 | 搜索框输入特殊字符验证 | P2 | ✅ 已实现 |
| TC023 | 空搜索验证 | P2 | ✅ 已实现 |
| TC025 | 整体操作流程时间验证 | P1 | ✅ 已实现 |

## 环境要求

- **Node.js**: >= 18.0.0
- **npm**: >= 9.0.0
- **操作系统**: Linux / macOS / Windows
- **浏览器**: Chromium（Playwright 自动管理）
- **AI 模型**: 需要配置 Midscene.js 视觉语言模型（VLM）

## 快速开始

### 1. 安装依赖

```bash
cd test-artifacts/baidu-alibaba-search/03-automation/v1/
npm install
```

### 2. 安装 Playwright 浏览器

```bash
npx playwright install chromium
```

### 3. 配置 AI 模型

Midscene.js 依赖视觉语言模型进行页面理解和操作。需要配置以下环境变量：

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
```

#### 环境变量说明

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `MIDSCENE_MODEL_BASE_URL` | AI 模型 API 地址 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| `MIDSCENE_MODEL_API_KEY` | API 密钥 | `sk-你的密钥` |
| `MIDSCENE_MODEL_NAME` | 模型名称 | `qwen3-vl-plus` |
| `MIDSCENE_MODEL_FAMILY` | 模型系列 | `qwen3-vl` |

### 4. 执行测试

```bash
# 执行所有测试（无头模式）
npm test

# 有头模式执行（可以看到浏览器操作过程）
npm run test:headed

# 调试模式执行
npm run test:debug

# 执行单个测试用例
npx playwright test -g "TC001"

# 执行 P0 优先级测试
npx playwright test -g "TC001|TC002|TC003|TC004|TC005|TC006"
```

### 5. 查看测试报告

```bash
# 查看 Playwright HTML 报告
npx playwright show-report

# Midscene.js 可视化报告位于
# ./midscene_run/report/
```

## 项目结构

```
test-artifacts/baidu-alibaba-search/03-automation/v1/
├── package.json                    # 项目依赖配置
├── playwright.config.js            # Playwright 测试配置
├── .env.example                    # 环境变量模板
├── README.md                       # 本文件
├── tests/
│   └── baidu-alibaba.spec.js       # 主测试文件（包含所有测试用例）
├── fixtures/                       # 测试数据目录
├── playwright-report/              # Playwright HTML 报告输出
├── test-results/                   # JSON 测试结果输出
└── midscene_run/                   # Midscene.js 报告和截图
    └── report/
        ├── index.html              # Midscene 可视化报告
        └── assets/                 # 截图和录屏资源
```

## 测试框架说明

### Playwright + Midscene.js

本项目采用 **Playwright** 作为浏览器自动化框架，结合 **Midscene.js** 的 AI 视觉驱动能力：

| 能力 | API | 说明 |
|------|-----|------|
| 自然语言操作 | `aiAct()` | AI 自动规划并执行 UI 操作序列 |
| 原子操作 | `aiTap()` / `aiInput()` / `aiKeyboardPress()` | 精确定位并执行单一操作 |
| 断言验证 | `aiAssert()` / `aiBoolean()` | AI 判断页面状态是否符合预期 |
| 数据提取 | `aiQuery()` / `aiString()` | 从页面提取结构化数据 |
| 等待条件 | `aiWaitFor()` | 等待页面状态满足条件 |
| 原生操作 | `evaluateJavaScript()` | 执行 JavaScript 获取 URL、标题等 |

### 测试模式

- **Auto Planning（自动规划）**：使用 `aiAct()` 一条指令完成多步操作
- **Workflow（工作流）**：使用 `aiInput()` + `aiTap()` + `aiAssert()` 分步精确控制

## 测试数据

测试数据定义在 `test-data.json` 中，主要配置：

```json
{
  "search": {
    "baidu_url": "https://www.baidu.com",
    "keyword": "阿里巴巴"
  },
  "expected_results": {
    "url_pattern": "alibaba.com",
    "page_title_keywords": ["阿里巴巴", "Alibaba"],
    "official_badge_text": "官方"
  },
  "performance_thresholds": {
    "baidu_homepage_load_ms": 3000,
    "search_results_load_ms": 5000,
    "alibaba_official_load_ms": 5000,
    "total_operation_time_s": 30
  }
}
```

## 常见问题

### Q: 测试执行时 AI 操作不准确怎么办？

A: 可以尝试以下方法：
1. 增加 `deepLocate: true` 选项提高定位精度
2. 使用 `aiWaitFor()` 等待页面完全加载
3. 切换更强大的视觉语言模型

### Q: 页面加载慢导致测试超时？

A: 调整 `playwright.config.js` 中的超时配置：
```javascript
timeout: 120000,          // 全局超时
expect: { timeout: 15000 }, // 断言超时
```

### Q: 如何只运行特定的测试用例？

A: 使用 `-g` 参数过滤：
```bash
npx playwright test -g "TC001"    # 只运行 TC001
npx playwright test -g "P0"       # 运行所有 P0 用例
```

### Q: 测试失败时如何查看详细信息？

A: 查看以下输出：
- Playwright HTML 报告：`playwright-report/index.html`
- Midscene 可视化报告：`midscene_run/report/index.html`
- 失败截图和视频：`test-results/` 目录

## 维护说明

- 测试用例与 `02-test-cases/v1/test-cases-detail.md` 保持同步
- 新增测试用例时，在 `baidu-alibaba.spec.js` 中添加对应的 `test()` 函数
- 定期更新依赖版本：`npm update`

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1 | 2026-04-22 | 初始版本，实现 TC001-TC008, TC021-TC023, TC025 |

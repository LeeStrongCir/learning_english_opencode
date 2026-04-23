---
name: visual-flow-to-midscene
description: >
  基于在线流程说明网页（含连续截图）和文本测试用例，生成 Midscene.js 自动化测试脚本。
  当用户提供一个包含操作步骤截图的在线流程说明页面 URL（如：创建虚拟机的完整流程截图：列表页→弹窗→提交反馈→结果页），
  同时提供对应功能的文本测试用例时，使用此 skill。
  触发场景：用户提到"基于截图生成测试"、"流程截图转自动化"、"截图驱动测试脚本"、"SOP 截图测试"、
  "流程说明页面转脚本"、"这个网页上的截图帮我转成测试"，或提供了一个包含操作步骤截图的网页 URL 并提及要创建自动化测试。
  注意：如果只是单张截图或没有明确的测试用例输入，请先引导用户补充。
---

# Visual Flow to Midscene

本 skill 的核心能力：读取包含完整操作流程的连续截图（通常来自一个流程说明网页或 SOP 文档），结合文本测试用例，生成使用 Midscene.js 的 AI 视觉驱动自动化测试脚本。

## 适用场景

典型输入：
- **流程说明页面/文档**：包含某个功能点的完整操作截图序列。例如"创建虚拟机"流程：
  1. 虚拟机列表页截图（看到"创建虚拟机"按钮）
  2. 点击弹出创建表单的弹窗截图
  3. 填写表单并点击提交后的反馈截图
  4. 返回列表页，确认新虚拟机出现在列表中
- **对应文本测试用例**：包含操作步骤、预期结果的详细描述

典型输出：
- 可执行的 Midscene.js + Playwright 测试脚本（`.spec.js` 文件）

## 工作流程

### 第一步：获取并解析流程说明页面

用户提供的是**在线可访问的 URL**（一个包含连续截图的流程说明网页）。

使用 `webfetch` 工具读取该网页内容：

```
webfetch: url="<用户提供的URL>", format="html"
```

读取后的分析步骤：

1. **提取截图**：从 HTML 中识别所有 `<img>` 标签或内联截图。按页面上的**排列顺序**理解截图流（从上到下、从左到右）。
2. **提取说明文字**：每张截图通常配有步骤编号或说明文字（如"步骤1：进入列表页"），一并提取作为操作上下文。
3. **截图编号**：如果没有编号，按页面顺序为截图编号（截图1、截图2...），并标注每张图的视觉特征。

**如果网页内容过大无法一次性读取**：先用 `webfetch(..., format="text")` 获取纯文本结构，定位截图所在区域后再针对性读取。

### 第二步：理解截图中的页面流

依次分析每张截图，建立**视觉页面地图**：

```
页面 1/入口：虚拟机列表页
  - 关键元素："创建虚拟机"按钮、虚拟机列表表格、搜索框、分页控件
  - 页面状态：空列表 / 已有若干虚拟机

页面 2：创建虚拟机弹窗
  - 关键元素：表单字段（名称、规格、镜像、网络等）、确定按钮、取消按钮
  - 页面状态：默认值、必填项标记

页面 3：提交反馈
  - 关键元素：成功提示 Toast/Alert、加载动画、错误提示
  - 页面状态：提交成功 / 失败

页面 4：列表页（结果验证）
  - 关键元素：新创建的虚拟机出现在列表中、状态为"运行中"
  - 页面状态：列表增加一条记录
```

对每个截图页面，记录：
- **页面标识**：如何判断当前在哪个页面（URL 特征、页面标题、关键元素）
- **关键元素**：截图可见的按钮、输入框、文本、列表项
- **状态变化**：从这张图到下一张图发生了什么

**如果有多张截图**：依次分析每张图，建立页面流图（page flow），标注每张图对应的操作动作和页面跳转。

### 第三步：映射文本测试用例到页面流

将文本测试用例的每一步映射到第一步识别的对应截图页面：

```
用例步骤                        → 对应截图           → 页面操作
─────────────────────────────────────────────────────────────
1. 导航到虚拟机管理页面          → 截图1：列表页       → aiAct/aiWaitFor
2. 确认"创建虚拟机"按钮可见     → 截图1：列表页       → aiAssert
3. 点击"创建虚拟机"按钮          → 截图1→截图2         → aiTap
4. 在弹窗中填写名称为"test-vm"  → 截图2：弹窗         → aiInput
5. 选择规格为"4核8G"             → 截图2：弹窗         → aiTap(aiLocate)
6. 选择镜像为"CentOS 7.9"       → 截图2：弹窗         → aiTap(aiLocate)
7. 点击"确定"提交                → 截图2→截图3         → aiTap
8. 验证提交成功提示              → 截图3：提示         → aiAssert
9. 验证新虚拟机出现在列表中      → 截图4：列表页       → aiQuery + aiAssert
```

映射时注意：
- **截图是权威来源**：截图上看到的 UI 布局和元素是真实的。如果文本用例描述的操作与截图不匹配（例如用例说"点击新建按钮"但截图中按钮文案是"创建虚拟机"），**以截图为准**。
- **补充缺失步骤**：如果用例缺少某些中间步骤（如等待页面加载、处理弹窗关闭），从截图流中推断并补充。

### 第四步：生成 Midscene.js 脚本

使用以下模板结构生成脚本。脚本保存到 `test-artifacts/{project}/06-ui-tests/v1/` 目录下。

#### 基础模板

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test.describe('功能模块名称', () => {
  test('用例标题', async ({ page }) => {
    const agent = new PlaywrightAgent(page);

    // ===== 预置条件：导航到入口页面 =====
    await page.goto('https://your-app-url/target-page');
    await agent.aiWaitFor('页面加载完成，能看到[页面关键特征]');

    // ===== 操作步骤：截图 1 → 截图 2 =====
    // 截图1：[页面名称] - [简要描述]
    await agent.aiAssert('[截图1上验证的前置条件]');
    await agent.aiTap('[截图1中操作的元素描述]');

    // 截图2：[页面名称] - [简要描述]
    await agent.aiWaitFor('[截图2上等待的状态或元素]');

    // 多步操作
    await agent.aiInput('[表单元素描述]', { value: '测试数据' });
    await agent.aiTap('[提交按钮描述]');

    // 截图3：[页面名称] - [简要描述]
    await agent.aiAssert('[截图3上验证的结果]');

    // ===== 结果验证：截图 4 =====
    // 截图4：[页面名称] - [简要描述]
    await agent.aiAssert('[最终验证条件]');

    // 如果需要提取数据验证
    const [resultData] = await agent.aiQuery('[{数据结构描述}]');
    // console.log('提取数据:', resultData);
  });
});
```

#### 生成规则

**从截图推导操作指令（关键！）**：

1. **按钮操作**：截取按钮周围的视觉上下文来描述
   - ❌ 差的写法：`aiTap('创建按钮')`
   - ✅ 好的写法：`aiTap('页面右上区域的主按钮，文案为"创建虚拟机"，蓝色背景')`

2. **表单输入**：用 label 和 field 的视觉关系描述
   - ✅ 好的写法：`aiInput('"名称"标签右侧的文本输入框', { value: 'test-vm-001' })`

3. **下拉/选择器**：描述选择器的视觉特征 + 选项文本
   - ✅ 两步法：
     ```javascript
     await agent.aiTap('"规格"标签下方的下拉选择器');
     await agent.aiTap('下拉选项中的"4核8G"选项');
     ```

4. **断言验证**：描述截图上用户能看到的验证结果
   - ✅ 好的写法：`aiAssert('页面顶部显示绿色成功提示"创建成功"，且虚拟机列表中出现名称为"test-vm-001"的新记录')`

5. **列表数据提取**：
   ```javascript
   const vmList = await agent.aiQuery('string[], 虚拟机名称列表');
   ```

#### 模式选择

根据流程复杂度选择 Midscene.js 的操作模式：

| 流程特征 | 使用模式 | 示例 |
|---------|---------|------|
| 3-5 步线性流程，无分支 | `aiAct()` 批量指令 | `aiAct('点击创建按钮 → 填写名称 → 点击确定')` |
| 需要精确控制的步骤 | 单步 API | `aiTap()` / `aiInput()` 逐个调用 |
| 需要验证中间状态 | `aiAssert()` 插入断点 | 每步操作后加 `aiAssert()` |
| 需要循环/条件 | `aiQuery()` + 原生 JS | 提取数据后 for/if 处理 |

**推荐默认策略**：对于基于截图生成的脚本，使用**单步 API 模式**（模式 B），因为截图提供了精确定位信息，分步执行更可靠、更容易调试。

#### Playwright 配置

同时确保有正确的 `playwright.config.js`：

```javascript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  timeout: 60000,
  use: {
    baseURL: process.env.APP_URL || '',
    viewport: { width: 1920, height: 1080 },
  },
  reporter: [['list'], ['@midscene/web/playwright-reporter']],
});
```

### 第五步：项目初始化

如果目标目录不存在，先初始化项目结构：

```bash
node <skill_dir>/scripts/init-test.js <project-name>
```

或者手动创建目录结构：

```
test-artifacts/{project-name}/
└── 06-ui-tests/v1/
    ├── package.json          # 依赖：@playwright/test, @midscene/web
    ├── playwright.config.js  # Playwright 配置
    ├── tests/
    │   └── {feature-name}-test.js   # 生成的测试脚本
    └── README.md             # 运行说明
```

### 第六步：交付

向用户提供：

1. **生成的测试脚本路径和内容**
2. **截图 → 步骤映射表**（让用户确认每步操作是否正确对应截图）
3. **运行命令**：
   ```bash
   cd test-artifacts/{project}/06-ui-tests/v1/
   npm install          # 首次执行
   npx playwright test  # 运行测试
   ```
4. **注意事项**：
   - 需要根据实际环境修改 `APP_URL` 环境变量和 `page.goto()` 的 URL
   - 需要根据实际截图内容验证 `aiTap()`/`aiInput()` 中的描述是否准确
   - 测试数据（如虚拟机名称、规格选项）需要替换为真实可用的值

## 质量检查清单

生成脚本后，逐项验证：

- [ ] 每个截图页面对应至少一个 `aiAct()` 或 `aiAssert()` 或 `aiWaitFor()` 调用
- [ ] 从截图推导的元素描述使用了视觉上下文（位置、颜色、文案），而非模糊描述
- [ ] 文本用例的每一步都在脚本中有对应操作
- [ ] 每个关键操作后有对应的断言验证
- [ ] 页面状态切换（如弹窗出现/消失、页面跳转）有 `aiWaitFor()` 等待
- [ ] 如果流程涉及下拉选择器，使用了两步法（先打开下拉，再选选项）
- [ ] 脚本中的测试数据使用的是占位符，并标注了需要替换的实际值

## 参考文档

- Midscene API 速查：参见 `ui-test-midscene` skill 的 `references/midscene-api-reference.md`
- 模型配置指南：参见 `ui-test-midscene` skill 的 `references/model-config-guide.md`
- 测试模式最佳实践：参见 `ui-test-midscene` skill 的 `references/test-patterns.md`

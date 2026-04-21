# 测试模式最佳实践

## 测试脚本组织结构

```
test-artifacts/{project}/06-ui-tests/v1/
├── package.json
├── playwright.config.js
├── tests/                    # 测试脚本
│   ├── login.spec.js         # 登录相关测试
│   ├── checkout.spec.js      # 结账相关测试
│   └── admin.spec.js         # 管理后台测试
├── fixtures/                 # 测试数据
│   ├── users.js              # 测试用户数据
│   └── products.js           # 测试商品数据
├── scenarios/                # YAML 场景定义（可选）
│   └── smoke-test.yaml
└── midscene_run/             # 执行产物（自动生成）
    └── report/               # HTML 报告
```

---

## 模式 1：端到端冒烟测试

最简单的场景，验证核心流程是否畅通。

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('冒烟测试：完整购物流程', async ({ page }) => {
  const agent = new PlaywrightAgent(page);

  await page.goto('https://example.com');

  // 搜索商品
  await agent.aiAct('在搜索框输入 "耳机"，点击搜索按钮');

  // 等待搜索结果
  await agent.aiWaitFor('页面显示搜索结果列表', { timeoutMs: 15000 });

  // 选择第一个商品
  await agent.aiTap('搜索结果中的第一个商品');

  // 添加到购物车
  await agent.aiTap('加入购物车按钮');

  // 验证购物车
  await agent.aiAssert('页面显示已添加到购物车的提示或购物车数量增加');
});
```

---

## 模式 2：表单填写测试

精确控制每个输入步骤。

```javascript
import { test, expect } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('注册表单填写', async ({ page }) => {
  const agent = new PlaywrightAgent(page);
  await page.goto('https://example.com/register');

  // 逐字段填写（精确控制）
  await agent.aiInput('用户名输入框', { value: 'testuser_001' });
  await agent.aiInput('邮箱输入框', { value: 'test001@example.com' });
  await agent.aiInput('密码输入框', { value: 'SecurePass123!' });
  await agent.aiInput('确认密码输入框', { value: 'SecurePass123!' });

  // 勾选协议
  await agent.aiTap('同意服务条款的复选框');

  // 提交
  await agent.aiTap('注册按钮');

  // 验证
  await agent.aiWaitFor('页面显示注册成功或跳转到欢迎页', { timeoutMs: 10000 });

  // 提取注册后的用户信息
  const userInfo = await agent.aiQuery(
    '{username: string, email: string, status: string}',
  );
  expect(userInfo.username).toBe('testuser_001');
});
```

---

## 模式 3：数据驱动测试

从外部数据源读取测试用例，批量执行。

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

const loginCases = [
  { username: 'valid_user', password: 'correct_pass', expectSuccess: true },
  { username: 'valid_user', password: 'wrong_pass', expectSuccess: false },
  { username: '', password: 'any', expectSuccess: false },
  { username: 'nonexistent', password: 'any', expectSuccess: false },
];

for (const tc of loginCases) {
  test(`登录测试: ${tc.username} / ${tc.password ? '有密码' : '无密码'}`, async ({ page }) => {
    const agent = new PlaywrightAgent(page);
    await page.goto('https://example.com/login');

    if (tc.username) {
      await agent.aiInput('用户名输入框', { value: tc.username });
    }
    if (tc.password) {
      await agent.aiInput('密码输入框', { value: tc.password });
    }

    await agent.aiTap('登录按钮');

    if (tc.expectSuccess) {
      await agent.aiAssert('登录成功，页面显示用户信息或跳转到首页');
    } else {
      await agent.aiAssert('页面显示错误提示或登录失败');
    }
  });
}
```

---

## 模式 4：条件分支测试

根据页面状态执行不同操作。

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('购物车条件操作', async ({ page }) => {
  const agent = new PlaywrightAgent(page);
  await page.goto('https://example.com/shop');

  // 获取商品列表和价格
  const items = await agent.aiQuery(
    '{name: string, price: number, inStock: boolean}[], 页面上的商品信息',
  );

  for (const item of items) {
    if (item.inStock && item.price < 500) {
      // 有货且价格低于 500 的商品加入购物车
      await agent.aiTap(`"${item.name}" 的加入购物车按钮`);
    }
  }

  // 验证购物车状态
  const cartCount = await agent.aiNumber('购物车中的商品数量');
  console.log(`已添加 ${cartCount} 件商品到购物车`);
});
```

---

## 模式 5：多页面流程测试

跨页面导航的完整流程。

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('完整购买流程', async ({ page }) => {
  const agent = new PlaywrightAgent(page);

  // 第 1 步：搜索
  await page.goto('https://example.com');
  await agent.aiAct('搜索 "笔记本电脑"');
  await agent.aiWaitFor('显示搜索结果');

  // 第 2 步：选择商品（会跳转到详情页）
  await agent.aiTap('搜索结果中第一个商品的标题或图片');
  await agent.aiWaitFor('进入商品详情页');

  // 第 3 步：添加到购物车
  await agent.aiAct('选择规格，点击加入购物车');
  await agent.aiAssert('页面提示已加入购物车');

  // 第 4 步：进入购物车
  await agent.aiTap('购物车图标或链接');
  await agent.aiWaitFor('显示购物车页面');

  // 第 5 步：结算
  const cartInfo = await agent.aiQuery(
    '{itemName: string, quantity: number, totalPrice: number}',
  );
  console.log('购物车信息:', cartInfo);

  await agent.aiTap('去结算按钮');
  await agent.aiWaitFor('进入结算页面');

  // 第 6 步：验证结算页面
  await agent.aiAssert('结算页面显示订单信息和支付选项');
});
```

---

## 模式 6：断言验证模式

### 方式 A：AI 断言（简洁）

```javascript
await agent.aiAssert('页面显示"操作成功"的绿色提示');
await agent.aiAssert('表单中所有必填字段都已填写');
```

### 方式 B：数据提取 + 原生断言（更可靠）

```javascript
// 提取数据
const items = await agent.aiQuery(
  '{name: string, price: number}[], 商品列表',
);

// 原生断言验证
const found = items.find(i => i.name === 'iPhone 15');
expect(found).toBeTruthy();
expect(found.price).toBeLessThan(8000);
```

### 方式 C：布尔值断言

```javascript
const hasLoginDialog = await agent.aiBoolean('页面弹出登录对话框');
expect(hasLoginDialog).toBe(true);
```

---

## 模式 7：YAML 场景定义

适合非技术人员编写测试场景。

```yaml
# scenarios/smoke-test.yaml
name: 冒烟测试
url: https://example.com
tasks:
  - name: 搜索商品
    flow:
      - ai: 在搜索框输入 "手机"，点击搜索
      - sleep: 3000
      - aiAssert: 页面显示搜索结果

  - name: 查看商品
    flow:
      - aiTap: 第一个搜索结果
      - sleep: 2000
      - aiAssert: 页面显示商品详情

  - name: 提取信息
    flow:
      - aiQuery: "商品名称和价格，{name: string, price: number}"
```

执行：

```javascript
const { result } = await agent.runYaml(
  fs.readFileSync('scenarios/smoke-test.yaml', 'utf-8'),
);
```

---

## 测试编写原则

### DO ✅

1. **描述清晰**：用自然语言描述操作时要具体
   ```javascript
   // 好
   await agent.aiTap('页面右上角的用户头像图标');
   // 不好
   await agent.aiTap('那个图标');
   ```

2. **适当等待**：操作后给页面留出稳定时间
   ```javascript
   await agent.aiTap('提交按钮');
   await agent.aiWaitFor('页面显示提交成功的提示', { timeoutMs: 10000 });
   ```

3. **混合使用**：简单流程用 aiAct，复杂逻辑用分步
   ```javascript
   // 简单流程一条指令
   await agent.aiAct('登录并进入个人中心');
   // 复杂逻辑分步控制
   const items = await agent.aiQuery('...');
   for (const item of items) { ... }
   ```

4. **报告记录**：关键节点记录到报告
   ```javascript
   await agent.recordToReport('登录前状态', {
     content: '用户未登录时的首页展示',
   });
   ```

### DON'T ❌

1. 不要在 aiAct 中混合过多步骤（建议不超过 5 步）
2. 不要依赖 AI 断言做关键验证（用 aiQuery + 原生断言更可靠）
3. 不要在页面未加载完成时就开始操作
4. 不要在测试中使用硬坐标（使用自然语言描述元素）

---

## 与 Playwright 原生 API 配合

Midscene 可以和 Playwright 原生 API 混合使用：

```javascript
import { test } from '@playwright/test';
import { PlaywrightAgent } from '@midscene/web';

test('混合使用示例', async ({ page }) => {
  const agent = new PlaywrightAgent(page);

  // Playwright 原生：导航、网络拦截
  await page.goto('https://example.com');
  await page.route('/api/**', route => route.fulfill({ body: '{}' }));

  // Midscene：UI 操作
  await agent.aiAct('填写搜索表单并提交');

  // Playwright 原生：等待网络请求
  await page.waitForResponse('/api/search');

  // Midscene：验证和数据提取
  await agent.aiAssert('搜索结果列表不为空');
  const results = await agent.aiQuery('string[], 搜索结果标题列表');
  console.log(results);

  // Playwright 原生：截图
  await page.screenshot({ path: 'screenshot.png' });
});
```

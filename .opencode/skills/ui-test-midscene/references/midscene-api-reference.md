# Midscene API 速查

## Agent 构造

### PlaywrightAgent（推荐）

```javascript
import { PlaywrightAgent } from '@midscene/web';

const agent = new PlaywrightAgent(page, {
  generateReport: true,           // 生成 HTML 报告（默认 true）
  reportFileName: 'my-test',      // 报告文件名
  waitAfterAction: 300,           // 操作后等待时间 ms（默认 300）
  replanningCycleLimit: 20,       // aiAct 最大重规划次数（默认 20）
  aiActContext: '先关闭弹窗',      // aiAct 背景知识
});
```

### PuppeteerAgent

```javascript
import { PuppeteerAgent } from '@midscene/web';

const agent = new PuppeteerAgent(page);
```

### Chrome Bridge Agent（控制已有浏览器）

```javascript
import { AgentOverChromeBridge } from '@midscene/web';

const agent = new AgentOverChromeBridge();
await agent.connect();
```

---

## 交互方法

### aiAct() — 自动规划执行

AI 自动拆分指令为步骤序列并执行。

```javascript
await agent.aiAct('点击登录按钮，输入用户名和密码，提交表单');

// 简写形式
await agent.ai('同上');

// 带选项
await agent.aiAct('完成注册表单填写', {
  deepThink: true,           // 启用深度思考（复杂任务）
  deepLocate: true,          // 启用深度定位（精确定位）
  abortSignal: controller.signal,  // 支持超时取消
});
```

### aiTap() — 点击

```javascript
await agent.aiTap('登录按钮');
await agent.aiTap('右上角的设置图标', { deepLocate: true });
await agent.aiTap('提交按钮', { xpath: '//button[@type="submit"]' });
```

### aiInput() — 输入文本

```javascript
// 推荐写法（locate 在前）
await agent.aiInput('用户名输入框', { value: 'testuser' });

// 模式选项
await agent.aiInput('搜索框', { value: 'hello', mode: 'replace' });  // 替换（默认）
await agent.aiInput('搜索框', { value: ' world', mode: 'typeOnly' }); // 追加
await agent.aiInput('搜索框', { value: '', mode: 'clear' });          // 清空
```

### aiKeyboardPress() — 按键

```javascript
await agent.aiKeyboardPress('搜索输入框', { keyName: 'Enter' });
await agent.aiKeyboardPress('表单', { keyName: 'Tab' });
```

### aiScroll() — 滚动

```javascript
// 向下滚动 200px
await agent.aiScroll('商品列表', {
  scrollType: 'singleAction',
  direction: 'down',
  distance: 200,
});

// 滚动到底部
await agent.aiScroll('页面', { scrollType: 'scrollToBottom' });

// 滚动到顶部
await agent.aiScroll('页面', { scrollType: 'scrollToTop' });
```

### aiDoubleClick() — 双击

```javascript
await agent.aiDoubleClick('文件名');
```

### aiHover() — 悬停

```javascript
await agent.aiHover('下拉菜单');
```

---

## 数据提取

### aiQuery() — 提取结构化数据

```javascript
// 提取对象
const user = await agent.aiQuery('{name: string, age: number, email: string}');

// 提取数组
const items = await agent.aiQuery('{name: string, price: number}[], 表格中的商品数据');

// 提取字符串数组
const fieldNames = await agent.aiQuery('string[], 表格列名');

// 包含 DOM 信息（提取不可见属性如链接）
const data = await agent.aiQuery('{name: string, link: string}[], 列表数据', {
  domIncluded: true,
});
```

### aiBoolean() — 提取布尔值

```javascript
const isLoggedIn = await agent.aiBoolean('用户已登录，页面显示用户名');
const hasError = await agent.aiBoolean('页面显示错误提示信息');
```

### aiNumber() — 提取数字

```javascript
const price = await agent.aiNumber('商品价格的数字');
const count = await agent.aiNumber('购物车中的商品数量');
```

### aiString() — 提取字符串

```javascript
const title = await agent.aiString('页面标题文字');
const userName = await agent.aiString('欢迎文字中的用户名');
```

### aiAsk() — 自然语言问答

```javascript
const answer = await agent.aiAsk('这个页面是做什么的？');
console.log(answer); // AI 返回的文字回答
```

---

## 断言验证

### aiAssert() — AI 断言

```javascript
// 断言成功：无返回值
await agent.aiAssert('页面显示"登录成功"');

// 断言失败：抛出错误
await agent.aiAssert('价格显示为 99.9', '价格不正确，期望 99.9');

// 结合 domIncluded
await agent.aiAssert('登录按钮有正确的链接', { domIncluded: true });
```

### 替代方案：aiQuery + 原生断言

更可靠的方式（减少 AI 幻觉）：

```javascript
// 提取数据后用原生断言验证
const items = await agent.aiQuery(
  '{name: string, price: number}[], 商品列表',
);
const target = items.find(i => i.name === 'Sauce Labs Onesie');
expect(target).toBeTruthy();
expect(target.price).toBe(7.99);
```

---

## 定位与等待

### aiLocate() — 元素定位

```javascript
const info = await agent.aiLocate('登录按钮');
console.log(info);
// {
//   rect: { left: 100, top: 50, width: 80, height: 30 },
//   center: [140, 65],
//   dpr: 1
// }
```

### aiWaitFor() — 等待条件

```javascript
// 等待元素出现
await agent.aiWaitFor('页面显示加载完成的内容', {
  timeoutMs: 30000,     // 超时时间（默认 15000）
  checkIntervalMs: 5000, // 检查间隔（默认 3000）
});
```

---

## 高级 API

### evaluateJavaScript() — 执行 JS

```javascript
const title = await agent.evaluateJavaScript('document.title');
const url = await agent.evaluateJavaScript('window.location.href');
```

### runYaml() — 执行 YAML 脚本

```javascript
const { result } = await agent.runYaml(`
tasks:
  - name: search
    flow:
      - ai: 在搜索框输入 "weather"，点击搜索
      - sleep: 3000
  - name: extract
    flow:
      - aiQuery: "搜索结果中的天气信息，{temperature: string, condition: string}"
`);
console.log(result);
```

### recordToReport() — 记录到报告

```javascript
await agent.recordToReport('登录前页面', {
  content: '用户未登录时的初始状态',
});
```

### freezePageContext() / unfreezePageContext() — 冻结页面上下文

```javascript
// 冻结后多次查询使用同一快照，提升性能
await agent.freezePageContext();

const [name, email, role] = await Promise.all([
  agent.aiString('用户名'),
  agent.aiString('邮箱'),
  agent.aiString('角色'),
]);

await agent.unfreezePageContext(); // 恢复实时状态
```

---

## 选项速查表

| 选项 | 适用 API | 说明 |
|------|---------|------|
| `deepLocate: true` | aiTap, aiInput, aiLocate 等 | 二次 AI 调用精确定位 |
| `xpath: '...'` | aiTap, aiInput, aiLocate 等 | 优先用 xpath 定位 |
| `cacheable: true` | 所有交互 API | 启用缓存加速回放 |
| `domIncluded: true` | aiQuery, aiAssert, aiBoolean 等 | 包含简化 DOM 信息 |
| `screenshotIncluded: true` | aiQuery, aiAssert, aiBoolean 等 | 包含截图（默认 true） |
| `deepThink: true` | aiAct | 启用深度思考模式 |
| `mode: 'replace'` | aiInput | 替换模式（默认） |
| `mode: 'typeOnly'` | aiInput | 追加输入 |
| `mode: 'clear'` | aiInput | 仅清空 |

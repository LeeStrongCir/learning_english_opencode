# 技术方案与 MCP 指南

本参考文档详细说明各类测试用例的最佳技术方案选择，以及可选的 MCP 服务集成方案。

---

## 一、纯 API/SDK 测试

### 推荐方案：pytest + requests

#### 为什么选这个方案

- `requests` 是 Python 最成熟的 HTTP 客户端，API 简洁直观
- `pytest` 提供强大的 fixture 系统、参数化测试、丰富的断言
- 组合轻量、无需额外配置，适合绝大多数 REST API 测试场景

#### 典型代码结构

```python
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self, api_session):
        self.session = api_session

    def test_create_user(self):
        response = api_post(self.session, "/api/users", json_data={
            "name": "test",
            "email": "test@example.com"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "test"
        assert "id" in data
```

#### 常见模式

| 场景 | 实现方式 |
|------|---------|
| 鉴权 | 在 conftest.py 的 session fixture 中统一处理 token 获取 |
| 数据清理 | 使用 fixture 的 yield 后部分做 teardown |
| 参数化 | 使用 `@pytest.mark.parametrize` 测试多组输入 |
| 异步 API | 使用 `httpx` 替代 `requests`，配合 `pytest-asyncio` |

#### 可选 MCP 服务

**API Explorer MCP**

- **用途**：自动解析 OpenAPI/Swagger 文档，获取接口定义、参数校验规则
- **何时使用**：接口文档频繁变更、需要自动生成请求 schema 验证时
- **安装**：`npx -y @anthropic-ai/mcp-server-api <openapi-url>`
- **替代方案**：手动维护接口定义文件，或使用 `pydantic` 做响应校验

---

## 二、纯 Web UI 测试

### 推荐方案：pytest + Playwright

#### 为什么选这个方案

- Playwright 支持 Chromium/Firefox/WebKit 多浏览器
- 自动等待机制（auto-wait），减少 flaky tests
- 强大的定位器策略（`get_by_role`, `get_by_text`, `get_by_test_id`）
- Python SDK 与 pytest 深度集成（`pytest-playwright`）

#### 典型代码结构

```python
class TestLoginPage:
    def setup_method(self, page: Page):
        self.page = page
        page.goto(f"{APP_URL}/login")

    def test_login_success(self):
        page = self.page
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')
        expect(page.locator(".dashboard")).to_be_visible()
```

#### 定位器优先级

1. `page.get_by_role("button", name="Submit")` — 语义化，最推荐
2. `page.get_by_text("Welcome")` — 文本匹配
3. `page.get_by_test_id("submit-btn")` — 需要开发配合添加 data-testid
4. `page.locator("#submit-btn")` — CSS 选择器
5. `page.locator("//button[@id='submit']")` — XPath（最后手段）

#### 常见模式

| 场景 | 实现方式 |
|------|---------|
| 等待元素 | `expect(locator).to_be_visible()` — 自动重试 |
| 等待网络 | `with page.expect_response("**/api/*") as resp:` |
| 截图对比 | `page.screenshot(path="actual.png")` + 人工对比 |
| 多标签页 | `with page.expect_popup() as popup:` |
| 文件上传 | `page.set_input_files('input[type="file"]', "path/to/file")` |

#### 可选 MCP 服务

**Playwright MCP**

- **用途**：通过 MCP 协议控制浏览器，支持交互式调试
- **何时使用**：需要实时查看页面状态、动态调整测试策略时
- **安装**：`npx -y @anthropic-ai/mcp-server-playwright`
- **注意**：生成的最终测试代码不需要 MCP，MCP 仅用于调试阶段

---

## 三、混合型测试（API + UI）

### 推荐方案：requests + Playwright 组合

#### 架构设计

```
┌─────────────────────────────────────────┐
│                 Test Case                │
├─────────────────────────────────────────┤
│  Setup:                                  │
│    1. API: 获取 token / 创建测试数据      │
│    2. UI:  登录并导航到目标页面           │
├─────────────────────────────────────────┤
│  Test Steps:                             │
│    - API 操作用于数据准备/验证            │
│    - UI 操作用于用户交互/视觉验证         │
├─────────────────────────────────────────┤
│  Assertions:                             │
│    - API: 状态码、响应体、业务逻辑         │
│    - UI:  元素可见性、文本内容、页面状态   │
└─────────────────────────────────────────┘
```

#### 典型代码结构

```python
class TestOrderFlow:
    def setup_method(self, api_session, page: Page):
        self.session = api_session
        self.page = page
        # API: 创建测试用户
        resp = api_post(self.session, "/api/users", json_data={"name": "test"})
        self.user_id = resp.json()["id"]
        # UI: 登录
        page.goto(f"{APP_URL}/login")
        page.fill('input[name="username"]', "test")
        page.click('button[type="submit"]')

    def test_create_order(self):
        # API: 创建商品
        resp = api_post(self.session, "/api/products", json_data={
            "name": "Test Product",
            "price": 99.99
        })
        product_id = resp.json()["id"]

        # UI: 验证商品显示
        self.page.reload()
        expect(self.page.locator(f"text=Test Product")).to_be_visible()

        # UI: 下单操作
        self.page.click("text=立即购买")
        self.page.click("text=确认订单")

        # API: 验证订单创建
        resp = api_get(self.session, f"/api/users/{self.user_id}/orders")
        assert len(resp.json()["orders"]) >= 1
```

#### 关键注意事项

1. **Session 共享**：API 的 token 需要传递给 UI 的认证流程
2. **数据同步**：API 创建的数据在 UI 上可能需要刷新或等待加载
3. **测试隔离**：每条用例创建独立数据，避免互相影响
4. **执行顺序**：API 操作通常比 UI 操作快，优先使用 API 做数据准备

---

## 四、APP 测试（预留）

> 当前版本暂不支持 APP 自动化，以下为预留方案。

### 推荐方案

| 平台 | 方案 | 说明 |
|------|------|------|
| Android | Appium + UiAutomator2 | 跨平台标准方案 |
| iOS | Appium + XCUITest | 需要 Mac 环境 |
| HarmonyOS | AppGallery Connect + 专属工具 | 华为生态专用 |

### 统一方案：Appium

- 支持 Android + iOS 跨平台
- 使用 WebDriver 协议，API 与 Selenium 类似
- Python SDK: `pip install Appium-Python-Client`

---

## 五、方案选择决策树

```
测试用例
  │
  ├─ 涉及 HTTP 请求/接口调用？
  │   ├─ 仅 API 操作 → 纯 API 方案 (requests + pytest)
  │   └─ 同时有页面操作 → 混合方案 (requests + playwright)
  │
  └─ 不涉及 API？
      └─ 页面交互/视觉验证 → 纯 Web UI 方案 (playwright + pytest)
```

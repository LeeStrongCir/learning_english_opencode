---
name: test-automation
description: >
  将 Excel/CSV 格式的测试用例自动转换为可执行的 Python 测试代码（pytest 框架）。当用户提供测试用例表格文件（.xlsx/.csv）并想要生成自动化测试脚本时使用此 skill。触发场景：用户提到"自动化测试用例"、"生成测试代码"、"测试用例转代码"、"pytest 实现"、"API 自动化"、"Web UI 自动化"、"测试脚本生成"，或上传了包含测试用例的 Excel/CSV 文件。支持纯 API、纯 Web UI、以及混合型测试用例的自动化实现。
---

# 测试用例自动化实现

本 skill 将 Excel/CSV 格式的测试用例转换为可执行的 Python pytest 测试代码，涵盖预置条件设置、操作步骤实现、以及预期结果与实际结果的对比验证。

## 工作流程

### 第一步：解析测试用例文件

读取用户提供的 Excel/CSV 文件，识别以下关键字段（字段名可能有变体）：

| 标准字段 | 常见变体 |
|---------|---------|
| 用例ID | Case ID, TC#, 编号 |
| 用例标题 | Title, 标题, Summary |
| 前置条件 | Precondition, 前置, 前提条件 |
| 测试步骤 | Steps, 操作步骤, 步骤描述 |
| 预期结果 | Expected, 期望结果, Expected Result |
| 优先级 | Priority, P0/P1/P2 |
| 测试类型 | Type, 类型, API/UI/E2E |

如果字段名不匹配，根据列内容智能推断。使用内置脚本解析：

```bash
python scripts/parse_test_cases.py <path-to-file> --output <output-json>
```

### 第二步：分析测试用例类型

对每条用例进行类型判定，决定使用何种技术方案：

#### 判定规则

| 类型 | 判定特征 | 技术方案 |
|------|---------|---------|
| **纯 API** | 涉及 HTTP 请求、接口调用、SDK 方法、JSON/XML 数据交互、状态码验证 | `requests` + `pytest` |
| **纯 Web UI** | 涉及页面操作、点击、输入、表单提交、元素可见性、页面跳转 | `playwright` + `pytest` |
| **混合型** | 同时包含 API 调用和 UI 操作（如：先调 API 创建数据，再在页面验证） | `requests` + `playwright` 组合 |

**判定依据关键词**：
- API 特征：`接口`、`API`、`请求`、`POST`、`GET`、`响应`、`状态码`、`token`、`鉴权`、`SDK`、`调用`
- Web UI 特征：`点击`、`输入`、`页面`、`按钮`、`表单`、`弹窗`、`下拉`、`跳转`、`可见`、`文本`、`链接`

如果"测试类型"列已明确标注，优先使用该标注。

### 第三步：生成测试代码

根据用例类型，使用对应的代码模板生成可执行的 pytest 测试文件。

#### 3.1 纯 API 测试

技术栈：`pytest` + `requests`

```python
import pytest
import requests

class TestAPI用例ID:
    """用例标题"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """预置条件"""
        # 根据前置条件生成 setup 代码
        # 如：获取 token、创建测试数据、设置 headers
        self.base_url = "https://api.example.com"
        self.headers = {"Authorization": f"Bearer {self.get_token()}"}
        yield
        # teardown: 清理测试数据

    def get_token(self):
        """获取鉴权 token"""
        resp = requests.post(f"{self.base_url}/auth/login", json={
            "username": "test_user",
            "password": "test_pass"
        })
        return resp.json()["token"]

    def test_用例ID(self):
        """测试步骤 + 预期结果验证"""
        # 步骤1: 发送请求
        response = requests.post(
            f"{self.base_url}/api/endpoint",
            headers=self.headers,
            json={"key": "value"}
        )

        # 验证预期结果
        assert response.status_code == 200, f"期望 200, 实际 {response.status_code}"
        data = response.json()
        assert data["field"] == "expected_value", f"字段值不匹配: {data['field']}"
```

**关键模式**：
- 使用 `pytest.fixture` 处理预置条件和清理
- 每个测试步骤后紧跟对应的断言，方便定位失败步骤
- 断言消息包含预期值和实际值，便于调试
- 复杂 API 链式调用时，将公共逻辑提取为 helper 方法

#### 3.2 纯 Web UI 测试

技术栈：`pytest` + `playwright`

```python
import pytest
from playwright.sync_api import Page, expect

class TestWebUI用例ID:
    """用例标题"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """预置条件"""
        # 如：登录、导航到指定页面、设置测试数据
        page.goto("https://app.example.com/login")
        page.fill('input[name="username"]', "test_user")
        page.fill('input[name="password"]', "test_pass")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
        self.page = page
        yield
        # teardown: 如退出登录、清理数据

    def test_用例ID(self):
        """测试步骤 + 预期结果验证"""
        page = self.page

        # 步骤1: 点击某个按钮
        page.click("text=新建")

        # 步骤2: 填写表单
        page.fill('input[name="title"]', "测试标题")
        page.click('button[type="submit"]')

        # 验证预期结果
        expect(page.locator(".success-message")).to_be_visible()
        expect(page.locator(".item-title")).to_contain_text("测试标题")
```

**关键模式**：
- 使用 `playwright.sync_api` 的同步 API（更简洁）
- 使用 `expect()` 进行自动重试的断言（等待元素状态）
- 定位器优先使用语义化选择器（`text=`, `role=`, `aria-`）
- 关键操作后使用 `wait_for_*` 确保页面状态稳定

#### 3.3 混合型测试

技术栈：`requests` + `playwright` 组合

```python
import pytest
import requests
from playwright.sync_api import Page, expect

class TestMixed用例ID:
    """用例标题"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        # API 预置条件：创建测试数据
        self.api_base = "https://api.example.com"
        token_resp = requests.post(f"{self.api_base}/auth/login", json={
            "username": "admin",
            "password": "admin123"
        })
        self.token = token_resp.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # UI 预置条件：登录并导航
        page.goto(f"{self.api_base.replace('/api', '')}/login")
        page.fill('input[name="username"]', "admin")
        page.fill('input[name="password"]', "admin123")
        page.click('button[type="submit"]')
        page.wait_for_url("**/dashboard")
        self.page = page
        yield

    def test_用例ID(self):
        page = self.page

        # 步骤1: 通过 API 创建数据
        create_resp = requests.post(
            f"{self.api_base}/api/items",
            headers=self.headers,
            json={"name": "测试项目", "status": "active"}
        )
        assert create_resp.status_code == 201
        item_id = create_resp.json()["id"]

        # 步骤2: 在 UI 上验证数据已显示
        page.reload()
        expect(page.locator(f"text=测试项目")).to_be_visible()

        # 步骤3: 在 UI 上操作
        page.click(f'tr[data-id="{item_id"] .edit-btn')
        page.fill('input[name="name"]', "修改后的名称")
        page.click('button:has-text("保存")')

        # 步骤4: 通过 API 验证修改生效
        get_resp = requests.get(
            f"{self.api_base}/api/items/{item_id}",
            headers=self.headers
        )
        assert get_resp.json()["name"] == "修改后的名称"
```

**关键模式**：
- API 用于数据准备和最终结果验证（更快、更可靠）
- UI 用于验证用户可见的行为和交互
- 共享 token/session 在 API 和 UI 之间传递
- 使用 API 创建的数据需要在 UI 上刷新或等待加载

### 第四步：输出文件结构

生成的测试代码按以下结构组织：

```
test_output/
├── conftest.py              # 公共 fixtures（base_url, auth, browser 配置）
├── test_api_cases.py        # 纯 API 测试用例
├── test_webui_cases.py      # 纯 Web UI 测试用例
├── test_mixed_cases.py      # 混合型测试用例
├── requirements.txt         # 依赖清单
└── README.md               # 运行说明
```

使用内置脚本生成完整项目结构：

```bash
python scripts/generate_test_code.py \
  --test-cases <parsed-json> \
  --output <output-directory> \
  --base-url <api-base-url> \
  --app-url <web-app-url>
```

### 第五步：交付与说明

向用户提供：
1. 生成的测试代码文件
2. 依赖安装命令：`pip install -r requirements.txt`
3. Playwright 浏览器安装：`playwright install`
4. 运行命令：`pytest test_output/ -v`
5. 用例类型分布统计和覆盖率说明

## MCP 方案建议

当需要增强测试能力时，可考虑以下 MCP 服务：

| MCP 服务 | 用途 | 适用场景 |
|---------|------|---------|
| **Playwright MCP** | 浏览器自动化控制 | Web UI 测试，需要实时浏览器交互 |
| **API Explorer MCP** | API 文档解析、Schema 验证 | API 测试，需要自动发现接口定义 |
| **Database MCP** | 数据库操作验证 | 需要直接查询数据库验证结果的场景 |

**注意**：MCP 服务是可选增强。本 skill 生成的代码使用标准 Python 库（requests, playwright），无需 MCP 即可独立运行。仅在需要交互式调试或动态 API 发现时才推荐引入 MCP。

## 质量准则

- **独立性**：每条测试用例可独立运行，不依赖其他用例的执行顺序
- **可读性**：测试代码结构清晰，步骤与原始用例一一对应，添加注释标明步骤编号
- **可调试性**：断言包含详细的预期值和实际值信息，失败时能快速定位问题
- **可维护性**：公共逻辑（登录、鉴权、base URL）提取到 conftest.py
- **稳定性**：UI 测试使用显式等待而非固定 sleep，API 测试处理网络异常

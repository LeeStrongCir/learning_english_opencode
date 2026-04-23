#!/usr/bin/env python3
"""Generate executable pytest test code from parsed test case JSON."""

import argparse
import json
import re
import textwrap
from pathlib import Path


def sanitize_id(case_id):
    """Convert case ID to valid Python identifier."""
    cleaned = re.sub(r"[^a-zA-Z0-9_]", "_", str(case_id))
    if cleaned and cleaned[0].isdigit():
        cleaned = "tc_" + cleaned
    return cleaned or "unknown"


def generate_conftest(base_url="", app_url=""):
    """Generate conftest.py with shared fixtures."""
    return '''import pytest
import requests
from playwright.sync_api import Browser, BrowserContext, Page

# ============ Configuration ============
BASE_URL = "{base_url}"
APP_URL = "{app_url}"
TEST_USER = "test_user"
TEST_PASSWORD = "test_pass"

# ============ API Fixtures ============

@pytest.fixture(scope="session")
def api_session():
    """Create a shared API session with authentication."""
    session = requests.Session()
    session.headers.update({{
        "Content-Type": "application/json",
        "Accept": "application/json",
    }})
    # Login to get token
    try:
        resp = session.post(f"{{BASE_URL}}/auth/login", json={{
            "username": TEST_USER,
            "password": TEST_PASSWORD,
        }})
        resp.raise_for_status()
        token = resp.json().get("token", resp.json().get("access_token", ""))
        session.headers.update({{"Authorization": f"Bearer {{token}}"}})
    except requests.exceptions.RequestException:
        pass  # Token optional for public endpoints
    yield session
    session.close()


@pytest.fixture(scope="session")
def auth_headers(api_session):
    """Get authenticated headers."""
    return dict(api_session.headers)


# ============ Browser Fixtures ============

@pytest.fixture(scope="session")
def browser_context(browser: Browser):
    """Create a reusable browser context."""
    context = browser.new_context(
        viewport={{"width": 1280, "height": 720}},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture
def page(browser_context: BrowserContext) -> Page:
    """Create a new page for each test."""
    new_page = browser_context.new_page()
    yield new_page
    new_page.close()


# ============ Helper Functions ============

def login_via_ui(page: Page, username: str = TEST_USER, password: str = TEST_PASSWORD):
    """Login through the web UI."""
    page.goto(f"{{APP_URL}}/login")
    page.fill('input[name="username"], input[type="text"], #username', username)
    page.fill('input[name="password"], input[type="password"], #password', password)
    page.click('button[type="submit"], input[type="submit"], .login-btn')
    page.wait_for_load_state("networkidle")


def api_get(session: requests.Session, path: str, **kwargs):
    """Helper for GET requests."""
    url = f"{{BASE_URL}}{{path}}"
    return session.get(url, **kwargs)


def api_post(session: requests.Session, path: str, json_data: dict = None, **kwargs):
    """Helper for POST requests."""
    url = f"{{BASE_URL}}{{path}}"
    return session.post(url, json=json_data, **kwargs)


def api_put(session: requests.Session, path: str, json_data: dict = None, **kwargs):
    """Helper for PUT requests."""
    url = f"{{BASE_URL}}{{path}}"
    return session.put(url, json=json_data, **kwargs)


def api_delete(session: requests.Session, path: str, **kwargs):
    """Helper for DELETE requests."""
    url = f"{{BASE_URL}}{{path}}"
    return session.delete(url, **kwargs)
'''.format(base_url=base_url or "https://api.example.com", app_url=app_url or "https://app.example.com")


def generate_api_test(case):
    """Generate a single API test class."""
    case_id = sanitize_id(case.get("case_id", ""))
    title = case.get("title", "Untitled")
    precondition = case.get("precondition", "")
    steps = case.get("steps", "")
    expected = case.get("expected", "")

    # Build setup code from precondition
    setup_code = ""
    if precondition:
        setup_code = f"""        # 前置条件: {precondition}
        # TODO: 根据前置条件实现 setup 逻辑
        # 常见模式: 获取 token、创建测试数据、配置环境
        pass
"""
    else:
        setup_code = "        pass\n"

    # Build test method from steps and expected
    test_code = f"""        # 测试步骤:
        # {steps}

        # TODO: 实现测试步骤
        # 示例:
        # response = api_post(self.session, "/api/endpoint", json_data={{"key": "value"}})
        # assert response.status_code == 200

        # 预期结果验证:
        # {expected}

        # TODO: 实现断言
        # 示例:
        # assert response.status_code == 200, f"期望 200, 实际 {{response.status_code}}"
        # data = response.json()
        # assert data["field"] == "expected", f"字段值不匹配"

        assert True, "TODO: 实现测试逻辑"
"""

    return f'''
class TestAPI{sanitize_id(case_id)}:
    """{title}"""

    def setup_method(self, api_session):
        """Setup: {precondition or 'None'}"""
        self.session = api_session
        self.base_url = BASE_URL
{setup_code}

    def test_{case_id}(self):
        """{title}"""
{test_code}
'''


def generate_webui_test(case):
    """Generate a single Web UI test class."""
    case_id = sanitize_id(case.get("case_id", ""))
    title = case.get("title", "Untitled")
    precondition = case.get("precondition", "")
    steps = case.get("steps", "")
    expected = case.get("expected", "")

    setup_code = ""
    if precondition:
        setup_code = f"""        # 前置条件: {precondition}
        # TODO: 实现预置条件 (如登录、导航到页面)
        # 示例: page.goto(f"{{APP_URL}}/target-page")
        pass
"""
    else:
        setup_code = "        pass\n"

    test_code = f"""        page = self.page

        # 测试步骤:
        # {steps}

        # TODO: 实现 UI 操作步骤
        # 示例:
        # page.click("text=新建")
        # page.fill('input[name="title"]', "测试标题")
        # page.click('button[type="submit"]')

        # 预期结果验证:
        # {expected}

        # TODO: 实现断言
        # 示例:
        # expect(page.locator(".success-message")).to_be_visible()
        # expect(page.locator(".item-title")).to_contain_text("测试标题")

        assert True, "TODO: 实现测试逻辑"
"""

    return f'''
class TestWebUI{sanitize_id(case_id)}:
    """{title}"""

    def setup_method(self, page: Page):
        """Setup: {precondition or 'None'}"""
        self.page = page
{setup_code}

    def test_{case_id}(self):
        """{title}"""
{test_code}
'''


def generate_mixed_test(case):
    """Generate a single mixed (API + UI) test class."""
    case_id = sanitize_id(case.get("case_id", ""))
    title = case.get("title", "Untitled")
    precondition = case.get("precondition", "")
    steps = case.get("steps", "")
    expected = case.get("expected", "")

    setup_code = f"""        # 前置条件: {precondition}
        # TODO: 实现 API + UI 预置条件
        # 示例:
        # 1. API: 获取 token / 创建测试数据
        # 2. UI: 登录并导航到目标页面
        pass
"""

    test_code = f"""        page = self.page

        # 测试步骤 (API + UI 混合):
        # {steps}

        # TODO: 实现混合测试步骤
        # 模式:
        # 1. API 操作: response = api_post(self.session, "/api/...", json_data={{...}})
        # 2. UI 验证: expect(page.locator("...")).to_be_visible()
        # 3. UI 操作: page.click("...")
        # 4. API 验证: response = api_get(self.session, "/api/...")

        # 预期结果验证:
        # {expected}

        # TODO: 实现断言 (API 断言 + UI 断言)

        assert True, "TODO: 实现测试逻辑"
"""

    return f'''
class TestMixed{sanitize_id(case_id)}:
    """{title}"""

    def setup_method(self, api_session, page: Page):
        """Setup: {precondition or 'None'}"""
        self.session = api_session
        self.page = page
        self.base_url = BASE_URL
{setup_code}

    def test_{case_id}(self):
        """{title}"""
{test_code}
'''


def generate_requirements():
    """Generate requirements.txt."""
    return """pytest>=7.0
requests>=2.28
playwright>=1.40
pytest-playwright>=0.4
openpyxl>=3.1  # for Excel file support
"""


def generate_readme(base_url="", app_url=""):
    """Generate README.md with run instructions."""
    return f"""# 自动化测试项目

由 test-automation skill 自动生成。

## 环境配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Playwright 浏览器

```bash
playwright install
```

### 3. 配置测试环境

编辑 `conftest.py`，修改以下配置：

- `BASE_URL`: `{base_url or 'https://api.example.com'}`
- `APP_URL`: `{app_url or 'https://app.example.com'}`
- `TEST_USER` / `TEST_PASSWORD`: 测试账号

## 运行测试

```bash
# 运行所有测试
pytest -v

# 只运行 API 测试
pytest test_api_cases.py -v

# 只运行 Web UI 测试
pytest test_webui_cases.py -v

# 只运行混合测试
pytest test_mixed_cases.py -v

# 运行指定用例
pytest -v -k "test_TC001"

# 生成 HTML 报告
pytest --html=report.html --self-contained-html
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `conftest.py` | 公共 fixtures 和 helper 函数 |
| `test_api_cases.py` | 纯 API 测试用例 |
| `test_webui_cases.py` | 纯 Web UI 测试用例 |
| `test_mixed_cases.py` | 混合型测试用例 |

## 注意事项

- 生成的代码包含 `TODO` 标记，需要根据实际业务逻辑补充实现
- API 端点路径、请求参数、断言条件需根据实际接口文档调整
- UI 定位器需根据实际页面结构调整
"""


def main():
    parser = argparse.ArgumentParser(description="Generate pytest test code from parsed test cases")
    parser.add_argument("--test-cases", required=True, help="Path to parsed test case JSON")
    parser.add_argument("--output", "-o", required=True, help="Output directory")
    parser.add_argument("--base-url", default="", help="API base URL")
    parser.add_argument("--app-url", default="", help="Web app URL")
    args = parser.parse_args()

    # Load test cases
    with open(args.test_cases, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data["cases"]
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Categorize cases
    api_cases = [c for c in cases if c["case_type"] == "api"]
    webui_cases = [c for c in cases if c["case_type"] == "webui"]
    mixed_cases = [c for c in cases if c["case_type"] == "mixed"]

    # Generate conftest.py
    (output_dir / "conftest.py").write_text(
        generate_conftest(args.base_url, args.app_url), encoding="utf-8"
    )

    # Generate API tests
    if api_cases:
        api_content = '"""\nAuto-generated API test cases.\n"""\nimport pytest\nimport requests\nfrom conftest import BASE_URL, api_post, api_get, api_put, api_delete\n'
        for case in api_cases:
            api_content += generate_api_test(case)
        (output_dir / "test_api_cases.py").write_text(api_content, encoding="utf-8")

    # Generate Web UI tests
    if webui_cases:
        webui_content = '"""\nAuto-generated Web UI test cases.\n"""\nimport pytest\nfrom playwright.sync_api import Page, expect\nfrom conftest import APP_URL\n'
        for case in webui_cases:
            webui_content += generate_webui_test(case)
        (output_dir / "test_webui_cases.py").write_text(webui_content, encoding="utf-8")

    # Generate Mixed tests
    if mixed_cases:
        mixed_content = '"""\nAuto-generated mixed (API + UI) test cases.\n"""\nimport pytest\nimport requests\nfrom playwright.sync_api import Page, expect\nfrom conftest import BASE_URL, APP_URL, api_post, api_get\n'
        for case in mixed_cases:
            mixed_content += generate_mixed_test(case)
        (output_dir / "test_mixed_cases.py").write_text(mixed_content, encoding="utf-8")

    # Generate requirements.txt and README.md
    (output_dir / "requirements.txt").write_text(generate_requirements(), encoding="utf-8")
    (output_dir / "README.md").write_text(generate_readme(args.base_url, args.app_url), encoding="utf-8")

    # Print summary
    print(f"Generated test code in: {output_dir}")
    print(f"  API tests:    {len(api_cases)} cases -> test_api_cases.py")
    print(f"  Web UI tests: {len(webui_cases)} cases -> test_webui_cases.py")
    print(f"  Mixed tests:  {len(mixed_cases)} cases -> test_mixed_cases.py")
    print(f"  Common:       conftest.py, requirements.txt, README.md")
    print(f"\nNext steps:")
    print(f"  1. cd {output_dir}")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. playwright install")
    print(f"  4. Edit conftest.py with your base URLs and credentials")
    print(f"  5. Implement TODO sections in generated test files")


if __name__ == "__main__":
    main()

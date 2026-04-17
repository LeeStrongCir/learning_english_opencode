"""
Pytest 配置文件 (conftest.py)

提供全局 fixtures、hooks 和配置。
- 浏览器上下文管理
- 页面对象注入
- 测试数据加载
- 失败截图
- 日志配置
"""

import os
import json
import logging
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = PROJECT_ROOT / "fixtures"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"

# 确保截图目录存在
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 日志配置
# ============================================================

def setup_logging():
    """配置日志输出"""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                PROJECT_ROOT / f"test_{datetime.now():%Y%m%d_%H%M%S}.log",
                encoding="utf-8"
            )
        ]
    )


setup_logging()
logger = logging.getLogger(__name__)


# ============================================================
# 测试数据加载
# ============================================================

@pytest.fixture(scope="session")
def test_data():
    """
    加载测试数据

    Returns:
        dict: 从 test-data.json 加载的测试数据
    """
    data_file = FIXTURES_DIR / "test-data.json"
    logger.info(f"Loading test data from: {data_file}")

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info("Test data loaded successfully")
    return data


# ============================================================
# Playwright 浏览器 Fixture
# ============================================================

@pytest.fixture(scope="session")
def playwright_instance():
    """
    创建 Playwright 实例（session 级别）

    Yields:
        SyncPlaywright: Playwright 实例
    """
    logger.info("Starting Playwright...")
    with sync_playwright() as pw:
        yield pw
    logger.info("Playwright stopped")


@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    """
    创建浏览器实例（session 级别）

    支持通过命令行参数指定浏览器类型：
    --browser=chromium (默认)
    --browser=firefox
    --browser=webkit

    Yields:
        Browser: Playwright Browser 实例
    """
    browser_type = request.config.getoption("--browser", default="chromium")
    logger.info(f"Launching browser: {browser_type}")

    # 获取浏览器类型
    if browser_type == "firefox":
        browser = playwright_instance.firefox.launch(
            headless=True,
            args=["--no-sandbox"]
        )
    elif browser_type == "webkit":
        browser = playwright_instance.webkit.launch(
            headless=True
        )
    else:
        browser = playwright_instance.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

    logger.info(f"Browser launched: {browser_type}")
    yield browser

    logger.info("Closing browser...")
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    """
    创建浏览器上下文（function 级别）

    每个测试函数获得独立的浏览器上下文，
    包含独立的 cookies、localStorage 等。

    Yields:
        BrowserContext: Playwright BrowserContext 实例
    """
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        # 忽略 HTTPS 证书错误（测试环境可能需要）
        ignore_https_errors=False,
    )

    # 启用控制台日志捕获
    context.on("console", lambda msg: logger.debug(f"Browser console: {msg.text}"))

    yield context

    # 清理上下文
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """
    创建页面对象（function 级别）

    Yields:
        Page: Playwright Page 实例
    """
    page = context.new_page()

    # 设置页面加载超时
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)

    yield page

    # 测试结束后关闭页面
    page.close()


# ============================================================
# 页面对象 Fixture
# ============================================================

@pytest.fixture(scope="function")
def login_page(page, test_data):
    """
    创建登录页面对象并导航到登录页面

    Args:
        page: Playwright Page 实例
        test_data: 测试数据

    Yields:
        LoginPage: 登录页面对象
    """
    from pages.login_page import LoginPage

    login_page = LoginPage(page, test_data["base_url"])
    login_page.navigate()

    yield login_page


# ============================================================
# 失败截图 Hook
# ============================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动截图

    在每个测试用例执行后，如果测试失败，
    自动截取当前页面截图并保存到 screenshots 目录。
    """
    outcome = yield
    rep = outcome.get_result()

    # 只在测试失败时截图
    if rep.when == "call" and rep.failed:
        try:
            # 获取 page fixture
            page = item.funcargs.get("page")
            if page:
                # 生成截图文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                test_name = rep.nodeid.replace("::", "_").replace("/", "_")
                screenshot_path = SCREENSHOTS_DIR / f"{test_name}_{timestamp}.png"

                # 截图
                page.screenshot(path=str(screenshot_path), full_page=True)
                logger.info(f"Screenshot saved: {screenshot_path}")

                # 同时保存页面 HTML 以便调试
                html_path = SCREENSHOTS_DIR / f"{test_name}_{timestamp}.html"
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(page.content())
                logger.info(f"Page HTML saved: {html_path}")

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


# ============================================================
# 命令行参数
# ============================================================

def pytest_addoption(parser):
    """添加自定义命令行参数"""
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to use: chromium, firefox, webkit (default: chromium)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    parser.addoption(
        "--slow-mo",
        action="store",
        default=0,
        type=int,
        help="Slow down operations by specified milliseconds (default: 0)"
    )


# ============================================================
# 重试机制
# ============================================================

def retry_on_failure(func, max_retries=3, delay=1):
    """
    重试装饰器

    Args:
        func: 要重试的函数
        max_retries: 最大重试次数
        delay: 重试间隔（秒）

    Returns:
        函数执行结果
    """
    import time

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"Attempt {attempt + 1} failed: {e}, retrying...")
            time.sleep(delay)

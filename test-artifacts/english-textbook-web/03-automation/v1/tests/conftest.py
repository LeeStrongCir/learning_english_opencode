"""
pytest 配置和共享 fixture
"""
import os
import pytest
from playwright.sync_api import Page, expect

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_FILE = os.path.join(
    BASE_DIR, "..", "..", "..", "..", "..", "index.html"
)
abs_path = os.path.abspath(HTML_FILE)
abs_path = abs_path.replace('\\', '/')
FILE_URL = f"file:///{abs_path}"


@pytest.fixture(scope="session")
def base_url():
    """返回本地 HTML 文件的 file:// URL"""
    return FILE_URL


@pytest.fixture()
def page_goto(page: Page, base_url: str):
    """
    每个测试自动导航到首页。
    使用此 fixture 的测试无需手动 page.goto()。
    """
    page.goto(base_url)
    page.wait_for_selector(".grade-card")
    return page


@pytest.fixture()
def page_with_grade(page: Page, base_url: str):
    """
    导航到首页并选择三年级，停留在内容视图。
    """
    page.goto(base_url)
    page.wait_for_selector('.grade-card[data-grade="g3"]')
    page.click('.grade-card[data-grade="g3"]')
    page.wait_for_selector("#volume-selector .volume-btn")
    return page


@pytest.fixture()
def page_with_unit(page: Page, base_url: str):
    """
    完成完整选择链路：三年级 -> 上册 -> Unit 1
    停留在内容展示页面。
    """
    page.goto(base_url)
    page.wait_for_selector('.grade-card[data-grade="g3"]')

    # 选择年级
    page.click('.grade-card[data-grade="g3"]')
    page.wait_for_selector('#volume-selector .volume-btn[data-volume="v1"]')

    # 选择册次
    page.click('.volume-btn[data-volume="v1"]')
    page.wait_for_selector('#unit-selector .unit-btn[data-unit="u1"]')

    # 选择单元
    page.click('.unit-btn[data-unit="u1"]')
    page.wait_for_selector("#content-display h2")

    return page

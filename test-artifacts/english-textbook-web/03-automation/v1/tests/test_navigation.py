"""
导航功能测试：首页 / 内容 / 关于 视图切换
"""
import pytest
from playwright.sync_api import Page, expect


class TestNavigation:
    """导航按钮功能测试"""

    def test_default_view_is_home(self, page_goto: Page):
        """TC001: 页面加载后默认显示首页"""
        home_view = page_goto.locator("#home-view")
        expect(home_view).to_be_visible()

        content_view = page_goto.locator("#content-view")
        expect(content_view).not_to_be_visible()

        about_view = page_goto.locator("#about-view")
        expect(about_view).not_to_be_visible()

    def test_nav_home_button_active(self, page_goto: Page):
        """TC002: 首页导航按钮默认处于激活状态"""
        home_btn = page_goto.locator('.nav-btn[data-view="home"]')
        expect(home_btn).to_have_class("active", use_inner_text=False)

    def test_switch_to_content_view(self, page_goto: Page):
        """TC003: 点击「课本内容」按钮切换到内容视图"""
        page_goto.click('.nav-btn[data-view="content"]')

        content_view = page_goto.locator("#content-view")
        expect(content_view).to_be_visible()

        home_view = page_goto.locator("#home-view")
        expect(home_view).not_to_be_visible()

        content_btn = page_goto.locator('.nav-btn[data-view="content"]')
        expect(content_btn).to_have_class("active")

    def test_switch_to_about_view(self, page_goto: Page):
        """TC004: 点击「关于」按钮切换到关于视图"""
        page_goto.click('.nav-btn[data-view="about"]')

        about_view = page_goto.locator("#about-view")
        expect(about_view).to_be_visible()

        home_view = page_goto.locator("#home-view")
        expect(home_view).not_to_be_visible()

        about_btn = page_goto.locator('.nav-btn[data-view="about"]')
        expect(about_btn).to_have_class("active")

    def test_switch_back_to_home(self, page_goto: Page):
        """TC005: 从其他视图切换回首页"""
        # 先切换到关于
        page_goto.click('.nav-btn[data-view="about"]')
        expect(page_goto.locator("#about-view")).to_be_visible()

        # 再切换回首页
        page_goto.click('.nav-btn[data-view="home"]')
        expect(page_goto.locator("#home-view")).to_be_visible()
        expect(page_goto.locator("#about-view")).not_to_be_visible()

    def test_nav_buttons_count(self, page_goto: Page):
        """TC006: 导航栏有且仅有 3 个按钮"""
        nav_buttons = page_goto.locator(".nav-btn")
        expect(nav_buttons).to_have_count(3)

    def test_nav_button_labels(self, page_goto: Page):
        """TC007: 导航按钮文本正确"""
        expect(page_goto.locator('.nav-btn[data-view="home"]')).to_have_text("首页")
        expect(page_goto.locator('.nav-btn[data-view="content"]')).to_have_text("课本内容")
        expect(page_goto.locator('.nav-btn[data-view="about"]')).to_have_text("关于")

    def test_about_view_content(self, page_goto: Page):
        """TC008: 关于页面包含项目描述文本"""
        page_goto.click('.nav-btn[data-view="about"]')
        about_card = page_goto.locator(".about-card")
        expect(about_card).to_be_visible()
        expect(about_card).to_contain_text("人教版")
        expect(about_card).to_contain_text("PEP")

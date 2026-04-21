"""
单元选择测试：单元按钮点击与状态验证
"""
import pytest
from playwright.sync_api import Page, expect


class TestUnitSelection:
    """单元选择功能测试"""

    def test_unit_buttons_count(self, page_with_grade: Page):
        """TC040: 选择册次后显示 6 个单元按钮"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        btns = page_with_grade.locator("#unit-selector .unit-btn")
        expect(btns).to_have_count(6)

    def test_unit_buttons_have_emojis(self, page_with_grade: Page):
        """TC041: 单元按钮包含 emoji 图标"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")

        # 三年级上册 Unit 1 应该有 👋 emoji
        u1 = page_with_grade.locator('.unit-btn[data-unit="u1"]')
        expect(u1).to_contain_text("👋")

    def test_unit_button_labels(self, page_with_grade: Page):
        """TC042: 单元按钮文本包含单元名称"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")

        expect(page_with_grade.locator('.unit-btn[data-unit="u1"]')).to_contain_text("Unit 1")
        expect(page_with_grade.locator('.unit-btn[data-unit="u2"]')).to_contain_text("Unit 2")
        expect(page_with_grade.locator('.unit-btn[data-unit="u6"]')).to_contain_text("Unit 6")

    def test_select_unit_shows_content(self, page_with_grade: Page):
        """TC043: 点击单元按钮后展示内容"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        content = page_with_grade.locator("#content-display")
        expect(content).to_be_visible()
        expect(content).not_to_have_css("display", "none")

    def test_select_unit_active_state(self, page_with_grade: Page):
        """TC044: 选中的单元按钮有 active 样式"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')

        btn = page_with_grade.locator('.unit-btn[data-unit="u1"]')
        expect(btn).to_have_class("active")

    def test_select_unit_switches_active(self, page_with_grade: Page):
        """TC045: 切换单元后 active 状态跟随"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")

        page_with_grade.click('.unit-btn[data-unit="u1"]')
        expect(page_with_grade.locator('.unit-btn[data-unit="u1"]')).to_have_class("active")

        page_with_grade.click('.unit-btn[data-unit="u2"]')
        expect(page_with_grade.locator('.unit-btn[data-unit="u2"]')).to_have_class("active")
        expect(page_with_grade.locator('.unit-btn[data-unit="u1"]')).not_to_have_class("active")

    def test_select_unit_updates_breadcrumb(self, page_with_grade: Page):
        """TC046: 选择单元后面包屑显示单元名称"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        breadcrumb = page_with_grade.locator("#breadcrumb")
        expect(breadcrumb).to_contain_text("Unit 1")

    def test_select_unit_shows_unit_title(self, page_with_grade: Page):
        """TC047: 内容展示区标题与所选单元一致"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        title = page_with_grade.locator("#content-display h2")
        expect(title).to_contain_text("Unit 1 Hello!")

    def test_different_grades_different_units(self, page_goto: Page):
        """TC048: 不同年级的单元内容不同"""
        # 三年级上册 Unit 1
        page_goto.click('.grade-card[data-grade="g3"]')
        page_goto.wait_for_selector("#volume-selector .volume-btn")
        page_goto.click('.volume-btn[data-volume="v1"]')
        page_goto.wait_for_selector("#unit-selector .unit-btn")
        page_goto.click('.unit-btn[data-unit="u1"]')
        page_goto.wait_for_selector("#content-display h2")
        expect(page_goto.locator("#content-display h2")).to_contain_text("Hello!")

        # 切换到六年级上册 Unit 1
        page_goto.click('.breadcrumb-item[data-action="reset"]')
        page_goto.wait_for_selector(".grade-card")
        page_goto.click('.grade-card[data-grade="g6"]')
        page_goto.wait_for_selector("#volume-selector .volume-btn")
        page_goto.click('.volume-btn[data-volume="v1"]')
        page_goto.wait_for_selector("#unit-selector .unit-btn")
        page_goto.click('.unit-btn[data-unit="u1"]')
        page_goto.wait_for_selector("#content-display h2")
        expect(page_goto.locator("#content-display h2")).to_contain_text("How can I get there?")

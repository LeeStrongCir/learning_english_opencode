"""
面包屑导航测试：路径显示与回退功能
"""
import pytest
from playwright.sync_api import Page, expect


class TestBreadcrumb:
    """面包屑导航功能测试"""

    def test_breadcrumb_empty_on_home(self, page_goto: Page):
        """TC070: 首页面包屑为空"""
        breadcrumb = page_goto.locator("#breadcrumb")
        expect(breadcrumb).to_be_visible()
        # 首页时面包屑容器存在但无内容
        items = breadcrumb.locator(".breadcrumb-item")
        expect(items).to_have_count(0)

    def test_breadcrumb_shows_grade(self, page_with_grade: Page):
        """TC071: 选择年级后面包屑显示年级名称"""
        breadcrumb = page_with_grade.locator("#breadcrumb")
        expect(breadcrumb).to_contain_text("三年级")

    def test_breadcrumb_grade_item_count(self, page_with_grade: Page):
        """TC072: 选择年级后面包屑有 1 个项目"""
        items = page_with_grade.locator("#breadcrumb .breadcrumb-item")
        expect(items).to_have_count(1)

    def test_breadcrumb_shows_volume(self, page_with_grade: Page):
        """TC073: 选择册次后面包屑显示年级 + 册次"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#breadcrumb .breadcrumb-item")

        items = page_with_grade.locator("#breadcrumb .breadcrumb-item")
        expect(items).to_have_count(2)
        expect(page_with_grade.locator("#breadcrumb")).to_contain_text("上册")

    def test_breadcrumb_shows_unit(self, page_with_grade: Page):
        """TC074: 选择单元后面包屑显示完整路径"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        items = page_with_grade.locator("#breadcrumb .breadcrumb-item")
        expect(items).to_have_count(3)

        breadcrumb_text = page_with_grade.locator("#breadcrumb").text_content()
        assert "三年级" in breadcrumb_text
        assert "上册" in breadcrumb_text
        assert "Unit 1" in breadcrumb_text

    def test_breadcrumb_active_unit(self, page_with_grade: Page):
        """TC075: 当前单元在面包屑中为 active 状态"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        active_item = page_with_grade.locator("#breadcrumb .breadcrumb-item.active")
        expect(active_item).to_be_visible()
        expect(active_item).to_contain_text("Unit 1")

    def test_breadcrumb_separator(self, page_with_grade: Page):
        """TC076: 面包屑项目之间有分隔符"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        separators = page_with_grade.locator("#breadcrumb .breadcrumb-sep")
        expect(separators).to_have_count(2)

    def test_breadcrumb_click_grade_resets(self, page_with_grade: Page):
        """TC077: 点击面包屑中的年级回到首页"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        # 点击年级面包屑项（data-action="reset"）
        page_with_grade.click('#breadcrumb .breadcrumb-item[data-action="reset"]')

        expect(page_with_grade.locator("#home-view")).to_be_visible()
        expect(page_with_grade.locator("#content-view")).not_to_be_visible()

    def test_breadcrumb_click_volume_goes_back(self, page_with_grade: Page):
        """TC078: 点击面包屑中的册次回到册次选择"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        # 点击册次面包屑项（data-action="select-volume"）
        page_with_grade.click('#breadcrumb .breadcrumb-item[data-action="select-volume"]')

        # 应该回到册次选择状态，内容隐藏
        content = page_with_grade.locator("#content-display")
        expect(content).to_have_css("display", "none")

        # 单元选择器应被清空（因为重置了 selectedUnit）
        unit_btns = page_with_grade.locator("#unit-selector .unit-btn")
        expect(unit_btns).to_have_count(0)

    def test_breadcrumb_after_reset_empty(self, page_with_grade: Page):
        """TC079: 重置选择后面包屑为空"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")

        page_with_grade.click('#breadcrumb .breadcrumb-item[data-action="reset"]')
        page_with_grade.wait_for_selector(".grade-card")

        items = page_with_grade.locator("#breadcrumb .breadcrumb-item")
        expect(items).to_have_count(0)

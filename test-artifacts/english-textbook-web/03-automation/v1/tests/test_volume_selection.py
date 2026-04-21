"""
册次选择测试：上册/下册按钮点击与状态验证
"""
import pytest
from playwright.sync_api import Page, expect


VOLUMES = [
    ("v1", "上册"),
    ("v2", "下册"),
]


class TestVolumeSelection:
    """册次选择功能测试"""

    def test_volume_buttons_count(self, page_with_grade: Page):
        """TC030: 册次选择器显示 2 个按钮"""
        btns = page_with_grade.locator("#volume-selector .volume-btn")
        expect(btns).to_have_count(2)

    @pytest.mark.parametrize("vol_id,vol_name", VOLUMES)
    def test_volume_button_exists(self, page_with_grade: Page, vol_id, vol_name):
        """TC031-TC032: 上册/下册按钮都存在且文本正确"""
        btn = page_with_grade.locator(f'.volume-btn[data-volume="{vol_id}"]')
        expect(btn).to_be_visible()
        expect(btn).to_contain_text(vol_name)

    def test_volume_button_emojis(self, page_with_grade: Page):
        """TC033: 册次按钮包含 emoji（📗 上册 / 📕 下册）"""
        expect(page_with_grade.locator('.volume-btn[data-volume="v1"]')).to_contain_text("📗")
        expect(page_with_grade.locator('.volume-btn[data-volume="v2"]')).to_contain_text("📕")

    def test_select_volume_shows_unit_selector(self, page_with_grade: Page):
        """TC034: 点击册次按钮后显示单元选择器"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        unit_btns = page_with_grade.locator("#unit-selector .unit-btn")
        expect(unit_btns).to_have_count(6)

    def test_select_volume_active_state(self, page_with_grade: Page):
        """TC035: 选中的册次按钮有 active 样式"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        btn = page_with_grade.locator('.volume-btn[data-volume="v1"]')
        expect(btn).to_have_class("active")

    def test_select_volume_switches_active(self, page_with_grade: Page):
        """TC036: 切换册次后 active 状态跟随切换"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        expect(page_with_grade.locator('.volume-btn[data-volume="v1"]')).to_have_class("active")

        page_with_grade.click('.volume-btn[data-volume="v2"]')
        expect(page_with_grade.locator('.volume-btn[data-volume="v2"]')).to_have_class("active")
        expect(page_with_grade.locator('.volume-btn[data-volume="v1"]')).not_to_have_class("active")

    def test_select_volume_updates_breadcrumb(self, page_with_grade: Page):
        """TC037: 选择册次后面包屑更新"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        breadcrumb = page_with_grade.locator("#breadcrumb")
        expect(breadcrumb).to_contain_text("上册")

    def test_select_volume_resets_unit(self, page_with_grade: Page):
        """TC038: 切换册次后单元选择器重新渲染（对应新册次的单元）"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        first_unit_v1 = page_with_grade.locator("#unit-selector .unit-btn").first
        expect(first_unit_v1).to_contain_text("Unit 1")

        page_with_grade.click('.volume-btn[data-volume="v2"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        first_unit_v2 = page_with_grade.locator("#unit-selector .unit-btn").first
        expect(first_unit_v2).to_contain_text("Unit 1")

    def test_select_volume_hides_content(self, page_with_grade: Page):
        """TC039: 选择册次后内容展示区隐藏（需选择单元后才展示）"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        content = page_with_grade.locator("#content-display")
        # 选择册次后 content-display 应被隐藏
        expect(content).to_have_css("display", "none")

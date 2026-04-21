"""
年级选择测试：三至六年级卡片点击与状态验证
"""
import pytest
from playwright.sync_api import Page, expect


GRADES = [
    ("g3", "三年级"),
    ("g4", "四年级"),
    ("g5", "五年级"),
    ("g6", "六年级"),
]


class TestGradeSelection:
    """年级选择功能测试"""

    def test_grade_cards_count(self, page_goto: Page):
        """TC010: 首页显示 4 个年级卡片"""
        cards = page_goto.locator(".grade-card")
        expect(cards).to_have_count(4)

    @pytest.mark.parametrize("grade_id,grade_name", GRADES)
    def test_grade_card_exists(self, page_goto: Page, grade_id, grade_name):
        """TC011-TC014: 每个年级卡片都存在且文本正确"""
        card = page_goto.locator(f'.grade-card[data-grade="{grade_id}"]')
        expect(card).to_be_visible()
        expect(card).to_contain_text(grade_name)

    def test_select_grade_switches_to_content(self, page_goto: Page):
        """TC015: 点击年级卡片后自动切换到内容视图"""
        page_goto.click('.grade-card[data-grade="g3"]')

        expect(page_goto.locator("#content-view")).to_be_visible()
        expect(page_goto.locator("#home-view")).not_to_be_visible()

    def test_select_grade_shows_volume_selector(self, page_goto: Page):
        """TC016: 选择年级后显示册次选择器"""
        page_goto.click('.grade-card[data-grade="g3"]')
        volume_btns = page_goto.locator("#volume-selector .volume-btn")
        expect(volume_btns).to_have_count(2)

    def test_select_grade_nav_button_active(self, page_goto: Page):
        """TC017: 选择年级后「课本内容」导航按钮激活"""
        page_goto.click('.grade-card[data-grade="g3"]')

        expect(page_goto.locator('.nav-btn[data-view="content"]')).to_have_class("active")
        expect(page_goto.locator('.nav-btn[data-view="home"]')).not_to_have_class("active")

    def test_select_grade_highlights_card(self, page_goto: Page):
        """TC018: 选中的年级卡片有边框高亮"""
        page_goto.click('.grade-card[data-grade="g4"]')

        card = page_goto.locator('.grade-card[data-grade="g4"]')
        style = card.get_attribute("style")
        assert "border-color" in style or "borderColor" in style

    @pytest.mark.parametrize("grade_id,grade_name", GRADES)
    def test_select_each_grade(self, page_goto: Page, grade_id, grade_name):
        """TC019-TC022: 分别选择每个年级都能正常切换"""
        page_goto.click(f'.grade-card[data-grade="{grade_id}"]')
        expect(page_goto.locator("#content-view")).to_be_visible()

        breadcrumb = page_goto.locator("#breadcrumb")
        expect(breadcrumb).to_contain_text(grade_name)

    def test_grade_card_emojis(self, page_goto: Page):
        """TC023: 年级卡片包含 emoji 图标"""
        emojis = ["🌱", "🌿", "🌳", "🌲"]
        for emoji in emojis:
            expect(page_goto.locator(f"text={emoji}").first).to_be_visible()

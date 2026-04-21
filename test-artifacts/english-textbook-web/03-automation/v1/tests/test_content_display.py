"""
内容展示测试：词汇卡片 / 句型卡片 / 对话项 渲染验证
"""
import pytest
from playwright.sync_api import Page, expect


class TestContentDisplay:
    """内容展示功能测试"""

    def test_content_has_word_section(self, page_with_unit: Page):
        """TC050: 内容展示区包含词汇部分"""
        expect(page_with_unit.locator("#content-display")).to_contain_text("重点词汇")

    def test_content_has_sentence_section(self, page_with_unit: Page):
        """TC051: 内容展示区包含句型部分"""
        expect(page_with_unit.locator("#content-display")).to_contain_text("重点句型")

    def test_content_has_dialogue_section(self, page_with_unit: Page):
        """TC052: 内容展示区包含对话部分"""
        expect(page_with_unit.locator("#content-display")).to_contain_text("情景对话")

    def test_word_cards_rendered(self, page_with_unit: Page):
        """TC053: 词汇卡片正确渲染（三年级上册 Unit 1 有 6 个单词）"""
        cards = page_with_unit.locator(".word-card")
        expect(cards).to_have_count(6)

    def test_word_card_content(self, page_with_unit: Page):
        """TC054: 词汇卡片包含英文、音标、中文"""
        first_card = page_with_unit.locator(".word-card").first

        expect(first_card.locator(".english")).to_be_visible()
        expect(first_card.locator(".phonetic")).to_be_visible()
        expect(first_card.locator(".chinese")).to_be_visible()

    def test_first_word_is_hello(self, page_with_unit: Page):
        """TC055: 三年级上册 Unit 1 第一个单词是 hello"""
        first_english = page_with_unit.locator(".word-card .english").first
        expect(first_english).to_have_text("hello")

    def test_sentence_cards_rendered(self, page_with_unit: Page):
        """TC056: 句型卡片正确渲染（三年级上册 Unit 1 有 3 个句型）"""
        cards = page_with_unit.locator(".sentence-card")
        expect(cards).to_have_count(3)

    def test_sentence_card_content(self, page_with_unit: Page):
        """TC057: 句型卡片包含英文和中文"""
        first_sentence = page_with_unit.locator(".sentence-card").first

        expect(first_sentence.locator(".english")).to_be_visible()
        expect(first_sentence.locator(".chinese")).to_be_visible()

    def test_first_sentence(self, page_with_unit: Page):
        """TC058: 三年级上册 Unit 1 第一个句型是 Hello, I'm Mike."""
        first_english = page_with_unit.locator(".sentence-card .english").first
        expect(first_english).to_have_text("Hello, I'm Mike.")

    def test_dialogue_items_rendered(self, page_with_unit: Page):
        """TC059: 对话项正确渲染（三年级上册 Unit 1 有 2 条对话）"""
        items = page_with_unit.locator(".dialogue-item")
        expect(items).to_have_count(2)

    def test_dialogue_has_avatar(self, page_with_unit: Page):
        """TC060: 对话项包含头像"""
        avatars = page_with_unit.locator(".dialogue-avatar")
        expect(avatars).to_have_count(2)

    def test_dialogue_has_speaker(self, page_with_unit: Page):
        """TC061: 对话项包含说话人标识"""
        speakers = page_with_unit.locator(".dialogue-content .speaker")
        expect(speakers).to_have_count(2)

    def test_dialogue_has_text(self, page_with_unit: Page):
        """TC062: 对话项包含英文对话文本"""
        texts = page_with_unit.locator(".dialogue-content .text")
        expect(texts).to_have_count(2)

    def test_dialogue_has_translation(self, page_with_unit: Page):
        """TC063: 对话项包含中文翻译"""
        translations = page_with_unit.locator(".dialogue-content .translation")
        expect(translations).to_have_count(2)

    def test_content_title_matches_unit(self, page_with_unit: Page):
        """TC064: 内容标题与所选单元匹配"""
        title = page_with_unit.locator("#content-display h2")
        expect(title).to_contain_text("Unit 1 Hello!")
        expect(title).to_contain_text("👋")

    def test_different_unit_different_content(self, page_with_grade: Page):
        """TC065: 不同单元展示不同内容"""
        # 选择 Unit 1
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")
        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display h2")
        expect(page_with_grade.locator("#content-display h2")).to_contain_text("Hello!")

        # 选择 Unit 2
        page_with_grade.click('.unit-btn[data-unit="u2"]')
        page_with_grade.wait_for_selector("#content-display h2")
        expect(page_with_grade.locator("#content-display h2")).to_contain_text("Colours")

    def test_word_count_varies_by_unit(self, page_with_grade: Page):
        """TC066: 不同单元的词汇数量可能不同"""
        page_with_grade.click('.volume-btn[data-volume="v1"]')
        page_with_grade.wait_for_selector("#unit-selector .unit-btn")

        page_with_grade.click('.unit-btn[data-unit="u1"]')
        page_with_grade.wait_for_selector("#content-display .word-card")
        u1_count = page_with_grade.locator(".word-card").count()

        page_with_grade.click('.unit-btn[data-unit="u3"]')
        page_with_grade.wait_for_selector("#content-display .word-card")
        u3_count = page_with_grade.locator(".word-card").count()

        # 两个单元都有词汇卡片（至少 1 个）
        assert u1_count >= 1
        assert u3_count >= 1

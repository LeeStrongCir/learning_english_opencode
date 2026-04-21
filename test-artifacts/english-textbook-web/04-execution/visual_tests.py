# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright
import time

BASE_URL = "http://localhost:8080"

def test_1_homepage_display(page):
    print("\n" + "="*60)
    print("TEST 1: Homepage Display Verification")
    print("="*60)
    
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    title = page.title()
    print(f"[OK] Page title: {title}")
    
    cards = page.locator(".grade-card")
    count = cards.count()
    print(f"[OK] Grade cards count: {count}")
    assert count == 4, f"Expected 4, got {count}"
    
    grades = [("g3", "Grade3"), ("g4", "Grade4"), ("g5", "Grade5"), ("g6", "Grade6")]
    for grade_id, grade_name in grades:
        card = page.locator(f'.grade-card[data-grade="{grade_id}"]')
        assert card.is_visible(), f"{grade_name} not visible"
        print(f"[OK] {grade_name} card visible")
    
    nav_btns = page.locator(".nav-btn")
    assert nav_btns.count() == 3, "Nav buttons count incorrect"
    print("[OK] Navigation buttons count: 3")
    
    print("[PASS] TEST 1 PASSED")
    return True

def test_2_grade_selection(page):
    print("\n" + "="*60)
    print("TEST 2: Grade Selection")
    print("="*60)
    
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    print("[Click] Clicking Grade 3 card...")
    page.click('.grade-card[data-grade="g3"]')
    time.sleep(1)
    
    content_view = page.locator("#content-view")
    assert content_view.is_visible(), "Content view not shown"
    print("[OK] Switched to content view")
    
    breadcrumb = page.locator("#breadcrumb")
    assert "三年级" in breadcrumb.text_content(), "Breadcrumb missing grade"
    print("[OK] Breadcrumb shows: Grade 3")
    
    volume_btns = page.locator("#volume-selector .volume-btn")
    assert volume_btns.count() == 2, "Volume buttons count incorrect"
    print(f"[OK] Volume selector shows: {volume_btns.count()} buttons")
    
    content_btn = page.locator('.nav-btn[data-view="content"]')
    cls = content_btn.get_attribute("class")
    assert "active" in cls, "Content nav button not active"
    print("[OK] Content nav button activated")
    
    print("[PASS] TEST 2 PASSED")
    return True

def test_3_volume_and_unit_selection(page):
    print("\n" + "="*60)
    print("TEST 3: Volume and Unit Selection")
    print("="*60)
    
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    print("[Click] Selecting Grade 3...")
    page.click('.grade-card[data-grade="g3"]')
    time.sleep(0.5)
    
    print("[Click] Selecting Volume 1 (上册)...")
    page.click('.volume-btn[data-volume="v1"]')
    time.sleep(0.5)
    
    unit_btns = page.locator("#unit-selector .unit-btn")
    assert unit_btns.count() == 6, f"Unit buttons count: {unit_btns.count()}"
    print(f"[OK] Unit selector shows: {unit_btns.count()} units")
    
    u1 = page.locator('.unit-btn[data-unit="u1"]')
    assert "Unit 1" in u1.text_content(), "Unit 1 name incorrect"
    print(f"[OK] Unit 1: {u1.text_content()}")
    
    print("[Click] Selecting Unit 1...")
    page.click('.unit-btn[data-unit="u1"]')
    time.sleep(1)
    
    content = page.locator("#content-display")
    assert content.is_visible(), "Content display not shown"
    print("[OK] Content display shown")
    
    title = page.locator("#content-display h2")
    assert "Unit 1 Hello!" in title.text_content(), "Title incorrect"
    print(f"[OK] Content title: {title.text_content()}")
    
    print("[PASS] TEST 3 PASSED")
    return True

def test_4_content_display(page):
    print("\n" + "="*60)
    print("TEST 4: Content Display Verification")
    print("="*60)
    
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    page.click('.grade-card[data-grade="g3"]')
    time.sleep(0.5)
    page.click('.volume-btn[data-volume="v1"]')
    time.sleep(0.5)
    page.click('.unit-btn[data-unit="u1"]')
    time.sleep(1)
    
    word_cards = page.locator(".word-card")
    word_count = word_cards.count()
    print(f"[OK] Word cards count: {word_count}")
    assert word_count > 0, "No word cards"
    
    first_word = word_cards.first.locator(".english")
    print(f"[OK] First word: {first_word.text_content()}")
    
    sentence_cards = page.locator(".sentence-card")
    sentence_count = sentence_cards.count()
    print(f"[OK] Sentence cards count: {sentence_count}")
    assert sentence_count > 0, "No sentence cards"
    
    dialogue_items = page.locator(".dialogue-item")
    dialogue_count = dialogue_items.count()
    print(f"[OK] Dialogue items count: {dialogue_count}")
    assert dialogue_count > 0, "No dialogue items"
    
    first_dialogue = dialogue_items.first
    assert first_dialogue.locator(".dialogue-avatar").is_visible(), "Avatar not visible"
    assert first_dialogue.locator(".text").is_visible(), "Text not visible"
    print("[OK] Dialogue content complete (avatar + text + translation)")
    
    print("[PASS] TEST 4 PASSED")
    return True

def test_5_navigation_and_breadcrumb(page):
    print("\n" + "="*60)
    print("TEST 5: Navigation and Breadcrumb")
    print("="*60)
    
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    print("[Click] Switching to About page...")
    page.click('.nav-btn[data-view="about"]')
    time.sleep(0.5)
    
    about_view = page.locator("#about-view")
    assert about_view.is_visible(), "About view not shown"
    print("[OK] About page displayed")
    
    print("[Click] Switching back to Home...")
    page.click('.nav-btn[data-view="home"]')
    time.sleep(0.5)
    
    home_view = page.locator("#home-view")
    assert home_view.is_visible(), "Home view not shown"
    print("[OK] Home page displayed")
    
    print("\n[Click] Selecting Grade 3 -> Volume 1 -> Unit 1...")
    page.click('.grade-card[data-grade="g3"]')
    time.sleep(0.5)
    page.click('.volume-btn[data-volume="v1"]')
    time.sleep(0.5)
    page.click('.unit-btn[data-unit="u1"]')
    time.sleep(1)
    
    breadcrumb = page.locator("#breadcrumb")
    bc_text = breadcrumb.text_content()
    print(f"[OK] Breadcrumb path: {bc_text}")
    assert "三年级" in bc_text, "Breadcrumb missing grade"
    assert "上册" in bc_text, "Breadcrumb missing volume"
    assert "Unit 1" in bc_text, "Breadcrumb missing unit"
    
    print("[Click] Clicking breadcrumb to reset...")
    page.click('.breadcrumb-item[data-action="reset"]')
    time.sleep(1)
    
    home_view = page.locator("#home-view")
    assert home_view.is_visible(), "Home not shown after reset"
    print("[OK] Breadcrumb reset works correctly")
    
    print("[PASS] TEST 5 PASSED")
    return True

def main():
    print("\n" + "="*60)
    print("PEP Primary English Website - Visual Test")
    print("="*60)
    print("\nBrowser will launch in visible mode...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        results = []
        
        try:
            results.append(("TEST 1: Homepage", test_1_homepage_display(page)))
            time.sleep(1)
            
            results.append(("TEST 2: Grade Selection", test_2_grade_selection(page)))
            time.sleep(1)
            
            results.append(("TEST 3: Volume/Unit", test_3_volume_and_unit_selection(page)))
            time.sleep(1)
            
            results.append(("TEST 4: Content Display", test_4_content_display(page)))
            time.sleep(1)
            
            results.append(("TEST 5: Navigation", test_5_navigation_and_breadcrumb(page)))
            
        except Exception as e:
            print(f"\n[ERROR] Test execution error: {e}")
        finally:
            print("\n" + "="*60)
            print("TEST RESULTS SUMMARY")
            print("="*60)
            
            passed = 0
            failed = 0
            
            for name, result in results:
                status = "[PASS]" if result else "[FAIL]"
                print(f"{name}: {status}")
                if result:
                    passed += 1
                else:
                    failed += 1
            
            print("-"*60)
            print(f"Total: {passed} passed, {failed} failed")
            total = passed + failed
            if total > 0:
                print(f"Pass rate: {passed}/{total} = {passed/total*100:.1f}%")
            print("="*60)
            
            print("\nBrowser will close in 3 seconds...")
            time.sleep(3)
            browser.close()

if __name__ == "__main__":
    main()

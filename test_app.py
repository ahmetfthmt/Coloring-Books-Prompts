"""Coloring Book Prompts uygulaması için stabil Playwright smoke testi."""

import os
import re
from playwright.sync_api import sync_playwright, expect


def test_coloring_book_app():
    headless = os.getenv("HEADLESS", "1") == "1"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        console_messages = []
        page.on("console", lambda msg: console_messages.append(f"{msg.type}: {msg.text}"))

        page.goto("http://localhost:8000", wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")

        expect(page.locator("#welcomeScreen")).to_be_visible()
        expect(page.locator(".welcome-title")).to_contain_text("Coloring Book Prompts")

        # Scroll ile uygulamayı görünür hale getir
        page.evaluate(
            """
            () => {
                const spacer = document.createElement('div');
                spacer.id = 'test-spacer';
                spacer.style.height = '1400px';
                document.body.appendChild(spacer);
                const ws = document.getElementById('welcomeScreen');
                const target = Math.max(200, ws.offsetHeight * 0.6) + 80;
                window.scrollTo(0, target);
            }
            """
        )
        page.wait_for_function("document.getElementById('mainApp').classList.contains('active')")

        search_input = page.locator("#searchInput")
        prompts_grid = page.locator("#promptsGrid")

        search_input.fill("cat")
        expect(prompts_grid).to_be_visible()
        page.wait_for_function("document.querySelectorAll('.prompt-card').length > 0")

        # Kategori butonları render edildi mi?
        page.wait_for_function("document.querySelectorAll('.pill').length > 0")
        first_pill = page.locator(".pill").first
        first_pill.click()
        expect(first_pill).to_have_class(re.compile(r".*active.*"))

        # Highlight kontrolü
        page.wait_for_function("document.querySelectorAll('.match').length > 0")

        # Boş sonuç kontrolü
        search_input.fill("__this_should_not_exist__")
        expect(page.locator("text=No prompts found")).to_be_visible()

        js_errors = [m for m in console_messages if "error" in m.lower()]
        assert not js_errors, f"Console error bulundu: {js_errors[:3]}"

        browser.close()


if __name__ == "__main__":
    test_coloring_book_app()

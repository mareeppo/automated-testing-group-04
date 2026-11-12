import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://demo.playwright.dev/todomvc/")
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_role("textbox", name="What needs to be done?").fill("Try the recorder")
    page.get_by_role("textbox", name="What needs to be done?").press("Enter")
    expect(page.get_by_test_id("todo-title")).to_contain_text("Try the recorder")
    expect(page.locator(".todo-list li label")).to_have_text(
    ["Try the recorder"]
)
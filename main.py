from playwright.sync_api import sync_playwright
from humanoid import HumanoidMouse
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    mouse = HumanoidMouse(page=page)
    page.goto("http://localhost:8000/bands/")
    path = mouse.click("//button")
    page.close()

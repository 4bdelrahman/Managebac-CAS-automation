"""
Direct CAS submission - simplified version.
"""

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

with open('.tmp/generated_reflection.txt', 'r', encoding='utf-8') as f:
    reflection = f.read()

print("🚀 Opening ManageBac...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Login
    print("🔐 Please log in manually in the browser...")
    page.goto("https://eiszayed.managebac.com/")
    
    # Wait for user to login
    print("⏳ Waiting for you to log in...")
    page.wait_for_url("**/student/**", timeout=60000)
    
    print("✅ Logged in!")
    
    # Go to reflections page
    print("📍 Navigating to CAS reflections...")
    page.goto("https://eiszayed.managebac.com/student/ib/activity/cas/26158447/reflections")
    time.sleep(3)
    
    # Click Journal
    print("✍️ Clicking Journal...")
    page.locator('text=Journal').click()
    time.sleep(2)
    
    # Fill reflection
    print("📝 Filling in reflection...")
    editor = page.locator('div[contenteditable="true"]').first
    editor.click()
    editor.fill(reflection)
    
    print("\n✅ Reflection filled!")
    print("📌 Now please:")
    print("  1. Select learning outcomes 1, 4, 5")
    print("  2. Click 'Add Entry'")
    print("\nPress Enter when done...")
    input()
    
    # Screenshot
    page.screenshot(path=".tmp/submission_screenshot.png")
    print("📸 Screenshot saved!")
    
    browser.close()

print("✅ Complete!")

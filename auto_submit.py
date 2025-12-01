"""
Fully automated CAS reflection submission.
"""

import os
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

with open('.tmp/generated_reflection.txt', 'r', encoding='utf-8') as f:
    reflection = f.read()

print("🚀 FULLY AUTOMATED CAS SUBMISSION")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Step 1: Login
    print("🔐 Logging in...")
    page.goto("https://eiszayed.managebac.com/")
    time.sleep(2)
    
    page.fill('input[type="email"]', os.getenv('MANAGEBAC_USERNAME'))
    page.fill('input[type="password"]', os.getenv('MANAGEBAC_PASSWORD'))
    page.keyboard.press('Enter')
    
    print("⏳ Waiting for login...")
    time.sleep(5)
    
    # Step 2: Navigate to CAS reflections
    print("📍 Going to CAS reflections page...")
    page.goto("https://eiszayed.managebac.com/student/ib/activity/cas/26158447/reflections")
    time.sleep(3)
    
    # Step 3: Click Journal button
    print("✍️ Clicking Journal button...")
    page.get_by_role("link", name="Journal").click()
    time.sleep(2)
    
    # Step 4: Fill in reflection
    print("📝 Filling reflection text...")
    # Use JavaScript to set content directly (faster than typing)
    reflection_escaped = reflection.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    page.evaluate(f'''
        document.querySelector('div[contenteditable="true"]').innerHTML = "{reflection_escaped}";
    ''')
    time.sleep(1)
    
    # Step 5: Select learning outcomes (1, 4, 5)
    print("🎯 Selecting learning outcomes...")
    
    # Click outcome 1 - use the label
    page.get_by_text("Identify own strengths and develop areas for growth", exact=True).click()
    time.sleep(0.5)
    
    # Click outcome 4
    page.get_by_text("Show commitment to and perseverance in CAS experiences", exact=True).click()
    time.sleep(0.5)
    
    # Click outcome 5
    page.get_by_text("Demonstrate the skills and recognize the benefits of working collaboratively", exact=True).click()
    time.sleep(1)
    
    # Step 6: Submit
    print("✅ Clicking Add Entry...")
    page.get_by_role("button", name="Add Entry").click()
    time.sleep(3)
    
    # Take screenshot
    print("📸 Taking screenshot...")
    page.screenshot(path=".tmp/submission_success.png")
    
    print("\n" + "=" * 60)
    print("✅ SUBMISSION COMPLETE!")
    print("=" * 60)
    print("📸 Screenshot saved to: .tmp/submission_success.png")
    
    time.sleep(3)
    browser.close()

print("\n🎉 Done! Your CAS reflection has been submitted!")

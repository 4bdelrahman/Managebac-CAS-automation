"""
Simple browser opener - you do the rest manually.
"""

from playwright.sync_api import sync_playwright
import time

# Read the reflection
with open('.tmp/generated_reflection.txt', 'r', encoding='utf-8') as f:
    reflection = f.read()

print("=" * 60)
print("CAS REFLECTION - READY TO SUBMIT")
print("=" * 60)
print("\nYour reflection:")
print("-" * 60)
print(reflection)
print("-" * 60)

print("\n📋 INSTRUCTIONS:")
print("1. Browser will open to ManageBac")
print("2. Log in with your credentials")
print("3. Go to: https://eiszayed.managebac.com/student/ib/activity/cas/26158447/reflections")
print("4. Click 'Journal' button")
print("5. Paste the reflection (it's copied to clipboard)")
print("6. Select learning outcomes: 1, 4, 5")
print("7. Click 'Add Entry'")

input("\nPress Enter to open browser...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Copy reflection to clipboard
    page.evaluate(f"navigator.clipboard.writeText(`{reflection}`)")
    
    # Open ManageBac
    page.goto("https://eiszayed.managebac.com/")
    
    print("\n✅ Browser opened!")
    print("📋 Reflection is copied to clipboard - just paste it!")
    print("\nPress Enter when you're done to close browser...")
    input()
    
    browser.close()

print("✅ Done!")

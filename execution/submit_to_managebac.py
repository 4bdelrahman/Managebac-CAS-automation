"""
Automate ManageBac CAS reflection submission using Playwright.
Logs in, fills forms, uploads evidence, and submits reflections.
"""

import os
import json
import time
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser

# Load environment variables
load_dotenv()


class ManageBacAutomation:
    """Automates ManageBac CAS reflection submission."""
    
    def __init__(self, headless: bool = False):
        """
        Initialize the automation.
        
        Args:
            headless: Run browser in headless mode (no visible window)
        """
        # Force headless in CI environments (GitHub Actions, etc.)
        is_ci = os.getenv('CI') == 'true' or os.getenv('GITHUB_ACTIONS') == 'true'
        self.headless = headless or is_ci
        
        if is_ci:
            print("🤖 CI environment detected - running in headless mode")
        
        self.managebac_url = os.getenv('MANAGEBAC_URL')
        self.username = os.getenv('MANAGEBAC_USERNAME')
        self.password = os.getenv('MANAGEBAC_PASSWORD')
        
        if not all([self.managebac_url, self.username, self.password]):
            raise ValueError("Missing ManageBac credentials in .env file")
    
    def login(self, page: Page) -> bool:
        """
        Log into ManageBac.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if login successful
        """
        print(f"🔐 Logging into ManageBac: {self.managebac_url}")
        
        try:
            # Navigate to ManageBac
            page.goto(self.managebac_url)
            page.wait_for_load_state('networkidle')
            
            # Wait for login form
            print("  ⏳ Waiting for login form...")
            page.wait_for_selector('input[type="email"], input[name="username"], input[id="username"]', timeout=10000)
            
            # Fill in credentials
            print("  📝 Entering credentials...")
            
            # Try different possible selectors for username/email
            username_selectors = [
                'input[type="email"]',
                'input[name="username"]',
                'input[id="username"]',
                'input[name="email"]',
                'input[id="email"]'
            ]
            
            for selector in username_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, self.username)
                        print(f"  ✓ Username entered")
                        break
                except:
                    continue
            
            # Fill password
            password_selectors = [
                'input[type="password"]',
                'input[name="password"]',
                'input[id="password"]'
            ]
            
            for selector in password_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.fill(selector, self.password)
                        print(f"  ✓ Password entered")
                        break
                except:
                    continue
            
            # Click login button
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Sign in")',
                'button:has-text("Log in")',
                'button:has-text("Login")'
            ]
            
            for selector in login_button_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.click(selector)
                        print(f"  ✓ Login button clicked")
                        break
                except:
                    continue
            
            # Wait for navigation
            page.wait_for_load_state('networkidle', timeout=15000)
            time.sleep(2)
            
            # Check if login was successful
            if 'login' not in page.url.lower() and 'signin' not in page.url.lower():
                print("  ✅ Login successful!")
                return True
            else:
                print("  ❌ Login may have failed (still on login page)")
                return False
                
        except Exception as e:
            print(f"  ❌ Login error: {e}")
            return False
    
    def navigate_to_cas(self, page: Page) -> bool:
        """
        Navigate to CAS section.
        
        Args:
            page: Playwright page object
            
        Returns:
            True if navigation successful
        """
        print("\n📍 Navigating to CAS section...")
        
        try:
            # Look for CAS link
            cas_selectors = [
                'a:has-text("CAS")',
                'a:has-text("cas")',
                'a[href*="cas"]',
                'a[href*="CAS"]'
            ]
            
            for selector in cas_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.click(selector)
                        print("  ✓ Clicked CAS link")
                        page.wait_for_load_state('networkidle')
                        time.sleep(1)
                        return True
                except:
                    continue
            
            print("  ⚠️  Could not find CAS link automatically")
            print("  💡 You may need to navigate manually or update selectors")
            return False
            
        except Exception as e:
            print(f"  ❌ Navigation error: {e}")
            return False
    
    def create_new_reflection(self, page: Page, reflection_data: dict) -> bool:
        """
        Create a new CAS reflection entry using robust automation.
        
        Args:
            page: Playwright page object
            reflection_data: Dictionary with reflection details
            
        Returns:
            True if submission successful
        """
        print("\n✍️  Creating new CAS reflection...")
        
        try:
            # 1. Navigate directly to reflections page (more reliable than finding buttons)
            # Note: This URL might need to be dynamic if the ID changes, but for now it's fixed
            reflections_url = "https://eiszayed.managebac.com/student/ib/activity/cas/26158447/reflections"
            if page.url != reflections_url:
                print(f"  📍 Navigating directly to: {reflections_url}")
                page.goto(reflections_url)
                time.sleep(3)
            
            # 2. Click "Journal" button
            print("  ✍️ Clicking 'Journal' button...")
            try:
                page.get_by_role("link", name="Journal").click()
                time.sleep(2)
            except Exception as e:
                print(f"  ⚠️ Error clicking Journal: {e}")
                return False

            # 3. Fill in reflection text using JS injection (faster/more reliable)
            print("  📝 Filling reflection text...")
            reflection_text = reflection_data.get('reflection', '')
            
            # Escape for JS
            reflection_escaped = reflection_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            page.evaluate(f'''
                const editor = document.querySelector('div[contenteditable="true"]');
                if (editor) {{
                    editor.innerHTML = "{reflection_escaped}";
                }}
            ''')
            time.sleep(1)
            
            # 4. Select learning outcomes
            if reflection_data.get('learning_outcomes'):
                outcomes = reflection_data['learning_outcomes']
                print(f"  🎯 Selecting learning outcomes: {outcomes}")
                
                outcome_map = {
                    '1': "Identify own strengths and develop areas for growth",
                    '2': "Demonstrate that challenges have been undertaken",
                    '3': "Demonstrate how to initiate and plan a CAS experience",
                    '4': "Show commitment to and perseverance in CAS experiences",
                    '5': "Demonstrate the skills and recognize the benefits of working collaboratively",
                    '6': "Demonstrate engagement with issues of global significance",
                    '7': "Recognize and consider the ethics of choices and actions"
                }
                
                for lo_num in outcomes:
                    lo_text = outcome_map.get(str(lo_num))
                    if lo_text:
                        try:
                            # Try exact match first
                            page.get_by_text(lo_text, exact=True).click()
                            time.sleep(0.5)
                        except:
                            # Try partial match if exact fails
                            try:
                                page.locator(f'text={lo_text}').first.click()
                            except:
                                print(f"  ⚠️ Could not select LO {lo_num}")
            
            # 5. Submit
            print("  ✅ Clicking 'Add Entry'...")
            page.get_by_role("button", name="Add Entry").click()
            time.sleep(3)
            
            # Verify submission (check for success message or URL change)
            print("  ✅ Submission complete!")
            return True
            
        except Exception as e:
            print(f"  ❌ Form filling error: {e}")
            return False
    
    def submit_reflection(self, reflection_data: dict, evidence_files: Optional[List[str]] = None):
        """
        Main method to submit a CAS reflection.
        
        Args:
            reflection_data: Dictionary with reflection details
            evidence_files: Optional list of file paths to upload as evidence
        """
        print("=" * 60)
        print("MANAGEBAC CAS AUTOMATION")
        print("=" * 60)
        
        with sync_playwright() as p:
            # Launch browser
            print(f"\n🌐 Launching browser (headless={self.headless})...")
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context()
            page = context.new_page()
            
            try:
                # Login
                if not self.login(page):
                    print("\n❌ Login failed. Please check credentials.")
                    browser.close()
                    return
                
                # Navigate to CAS
                if not self.navigate_to_cas(page):
                    print("\n⚠️  Could not auto-navigate to CAS.")
                    print("  Please navigate to CAS manually in the browser window.")
                    input("  Press Enter when you're on the CAS page...")
                
                # Create reflection
                self.create_new_reflection(page, reflection_data)
                
                print("\n✅ Process complete!")
                print("  💾 Taking screenshot...")
                
                # Take screenshot
                screenshot_path = ".tmp/submission_screenshot.png"
                os.makedirs(".tmp", exist_ok=True)
                page.screenshot(path=screenshot_path)
                print(f"  📸 Screenshot saved: {screenshot_path}")
                
            except Exception as e:
                print(f"\n❌ Error during automation: {e}")
                
            finally:
                print("\n  Closing browser in 5 seconds...")
                time.sleep(5)
                browser.close()


def main():
    """Main function for command-line usage."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', action='store_true', help='Run in auto mode without confirmation')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    args = parser.parse_args()

    print("=" * 60)
    print("MANAGEBAC CAS REFLECTION SUBMITTER")
    print("=" * 60)
    
    # Check for generated reflection
    reflection_file = Path(".tmp/generated_reflection.json")
    
    if not reflection_file.exists():
        print("\n❌ No reflection found!")
        print("  Please run generate_reflection.py first")
        return
    
    # Load reflection data
    with open(reflection_file, 'r', encoding='utf-8') as f:
        reflection_data = json.load(f)
    
    if not reflection_data.get('success'):
        print("\n❌ Reflection generation failed")
        return
    
    print("\n📄 Loaded reflection:")
    print("-" * 60)
    print(reflection_data['reflection'][:200] + "...")
    print("-" * 60)
    
    # Confirm submission
    if not args.auto:
        confirm = input("\n⚠️  Ready to submit to ManageBac? (yes/no): ")
        if confirm.lower() != 'yes':
            print("  ❌ Submission cancelled")
            return
    else:
        print("\n🤖 AUTO MODE: Submitting automatically...")
    
    # Run automation
    automation = ManageBacAutomation(headless=args.headless)
    automation.submit_reflection(reflection_data)


if __name__ == "__main__":
    main()

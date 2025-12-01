"""
Setup script for CAS Automation.
Checks dependencies and configuration.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required = {
        'google.generativeai': 'google-generativeai',
        'playwright': 'playwright',
        'dotenv': 'python-dotenv',
        'PIL': 'Pillow'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
            missing.append(package)
    
    return missing


def check_env_file():
    """Check if .env file exists and has required variables."""
    print("\n⚙️  Checking configuration...")
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("  ❌ .env file not found")
        print("\n  📝 Creating .env file from env_config.txt...")
        
        config_file = Path('env_config.txt')
        if config_file.exists():
            # Copy to .env
            with open(config_file, 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("  ✅ .env file created")
            print("  ⚠️  Please edit .env and add your ManageBac credentials!")
            return False
        else:
            print("  ❌ env_config.txt not found either")
            return False
    
    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['GEMINI_API_KEY', 'MANAGEBAC_URL', 'MANAGEBAC_USERNAME', 'MANAGEBAC_PASSWORD']
    missing = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing.append(var)
            print(f"  ❌ {var} (not set)")
        else:
            # Mask sensitive values
            if 'KEY' in var or 'PASSWORD' in var:
                display = value[:10] + '...' if len(value) > 10 else '***'
            else:
                display = value
            print(f"  ✅ {var} = {display}")
    
    if missing:
        print(f"\n  ⚠️  Please set these variables in .env: {', '.join(missing)}")
        return False
    
    return True


def check_training_data():
    """Check if training data exists."""
    print("\n📚 Checking training data...")
    
    training_path = Path('Resala CAS Project trainng')
    
    if not training_path.exists():
        print(f"  ❌ Training data folder not found: {training_path}")
        return False
    
    text_path = training_path / 'Text training'
    photos_path = training_path / 'Photos training'
    
    if text_path.exists():
        reflections = list(text_path.glob('*.txt'))
        print(f"  ✅ Found {len(reflections)} text files")
    else:
        print(f"  ❌ Text training folder not found")
        return False
    
    if photos_path.exists():
        photos = list(photos_path.glob('*.jpeg')) + list(photos_path.glob('*.jpg')) + list(photos_path.glob('*.png'))
        print(f"  ✅ Found {len(photos)} photos")
    else:
        print(f"  ⚠️  Photos training folder not found")
    
    return True


def check_playwright_browsers():
    """Check if Playwright browsers are installed."""
    print("\n🌐 Checking Playwright browsers...")
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                print("  ✅ Chromium browser installed")
                return True
            except Exception as e:
                print("  ❌ Chromium browser not installed")
                print(f"     Error: {e}")
                return False
    except Exception as e:
        print(f"  ❌ Playwright not properly installed: {e}")
        return False


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("CAS AUTOMATION SETUP CHECK")
    print("=" * 60)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check dependencies
    missing = check_dependencies()
    if missing:
        all_good = False
        print(f"\n  📥 To install missing packages, run:")
        print(f"     pip install {' '.join(missing)}")
    
    # Check .env file
    if not check_env_file():
        all_good = False
    
    # Check training data
    if not check_training_data():
        all_good = False
    
    # Check Playwright browsers
    if not check_playwright_browsers():
        print("\n  📥 To install Playwright browsers, run:")
        print("     playwright install chromium")
        all_good = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_good:
        print("✅ SETUP COMPLETE - Ready to go!")
        print("=" * 60)
        print("\n🚀 To run the automation:")
        print("   python execution/cas_workflow_orchestrator.py")
    else:
        print("⚠️  SETUP INCOMPLETE - Please fix the issues above")
        print("=" * 60)
        print("\n📝 Quick setup commands:")
        if missing:
            print(f"   pip install {' '.join(missing)}")
        print("   playwright install chromium")
        print("   # Edit .env file with your credentials")
    
    print()


if __name__ == "__main__":
    main()

@echo off
echo ========================================
echo CAS Automation - Quick Setup
echo ========================================
echo.

echo [1/3] Installing Python packages...
pip install -q google-generativeai playwright python-dotenv Pillow

echo.
echo [2/3] Installing Playwright browser...
playwright install chromium

echo.
echo [3/3] Running setup check...
python execution\setup_check.py

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run the automation:
echo   python execution\cas_workflow_orchestrator.py
echo.
pause

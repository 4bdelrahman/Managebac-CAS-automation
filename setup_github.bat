@echo off
echo ========================================================
echo   CAS AUTOPILOT - GITHUB SETUP HELPER
echo ========================================================
echo.
echo This script will help you push your code to GitHub
echo and configure the secrets for the cloud autopilot.
echo.

:: 1. Create Repo
echo [1/3] Opening GitHub to create a new repository...
echo Please create a PRIVATE repository named "cas-automation"
start https://github.com/new
echo.
set /p REPO_URL="Paste the repository URL here (e.g., https://github.com/user/repo.git): "

:: 2. Push Code
echo.
echo [2/3] Pushing code to GitHub...
git remote add origin %REPO_URL%
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Push failed. Please check the URL and try again.
    pause
    exit /b
)

:: 3. Configure Secrets
echo.
echo [3/3] Opening Secrets configuration page...
echo.
echo ⚠️  You need to add these 4 Repository Secrets:
echo.
echo   1. GEMINI_API_KEY
echo   2. MANAGEBAC_URL
echo   3. MANAGEBAC_USERNAME
echo   4. MANAGEBAC_PASSWORD
echo.
echo (Copy these values from your .env file)
echo.

:: Extract repo name for the URL
for /f "tokens=4,5 delims=/" %%a in ("%REPO_URL%") do (
    set USER=%%a
    set REPO=%%b
)
:: Remove .git from repo name if present
set REPO=%REPO:.git=%

start https://github.com/%USER%/%REPO%/settings/secrets/actions

echo ✅ Setup Complete!
echo The cloud autopilot will now run every 4 days.
echo.
pause

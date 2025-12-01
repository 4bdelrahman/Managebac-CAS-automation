@echo off
echo ========================================================
echo   CAS AUTOPILOT - LOCAL SCHEDULER SETUP
echo ========================================================
echo.
echo This script will schedule the CAS automation to check
echo for due reflections every time you log in to Windows.
echo.

set "PYTHON_PATH=python"
set "SCRIPT_PATH=%~dp0execution\run_if_due.py"

echo Script path: %SCRIPT_PATH%
echo.

:: Create the task
schtasks /Create /SC ONLOGON /TN "CAS_Autopilot_Check" /TR "%PYTHON_PATH% \"%SCRIPT_PATH%\"" /F

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Task scheduled.
    echo The automation will now check if a reflection is due
    echo every time you log in.
) else (
    echo.
    echo ❌ FAILED. You might need to run this as Administrator.
)

echo.
pause

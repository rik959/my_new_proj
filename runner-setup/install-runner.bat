@echo off
echo ============================================
echo  💚 Love Pipeline — Self-Hosted Runner Setup
echo ============================================
echo.

:: --- Config ---
set RUNNER_DIR=C:\actions-runner
set RUNNER_VERSION=2.321.0

:: --- Check if Docker is installed ---
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is NOT installed. Install Docker Desktop first.
    echo    https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✅ Docker found.

:: --- Create runner directory ---
if not exist "%RUNNER_DIR%" mkdir "%RUNNER_DIR%"
cd /d "%RUNNER_DIR%"

:: --- Download runner ---
echo.
echo ⬇️  Downloading GitHub Actions Runner v%RUNNER_VERSION%...
curl -o actions-runner-win-x64.zip -L "https://github.com/actions/runner/releases/download/v%RUNNER_VERSION%/actions-runner-win-x64-%RUNNER_VERSION%.zip"

:: --- Extract ---
echo 📦 Extracting...
tar -xf actions-runner-win-x64.zip
del actions-runner-win-x64.zip

echo.
echo ============================================
echo  NEXT STEPS (manual):
echo ============================================
echo.
echo 1. Go to your GitHub repo:
echo    Settings → Actions → Runners → New self-hosted runner
echo.
echo 2. Copy the TOKEN from that page
echo.
echo 3. Run this command in C:\actions-runner:
echo    .\config.cmd --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN --name love-server --labels love-server
echo.
echo 4. Then start the runner:
echo    .\run.cmd
echo.
echo    OR install as a Windows service (auto-start on boot):
echo    .\svc.cmd install
echo    .\svc.cmd start
echo.
echo ============================================
pause

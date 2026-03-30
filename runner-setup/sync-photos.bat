@echo off
echo ============================================
echo  📸 Syncing photos to deployment volume
echo ============================================

set PHOTOS_SRC=%~dp0..\my_new_proj\photos
set PHOTOS_DST=%USERPROFILE%\love-pipeline-photos

if not exist "%PHOTOS_DST%" mkdir "%PHOTOS_DST%"

echo Source: %PHOTOS_SRC%
echo Dest:   %PHOTOS_DST%
echo.

xcopy "%PHOTOS_SRC%" "%PHOTOS_DST%" /E /I /Y /D

echo.
echo ✅ Photos synced! New photos will show up in the app.
echo    (Container mounts %PHOTOS_DST% as the photos directory)
pause

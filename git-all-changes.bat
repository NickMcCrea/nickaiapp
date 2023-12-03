@echo off
setlocal

REM Check if number of days was provided
if "%~1"=="" (
    echo Please provide the number of days as an argument.
    exit /b 1
)

REM Set the number of days
set "days=%~1"

REM Get the commit hash from X days ago
for /f "delims=" %%i in ('git rev-list -1 --before="%days% days ago" HEAD') do set "old_commit=%%i"

REM Show detailed changes for all files since that commit
git diff %old_commit% HEAD

endlocal

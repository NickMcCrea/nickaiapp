@echo off
setlocal

REM Check if file name and number of days were provided
if "%~1"=="" (
    echo Please provide the file name as the first argument.
    exit /b 1
)
if "%~2"=="" (
    echo Please provide the number of days as the second argument.
    exit /b 1
)

REM Set the file name and number of days
set "filename=%~1"
set "days=%~2"

REM Get the commit hash from X days ago
for /f "delims=" %%i in ('git rev-list -1 --before="%days% days ago" HEAD') do set "old_commit=%%i"

REM Show diff of the file since that commit
git diff %old_commit% HEAD -- "%filename%"

endlocal

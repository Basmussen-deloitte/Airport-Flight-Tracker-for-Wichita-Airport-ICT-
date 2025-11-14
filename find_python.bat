@echo off
REM Find Python installation
echo Searching for Python...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Python found in PATH:
    where python
) else (
    echo Python NOT in PATH. Checking common locations...
)

REM Check common Python install locations
if exist "C:\Python313\python.exe" echo Found: C:\Python313\python.exe
if exist "C:\Python312\python.exe" echo Found: C:\Python312\python.exe
if exist "C:\Python311\python.exe" echo Found: C:\Python311\python.exe
if exist "C:\Program Files\Python313\python.exe" echo Found: C:\Program Files\Python313\python.exe
if exist "%APPDATA%\Python\Python313\Scripts\pip.exe" echo Found: %APPDATA%\Python\Python313\Scripts\pip.exe

REM Check Python in user AppData
echo.
echo Checking user AppData\Local\Programs\Python...
dir "%LOCALAPPDATA%\Programs\Python" 2>nul

echo.
echo Get full Python path:
py -c "import sys; print(sys.executable)" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ^(Using 'py' launcher - this should work^)
) else (
    echo 'py' launcher not found either
)

echo.
echo System info:
wmic os get osarchitecture

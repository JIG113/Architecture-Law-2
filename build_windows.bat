@echo off
setlocal

if not exist .venv (
  py -m venv .venv
)
call .venv\Scripts\activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller==6.11.1

set ICON_ARG=
if exist assets\app.ico set ICON_ARG=--icon assets\app.ico

pyinstaller --noconfirm --windowed --name ArchitectureNoticeLauncher %ICON_ARG% --add-data "app;app" desktop_app.py

echo.
echo Build complete.
echo EXE path: dist\ArchitectureNoticeLauncher\ArchitectureNoticeLauncher.exe
pause

@echo off
nuitka main.py --standalone --onefile --enable-plugin=tk-inter --windows-icon-from-ico=icon.ico --include-package=modules --output-dir=build --output-filename=raider.exe --include-data-files=./icon.ico=./icon.ico
pause
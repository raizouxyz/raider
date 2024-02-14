@echo off
pyinstaller --clean --onefile --name raider --add-data icon.ico:icon.ico --add-binary tls-client-64.dll;tls_client/dependencies --icon icon.ico main.py
pause
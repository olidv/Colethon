@echo off

echo Limpando as pastas temporarias do projeto
del /f /q D:\Workspace\Python\Colethon\logs\*.*  1>nul  2>&1
del /f /q D:\Workspace\Python\Colethon\www\*.*   1>nul  2>&1
del /f /q D:\Workspace\Python\Colethon\tmp\*.*   1>nul  2>&1
echo.

rem DELME
exit /b

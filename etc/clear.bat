@echo off

echo Limpando as pastas temporarias do projeto
del /f /q D:\Workspace\Python\Infinite\logs\*.*  1>nul  2>&1
del /f /q D:\Workspace\Python\Infinite\www\*.*   1>nul  2>&1
del /f /q D:\Workspace\Python\Infinite\tmp\*.*   1>nul  2>&1
echo.

rem DELME
exit /b

@echo off
color E

rem Printa a apresentacao do deploy:
echo.
echo  DEPLOY DO INFINITE   [ D:\WORKSPACE\PYTHON\INFINITE\ETC\DEPLOY.BAT ]
echo.
echo.

echo  *********************************************
echo  **  INICIANDO  IMPLANTACAO  DO  INFINITE.  **
echo  *********************************************
echo.
echo.

echo Posicionando no diretorio raiz da aplicacao
cd /d C:\Apps\B3\Infinite
echo.

echo Limpando as pastas temporarias da aplicacao
rem del /f /q logs\*.*  1>nul  2>&1
del /f /q tmp\*.*   1>nul  2>&1
del /f /q www\*.*   1>nul  2>&1
echo.

echo Posicionando no diretorio do projeto
cd /d D:\Workspace\Python\Infinite\
echo.

echo Copiando os arquivos do projeto
xcopy dist\*.* C:\Apps\B3\Infinite  /E /C /Q /H /R /Y
echo.

rem Pausa final...
echo.
pause

@echo off
color E

rem Printa a apresentacao do deploy:
echo.
echo  DEPLOY DO COLETHON   [ D:\WORKSPACE\INFINITE\COLETHON\ETC\DEPLOY.BAT ]
echo.
echo.

echo  *********************************************
echo  **  INICIANDO  IMPLANTACAO  DO  COLETHON.  **
echo  *********************************************
echo.
echo.

echo Posicionando no diretorio raiz da aplicacao
mkdir C:\Apps\Infinite\Colethon  1>nul  2>&1
cd /d C:\Apps\Infinite\Colethon
echo.

echo Limpando as pastas temporarias da aplicacao
rem del /f /q logs\*.*  1>nul  2>&1
del /f /q tmp\*.*       1>nul  2>&1
del /f /q www\*.*       1>nul  2>&1
echo.

echo Posicionando no diretorio do projeto
cd /d D:\Workspace\Infinite\Colethon
echo.

echo Copiando os arquivos do projeto
xcopy dist\*.* C:\Apps\Infinite\Colethon  /E /C /Q /H /R /Y
echo.

echo Disponibilizando release da aplicacao para producao
copy /y dist\*.zip D:\Publico
echo.

rem Pausa final...
echo.
pause

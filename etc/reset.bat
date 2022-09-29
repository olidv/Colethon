@echo off

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Limpando as pastas temporarias do projeto
del /f /q logs\*.*  1>nul  2>&1
del /f /q www\*.*   1>nul  2>&1
del /f /q tmp\*.*   1>nul  2>&1
echo.

rem echo Limpando as pastas de arquivos dos terminais MT5
rem del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9AA5A2E564E1326FB93349159C9D30A4\MQL5\Files\*.*  1>nul  2>&1
rem del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9352866EDE8D3BAA5CDBEF2EC84D2C07\MQL5\Files\*.*  1>nul  2>&1
rem del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\886B601D7760693D209A707150753C26\MQL5\Files\*.*  1>nul  2>&1
rem echo.

rem echo Posicionando no diretorio  [ D:\PUBLICO ]
rem cd /D D:\Publico
rem echo.

rem echo Copiando arquivos das corretoras para o terminal da respectiva plataforma
rem xcopy genial\*.* C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9AA5A2E564E1326FB93349159C9D30A4\MQL5\Files  /E /C /Q /R /Y
rem xcopy modal\*.*  C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9352866EDE8D3BAA5CDBEF2EC84D2C07\MQL5\Files  /E /C /Q /R /Y
rem xcopy xm\*.*     C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\886B601D7760693D209A707150753C26\MQL5\Files  /E /C /Q /R /Y
rem echo.

rem Pausa final...
echo.
pause

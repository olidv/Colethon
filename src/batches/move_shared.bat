@echo off
color 6F

rem Printa a apresentacao do Colethon.
echo.
echo  MOVE SHARED   [ C:\APPS\INFINITE\COLETHON\BIN\MOVE_SHARED.BAT ]
echo.
echo.

rem verifica se o flag indicativo de processamento existe:
if exist D:\Publico\Colethon\safeToDelete.tmp goto yesfile

:nofile
color C
echo  ************************************************
echo  ** ATENCAO: FLAG safeToDelete NAO ENCONTRADO! **
echo  ************************************************
echo  **    ESTA  ROTINA  BATCH  SERA  ABORTADA.    **
echo  ************************************************
echo.
goto endbat

:yesfile
color B
echo  ************************************************
echo  **  FLAG OK: ARQUIVO safeToDelete ENCONTRADO. **
echo  ************************************************
echo  ** PREPARANDO P/ MOVER ARQUIVOS DE D:\PUBLICO **
echo  ************************************************
echo.
echo.

rem Obtem a data/hora atuais no formato AAAA-MM-DD:
set YYYY=%date:~-4%
set HOJE=%date:~-4%-%date:~3,2%
echo Data de referencia para as movimentacoes:  %HOJE%
echo.

echo Posicionando no diretorio D:\Publico
cd /D D:\Publico

echo Copiando arquivos contendo resultados das loterias da Caixa EF...
copy /y Colethon\Loto365\Lothon\data\caixa\D_*.htm C:\Apps\Loto365\Lothon\data\caixa\
move /Y Colethon\Loto365\Lothon\data\caixa\D_*.htm D:\Workspace\Loto365\Lothon\data\caixa\
echo.
copy /Y Colethon\Loto365\Lothon\data\cache\D_MAIS-MILIONARIA.csv D:\Workspace\Infinite\Colethon\data\
copy /Y Colethon\Loto365\Lothon\data\cache\D_*.csv C:\Apps\Loto365\Lothon\data\cache\
copy /Y Colethon\Loto365\Lothon\data\cache\D_*.csv D:\Workspace\Loto365\Lothon\data\cache\
move /Y Colethon\Loto365\Lothon\data\cache\D_*.csv D:\Workspace\Loto365\jLothon\data\cache\
echo.
copy /Y Colethon\Loto365\Lothon\data\cache\JC_*.csv C:\Apps\Loto365\Lothon\data\cache\
move /Y Colethon\Loto365\Lothon\data\cache\JC_*.csv D:\Workspace\Loto365\Lothon\data\cache\
echo.
copy /Y Colethon\Loto365\Lothon\data\palpite\*.csv C:\Apps\Loto365\Lothon\data\palpite\
move /Y Colethon\Loto365\Lothon\data\palpite\*.csv D:\Workspace\Loto365\Lothon\data\palpite\
echo.

echo Copiando arquivo CSV contendo a carteira do IBOVESP da Bolsa B3...
copy /Y Colethon\Infinite\Quanthon\data\b3\ibovespa\IBOVDia_*.csv C:\Apps\Infinite\Quanthon\data\b3\ibovespa
copy /Y Colethon\Infinite\Quanthon\data\b3\ibovespa\IBOVDia_*.csv C:\Apps\Infinite\Quanthon\data\b3\ibovespa
move /Y Colethon\Infinite\Quanthon\data\b3\ibovespa\IBOVDia_*.csv D:\B3\Data\B3\Carteira_IBOV\%YYYY%\%HOJE%
echo.

echo Copiando arquivos ZIP contendo cotacoes intraday da Bolsa B3...
copy /Y Colethon\Infinite\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip C:\Apps\Infinite\Quanthon\data\b3\cotacoes
copy /Y Colethon\Infinite\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip C:\Apps\Infinite\Quanthon\data\b3\cotacoes
move /Y Colethon\Infinite\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip D:\B3\Data\B3\Cotacoes_TRADEINTRADAY\%YYYY%\%HOJE%
echo.

echo Copiando arquivos de cotacoes da corretora Genial...
copy /Y Colethon\Infinite\Quanthon\data\mt5\genial\*.* C:\Apps\Infinite\Quanthon\data\mt5\genial
copy /Y Colethon\Infinite\Quanthon\data\mt5\genial\*.* C:\Apps\Infinite\Quanthon\data\mt5\genial
move /Y Colethon\Infinite\Quanthon\data\mt5\genial\*.* D:\B3\Data\Brasil\Genial_BookTick\mql5_files

echo Copiando arquivos de cotacoes da corretora Modal...
copy /Y Colethon\Infinite\Quanthon\data\mt5\modal\*.* C:\Apps\Infinite\Quanthon\data\mt5\modal
copy /Y Colethon\Infinite\Quanthon\data\mt5\modal\*.* C:\Apps\Infinite\Quanthon\data\mt5\modal
move /Y Colethon\Infinite\Quanthon\data\mt5\modal\*.* D:\B3\Data\Brasil\Modal_BookTick\mql5_files

echo Copiando arquivos de cotacoes da corretora XM Global...
copy /Y Colethon\Infinite\Quanthon\data\mt5\xm\*.* C:\Apps\Infinite\Quanthon\data\mt5\xm
copy /Y Colethon\Infinite\Quanthon\data\mt5\xm\*.* C:\Apps\Infinite\Quanthon\data\mt5\xm
move /Y Colethon\Infinite\Quanthon\data\mt5\xm\*.* D:\B3\Data\Exterior\XM_Tick\mql5_files
echo.

echo Criando arquivos flag nas pastas locais do Lothon e Quanthon [safeToDelete.tmp]...
touch C:\Apps\Loto365\Lothon\data\safeToDelete.tmp
touch C:\Apps\Infinite\Quanthon\data\safeToDelete.tmp
echo.

echo Removendo arquivo flag [safeToDelete.tmp]...
del /F /Q D:\Publico\Colethon\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
echo.
pause

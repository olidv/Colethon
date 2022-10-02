@echo off

rem Printa a apresentacao do Colethon.
echo.
echo  MOVE SHARED   [ C:\APPS\INFINITE\LOTHON\BIN\MOVE_SHARED.BAT ]
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

echo Copiando Arquivos HTM contendo resultados das loterias da Caixa EF...
copy /y Colethon\Lothon\data\caixa\D_*.htm C:\Apps\Infinite\Lothon\data\caixa
move /Y Colethon\Lothon\data\caixa\D_*.htm D:\Workspace\Python\Lothon\data\caixa\
echo.
copy /Y Colethon\Lothon\data\cache\D_*.csv C:\Apps\Infinite\Lothon\data\cache\
copy /Y Colethon\Lothon\data\cache\D_*.csv D:\Workspace\Python\Lothon\data\cache\
move /Y Colethon\Lothon\data\cache\D_*.csv D:\Workspace\Java\jLothon\data\cache\
echo.
copy /Y Colethon\Lothon\data\cache\JC_*.csv C:\Apps\Infinite\Lothon\data\cache\
move /Y Colethon\Lothon\data\cache\JC_*.csv D:\Workspace\Python\Lothon\data\cache\
echo.

echo Copiando Arquivos para publicacao dos palpites do dia...
del /F /Q C:\Users\qdev\Loto365\docs-templates\Social\*.*
move /Y Colethon\Lothon\Social\*.* C:\Users\qdev\Loto365\docs-templates\Social
echo.

echo Copiando Arquivo CSV contendo a carteira do IBOVESP da Bolsa B3...
copy /Y Colethon\Quanthon\data\b3\ibovespa\IBOVDia_*.csv C:\Apps\Infinite\Quanthon\data\b3\ibovespa\
copy /Y Colethon\Quanthon\data\b3\ibovespa\IBOVDia_*.csv D:\Workspace\Python\Quanthon\data\b3\ibovespa\
move /Y Colethon\Quanthon\data\b3\ibovespa\IBOVDia_*.csv D:\B3\Data\B3\Carteira_IBOV\%YYYY%\%HOJE%
echo.

echo Copiando Arquivos ZIP contendo cotacoes intraday da Bolsa B3...
copy /Y Colethon\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip C:\Apps\Infinite\Quanthon\data\b3\cotacoes\
copy /Y Colethon\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip D:\Workspace\Python\Quanthon\data\b3\cotacoes\
move /Y Colethon\Quanthon\data\b3\cotacoes\TradeIntraday_*.zip D:\B3\Data\B3\Cotacoes_TRADEINTRADAY\%YYYY%\%HOJE%
echo.

echo Copiando Arquivos de cotacoes da corretora Genial...
copy /Y Colethon\Quanthon\data\mt5\genial\*.* C:\Apps\Infinite\Quanthon\data\mt5\genial\
copy /Y Colethon\Quanthon\data\mt5\genial\*.* D:\Workspace\Python\Quanthon\data\mt5\genial\
move /Y Colethon\Quanthon\data\mt5\genial\*.* D:\B3\Data\Brasil\Genial_BookTick\mql5_files

echo Copiando Arquivos de cotacoes da corretora Modal...
copy /Y Colethon\Quanthon\data\mt5\modal\*.* C:\Apps\Infinite\Quanthon\data\mt5\modal\
copy /Y Colethon\Quanthon\data\mt5\modal\*.* D:\Workspace\Python\Quanthon\data\mt5\modal\
move /Y Colethon\Quanthon\data\mt5\modal\*.* D:\B3\Data\Brasil\Modal_BookTick\mql5_files

echo Copiando Arquivos de cotacoes da corretora XM Global...
copy /Y Colethon\Quanthon\data\mt5\xm\*.* C:\Apps\Infinite\Quanthon\data\mt5\xm\
copy /Y Colethon\Quanthon\data\mt5\xm\*.* D:\Workspace\Python\Quanthon\data\mt5\xm\
move /Y Colethon\Quanthon\data\mt5\xm\*.* D:\B3\Data\Exterior\XM_Tick\mql5_files
echo.

echo Criando arquivos flag nas pastas locais do Lothon e Quanthon [safeToDelete.tmp]...
touch C:\Apps\Infinite\Lothon\data\safeToDelete.tmp
touch C:\Apps\Infinite\Quanthon\data\safeToDelete.tmp
echo.

echo Removendo arquivo flag [safeToDelete.tmp]...
del /F /Q D:\Publico\Colethon\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
echo.
pause
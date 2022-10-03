@echo off
color 6F

rem Ativa o ambiente virtual da aplicacao:
call ..\venv\Scripts\activate.bat

rem Executa a aplicacao indicando o arquivo de configuracao:
python colethon.zip -c C:\Apps\Infinite\Colethon\conf -b

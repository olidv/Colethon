@echo off

rem Ativa o ambiente virtual da aplicacao:
call ..\venv\Scripts\activate.bat

rem Executa a aplicacao indicando o arquivo de configuracao:
python colethon.zip -c C:\Apps\B3\Colethon\conf -b

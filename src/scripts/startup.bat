@echo off

rem Ativa o ambiente virtual da aplicacao:
call ..\venv\Scripts\activate.bat

rem Executa a aplicacao indicando o arquivo de configuracao:
python infinite.zip -d -c C:\Apps\B3\Infinite\conf

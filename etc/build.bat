@echo off
color E

rem Printa a apresentacao do build:
echo.
echo  BUILD DO INFINITE   [ D:\WORKSPACE\PYTHON\INFINITE\ETC\BUILD.BAT ]
echo.
echo.

echo  ********************************************
echo  **  INICIANDO  COMPILACAO  DO  INFINITE.  **
echo  ********************************************
echo.
echo.

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Apagando a pasta de distribuicao para nova release [ \dist ]
rmdir /s /q dist  1>nul  2>&1
echo.

echo Criando nova estrutura para distribuir o pacote do executavel
mkdir dist  1>nul  2>&1
mkdir dist\bin  1>nul  2>&1
mkdir dist\conf  1>nul  2>&1
mkdir dist\logs  1>nul  2>&1
mkdir dist\tmp  1>nul  2>&1
mkdir dist\www  1>nul  2>&1
echo.

echo Atualizando a lista de dependencias do projeto [ requirements ]
python -m pip freeze > requirements.txt
copy requirements.txt dist\  
echo.

echo Apagando os arquivos de byte-code temporarios [ __pycache__ ]
forfiles /p .\src\main /s /m __pycache__ /c "cmd /c rmdir /s /q @file"  1>nul  2>&1
echo.

echo Compactando o codigo fonte para criar pacote executavel [ ZIP ]
python -m zipfile -c dist\bin\infinite.zip src\main\infinite src\main\__main__.py
echo.

echo Copiando para distribuicao os arquivos de resources e scripts
copy src\scripts\*.* dist\bin\
copy src\resources\prod\*.* dist\conf\
copy src\resources\README.md dist\
echo.

echo Compactando o build e gerando pacote de distribuicao da release [ ZIP ]
python -m zipfile -c infinite-1.0.zip dist\.
move infinite-1.0.zip dist\.  1>nul  2>&1
echo.

echo Executando o programa para testar se tudo ok [ -t  testing ]
cd dist\bin
python infinite.zip -c ..\conf -t .
echo.

rem Pausa final...
echo.
pause

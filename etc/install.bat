@echo off
color F

echo Verificando a versao atual do Python no sistema
python --version
echo.

echo Verificando a versao atual do pip no sistema
pip --version
echo.

echo Atualizando o pip no sistema para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Criando pasta do projeto
mkdir Colethon
echo.

echo Instalando ambiente virtual no projeto
python -m venv Colethon\venv
echo.

echo Posicionando no diretorio raiz do projeto
cd Colethon
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Instalando as dependencias do projeto no ambiente
@echo on
pip install -U setuptools
pip install -U wheel
pip install -U memory_profiler
pip install -U PyYAML
pip install -U requests
pip install -U beautifulsoup4
pip install -U selenium
pip install -U schedule
pip install -U Send2Trash
@echo off
echo.

echo Atualizando a lista de dependencias do projeto [ requirements ]
python -m pip freeze > requirements.txt
echo.

rem Pausa final...
echo.
pause

@echo off
color F

echo Criando pasta do projeto
mkdir Infinite
echo.

echo Posicionando no diretorio raiz do projeto
cd Infinite
echo.

echo Verificando a versao atual do Python no sistema
python --version
echo.

echo Atualizando o pip no sistema para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no sistema
pip --version
echo.

echo Instalando ambiente virtual no projeto
python -m venv Infinite\venv
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Verificando a versao atual do Python no ambiente
python --version
echo.

echo Atualizando o pip no ambiente para evitar conflitos
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no ambiente
pip --version
echo.

echo Instalando as dependencias do projeto no ambiente
@echo on
pip install -U wheel
pip install -U PyYAML
pip install -U requests
pip install -U selenium
pip install -U schedule
pip install -U Send2Trash
pip install -U memory_profiler
@echo off
echo.

echo Atualizando a lista de dependencias do projeto [ requirements ]
python -m pip freeze > requirements.txt
echo.

rem Pausa final...
echo.
pause

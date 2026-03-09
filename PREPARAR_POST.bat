@echo off
setlocal enabledelayedexpansion
echo =========================================
echo   STOIC MARKET ELITE v3.0 - PREPARADOR
echo =========================================
cd /d "%~dp0"

echo.
echo [1] Buscando a legenda mais recente...
python -c "import glob, os, pyperclip; output_dir='output'; files=glob.glob(os.path.join(output_dir, '*_legenda.txt')); latest=max(files, key=os.path.getmtime) if files else None; pyperclip.copy(open(latest, 'r', encoding='utf-8').read()) if latest else print('X Legenda nao encontrada!')"

echo.
echo [2] Abrindo a pasta de Midia...
if exist output (
    explorer "%~dp0output"
) else (
    echo X Pasta output nao encontrada. Gere um post primeiro!
)

echo.
echo [3] Abrindo Instagram...
start https://www.instagram.com/

echo.
echo ✨ TUDO PRONTO!
echo -----------------------------------------
echo 1. Clique em Criar (+) no Instagram.
echo 2. Arraste a imagem da pasta aberta.
echo 3. Na legenda, aperte CTRL + V.
echo -----------------------------------------
echo.
pause


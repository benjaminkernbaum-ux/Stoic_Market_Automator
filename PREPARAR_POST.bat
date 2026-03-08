@echo off
echo =========================================
echo   STOIC MARKET - PREPARADOR DE POST
echo =========================================
cd /d "%~dp0"

echo.
echo [1] Copiando a legenda para o seu Ctrl+V...
python -c "import pyperclip; f=open('output/disciplina_edge_legenda.txt', 'r', encoding='utf-8'); pyperclip.copy(f.read())"

echo [2] Abrindo a pasta com a imagem...
explorer "%~dp0output"

echo [3] Abrindo o Instagram no seu navegador...
start https://www.instagram.com/?hl=pt-br

echo.
echo TUDO PRONTO!
echo 1. No Instagram, clique em Criar (+)
echo 2. Arraste a imagem da pasta que abriu
echo 3. Na legenda, aperte Ctrl+V !
echo.
pause

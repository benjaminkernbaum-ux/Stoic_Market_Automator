import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configuração Base
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
OUT_DIR = BASE_DIR / "output"

load_dotenv(ENV_PATH)

def postar_telegram(caminho_imagem=None, caminho_legenda=None):
    """
    Envia a arte e a legenda para o canal do Telegram do Stoic Market.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id or token == "seu_token_aqui":
        print("❌ Telegram não configurado no .env")
        return False

    # Se não passar caminhos, busca os mais recentes
    if not caminho_imagem or not caminho_legenda:
        images = list(OUT_DIR.glob("*.png"))
        if not images:
            print("❌ Nenhuma imagem encontrada para o Telegram.")
            return False
        caminho_imagem = str(max(images, key=os.path.getmtime))
        
        # Procura legenda correspondente
        base_name = os.path.basename(caminho_imagem).replace(".png", "_legenda.txt")
        legenda_file = OUT_DIR / base_name
        if not legenda_file.exists():
            captions = list(OUT_DIR.glob("*_legenda.txt"))
            caminho_legenda = str(max(captions, key=os.path.getmtime)) if captions else None
        else:
            caminho_legenda = str(legenda_file)

    if not caminho_legenda:
        print("⚠️ Postando no Telegram sem legenda.")
        legenda = ""
    else:
        with open(caminho_legenda, 'r', encoding='utf-8') as f:
            legenda = f.read()

    print(f"📡 Enviando para Telegram: {os.path.basename(caminho_imagem)}")
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    
    try:
        with open(caminho_imagem, 'rb') as foto:
            payload = {
                "chat_id": chat_id,
                "caption": legenda,
                "parse_mode": "HTML"
            }
            files = {"photo": foto}
            response = requests.post(url, data=payload, files=files, timeout=15)
        
        if response.status_code == 200:
            print("✅ Telegram: Postagem realizada com sucesso!")
            return True
        else:
            print(f"❌ Telegram Erro: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Telegram Erro Crítico: {e}")
        return False

if __name__ == "__main__":
    postar_telegram()

import os
import sys
import glob
import logging
from pathlib import Path
from instagrapi import Client
from dotenv import load_dotenv

# Configuração Base
BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "output"
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")

if USERNAME == "seu_usuario_aqui" or not USERNAME:
    print("❌ Credenciais ausentes no .env")
    sys.exit(1)

def get_latest_post_files():
    images = list(OUT_DIR.glob("*.png"))
    if not images:
        return None, None
    
    latest_image = max(images, key=os.path.getmtime)
    caption_path = latest_image.with_name(latest_image.name.replace(".png", "_legenda.txt"))
    
    if not caption_path.exists():
        captions = list(OUT_DIR.glob("*_legenda.txt"))
        if captions:
            caption_path = max(captions, key=os.path.getmtime)
        else:
            caption_path = None
            
    return str(latest_image), str(caption_path) if caption_path else None

def run_upload():
    cl = Client()
    print(f"🔄 Login: @{USERNAME}")
    try:
        cl.login(USERNAME, PASSWORD)
    except Exception as e:
        print(f"❌ Erro login: {e}")
        sys.exit(1)

    image_path, caption_path = get_latest_post_files()
    if not image_path:
        print("❌ Nenhum post para enviar.")
        return

    caption = ""
    if caption_path:
        with open(caption_path, "r", encoding="utf-8") as f:
            caption = f.read()

    print(f"📸 Enviando: {os.path.basename(image_path)}")
    try:
        cl.photo_upload(image_path, caption)
        print("🎉 Postagem ELITE v3.0 realizada!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    run_upload()

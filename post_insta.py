import os
import sys
import glob
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("INSTA_USERNAME")
PASSWORD = os.getenv("INSTA_PASSWORD")

if USERNAME == "seu_usuario_aqui" or not USERNAME:
    print("❌ Por favor, adicione as credenciais INSTA_USERNAME e INSTA_PASSWORD no seu arquivo .env")
    sys.exit(1)

def get_latest_post_files():
    """Busca os arquivos mais recentes na pasta output."""
    output_dir = "output"
    images = glob.glob(os.path.join(output_dir, "*.png"))
    if not images:
        return None, None
    
    # Pega a imagem mais recente
    latest_image = max(images, key=os.path.getmtime)
    
    # Tenta achar a legenda correspondente (mesmo timestamp/nome)
    caption_path = latest_image.replace(".png", "_legenda.txt")
    
    if not os.path.exists(caption_path):
        # Se não achar por nome, pega a legenda mais recente da pasta
        captions = glob.glob(os.path.join(output_dir, "*_legenda.txt"))
        if captions:
            caption_path = max(captions, key=os.path.getmtime)
        else:
            caption_path = None
            
    return latest_image, caption_path

cl = Client()

print(f"🔄 Tentando login na conta @{USERNAME} no Instagram...")
try:
    cl.login(USERNAME, PASSWORD)
except Exception as e:
    print(f"❌ Erro ao logar no Instagram (bloqueio de segurança/senha incorreta): {e}")
    sys.exit(1)

print("✅ Login realizado com sucesso! Buscando arquivos...")

image_path, caption_path = get_latest_post_files()

if not image_path or not os.path.exists(image_path):
    print("❌ Nenhuma imagem de post encontrada na pasta output.")
    sys.exit(1)

if not caption_path or not os.path.exists(caption_path):
    print("⚠️ Legenda não encontrada. O post será feito sem legenda.")
    caption = ""
else:
    with open(caption_path, "r", encoding="utf-8") as file:
        caption = file.read()

print(f"📸 Enviando arquivo {image_path}...")

try:
    cl.photo_upload(image_path, caption)
    print("🎉 Sucesso! Postagem realizada com sucesso!")
except Exception as e:
    print(f"❌ Erro na publicação: {e}")

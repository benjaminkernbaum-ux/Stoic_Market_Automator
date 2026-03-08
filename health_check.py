import os
import sys
import subprocess
from dotenv import load_dotenv

def check_env():
    load_dotenv()
    keys = ["CLAUDE_API_KEY", "INSTA_USERNAME", "INSTA_PASSWORD"]
    missing = []
    placeholders = ["COLOQUE_SUA_CHAVE_AQUI", "seu_usuario_aqui", "sua_senha_aqui"]
    
    for key in keys:
        val = os.getenv(key)
        if not val or val in placeholders:
            missing.append(key)
    return missing

def check_dependencies():
    deps = ["anthropic", "requests", "html2image", "instagrapi", "dotenv", "pyperclip"]
    missing = []
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            missing.append(dep)
    return missing

if __name__ == "__main__":
    print("🔍 STOIC MARKET - HEALTH CHECK")
    print("-" * 30)
    
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"❌ Dependências faltando: {', '.join(missing_deps)}")
        print("💡 Sugestão: py -m pip install " + " ".join(missing_deps))
    else:
        print("✅ Todas as dependências Python estão instaladas.")
    
    missing_keys = check_env()
    if missing_keys:
        print(f"❌ Chaves faltando no .env: {', '.join(missing_keys)}")
        print("⚠️  Ação: Você precisa editar o arquivo .env com suas credenciais.")
    else:
        print("✅ Arquivo .env configurado com sucesso.")
    
    print("-" * 30)
    if not missing_deps and not missing_keys:
        print("🚀 SISTEMA PRONTO PARA OPERAR!")
    else:
        print("🛠️  Ajustes pendentes antes de rodar.")

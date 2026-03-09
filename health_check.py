import os
import sys
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Configuração base
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
CLAUDE_CONFIG = Path(os.getenv("APPDATA")) / "Claude" / "claude_desktop_config.json"

load_dotenv(ENV_PATH)

def check_env():
    keys = ["CLAUDE_API_KEY", "INSTA_USERNAME", "INSTA_PASSWORD", "HIGGSFIELD_API_KEY"]
    missing = []
    placeholders = ["seu_key_aqui", "seu_usuario_aqui", "sua_senha_aqui", "sk-ant-..."]
    
    for key in keys:
        val = os.getenv(key)
        if not val or any(p in val for p in placeholders):
            missing.append(key)
    return missing

def check_mcp_config():
    if not CLAUDE_CONFIG.exists():
        return "❌ Arquivo de configuração do Claude não encontrado."
    
    try:
        with open(CLAUDE_CONFIG, "r", encoding="utf-8") as f:
            config = json.load(f)
            servers = config.get("mcpServers", {})
            if "stoic_market_tools" in servers:
                return "✅ MCP Server (stoic_market_tools) configurado."
            else:
                return "⚠️  MCP Server não encontrado na configuração do Claude."
    except Exception as e:
        return f"❌ Erro ao ler config do Claude: {e}"

def check_dependencies():
    deps = ["anthropic", "requests", "html2image", "instagrapi", "dotenv", "pyperclip", "pathlib"]
    missing = []
    for dep in deps:
        try:
            # Map dependency names to import names if necessary
            import_name = dep.replace("-", "_")
            if dep == "instagrapi": import_name = "instagrapi"
            if dep == "python-dotenv": import_name = "dotenv"
            __import__(import_name)
        except ImportError:
            missing.append(dep)
    return missing

def run_diagnostic():
    print(f"\n{'━'*40}")
    print(" 🛡️  STOIC ELITE - DIAGNÓSTICO DO SISTEMA V3")
    print(f"{'━'*40}")
    
    # 1. Dependências
    missing_deps = check_dependencies()
    if missing_deps:
        print(f"🔴 Dependências Faltando: {', '.join(missing_deps)}")
        print(f"   👉 Execute: py -m pip install {' '.join(missing_deps)}")
    else:
        print("🟢 Dependências Python: OK")
    
    # 2. Ambiente (.env)
    missing_keys = check_env()
    if missing_keys:
        print(f"🔴 Chaves no .env: Faltando ({', '.join(missing_keys)})")
    else:
        print("🟢 Credenciais (.env): OK")
        
    # 3. Claude MCP
    print(f"🔵 Status Claude: {check_mcp_config()}")

    # 4. Estrutura de Pastas
    mcp_script = BASE_DIR / "stoic_mcp.py"
    if mcp_script.exists():
        print("🟢 Servidor MCP Local: Encontrado")
    else:
        print("🔴 Servidor MCP Local: NÃO ENCONTRADO")

    print(f"{'━'*40}")
    if not missing_deps and not missing_keys:
        print(" ✨ SISTEMA PRONTO PARA OPERAR EM ALTA PERFORMANCE!")
    else:
        print(" 🛠️  RESOLVA AS PENDÊNCIAS ACIMA PARA INICIAR.")
    print(f"{'━'*40}\n")

if __name__ == "__main__":
    run_diagnostic()

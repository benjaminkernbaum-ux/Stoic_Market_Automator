import os
import json
import sys

def setup():
    # Identifica o caminho %APPDATA%/Claude padrão e MSIX (Windows Store)
    appdata = os.getenv("APPDATA")
    localappdata = os.getenv("LOCALAPPDATA")
    
    # Verifica a versão MSIX/Store primeiro
    msix_path = os.path.join(localappdata, "Packages", "Claude_pzs8sxrjxfjjc", "LocalCache", "Roaming", "Claude")
    if os.path.exists(msix_path):
        claude_dir = msix_path
    else:
        claude_dir = os.path.join(appdata, "Claude")
        
    config_path = os.path.join(claude_dir, "claude_desktop_config.json")

    # Garante que as pastas e o arquivo existam
    os.makedirs(claude_dir, exist_ok=True)
    
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {"mcpServers": {}}
    else:
        config = {"mcpServers": {}}

    if "mcpServers" not in config:
        config["mcpServers"] = {}

    cwd = os.path.abspath(os.path.dirname(__file__))
    script_path = os.path.join(cwd, "stoic_mcp.py")

    # Adiciona o Stoic Market MCP 
    config["mcpServers"]["stoic_market_tools"] = {
        "command": sys.executable,  # Usa o exato python atual
        "args": [
            script_path
        ]
    }

    # Salva
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    print("✅ Integração com o Claude Desktop Protocol realizada!")
    print(f"O arquivo {config_path} foi atualizado.")
    print("-----------------------------------------------------")
    print("🔥 IMPORTANTE: REINICIE O SEU CLAUDE (feche o aplicativo totalmente no Windows e abra novamente).")
    print("Depois, mande uma mensagem pra ele: 'Gere o post stoic da manha e prepare a minha área de transferência'.")

if __name__ == "__main__":
    setup()

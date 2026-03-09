from mcp.server.fastmcp import FastMCP
import subprocess
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# Inicializa o servidor MCP Elite
mcp = FastMCP("Stoic Elite Terminal")

BASE_DIR = Path(__file__).resolve().parent

@mcp.tool()
def gerar_post_stoic(turno: str = "manha") -> str:
    """Gera imagem e legenda premium para o Instagram."""
    try:
        resultado = subprocess.run(
            [sys.executable, str(BASE_DIR / "generate_post.py"), turno],
            capture_output=True, text=True, cwd=str(BASE_DIR), check=True
        )
        return f"✅ Operação Concluída!\n{resultado.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ ERRO na geração: {e.stderr}\n{e.stdout}"

@mcp.tool()
def diagnostico_total() -> str:
    """Executa o Health Check completo do ecossistema."""
    try:
        resultado = subprocess.run(
            [sys.executable, str(BASE_DIR / "health_check.py")],
            capture_output=True, text=True, cwd=str(BASE_DIR), check=True
        )
        return resultado.stdout
    except Exception as e:
        return f"❌ Erro no diagnóstico: {str(e)}"

@mcp.tool()
def ativar_cyber_armor() -> str:
    """Aciona os protocolos de segurança ASUS Cyber Armor."""
    # O arquivo asus_armor.py deve estar na pasta CyberArmor_System
    armor_path = BASE_DIR.parent / "CyberArmor_System" / "asus_armor.py"
    try:
        resultado = subprocess.run(
            [sys.executable, str(armor_path)],
            capture_output=True, text=True, cwd=str(armor_path.parent), check=True
        )
        return f"🛡️ Protocolo Cyber Armor Ativado!\n{resultado.stdout}"
    except Exception as e:
        return f"❌ Falha ao ativar proteção: {str(e)}"

@mcp.tool()
def verificar_status_mercado() -> str:
    """Análise em tempo real do Bitcoin e Sentimento (Fear & Greed)."""
    try:
        fg_res = requests.get("https://api.alternative.me/fng/", timeout=5).json()
        value = int(fg_res['data'][0]['value'])
        sentiment = fg_res['data'][0]['value_classification']
        
        btc_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        price = float(btc_res['price'])
        
        status = f"📊 STATUS STOIC MARKET:\n"
        status += f"- BTC/USDT: ${price:,.2f}\n"
        status += f"- Medo & Ganância: {value}% ({sentiment})\n"
        
        if value < 25: status += "💡 FOCO: Oportunidade estóica de compra no pânico."
        elif value > 75: status += "💡 FOCO: Cuidado com a euforia. Sêneca ensina a sobriedade."
        return status
    except Exception as e:
        return f"⚠️ Erro na busca de dados: {str(e)}"

@mcp.tool()
def publicar_automatico() -> str:
    """Faz o push final para o Instagram (Requer login no .env)."""
    try:
        resultado = subprocess.run(
            [sys.executable, str(BASE_DIR / "post_insta.py")],
            capture_output=True, text=True, cwd=str(BASE_DIR), check=True
        )
        return f"🚀 Decolagem confirmada!\n{resultado.stdout}"
    except Exception as e:
        return f"❌ Abortar: {str(e)}"

@mcp.resource("output://preview")
def get_latest_preview() -> str:
    """Exibe o link do último arquivo HTML gerado."""
    path = BASE_DIR / "output"
    files = list(path.glob("*.html"))
    if not files: return "Nenhum post gerado ainda."
    latest = max(files, key=os.path.getmtime)
    return f"Última arte: {latest.name}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

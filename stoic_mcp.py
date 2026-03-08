from mcp.server.fastmcp import FastMCP
import subprocess
import os
import sys
import requests
from datetime import datetime

# Inicializa o servidor MCP
mcp = FastMCP("Stoic Market")

@mcp.tool()
def gerar_post_stoic(turno: str = "manha") -> str:
    """
    Gera a imagem e a legenda para o post do Stoic Market correspondente ao dia de hoje.
    """
    cwd = os.path.dirname(os.path.abspath(__file__))
    try:
        resultado = subprocess.run([sys.executable, "generate_post.py", turno], capture_output=True, text=True, cwd=cwd, check=True)
        return f"Post gerado com sucesso! \nSaída do log:\n{resultado.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ ERRO na geração: {e.stderr}\n{e.stdout}"
    except Exception as e:
        return f"❌ Erro inesperado: {str(e)}"

@mcp.tool()
def preparar_area_transferencia() -> str:
    """
    Copia a legenda para o Ctrl+V e abre a pasta com a foto.
    """
    cwd = os.path.dirname(os.path.abspath(__file__))
    try:
        resultado = subprocess.run(["cmd.exe", "/c", "PREPARAR_POST.bat"], capture_output=True, text=True, cwd=cwd, check=True)
        return "✅ Tudo preparado! A legenda está no Ctrl+V e a pasta aberta."
    except Exception as e:
        return f"❌ Erro ao preparar: {str(e)}"

@mcp.tool()
def publicar_no_instagram() -> str:
    """
    Realiza o upload automático do post gerado para o Instagram.
    """
    cwd = os.path.dirname(os.path.abspath(__file__))
    try:
        resultado = subprocess.run([sys.executable, "post_insta.py"], capture_output=True, text=True, cwd=cwd, check=True)
        return f"🚀 Publicado com sucesso!\n{resultado.stdout}"
    except subprocess.CalledProcessError as e:
        return f"❌ Erro no upload: {e.stderr}\n{e.stdout}"

@mcp.tool()
def verificar_status_mercado() -> str:
    """
    Analisa o sentimento atual do mercado (Fear & Greed) e preço do BTC para sugerir foco estoico.
    """
    try:
        # Fear & Greed Index
        fg_res = requests.get("https://api.alternative.me/fng/", timeout=5).json()
        value = int(fg_res['data'][0]['value'])
        sentiment = fg_res['data'][0]['value_classification']
        
        # Preço BTC
        btc_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        price = float(btc_res['price'])
        
        status = f"📊 STATUS DO MERCADO:\n"
        status += f"- Fear & Greed: {value} ({sentiment})\n"
        status += f"- BTC/USDT: ${price:,.2f}\n\n"
        
        if value < 30:
            status += "💡 SUGESTÃO: O mercado está em MEDO. Use pilares de Psicologia ou Frases de Marco Aurélio sobre resiliência."
        elif value > 70:
            status += "💡 SUGESTÃO: O mercado está em EUFORIA. Use pilares de Gestão de Risco ou Sêneca sobre a brevidade dos ganhos."
        else:
            status += "💡 SUGESTÃO: Sentimento neutro. Siga o calendário padrão de Análise Técnica."
            
        return status
    except Exception as e:
        return f"Erro ao buscar status: {str(e)}"

@mcp.resource("output://post_recente_img")
def get_latest_post_image() -> bytes:
    """Retorna a última imagem gerada na pasta output."""
    path = os.path.join(os.path.dirname(__file__), "output")
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".png")]
    if not files:
        return b""
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, "rb") as f:
        return f.read()

@mcp.resource("output://post_recente_txt")
def get_latest_post_caption() -> str:
    """Retorna a última legenda gerada na pasta output."""
    path = os.path.join(os.path.dirname(__file__), "output")
    files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith("_legenda.txt")]
    if not files:
        return "Nenhuma legenda encontrada."
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run(transport="stdio")

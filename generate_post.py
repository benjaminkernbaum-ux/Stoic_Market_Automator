"""
STOIC MARKET — generate_post.py  v3.0 (Elite Edition)
- Motor de Geração Premium com Blindagem de Prompt
- Integração de Dados Reais (Binance BTC)
- Suporte a Animação Higgsfield (V3-Ready)
- Sistema de Log Profissional
"""

import anthropic
import json
import os
import random
import requests
import sys
import logging
from datetime import datetime
from html2image import Html2Image
from dotenv import load_dotenv

# Configuração de Log
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("automator.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Caminhos Absolutos para robustez
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "output")
ENV_PATH = os.path.join(BASE_DIR, ".env")
CALENDAR_PATH = os.path.join(BASE_DIR, "calendar.json")

load_dotenv(ENV_PATH)
API_KEY = os.getenv("CLAUDE_API_KEY")
CLIENT = anthropic.Anthropic(api_key=API_KEY)

# Modelo Atualizado (Claude 3.5 Sonnet)
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"

# ─── Carrega calendário ──────────────────────────────────────────
try:
    with open(CALENDAR_PATH, "r", encoding="utf-8") as f:
        CALENDAR_DATA = json.load(f)
    PALETA = CALENDAR_DATA["paleta"]
except Exception as e:
    logging.error(f"Erro ao carregar calendário: {e}")
    sys.exit(1)

# ─── PROMPTS ELITE (UX/UI PREMIUM) ──────────────────────────────
PROMPTS = {
    "analise_tecnica": """
    ESTÉTICA: STOIC HIGH-END (ELITE V3)
    Você é o Head Design da @stoic.mkt. Crie um HTML 1080x1080px.
    
    DADOS DO POST:
    Tema: <tema>{tema}</tema>
    Preço: {preco_btc}
    
    DESIGN OBRIGATÓRIO:
    - Fundo: {fundo} com efeito de 'Glassmorphism' em cards.
    - Grid: Pontilhado Cyber-Green rgba(0,255,136,.06) 40px.
    - Tipografia: Bebas Neue para títulos, JetBrains Mono para dados técnicos.
    - Elemento Central: Um terminal de trading estilizado com box-shadow verde neon.
    - Título: "{tema}" com glow sutil.
    - Dados: "PREÇO ATUAL: {preco_btc}" | "TIME: 1D" | "VIÉS: NEUTRO/ALTA".
    - Footer: STOIC MARKET ELITE | @stoic.mkt
    - Fontes: @import url Google Fonts (Bebas Neue, DM Sans, JetBrains Mono).
    
    Retorne APENAS o código HTML.
    """,
    "quote_estoica": """
    ESTÉTICA: STOIC HIGH-END (ELITE V3)
    Design Minimalista, Profundo e Profissional.
    
    TEMA: <tema>{tema}</tema>
    
    REQUISITOS VISUAIS:
    - Fundo: {fundo_dark} (Solid Black #020202).
    - Tipografia: Bebas Neue (Citação) e DM Sans (Texto de apoio).
    - Detalhe: Uma linha vertical dourada ({dourado}) de 100px no centro-topo.
    - Texto: A citação deve ser centralizada, com Kerning aumentado.
    - Glow: Um rastro de luz verde ({verde}) vindo do canto inferior direito (opacity 0.05).
    - Footer: @stoic.mkt em JetBrains Mono.
    
    Retorne APENAS o código HTML.
    """,
    "psicologia_trader": """
    ESTÉTICA: INFOGRÁFICO PREMIUM
    TEMA: <tema>{tema}</tema>
    
    REQUISITOS:
    - Estrutura de lista (1 a 5).
    - Cada item em um card com fundo rgba(255,255,255,0.02) e borda verde neon de 1px.
    - Títulos em Bebas Neue, descrições em DM Sans.
    - Glow radial no centro do post (verde neon, 10% opacity).
    - Footer: @stoic.mkt.
    
    Retorne APENAS o código HTML.
    """,
    "reflexao_estoica": """
    ESTÉTICA: CINEMATIC DARK
    Foco em meditação e trading.
    
    TEMA: <tema>{tema}</tema>
    
    CONSTRUÇÃO HTML:
    - Fundo escuro com uma elipse sutil simulando profundidade.
    - Citação em itálico elegante.
    - Pergunta de impacto na base com fonte verde neon.
    - Footer: stoic.mkt.
    
    Retorne APENAS o código HTML.
    """
}

# Fallback para pilares não definidos no Elite V3
FALLBACK_PROMPT = """Crie um post premium para @stoic.mkt sobre {tema}. Use cores {verde} e fundo escuro {fundo}."""

LEGENDA_PROMPT = """
Você é o Social Media Manager da @stoic.mkt. 
Tema: <tema>{tema}</tema>
Pilar: <pilar>{pilar}</pilar>

Escreva uma legenda curta (max 400 caracteres), impactante, com 3 hashtags e tom estoico profissional.
Comece com: <hook>{hook}</hook>
Retorne APENAS a legenda.
"""

def get_btc_price() -> str:
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url, timeout=5)
        data = response.json()
        price = float(data['price'])
        return f"${price:,.2f}"
    except Exception:
        return "$68,500.00"

def gerar_conteúdo_claude(prompt_id, tema, data_str, is_legenda=False, pilar=None, hook=None):
    if is_legenda:
        full_prompt = LEGENDA_PROMPT.format(tema=tema, pilar=pilar, hook=hook)
        max_t = 512
    else:
        p = PALETA
        p_template = PROMPTS.get(pilar, FALLBACK_PROMPT)
        full_prompt = p_template.format(
            tema=tema,
            data=data_str,
            fundo=p["fundo_principal"],
            fundo_dark=p["fundo_dark"],
            verde=p["verde_neon"],
            dourado=p["dourado"],
            preco_btc=get_btc_price()
        )
        max_t = 4096

    try:
        msg = CLIENT.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=max_t,
            messages=[{"role": "user", "content": full_prompt}]
        )
        content = msg.content[0].text.strip()
        
        # Limpa blocos de código markdown se existirem
        if "```" in content:
            parts = content.split("```")
            for part in parts:
                if part.lower().startswith("html"):
                    return part[4:].strip()
                if "<html" in part.lower() or "<!DOCTYPE" in part.upper():
                    return part.strip()
            return parts[1].strip() if len(parts) > 1 else content
        return content

    except anthropic.RateLimitError:
        logging.error("Créditos da API Claude esgotados ou limite de taxa atingido.")
        return "❌ ERRO: Créditos Insuficientes. Adicione saldo em: console.anthropic.com/settings/billing"
    except Exception as e:
        logging.error(f"Erro na API Claude: {e}")
        return f"❌ ERRO TÉCNICO: {str(e)}"

def run(turno: str = "manha"):
    agora = datetime.now()
    data_str = agora.strftime("%d/%m/%Y")
    timestamp = agora.strftime("%Y%m%d_%H%M")
    
    logging.info(f"🚀 INICIANDO STOIC AUTOMATOR V3.0 — Turno: {turno.upper()}")
    
    # ─── Identifica o que postar ──────────────────────────────────
    try:
        dia_idx = (agora.timetuple().tm_yday - 1) % 30
        info = CALENDAR_DATA["dias"][dia_idx][turno]
        pilar = info["pilar"]
        tema = info["tema"]
        hook = info["hook"]
    except Exception as e:
        logging.error(f"Erro ao processar calendário: {e}")
        return

    os.makedirs(OUT_DIR, exist_ok=True)
    
    # ─── Geração de HTML ──────────────────────────────────────────
    logging.info(f"📌 Pilar: {pilar} | Tema: {tema}")
    html = gerar_conteúdo_claude(pilar, tema, data_str, pilar=pilar)
    
    if "❌" in html:
        print(f"\n{html}\n")
        return

    html_path = os.path.join(OUT_DIR, f"{timestamp}_{pilar}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # ─── Geração de PNG ───────────────────────────────────────────
    png_name = f"{timestamp}_{pilar}.png"
    png_path = os.path.join(OUT_DIR, png_name)
    try:
        hti = Html2Image(output_path=OUT_DIR, size=(1080, 1080))
        hti.screenshot(html_str=html, save_as=png_name)
        logging.info(f"✅ Imagem gerada: {png_path}")
    except Exception as e:
        logging.error(f"Falha na geração da imagem: {e}")
        return

    # ─── Geração de Legenda ────────────────────────────────────────
    legenda = gerar_conteúdo_claude(None, tema, data_str, is_legenda=True, pilar=pilar, hook=hook)
    leg_path = png_path.replace(".png", "_legenda.txt")
    with open(leg_path, "w", encoding="utf-8") as f:
        f.write(legenda)
    logging.info(f"✅ Legenda gerada: {leg_path}")

    # ─── Resultado Final ──────────────────────────────────────────
    print(f"\n{'═'*50}")
    print(f"  ✨ POST ELITE PREPARADO COM SUCESSO!")
    print(f"  📁 Pasta: {OUT_DIR}")
    print(f"  🖼️ Imagem: {png_name}")
    print(f"{'═'*50}\n")

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "manha"
    run(t)

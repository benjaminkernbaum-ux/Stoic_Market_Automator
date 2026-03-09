import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pathlib import Path
from dotenv import load_dotenv
from telegram_advanced import TelegramEliteBot

# Configuração Base
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

app = FastAPI(title="Stoic Market - TradingView Listener")
bot = TelegramEliteBot()

PASSPHRASE = os.getenv("TRADINGVIEW_PASSPHRASE", "STOIC_ELITE_SECRET")

@app.get("/")
async def root():
    return {"status": "Stoic Elite Listener Active"}

@app.post("/webhook")
async def tradingview_webhook(request: Request):
    """
    Recebe alertas do TradingView e encaminha para o Telegram.
    Exemplo de payload:
    {
        "passphrase": "sua_senha_aqui",
        "ticker": "BTCUSDT",
        "price": "66340",
        "action": "BUY",
        "reason": "RSI Oversold + Stoic Pattern"
    }
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # 🛡 Segurança: Verifica a Passphrase
    if data.get("passphrase") != PASSPHRASE:
        raise HTTPException(status_code=401, detail="Unauthorized")

    ticker = data.get("ticker", "Unknown")
    price = data.get("price", "???")
    action = data.get("action", "SIGNAL")
    reason = data.get("reason", "Análise técnica avançada detectada.")

    # Encaminha para o Telegram
    res = bot.send_market_alert(ticker, price, action, reason)
    
    if res.get("ok"):
        return {"status": "success", "message": "Signal forwarded to Telegram"}
    else:
        return {"status": "error", "message": res.get("description")}

if __name__ == "__main__":
    # Rodar localmente na porta 8000
    # Para expor para o TradingView, use: ngrok http 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

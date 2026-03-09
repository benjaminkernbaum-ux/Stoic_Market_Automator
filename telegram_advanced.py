import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# Configuração Base
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)

class TelegramEliteBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_market_alert(self, symbol, price, signal_type, reasoning):
        """Envio de Sinais de Trading com branding Elite."""
        emoji = "🚀 COMPRA" if signal_type.upper() == "BUY" else "📉 VENDA"
        message = (
            f"🏛 <b>STOIC MARKET - SINAL ELITE</b>\n\n"
            f"<b>Ativo:</b> {symbol}\n"
            f"<b>Ação:</b> {emoji}\n"
            f"<b>Preço:</b> ${price}\n\n"
            f"<b>Análise Estóica:</b>\n<i>{reasoning}</i>\n\n"
            f"⚠️ <i>Lembre-se: O mercado é soberano, mas sua disciplina é o que dita o lucro.</i>\n"
            f"----------------------------------\n"
            f"🔗 <a href='https://t.me/+CT5Lfz68ktRhM2Yx'>Comunidade Stoic Academy</a>"
        )
        return self._send_request("sendMessage", {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"})

    def send_news_flash(self, headline, summary, url):
        """Envio de Notícias de Impacto."""
        message = (
            f"🗞 <b>STOIC NEWS FLASH</b>\n\n"
            f"🔥 <b>{headline}</b>\n\n"
            f"{summary}\n\n"
            f"🔗 <a href='{url}'>Leia a análise completa</a>\n"
            f"----------------------------------\n"
            f"🏛 <i>Disciplina no caos, lucro no pânico.</i>"
        )
        return self._send_request("sendMessage", {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML", "disable_web_page_preview": False})

    def _send_request(self, method, data):
        if not self.token or not self.chat_id:
            return {"ok": False, "description": "Credenciais ausentes no .env"}
        try:
            response = requests.post(f"{self.base_url}/{method}", data=data, timeout=10)
            return response.json()
        except Exception as e:
            return {"ok": False, "description": str(e)}

if __name__ == "__main__":
    # Teste rápido
    bot = TelegramEliteBot()
    # bot.send_market_alert("BTC/USDT", "66,340", "BUY", "RSI em pânico extremo. Oportunidade estóica detectada.")

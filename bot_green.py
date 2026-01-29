import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================================================
# CONFIGURAÇÕES DE ACESSO (COLOQUE SUAS CHAVES AQUI)
# =========================================================
TELEGRAM_TOKEN = "8552516883:AAFtKo7DlP_aarvJTr4h4ls8dDYqD-Rh-kI"
FOOTBALL_API_KEY = "203bca72c4823b9b4f4b3e17202d639c" # Ex: API-Football (RapidAPI)
FOOTBALL_API_URL = "https://v3.football.api-sports.io/predictions"

# =========================================================
# LOGGING
# =========================================================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class FootballPredictor:
    """Classe para buscar dados reais e gerar lógica de acerto."""
    
    def __init__(self, api_key):
        self.headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': api_key
        }

    def get_analysis(self, league_id: int):
        """
        Busca a próxima partida e retorna a probabilidade da API.
        Nota: Você precisa do ID da liga (ex: Brasil Série A = 71)
        """
        # Aqui simulamos a chamada. Na prática, você buscaria o ID do próximo jogo.
        # A lógica de '89%' viria da análise do campo 'comparison' da API.
        
        try:
            # Exemplo de resposta estruturada para o usuário
            # Em um cenário real, o requests.get buscaria o jogo do dia.
            dados_mock = {
                "team_home": "Flamengo",
                "team_away": "Palmeiras",
                "probabilidade": "89.4%",
                "insight": "Forte tendência a Over 1.5 gols baseado no histórico."
            }
            return dados_mock
        except Exception as e:
            logging.error(f"Erro na API: {e}")
            return None

# --- HANDLERS DO TELEGRAM ---
class TelegramBot:
    def __init__(self, predictor):
        self.predictor = predictor

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = (
            "🤖 **Analista Pro v3.0**\n\n"
            "Escolha uma liga para receber a análise de alta precisão:\n"
            "/ligatuga - 🇵🇹 Liga Portugal\n"
            "/chp - 🏆 Champions League\n"
            "/uefa - 🇪🇺 Europa League\n"
            "/brasil - 🇧🇷 Série A"
        )
        await update.message.reply_text(msg, parse_mode='Markdown')

    async def handle_prediction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Mapeamento de IDs reais das ligas na API-Football
        league_map = {
            '/ligatuga': 94,
            '/chp': 2,
            '/uefa': 3,
            '/brasil': 71
        }
        
        cmd = update.message.text.split()[0]
        league_id = league_map.get(cmd)
        
        await update.message.reply_chat_action("typing")
        
        # Busca os dados na "Engine"
        data = self.predictor.get_analysis(league_id)
        
        if data:
            response = (
                f"📊 **ANÁLISE DE ALTA PRECISÃO**\n"
                f"🏆 Liga ID: {league_id}\n"
                f"⚽ Jogo: {data['team_home']} vs {data['team_away']}\n\n"
                f"🔥 **Confiança: {data['probabilidade']}**\n"
                f"📝 **Dica:** {data['insight']}\n\n"
                f"⚠️ *Lembre-se: Gestão de banca é essencial.*"
            )
        else:
            response = "❌ Sem jogos disponíveis para análise agora."

        await update.message.reply_text(response, parse_mode='Markdown')

# --- MAIN LOOP ---
if __name__ == '__main__':
    predictor = FootballPredictor(FOOTBALL_API_KEY)
    bot = TelegramBot(predictor)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Registro de comandos
    app.add_handler(CommandHandler("start", bot.start))
    for cmd in ["ligatuga", "chp", "uefa", "brasil"]:
        app.add_handler(CommandHandler(cmd, bot.handle_prediction))

    print("🚀 Bot rodando profissionalmente...")
    app.run_polling()
    
import os
import urllib.parse
from flask import Flask, render_template_string
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- INSTANCIAÇÃO DO SERVIDOR WEB E DO ROBÔ ---
app = Flask(__name__)
TOKEN_TELEGRAM = "8645090278:AAGSdrnx9dh4i4s7FFfkM8yU60CI-mUab10"
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# --- CONFIGURAÇÃO DOS AFILIADOS COM SEUS IDS NEUTROS (tf) ---
ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
ID_AFILIADO_AMAZON = "nsoc02-20"
ID_AFILIADO_MAGALU = "tf"
ID_AFILIADO_ALIEXPRESS = "shop99"

@app.route('/')
def home():
    return "<h1>StockNegócio - Buscador Automotivo Online e Ativo!</h1>"

# --- FLUXO DO TELEGRAM ---
@bot.message_handler(commands=['start', 'help'])
def enviar_boas_vindas(message):
    texto_boas_vindas = (
        "🏎️ **Bem-vindo ao StockNegócio!**\n\n"
        "O seu buscador inteligente de Mobilidade e Autopeças.\n"
        "Digite o modelo de um carro/moto (ex: *Civic 2020*) ou o nome de uma peça (ex: *Pneu aro 14*) que eu busco os melhores links para você!"
    )
    bot.reply_to(message, texto_boas_vindas, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def processar_busca_veiculo(message):
    texto_mensagem = message.text
    termo_limpo = urllib.parse.quote_plus(texto_mensagem)
    
    # Gerando os links com rastreamento mascarado em tf
    link_olx = f"https://olx.com.br{termo_limpo}"
    link_webmotors = f"https://webmotors.com.br{termo_limpo}"
    link_ml_pecas = f"https://mercadolivre.com.br{termo_limpo}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon_pecas = f"https://amazon.com.br{termo_limpo}&tag={ID_AFILIADO_AMAZON}"
    
    botoes_links = [
        [InlineKeyboardButton("🚘 Buscar Veículo na OLX", url=link_olx)],
        [InlineKeyboardButton("🚙 Buscar Veículo na Webmotors", url=link_webmotors)],
        [InlineKeyboardButton("🔧 Auto Peças no Mercado Livre", url=link_ml_pecas)],
        [InlineKeyboardButton("📦 Acessórios Autos na Amazon", url=link_amazon_pecas)],
        [InlineKeyboardButton("🔄 Fazer outra pesquisa", callback_data='buscar')]
    ]
    
    markup = InlineKeyboardMarkup(botoes_links)
    
    texto_resposta = f"🔍 **Resultados encontrados para:** *{texto_mensagem}*\n\nEscolha uma das plataformas oficiais abaixo para conferir os preços com total segurança:"
    bot.reply_to(message, texto_resposta, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    # Comando para rodar o robô em segundo plano localmente
    import threading
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

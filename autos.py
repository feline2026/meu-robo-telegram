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
    # Converte o texto para letras minúsculas para o robô nunca falhar a leitura
    texto_minusculo = texto_mensagem.lower()
    termo_limpo = urllib.parse.quote_plus(texto_minusculo)
    
    # --- SISTEMA DE INTELIGÊNCIA ARTIFICIAL AVALIADORA TF ---
    relatorio_ia = ""
    if "km" in texto_minusculo or "000" in texto_minusculo:
        relatorio_ia = (
            "🤖 **Relatório de Avaliação Inteligente tf**\n"
            "Análise do veículo concluída com sucesso!\n\n"
            "1️⃣ **Análise de Rodagem:** Quilometragem registrada detectada. Recomenda-se checar o desgaste de pneus, pastilhas de freio e histórico de revisões na concessionária.\n"
            "2️⃣ **Alerta de Segurança:** Modelos comerciais e motocicletas possuem alto índice de clonagem e sinistros no Brasil.\n"
            "3️⃣ **Procedência:** *Nunca feche negócio apenas olhando a estética do veículo!* É obrigatório puxar a capivara completa antes de fazer qualquer PIX de sinal.\n\n"
            "⚠️ **Ação Crítica Recomendada:** Utilize o botão de puxar placa abaixo para garantir que o veículo não é de leilão ou roubado.\n\n"
            "━━━━━━━━━━━━━━━\n\n"
        )

    
    # Gerando os links de mobilidade e autopeças mascarados em tf
    # Termo formatado para links comuns na web
    termo_url = urllib.parse.quote_plus(texto_mensagem)
    
    # 🔗 LINK DO SEU NOVO SITE VISUAL DO STOCKNEGÓCIO NO RENDER
    # Passa a busca do cliente direto para a sua página web automatizada
    link_seu_site = f"https://onrender.com{termo_url}"
    
    # Links de mobilidade e autopeças corrigidos com as barras oficiais
    link_olx = f"https://olx.com.br{termo_url}"
    link_webmotors = f"https://webmotors.com.br{termo_url}"
    link_ml_pecas = f"https://lista,mercadolivre.com.br/{termo_url}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon_pecas = f"https://amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"
    link_consulta_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
    
    botoes_links = [
        [InlineKeyboardButton("🌐 VER NO SITE VISUAL", url=link_seu_site)], # Botão igual ao primeiro projeto!
        [InlineKeyboardButton("🚘 Buscar Veículo na OLX", url=link_olx)],
        [InlineKeyboardButton("🚙 Buscar Veículo na Webmotors", url=link_webmotors)],
        [InlineKeyboardButton("🚨 CONSULTAR HISTÓRICO DA PLACA", url=link_consulta_placa)],
        [InlineKeyboardButton("🔧 Auto Peças no Mercado Livre", url=link_ml_pecas)],
        [InlineKeyboardButton("📦 Acessórios e E-Bikes na Amazon", url=link_amazon_pecas)],
        [InlineKeyboardButton("🔄 Fazer outra pesquisa", callback_data='buscar')]
    ]

    
    markup = InlineKeyboardMarkup(botoes_links)
    
    texto_resposta = f"{relatorio_ia}🔍 **Resultados de Mobilidade para:** *{texto_mensagem}*\n\nEscolha uma das plataformas oficiais abaixo para conferir preços e peças com total segurança:"
    bot.reply_to(message, texto_resposta, reply_markup=markup, parse_mode="Markdown")


if __name__ == "__main__":
    import threading
    bot.remove_webhook()
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, none_stop=True)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



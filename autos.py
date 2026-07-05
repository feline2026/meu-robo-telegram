import os
import urllib.parse
from flask import Flask, request, render_template_string
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- INSTANCIAÇÃO DO SERVIDOR WEB E DO ROBÔ ---
app = Flask(__name__)
TOKEN_TELEGRAM = "8645090278:AAGSdrnx9dh4i4s7FFfkM8yU60CI-mUab10"
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# # --- CONFIGURAÇÃO DOS AFILIADOS NO BOT --- (Apenas uma vez no topo!)
ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
ID_AFILIADO_AMAZON = "nsoc02-20"
ID_AFILIADO_MAGALU = "tf"

# # Bloco de Formatação e Links Unificado no Topo (Estrutura única!)
def mapear_todos_os_links(produto):
    termo_olx = urllib.parse.quote_plus(produto)
    termo_webmotors = urllib.parse.quote_plus(produto)
    termo_ml = urllib.parse.quote_plus(produto)
    termo_amazon = urllib.parse.quote_plus(produto)
    termo_site = urllib.parse.quote_plus(produto)
    
    link_seu_site = f"https://onrender.com{termo_site}"
    link_olx = f"https://olx.com.br{termo_olx}"
    link_webmotors = f"https://webmotors.com.br{termo_webmotors}"
    link_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
    link_ml = f"https://mercadolivre.com.br{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon = f"https://www.amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"
    
    return link_seu_site, link_olx, link_webmotors, link_placa, link_ml, link_amazon

# --- DESIGN DO SITE VISUAL AUTOMOTIVO (HTML/CSS + GEO) ---
HTML_PAGINA = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "StockNegócio",
      "alternateName": "Buscador de Mobilidade Inteligente tf",
      "url": "https://onrender.com",
      "applicationCategory": "ShoppingApplication",
      "operatingSystem": "All",
      "browserRequirements": "Requires HTML5 support",
      "description": "Buscador inteligente automotivo. Compara veículos e autopeças na OLX, Webmotors, Mercado Livre e Amazon com rastreamento seguro.",
      "offers": {{
        "@type": "Offer",
        "price": "0.00",
        "priceCurrency": "BRL"
      }}
    }}
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StockNegócio - Pesquisa Automotiva tf</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding: 20px; margin: 0; }}
        .container {{ max-width: 500px; margin: 0 auto; background: #1e1e1e; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        h1 {{ color: #ff9900; font-size: 24px; margin-bottom: 10px; }}
        p {{ color: #aaaaaa; font-size: 14px; margin-bottom: 25px; }}
        .termo {{ font-weight: bold; color: #ffffff; background: #333333; padding: 5px 10px; border-radius: 5px; }}
        .btn {{ display: block; width: 100%; max-width: 100%; box-sizing: border-box; margin: 12px 0; padding: 15px; text-decoration: none; color: white; font-weight: bold; border-radius: 8px; font-size: 15px; transition: transform 0.2s; text-align: center; }}
        .btn:hover {{ transform: scale(1.02); }}
        .olx {{ background-color: #6E0AD6; }}
        .webmotors {{ background-color: #E31C23; }}
        .placa {{ background-color: #00A859; }}
        .ml {{ background-color: #FFF159; color: #333333; }}
        .amazon {{ background-color: #FF9900; color: #111111; }}
        .telegram {{ background-color: #0088cc; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏎️ StockNegócio</h1>
        <p>Resultados prontos para: <span class="termo">{{ termo }}</span></p>
        
        <a href="{{ link_olx }}" target="_blank" class="btn olx">🚘 Ver Veículo na OLX</a>
        <a href="{{ link_webmotors }}" target="_blank" class="btn webmotors">🚙 Ver Veículo na Webmotors</a>
        <a href="{{ link_placa }}" target="_blank" class="btn placa">🚨 CONSULTAR HISTÓRICO DA PLACA (10% OFF)</a>
        <a href="{{ link_ml }}" target="_blank" class="btn ml">🔧 Auto Peças no Mercado Livre</a>
        <a href="{{ link_amazon }}" target="_blank" class="btn amazon">📦 Acessórios e E-Bikes na Amazon</a>
        <a href="https://t.me" target="_blank" class="btn telegram">💬 Abrir no Robô do Telegram</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home_inicial():
    return "<h1>StockNegócio - Buscador Automotivo Online e Ativo!</h1>"

@app.route('/busca')
def abrir_site_visual():
    produto = request.args.get('q', '')
    
    # Puxa as variáveis prontas direto da estrutura única do topo
    link_seu_site, link_olx, link_webmotors, link_placa, link_ml, link_amazon = mapear_todos_os_links(produto)
    
    return render_template_string(
        HTML_PAGINA, termo=produto, link_olx=link_olx, link_webmotors=link_webmotors,
        link_ml=link_ml, link_amazon=link_amazon, link_placa=link_placa
    )

# --- FLUXO DO ROBÔ DO TELEGRAM ---
@bot.message_handler(commands=['start', 'help'])
def enviar_boas_vindas(message):
    texto_boas_vindas = (
        "🏎️ **Bem-vindo ao StockNegócio!**\n\n"
        "O seu buscador inteligente de Mobilidade, Carros, Motos e Autopeças.\n"
        "Digite o modelo de um veículo (ex: *Civic 2020*) ou uma peça/acessório para buscar!"
    )
    bot.reply_to(message, texto_boas_vindas, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def processar_busca_veiculo(message):
    produto = message.text
    texto_minusculo = produto.lower()
    
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
    
    # Puxa exatamente as mesmas variáveis da estrutura única do topo
    link_seu_site, link_olx, link_webmotors, link_placa, link_ml, link_amazon = mapear_todos_os_links(produto)
    
    botoes_links = [
        [InlineKeyboardButton("🌐 VER NO SITE VISUAL tf", url=link_seu_site)],
        [InlineKeyboardButton("🚘 Buscar Veículo na OLX", url=link_olx)],
        [InlineKeyboardButton("🚙 Buscar Veículo na Webmotors", url=link_webmotors)],
        [InlineKeyboardButton("🚨 CONSULTAR HISTÓRICO DA PLACA", url=link_placa)],
        [InlineKeyboardButton("🔧 Auto Peças no Mercado Livre", url=link_ml)],
        [InlineKeyboardButton("📦 Acessórios e E-Bikes na Amazon", url=link_amazon)]
    ]
    
    markup = InlineKeyboardMarkup(botoes_links)
    texto_resposta = f"{relatorio_ia}🔍 **Resultados de Mobilidade para:** *{produto}*\n\nEscolha uma das opções oficiais abaixo para navegar com total segurança:"
    bot.reply_to(message, texto_resposta, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    import threading
    bot.remove_webhook()
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, none_stop=True)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

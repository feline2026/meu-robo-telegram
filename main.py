import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =====================================================================
#  ⚙️ CÓDIGO DO SITE (VISUAL PREMIUM + ROTAS 100% CORRIGIDAS)
# =====================================================================
class VisualSiteHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        produto = query_params.get('p', [''])
        
        html_botoes = ""
        texto_resultados = ""
        
        if produto and produto[0]:
            prod_texto = produto[0]
            
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_SHOPEE = "18325271196"

            termo_ml = urllib.parse.quote(prod_texto.strip().replace(" ", "-"))
            termo_shopee = urllib.parse.quote(prod_texto.strip().lower().replace(" ", "-"))
            termo_amazon = urllib.parse.quote(prod_texto.strip())

            # Links com as rotas oficiais e o WWW obrigatório na Amazon
            link_ml = f"https://mercadolivre.com.br{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
            link_shopee = f"https://shopee.com.br{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
            link_amazon = f"https://amazon.com.br{termo_amazon}"
            
            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2>"
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🛒 Ver no Mercado Livre</a>
                <a href="{link_shopee}" target="_blank" class="btn btn-shopee">🛍️ Ver na Shopee</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a>
            </div>
            """

        html_pagina = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Não Sabe Onde Comprar - Clique Aqui</title>
            <style>
                body {{
                    margin: 0; padding: 0; background-color: #121214; color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    display: flex; flex-direction: column; align-items: center; min-height: 100vh;
                }}
                .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; }}
                h1 {{ font-size: 26px; margin-bottom: 5px; font-weight: 800; }}
                .sub {{ color: #a8a8b3; font-size: 16px; margin-bottom: 40px; }}
                form {{ width: 100%; display: flex; flex-direction: column; gap: 15px; }}
                input[type="text"] {{
                    width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px;
                    background-color: #202024; color: #ffffff; font-size: 16px; outline: none; box-sizing: border-box;
                }}
                input[type="text"]:focus {{ border-color: #00b37e; }}
                button {{
                    width: 100%; padding: 16px; border: none; border-radius: 8px;
                    background-color: #00b37e; color: #ffffff; font-size: 16px; font-weight: bold; cursor: pointer;
                }}
                h2 {{ font-size: 16px; color: #a8a8b3; margin-top: 30px; }}
                h2 span {{ color: #00b37e; }}
                .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 20px; }}
                .btn {{
                    display: block; padding: 16px; text-decoration: none; color: white; font-weight: bold;
                    border-radius: 8px; text-align: center; font-size: 15px;
                }}
                .btn-ml {{ background-color: #fff159; color: #333333; }}
                .btn-shopee {{ background-color: #ee4d2d; }}
                .btn-amazon {{ background-color: #ff9900; color: #111111; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Não Sabe Onde Comprar</h1>
                <div class="sub">Clique Aqui 👇</div>
                
                <form action="/" method="GET">
                    <input type="text" name="p" value="{produto[0] if produto and produto[0] else ''}" placeholder="O que você quer buscar hoje?" required>
                    <button type="submit">🔍 Buscar Ofertas</button>
                </form>
                
                {texto_resultados}
                {html_botoes}
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_pagina.encode('utf-8'))

def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), VisualSiteHandler)
    server.serve_forever()

threading.Thread(target=ligar_site_producao, daemon=True).start()

# =====================================================================
#  🤖 CÓDIGO DO ROBÔ DO TELEGRAM (SIMPLIFICADO E DIRETO)
# =====================================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Limpa qualquer resquício de memória ao iniciar
    context.user_data.clear()
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text

    ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
    ID_AFILIADO_SHOPEE = "18325271196"

    # Formatação limpa usando urllib.parse.quote para conversão estável de acentos e caracteres
    termo_ml = urllib.parse.quote(produto.strip().replace(" ", "-"))
    termo_shopee = urllib.parse.quote(produto.strip().lower().replace(" ", "-"))
    termo_amazon = urllib.parse.quote(produto.strip())

    # Links oficiais com o WWW travado no robô
    link_ml = f"https://mercadolivre.com.br{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
    link_shopee = f"https://shopee.com.br{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
    link_amazon = f"https://amazon.com.br{termo_amazon}"

    botoes_links = [
        [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
        [InlineKeyboardButton("🛍️ Ver na Shopee", url=link_shopee)],
        [InlineKeyboardButton("📦 Ver na Amazon", url=link_amazon)],
        [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
    ]

    structure_links = InlineKeyboardMarkup(botoes_links)

    await update.message.reply_text(
        f"Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
        reply_markup=structure_links,
        parse_mode="Markdown"
    )

async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # Limpa a memória para garantir que a próxima digitação venha do zero
    context.user_data.clear()
    await query.message.reply_text("Pode enviar o nome do novo produto que deseja buscar!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^buscar$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    application.run_polling()

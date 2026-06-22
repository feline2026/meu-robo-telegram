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
#  ⚙️ CÓDIGO DO SITE (VISUAL PREMIUM + ROTAS DIRETAS DE BUSCA)
# =====================================================================
class VisualSiteHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        produto = query_params.get('p', [''])
        
        html_botoes = ""
        texto_resultados = ""
        
        # Correção da lista: Extrai a busca sem os colchetes ['']
        if produto and produto[0]:
            prod_texto = produto[0].strip()
            
            # --- CONFIGURAÇÃO DOS AFILIADOS ---
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_SHOPEE = "18325271196"
            ID_AFILIADO_AMAZON = "nsoc02-20"
            ID_AFILIADO_MAGALU = "SEU_ID_MAGALU"       
            ID_AFILIADO_NETSHOES = "SEU_ID_NETSHOES"

            # Formatação de strings limpas para as buscas
            termo_ml = urllib.parse.quote_plus(prod_texto.replace(" ", "-"))
            termo_shopee = urllib.parse.quote_plus(prod_texto.lower().replace(" ", "-"))
            termo_amazon = urllib.parse.quote_plus(prod_texto)
            termo_magalu = urllib.parse.quote_plus(prod_texto)
            termo_netshoes = urllib.parse.quote_plus(prod_texto)

            # --- LINKS DAS LOJAS ---
            link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
            link_shopee = f"https://shopee.com.br/list/{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
            link_amazon = f"https://amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"
            link_magalu = f"https://magazineluiza.com.br/busca/{termo_magalu}/?partner_id={ID_AFILIADO_MAGALU}"
            link_netshoes = f"https://netshoes.com.br/?q={termo_netshoes}&utm_source=afiliados&utm_campaign={ID_AFILIADO_NETSHOES}"

            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2>"
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🛒 Ver no Mercado Livre</a>
                <a href="{link_shopee}" target="_blank" class="btn btn-shopee">🛍️ Ver na Shopee</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a>
                <a href="{link_magalu}" target="_blank" class="btn btn-magalu">💙 Ver na Magalu</a>
                <a href="{link_netshoes}" target="_blank" class="btn btn-netshoes">👟 Ver na Netshoes</a>
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
                    display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh;
                }}
                .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: auto; }}
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
                .btn-magalu {{ background-color: #0086ff; color: white; }}
                .btn-netshoes {{ background-color: #532d85; color: white; }}
                
                footer {{ width: 100%; padding: 15px; text-align: center; font-size: 12px; color: #737380; background-color: #1a1a1e; box-sizing: border-box; }}
                footer a {{ color: #00b37e; text-decoration: none; font-weight: bold; }}
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
            
            <footer>
                Buscador gratuito e independente de utilidade pública. <a href="#" onclick="alert('Aviso de Transparência:\\n\\nO naosabeondecomprar é um buscador independente de ofertas. Não realizamos vendas, não processamos pagamentos e não coletamos dados pessoais.\\n\\nAo clicar nos botões que direcionam para as lojas parceiras (Mercado Livre, Amazon, Shopee, Magalu e Netshoes), nós poderemos receber uma comissão caso uma compra seja realizada, sem nenhum custo adicional para você.')">Informações de Transparência</a>
            </footer>
        </body>
        </html>
        """
        self.wfile.write(html_pagina.encode('utf-8'))

def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), VisualSiteHandler)
    server.serve_forever()

# =====================================================================
#  🤖 CÓDIGO DO ROBÔ DO TELEGRAM (FORMATO SEGURO E CORRIGIDO)
# =====================================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    botoes_start = [[InlineKeyboardButton("📜 Transparência e Aviso Legal", callback_data='ver_transparencia')]]
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.", reply_markup=InlineKeyboardMarkup(botoes_start))

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()
    termo_busca = urllib.parse.quote_plus(produto)
    
    # URL do site hospedado no Render
    url_site = f"https://onrender.com{termo_busca}"
    
    botoes = [[InlineKeyboardButton("🔍 Ver Lojas Disponíveis", url=url_site)]]
    await update.message.reply_text(
        f"Resultados prontos para: *{produto}*\nClique abaixo para escolher a loja desejada!",
        reply_markup=InlineKeyboardMarkup(botoes),
        parse_mode="Markdown"
    )

async def lidar_botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'ver_transparencia':
        aviso = (
            "Aviso de Transparência:\n\n"
            "O buscador é independente. Não realizamos vendas nem processamos pagamentos.\n"
            "Podemos receber comissão das lojas parceiras caso uma compra aconteça."
        )
        await query.message.reply_text(aviso)

def principal():
    if TOKEN:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
        app.add_handler(CallbackQueryHandler(lidar_botoes))
        
        print("🤖 Robô do Telegram iniciado...")
        app.run_polling()
    else:
        print("⚠️ Erro: TELEGRAM_TOKEN não configurado no Render.")

if __name__ == "__main__":
    # Inicia o site em segundo plano
    threading.Thread(target=ligar_site_producao, daemon=True).start()
    # Inicia o Telegram principal
    principal()

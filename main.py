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
        
        if produto and produto:
            prod_texto = produto.strip()
            
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_SHOPEE = "18325271196"
            ID_AFILIADO_AMAZON = "nsoc02-20"
            ID_AFILIADO_MAGALU = "SEU_ID_MAGALU"       
            ID_AFILIADO_SHEIN = "SEU_ID_SHEIN"         

            termo_ml = urllib.parse.quote_plus(prod_texto.replace(" ", "-"))
            termo_shopee = urllib.parse.quote_plus(prod_texto.lower().replace(" ", "-"))
            termo_amazon = urllib.parse.quote_plus(prod_texto)
            termo_magalu = urllib.parse.quote_plus(prod_texto)
            termo_shein = urllib.parse.quote_plus(prod_texto.lower())

            link_ml = f"https://mercadolivre.com.br{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
            link_shopee = f"https://shopee.com.br{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
            link_amazon = f"https://amazon.com.br{termo_amazon}&tag={ID_AFILIADO_AMAZON}"
            link_magalu = f"https://magazineluiza.com.br{termo_magalu}/?partner_id={ID_AFILIADO_MAGALU}"
            link_shein = f"https://shein.com{termo_shein}&sub_aff_id={ID_AFILIADO_SHEIN}"

            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2>"
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🛒 Ver no Mercado Livre</a>
                <a href="{link_shopee}" target="_blank" class="btn btn-shopee">🛍️ Ver na Shopee</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a>
                <a href="{link_magalu}" target="_blank" class="btn btn-magalu">💙 Ver na Magalu</a>
                <a href="{link_shein}" target="_blank" class="btn btn-shein">🖤 Ver na Shein</a>
            </div>
            """

        html_pagina = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Não Sabe Onde Comprar - Buscador de Ofertas</title>
            <style>
                body {{
                    margin: 0; padding: 0; background-color: #0f111a; color: #ffffff;
                    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
                    display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh;
                    box-sizing: border-box;
                }}
                .container {{ width: 100%; max-width: 550px; padding: 60px 20px; text-align: center; box-sizing: border-box; margin: auto; }}
                h1 {{ font-size: 32px; margin-bottom: 8px; font-weight: 800; letter-spacing: -0.5px; background: linear-gradient(45deg, #00b37e, #00e6a6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
                .sub {{ color: #9aa0a6; font-size: 16px; margin-bottom: 35px; line-height: 1.4; }}
                form {{ width: 100%; display: flex; flex-direction: column; gap: 15px; background: #161b26; padding: 25px; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); border: 1px solid #252d3d; }}
                input[type="text"] {{
                    width: 100%; padding: 18px; border: 2px solid #2d3748; border-radius: 10px;
                    background-color: #0f111a; color: #ffffff; font-size: 16px; outline: none; box-sizing: border-box; transition: all 0.3s;
                }}
                input[type="text"]:focus {{ border-color: #00b37e; box-shadow: 0 0 0 3px rgba(0, 179, 126, 0.2); }}
                button {{
                    width: 100%; padding: 16px; border: none; border-radius: 10px;
                    background-color: #00b37e; color: #ffffff; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.2s;
                }}
                button:hover {{ background-color: #009e6f; }}
                
                .badge-container {{ display: flex; justify-content: center; gap: 8px; margin-top: 15px; flex-wrap: wrap; }}
                .badge {{ font-size: 11px; padding: 5px 10px; border-radius: 20px; font-weight: 600; text-transform: uppercase; color: #111; }}
                .bg-ml {{ background: #fff159; }} .bg-shopee {{ background: #ee4d2d; color: #fff; }} .bg-amazon {{ background: #ff9900; }} .bg-magalu {{ background: #0086ff; color: #fff; }} .bg-shein {{ background: #fff; }}

                h2 {{ font-size: 16px; color: #9aa0a6; margin-top: 35px; font-weight: 500; }}
                h2 span {{ color: #00b37e; font-weight: 700; }}
                .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 20px; }}
                .btn {{
                    display: block; padding: 16px; text-decoration: none; color: white; font-weight: bold;
                    border-radius: 10px; text-align: center; font-size: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: transform 0.2s;
                }}
                .btn:hover {{ transform: translateY(-2px); }}
                .btn-ml {{ background-color: #fff159; color: #333333; }}
                .btn-shopee {{ background-color: #ee4d2d; }}
                .btn-amazon {{ background-color: #ff9900; color: #111111; }}
                .btn-magalu {{ background-color: #0086ff; color: white; }}
                .btn-shein {{ background-color: #000000; color: white; border: 1px solid #333; }}
                
                footer {{ width: 100%; padding: 20px; text-align: center; font-size: 13px; color: #6b7280; border-top: 1px solid #161b26; background: #0b0d14; box-sizing: border-box; }}
                footer a {{ color: #00b37e; text-decoration: none; font-weight: 600; }}
                footer a:hover {{ text-decoration: underline; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Não Sabe Onde Comprar</h1>
                <div class="sub">Pesquise uma vez e compare instantaneamente nas maiores lojas da internet de forma gratuita e sem cadastros.</div>
                
                <form action="/" method="GET">
                    <input type="text" name="p" value="{produto if produto and produto else ''}" placeholder="O que você quer buscar hoje?" required autocomplete="off">
                    <button type="submit">🔍 Buscar Ofertas</button>
                    
                    <div class="badge-container">
                        <span class="badge bg-ml">Mercado Livre</span>
                        <span class="badge bg-shopee">Shopee</span>
                        <span class="badge bg-amazon">Amazon</span>
                        <span class="badge bg-magalu">Magalu</span>
                        <span class="badge bg-shein">Shein</span>
                    </div>
                </form>
                
                {texto_resultados}
                {html_botoes}
            </div>
            
            <footer>
                Independentes e transparentes. Ferramenta gratuita útil à comunidade. <a href="#" onclick="alert('Aviso de Transparência:\\n\\nEste site é um buscador independente e gratuito de ofertas. Não realizamos vendas diretas, não processamos pagamentos e não coletamos dados pessoais.\\n\\nAo clicar nos botões das lojas parceiras, podemos receber uma comissão caso uma compra seja realizada, sem nenhum custo adicional para você.')">Ler Termos de Transparência</a>
            </footer>
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
#  🤖 CÓDIGO DO ROBÔ DO TELEGRAM (FORMATO FLUIDO E PREVINIDO DE SPAÇO)
# =====================================================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    botoes_start = [[InlineKeyboardButton("📜 Transparência e Aviso Legal", callback_data='ver_transparencia')]]
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.", reply_markup=InlineKeyboardMarkup(botoes_start))

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()
    ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
    ID_AFILIADO_SHOPEE = "18325271196"
    ID_AFILIADO_AMAZON = "nsoc02-20"
    ID_AFILIADO_MAGALU = "SEU_ID_MAGALU"  

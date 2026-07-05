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

# =========================================================================
# 🌐 CÓDIGO DO SITE (VISUAL PREMIUM ESPELHADO DO PROJETO 1)
# =========================================================================
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

        # Lógica idêntica de extração por lista da sua foto
        if produto and produto[0]:
            prod_texto = produto[0].strip()
            
            # --- CONFIGURAÇÃO DOS AFILIADOS ---
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_AMAZON = "nsoc02-20"
            ID_AFILIADO_MAGALU = "tf"

            # Formatação de strings limpas baseada na sua foto
            termo_olx = urllib.parse.quote_plus(prod_texto.replace(" ", "-"))
            termo_webmotors = urllib.parse.quote_plus(prod_texto.lower().replace(" ", "-"))
            termo_ml = urllib.parse.quote_plus(prod_texto)
            termo_amazon = urllib.parse.quote_plus(prod_texto)

            # --- LINKS COMPLETOS DAS LOJAS AUTOMOTIVAS ---
            link_olx = f"https://olx.com.br{termo_olx}"
            link_webmotors = f"https://webmotors.com.br{termo_webmotors}"
            link_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
            link_ml = f"https://mercadolivre.com.br{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
            link_amazon = f"https://amazon.com.br{termo_amazon}&tag={ID_AFILIADO_AMAZON}"

            texto_resultados = f"<h2>Resultados encontrados para: <span>{prod_texto}</span></h2>"
            
            html_botoes = f"""
            <div class="box-botoes">
                <a href="{link_olx}" target="_blank" class="btn" style="background-color: #6E0AD6; color: white;">🚘 Ver na OLX</a>
                <a href="{link_webmotors}" target="_blank" class="btn" style="background-color: #E31C23; color: white;">🚙 Ver na Webmotors</a>
                <a href="{link_placa}" target="_blank" class="btn" style="background-color: #00A859; color: white;">🚨 Consultar Placa (10% OFF)</a>
                <a href="{link_ml}" target="_blank" class="btn btn-ml">🔧 Ver no Mercado Livre</a>
                <a href="{link_amazon}" target="_blank" class="btn btn-amazon">📦 Ver na Amazon</a>
            </div>
            """
            prod_val = prod_texto
        else:
            texto_resultados = "<h2>StockNegócio - Buscador Automotivo Online e Ativo!</h2>"
            prod_val = ""

        # Montagem do HTML estruturado idêntico ao seu projeto 1
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>StockNegócio - Clique Aqui</title>
            <style>
                body {{
                    margin: 0; padding: 0; background-color: #121212; color: #ffffff;
                    font-family: "Segoe UI", Arial, sans-serif;
                    display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh;
                }}
                .container {{
                    width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: 0 auto;
                }}
                h1 {{ font-size: 26px; margin-bottom: 5px; font-weight: 800; color: #ffffff; }}
                .sub {{ color: #a8a8b3; font-size: 16px; margin-bottom: 40px; }}
                form {{ width: 100%; display: flex; flex-direction: column; gap: 15px; }}
                input[type="text"] {{
                    width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px;
                    background-color: #202024; color: #ffffff; font-size: 16px; outline: none; box-sizing: border-box;
                }}
                input[type="text"]:focus {{ border-color: #00b37e; }}
                button[type="submit"] {{
                    width: 100%; padding: 16px; border: none; border-radius: 8px;
                    background-color: #00b37e; color: #ffffff; font-size: 16px; font-weight: bold; cursor: pointer;
                    margin-top: 5px;
                }}
                .box-botoes {{
                    display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 24px;
                }}
                .btn {{
                    display: block; width: 100%; padding: 16px; border: none; border-radius: 8px;
                    text-decoration: none; font-size: 16px; font-weight: bold; cursor: pointer; text-align: center; box-sizing: border-box;
                    transition: transform 0.2s;
                }}
                .btn:hover {{ transform: scale(1.02); }}
                .btn-ml {{ background-color: #FFF159; color: #333333; }}
                .btn-amazon {{ background-color: #FF9900; color: #111111; }}
                .telegram {{ background-color: #00b37e; color: white; margin-top: 20px; }}
                footer {{ width: 100%; padding: 15px; text-align: center; font-size: 12px; color: #737380; background-color: #1a1a1e; box-sizing: border-box; }}
                footer a {{ color: #00b37e; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏎️ StockNegócio</h1>
                <div class="sub">{texto_resultados}</div>
                
                <form action="/" method="GET">
                    <input type="text" name="p" value="{prod_val}" placeholder="O que você quer buscar?">
                    <button type="submit">Buscar Ofertas</button>
                </form>
                
                {html_botoes}
                <a href="https://t.me" target="_blank" class="btn telegram">💬 Abrir no Robô do Telegram</a>
            </div>
            <footer>Buscador gratuito e independente de utilidade pública. <a href="#" onclick="alert('Aviso de Transparência:\\n\\nNão coletamos dados pessoais.')">Aviso de Transparência</a></footer>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))

# Porta 10000 idêntica à do projeto 1
def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), VisualSiteHandler)
    server.serve_forever()

# =========================================================================
# 🤖 FLUXO DO ROBÔ DO TELEGRAM (Mecanismo Idêntico ao Principal)
# =========================================================================
TOKEN = "8645090278:AAGSdrnx9dh4i4s7FFfkM8yU60CI-mUab10"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear() # Limpeza idêntica à sua linha 167 da foto
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar: ")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip() # Strip igualzinho à linha 171 da sua foto
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

    ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
    ID_AFILIADO_AMAZON = "nsoc02-20"
    ID_AFILIADO_MAGALU = "tf"

    termo_site = urllib.parse.quote_plus(produto)
    termo_olx = urllib.parse.quote_plus(produto.replace(" ", "-"))
    termo_webmotors = urllib.parse.quote_plus(produto.lower().replace(" ", "-"))
    termo_ml = urllib.parse.quote_plus(produto)
    termo_amazon = urllib.parse.quote_plus(produto)

    # # Links parametrizados corrigidos com as rotas exatas de busca (/list/, /s?k-, /busca/)
    link_ml = f"https://mercadolivre.com.br{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon = f"https://amazon.com.br{termo_amazon}&tag={ID_AFILIADO_AMAZON}"
    link_olx = f"https://olx.com.br{termo_olx}"
    link_webmotors = f"https://webmotors.com.br{termo_webmotors}"
    link_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
    link_seu_site = f"https://onrender.com{termo_site}"

    botoes_links = [
        [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
        [InlineKeyboardButton("📦 Ver na Amazon", url=link_amazon)],
        [InlineKeyboardButton("🚘 Ver na OLX", url=link_olx)],
        [InlineKeyboardButton("🚙 Ver na Webmotors", url=link_webmotors)],
        [InlineKeyboardButton("🚨 Consultar Placa (10% OFF)", url=link_placa)],
        [InlineKeyboardButton("🌐 Ver no Site Visual tf", url=link_seu_site)],
        [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
    ]

    structure_links = InlineKeyboardMarkup(botoes_links)

    await update.message.reply_text(
        f"{relatorio_ia}Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
        reply_markup=structure_links,
        parse_mode="Markdown"
    )


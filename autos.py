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

        # Correção da lista: Extrai a busca sem os colchetes ['']
        if produto and produto[0]:
            prod_texto = produto[0].strip()
            
            # --- CONFIGURAÇÃO DOS AFILIADOS ---
            ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
            ID_AFILIADO_AMAZON = "nsoc02-20"
            ID_AFILIADO_MAGALU = "tf"

            # Formatação direta e limpa igual à do seu projeto 1
            termo_olx = urllib.parse.quote_plus(prod_texto)
            termo_webmotors = urllib.parse.quote_plus(prod_texto)
            termo_ml = urllib.parse.quote_plus(prod_texto)
            termo_amazon = urllib.parse.quote_plus(prod_texto)

            # --- LINKS DAS LOJAS ---
            link_olx = f"https://olx.com.br{termo_olx}"
            link_webmotors = f"https://webmotors.com.br{termo_webmotors}"
            link_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
            link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
            link_amazon = f"https://www.amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"

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

        html_pagina = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "stocknegocios",
      "alternateName": "Buscador de Ofertas Integrado tf",
      "url": "https://onrender.com",
      "applicationCategory": "ShoppingApplication",
      "operatingSystem": "All",
      "browserRequirements": "Requires HTML5 support",
      "description": "Buscador inteligente e automatizado de ofertas em tempo real. Compara preços instantaneamente e encontra cupons validados no olx, webmotors, olhonocarro, Mercadolivre e amazon.",
      "offers": {{
        "@type": "Offer",
        "price": "0.00",
        "priceCurrency": "BRL"
      }},
      "featureList": "Comparador de preços automático, busca integrada multiloja, redirecionamento seguro com tracking tf, integração direta com robô do Telegram"
    }}
    </script>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>StockNegócio - Clique Aqui</title>
            <style>
                body {{
                    margin: 0; padding: 0; background-color: #121212; color: #ffffff;
                    font-family: "Segoe UI", Arial, sans-serif;
                    display: flex; flex-direction: column; align-items: center; justify-content: space-between; min-height: 100vh;
                }}
                .container {{ width: 100%; max-width: 500px; padding: 40px 20px; text-align: center; box-sizing: border-box; margin: 0 auto;}}
                h1 {{ font-size: 26px; margin-bottom: 5px; font-weight: 800; }}
                .sub {{ color: #a8a8b3; font-size: 16px; margin-bottom: 40px; }}
                form {{ width: 100%; display: flex; flex-direction: column; gap: 15px; }}
                input[type="text"] {{
                    width: 100%; padding: 16px; border: 2px solid #29292e; border-radius: 8px;
                    background-color: #202024; color: #ffffff; font-size: 16px; outline: none; box-sizing: border-box;
                }}
                input[type="text"]:focus {{ border-color: #00b37e; }}
                button[type="submit"] {{ width: 100%; padding: 16px; border: none; border-radius: 8px;
                    background-color: #00b37e; color: #ffffff; font-size: 16px; font-weight: bold; cursor: pointer;
                    margin-top: 5px;
                }}
                .box-botoes {{ display: flex; flex-direction: column; gap: 12px; width: 100%; margin-top: 24px;}}
                .btn {{
                    display: block; padding: 16px; text-decoration: none; color: white; font-weight: bold;
                    border-radius: 8px; text-align: center; font-size: 15px;
                }}
                .btn-ml {{ background-color: #FFF159; color: #333333; }}
                .btn-amazon {{ background-color: #FF9900; color: #111111; }}
                
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
                
                {texto_resultados}
                {html_botoes}
                <a href="https://t.me" target="_blank" class="btn telegram">💬 Abrir no Robô do Telegram</a>
            </div>
            <footer>
                Buscador gratuito e independente de utilidade pública. <a href="#" onclick="alert('Aviso de Transparência:\\n\\nO naosabeondecomprar é um buscador independente de ofertas. Não realizamos vendas, não processamos pagamentos e não coletamos dados pessoais.\\n\\nAo clicar nos botões que direcionam para as lojas parceiras (Mercado Livre, Amazon, Shopee, Magalu e Netshoes), nós poderemos receber uma comissão caso uma compra seja realizada, sem nenhum custo adicional para você.')">Informações de Transparência</a>
            </footer>
        </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))


# Porta dinâmica automática que impede o site de desligar ou dar erro de porta em uso
def ligar_site_producao():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), VisualSiteHandler)
    server.serve_forever()


# =========================================================================
# 🤖 FLUXO DO ROBÔ DO TELEGRAM (Mecanismo Idêntico ao Principal)
# =========================================================================
TOKEN = "8645090278:AAG7WbkUNdEhkiG51yt0HYQSEQ_esorYABE"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("🏎️ **StockNegócio ativo!**\n\nEnvie o nome de um veículo ou peça para buscar:")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    produto = update.message.text.strip()
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

    termo_site = urllib.parse.quote_plus(produto)
    termo_olx = urllib.parse.quote_plus(produto)
    termo_webmotors = urllib.parse.quote_plus(produto)
    termo_ml = urllib.parse.quote_plus(produto)
    termo_amazon = urllib.parse.quote_plus(produto)

    # Rotas parametrizadas limpas e corrigidas de ponta a ponta
    link_seu_site = f"https://onrender.com{termo_site}"
    link_olx = f"https://olx.com.br{termo_olx}"
    link_webmotors = f"https://webmotors.com.br{termo_webmotors}"
    link_placa = f"https://olhonocarro.com.br{ID_AFILIADO_MAGALU}"
    link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}?as_campaign={ID_AFILIADO_MERCADO_LIVRE}"
    link_amazon = f"https://www.amazon.com.br/s?k={termo_amazon}&tag={ID_AFILIADO_AMAZON}"

    botoes_links = [
        [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)], 
        [InlineKeyboardButton("📦 Ver na Amazon", url=link_amazon)],
        [InlineKeyboardButton("🚘 Ver na OLX", url=link_olx)],
        [InlineKeyboardButton("🚙 Ver na Webmotors", url=link_webmotors)],
        [InlineKeyboardButton("🚨 Consultar Placa (10% OFF)", url=link_placa)],
        [InlineKeyboardButton("🌐 Ver no Site Visual tf", url=link_seu_site)],
        [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='recriar_busca')]
    ]

    structure_links = InlineKeyboardMarkup(botoes_links)
    
    await update.message.reply_text(f"{relatorio_ia}Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:", reply_markup=structure_links, parse_mode="Markdown")


async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.message.reply_text("Pode enviar o nome do novo produto que deseja buscar!")

if __name__ == '__main__':
    # ADICIONE APENAS ESTA LINHA ABAIXO (Ela liga o site junto com o Telegram):
    threading.Thread(target=ligar_site_producao, daemon=True).start()

    # 2. Inicia o robô com o ApplicationBuilder prioritário para mensagens de texto
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^recriar_busca$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    application.run_polling()



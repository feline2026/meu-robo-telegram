import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- CÓDIGO PARA ENGANAR O RENDER (ROBÔ NÃO CAIR) ---
def rodar_servidor_falso():
    porta = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', porta), SimpleHTTPRequestHandler)
    server.serve_forever()

# Inicia o servidor falso em segundo plano para o Render ficar feliz
threading.Thread(target=rodar_servidor_falso, daemon=True).start()
# ----------------------------------------------------

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")
    context.user_data['aguardando_busca'] = True 

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'aguardando_busca' not in context.user_data:
        context.user_data['aguardando_busca'] = True

    if context.user_data.get('aguardando_busca'):
        produto = update.message.text
        context.user_data['aguardando_busca'] = False

        # Configuração dos IDs de Afiliado (Coloque as suas Tags reais)
        ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
        ID_AFILIADO_SHOPEE = "18325271196"
        TAG_AFILIADO_AMAZON = "SUA_TAG_AMAZON_AQUI" # ex: seunome-20

        # Formatação correta dos termos de busca para cada plataforma
        termo_ml = urllib.parse.quote(produto.strip().replace(" ", "-"))
        termo_shopee = urllib.parse.quote(produto.strip().lower())
        termo_amazon = urllib.parse.quote(produto.strip())

        # Links estruturados de Afiliados
        link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
        link_shopee = f"https://shopee.com.br/list/{termo_shopee}?utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"
        link_amazon = f"https://lista.amazon.com.br{termo_amazon}&tag={TAG_AFILIADO_AMAZON}"

        # LISTA CORRIGIDA: Agora com os 3 botões de lojas juntos!
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
    context.user_data['aguardando_busca'] = True
    await query.message.reply_text("Pode enviar o nome do novo produto que deseja buscar!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^buscar$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))
    application.run_polling()

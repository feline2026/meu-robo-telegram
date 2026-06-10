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
TOKEN = os.environ.get("TELEGRAM_TOKEN")




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")
    context.user_data['aguardando_busca'] = True 

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Se o usuário não iniciou a busca pelo start ou pelo botão, ativa o estado para garantir
    if 'aguardando_busca' not in context.user_data:
        context.user_data['aguardando_busca'] = True

    if context.user_data.get('aguardando_busca'):
        produto = update.message.text
        context.user_data['aguardando_busca'] = False

        ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
        ID_AFILIADO_SHOPEE = "18325271196"

        # Formatação correta dos termos de busca
        termo_ml = urllib.parse.quote(produto.strip().replace(" ", "-"))
        termo_shopee = urllib.parse.quote(produto.strip())

        # Links estruturados com os IDs de afiliado
        link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
        link_shopee = f"https://shopee.com.br/search?keyword={termo_shopee}&utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"

        botoes_links = [
            [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
            [InlineKeyboardButton("🛍️ Ver na Shopee", url=link_shopee)],
            [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
        ]

        structure_links = InlineKeyboardMarkup(botoes_links)

        await update.message.reply_text(
            f"Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
            reply_markup=structure_links,
            parse_mode="Markdown"
        )

async def responder_botao_rebusca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gerencia o clique no botão de buscar outro produto"""
    query = update.callback_query
    await query.answer()
    
    # Ativa novamente o estado de busca e pede o nome do produto
    context.user_data['aguardando_busca'] = True
    await query.message.reply_text("Pode enviar o nome do novo produto que deseja buscar!")

if __name__ == '__main__':
    # Inicializa o bot com o Token configurado
    application = ApplicationBuilder().token(TOKEN).build()

    # Registra o comando /start
    application.add_handler(CommandHandler("start", start))

    # Registra o clique no botão "Buscar outro produto"
    application.add_handler(CallbackQueryHandler(responder_botao_rebusca, pattern='^buscar$'))

    # Escuta as mensagens de texto enviadas pelos usuários (evita ler comandos)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))

    # Mantém o processo do bot ativo em loop contínuo (resolve o erro do Render)
    application.run_polling()

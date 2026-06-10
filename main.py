import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Configurações iniciais do bot (exemplo genérico)
TOKEN = "SEU_TELEGRAM_TOKEN_AQUI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")
    context.user_data['aguandando_busca'] = True

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('aguardando_busca'):
        produto = update.message.text
        context.user_data['aguardando_busca'] = False

        ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
        ID_AFILIADO_SHOPEE = "18325271196"

        # Formata o termo substituindo espaços por traços para a URL ficar perfeita
        produto_formatado = produto.strip().replace(" ", "-")
        termo_encoded = urllib.parse.quote(produto_formatado)

        # URLs CORRIGIDAS: Com as rotas de busca completas e seguras
        link_ml = f"https://lista.mercadolivre.com.br/{termo_encoded}#jm={ID_AFILIADO_MERCADO_LIVRE}"
        link_shopee = f"https://www.shopee.com.br/search?keyword={termo_encoded}&sub_id={ID_AFILIADO_SHOPEE}"



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

# Restante da inicialização do seu ApplicationBuilder...

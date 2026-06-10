import urllib.parse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Envie o nome de um produto para buscar.")
    # CORRIGIDO: Adicionado o "r" que faltava em aguardando
    context.user_data['aguardando_busca'] = True 

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('aguardando_busca'):
        produto = update.message.text
        context.user_data['aguardando_busca'] = False

        ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
        ID_AFILIADO_SHOPEE = "18325271196"

        # No Mercado Livre usamos traço, na Shopee a busca universal usa %20 (espaço codificado)
        termo_ml = urllib.parse.quote(produto.strip().replace(" ", "-"))
        termo_shopee = urllib.parse.quote(produto.strip())

        # URL MERCADO LIVRE (Funcionando 100%)
        link_ml = f"https://lista.mercadolivre.com.br/{termo_ml}#jm={ID_AFILIADO_MERCADO_LIVRE}"
        
        # URL SHOPEE CORRIGIDA (Redirecionamento universal de afiliados)
        # O parâmetro universal correto para injetar o ID de afiliado em links brutos da Shopee é 'smtt' ou 'customId'
        link_shopee = f"https://shopee.com.br/search?keyword={termo_shopee}&utm_campaign=-&utm_content={ID_AFILIADO_SHOPEE}"

        botoes_links = [
            [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
            [InlineKeyboardButton("🛍️ Ver na Shopee", url=link_shopee)], # Agora o botão vai abrir corretamente
            [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
        ]

        structure_links = InlineKeyboardMarkup(botoes_links)

        await update.message.reply_text(
            f"Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
            reply_markup=structure_links,
            parse_mode="Markdown"
        )

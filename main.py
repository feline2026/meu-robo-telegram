import os
import urllib.parse
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

app = Flask('')

@app.route('/')
def home():
    return "Robô está online e ativo!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# SEU TOKEN CONFIGURADO COM SEGURANÇA NA RENDER
TOKEN = os.environ.get("TELEGRAM_TOKEN").strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    botoes = [
        [InlineKeyboardButton("🔍 Buscar Produtos", callback_data='buscar')],
        [InlineKeyboardButton("📋 Como Funciona?", callback_data='duvidas')],
    ]
    estrutura_menu = InlineKeyboardMarkup(botoes)
    await update.message.reply_text(
        "Olá! Seja bem-vindo ao nosso assistente de compras.\nEscolha uma opção:",
        reply_markup=estrutura_menu
    )

async def gerenciar_clique_botao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'buscar':
        context.user_data['aguardando_busca'] = True
        await query.message.reply_text("Digite o nome do produto que você deseja procurar (Ex: Pneu aro 29, Smartphone):")
    elif query.data == 'duvidas':
        await query.message.reply_text("Nós encontramos as melhores ofertas para você! Basta clicar em 'Buscar Produtos' e digitar o que você quer.")

async def processar_busca_produto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('aguardando_busca'):
        produto = update.message.text
        context.user_data['aguardando_busca'] = False
        
        ID_AFILIADO_MERCADO_LIVRE = "TARCFELL"
        
        # Formata o termo substituindo espaços por traços para a URL ficar perfeita
        produto_formatado = produto.strip().replace(" ", "-")
        termo_encoded = urllib.parse.quote(produto_formatado)
        
        # URL CORRIGIDA: Sem caracteres que quebram o Telegram
        link_ml = f"https://lista.mercadolivre.com.br/{termo_encoded}#jm={ID_AFILIADO_MERCADO_LIVRE}"
        
        botoes_links = [
            [InlineKeyboardButton("🛒 Ver no Mercado Livre", url=link_ml)],
            [InlineKeyboardButton("🔄 Buscar outro produto", callback_data='buscar')]
        ]
        structure_links = InlineKeyboardMarkup(botoes_links)
        
        await update.message.reply_text(
            f"Aqui estão os melhores resultados que encontrei para: *{produto}*\n\nClique no botão abaixo para ver as ofertas:",
            parse_mode="Markdown",
            reply_markup=structure_links
        )

def main():
    app_telegram = Application.builder().token(TOKEN).build()

    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(CallbackQueryHandler(gerenciar_clique_botao))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, processar_busca_produto))

    print("Bot de Afiliados Ativo!")
    app_telegram.run_polling()

if __name__ == "__main__":
    flask_thread = Thread(target=run, daemon=True)
    flask_thread.start()
    main()


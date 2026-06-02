import telebot
import requests

CHAVE_API_TELEGRAM = "8934530926:AAFGj7EaSJHcwO2ncC4DUKetbXPWtHKsg_8"
bot = telebot.TeleBot(CHAVE_API_TELEGRAM)

@bot.message_handler(func=lambda message: True)
def responder_cliente(message):
    termo_busca = message.text
    bot.reply_to(message, f"🔍 Buscando '{termo_busca}' no Mercado Livre... Aguarde.")
    
    try:
        url = f"https://mercadolibre.com{termo_busca}"
        response = requests.get(url, timeout=15).json()
        resultados = response.get('results', [])
        
        if not resultados:
            bot.reply_to(message, "❌ Não encontrei nenhum produto com essa descrição. Tente digitar de outra forma.")
            return

        produto = resultados[0]
        titulo = produto.get('title')
        preco = produto.get('price')
        link_original = produto.get('permalink')
        
        mensagem_final = (
            f"✅ *ITEM LOCALIZADO!*\n\n"
            f"📦 *Produto:* {titulo}\n"
            f"💵 *Preço:* R$ {preco:.2f}\n\n"
            f"🛒 *Clique no link abaixo para comprar com segurança:*\n"
            f"{link_original}"
        )
        bot.reply_to(message, mensagem_final, parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "⚠️ Ocorreu uma instabilidade na pesquisa. Por favor, tente enviar novamente.")

bot.polling(none_stop=True)


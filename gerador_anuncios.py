import os
import asyncio
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN_ELETRONICOS = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# SERVIDOR WEB OBRIGATÓRIO PARA O RENDER NÃO RECLAMAR DE PORTA
def ligar_servidor_obrigatorio():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class RenderHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.send_header('Content-type', 'text/plain; charset=utf-8'); self.end_headers()
            self.wfile.write(b"Gerador de Anuncios Ativo e Operacional!")
    porta = int(os.environ.get("PORT", 10000))
    try:
        HTTPServer(('0.0.0.0', porta), RenderHandler).serve_forever()
    except Exception:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 *Bem-vindo ao seu Assistente de Eletrônicos Tarciso!*\n\n"
        "Estou pronto para catalogar o seu lote. "
        "Basta me enviar a *FOTO* de qualquer aparelho ou eletrodoméstico "
        "que eu vou calcular os preços de mercado e criar o anúncio pronto!"
    )

async def processar_foto_eletronico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
        
    mensagem_aguarde = await update.message.reply_text("📸 _Analisando o aparelho e pesquisando preços... Aguarde..._")
    
    try:
        foto_maior = update.message.photo[-1]
        file = await context.bot.get_file(foto_maior.file_id)
        img_bytes = await file.download_as_bytearray()
        
        # IMPORTAÇÃO NATIVA DIRETA DA BIBLIOTECA DO GOOGLE
        import google.generativeai as genai
        
        # Configura a chave sem depender de objetos complexos de tipos
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "Aja como um especialista em e-commerce no Brasil. Analise cuidadosamente a imagem deste produto. Com base no modelo identificado, faça:\n\n"
            "1. RELATÓRIO DE PREÇOS: Forneça o Preço Menor (Desapego), Preço Médio (Justo) e Preço Maior praticados na OLX e Mercado Livre no Brasil atualmente.\n\n"
            "2. ANÚNCIO PRONTO PARA COPIAR: Crie uma descrição de vendas magnética (copywriting) para colar nas plataformas. Inclua um Título curto e chamativo, destaques com emojis e uma ficha técnica limpa usando linhas simples para eu preencher manual se não puder ler na foto.\n\n"
            "Seja muito direto, remova todos os asteriscos do texto e use emojis organizados."
        )
        
        # Envia a foto usando a estrutura multimodal síncrona/assíncrona limpa de dicionário
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": bytes(img_bytes)},
            prompt
        ])
        
        texto_ia = response.text
        texto_limpo = texto_ia.replace("**", "").replace("*", "").replace("#", "")
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=mensagem_aguarde.message_id)
        await update.message.reply_text(texto_limpo)
        return
                
    except Exception as e:
        await update.message.reply_text("❌ Ocorreu um erro ao processar a imagem. Garanta que a foto está nítida.")

if __name__ == '__main__':
    import threading
    threading.Thread(target=ligar_servidor_obrigatorio, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN_ELETRONICOS).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, processar_foto_eletronico))
    application.run_polling()

import os
import asyncio
import httpx
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN_ELETRONICOS = "8629034952:AAEKXMwlkOU34iGdBHx3ToKMlZG16GsFs_c"
GEMINI_KEY = "AIzaSy..."AQ.Ab8RN6Li4Ur45FCEDf_XdUHeTxrXmvtUbxv8ynFnfKUXKq0ujA

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 *Bem-vindo ao seu Assistente de Eletrônicos Tarciso!*\n\n"
        "Estou pronto para catalogar o seu lote. "
        "Basta me enviar a *FOTO* de qualquer aparelho (iPhone, videogame, notebook) "
        "que eu vou calcular os preços de mercado e criar o anúncio pronto!"
    )

async def processar_foto_eletronico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
        
    mensagem_aguarde = await update.message.reply_text("📸 _Analisando o aparelho e pesquisando preços... Aguarde..._")
    
    try:
        # Pega a foto em tamanho maior enviada no chat
        foto_maior = update.message.photo[-1]
        file = await context.bot.get_file(foto_maior.file_id)
        
        # MÉTODO OFICIAL ATUALIZADO DA BIBLIOTECA (VERSÃO 20+):
        img_bytes = await file.download_as_bytearray()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        url = f"https://googleapis.com{GEMINI_KEY}"
        headers = {"Content-Type": "application/json"}
        
        prompt = (
            "Analise cuidadosamente a imagem deste produto eletrônico. Com base no modelo identificado, faça:\n\n"
            "1. RELATÓRIO DE PREÇOS: Forneça o Preço Menor (Desapego), Preço Médio (Justo) e Preço Maior praticados na OLX e Mercado Livre no Brasil atualmente.\n\n"
            "2. ANÚNCIO PRONTO PARA COPIAR: Crie uma descrição de vendas magnética (copywriting) para colar nas plataformas. Inclua um Título curto e chamativo, destaques com emojis e uma ficha técnica limpa com espaços em branco como [Saúde da Bateria: __%] para eu preencher manual se não puder ler na foto.\n\n"
            "Seja muito direto, remova todos os asteriscos do texto e use emojis organizados."
        )
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_base64}}
                ]
            }]
        }
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=payload, headers=headers, timeout=25.0)
            if response.status_code == 200:
                dados = response.json()
                texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
                texto_limpo = texto_ia.replace("**", "").replace("*", "").replace("#", "")

                texto_limpo = texto_ia.replace("**", "").replace("*", "").replace("#", "")
                
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=mensagem_aguarde.message_id)
                await update.message.reply_text(texto_limpo)
                return
                
            await update.message.reply_text(f"❌ Erro na consulta do Google (HTTP {response.status_code})")
    except Exception as e:
        await update.message.reply_text("❌ Ocorreu um erro ao ler a imagem. Garanta que a foto está nítida.")

# SERVIDOR WEB ATIVO QUE RESPONDE INSTANTANEAMENTE PARA ENGANAR O RENDER
def ligar_servidor_obrigatorio():
    from http.server import BaseHTTPRequestHandler, HTTPServer
    class RenderHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b"Gerador de Anuncios Ativo e Operacional!")
    
    import os
    porta = int(os.environ.get("PORT", 10000))
    HTTPServer(('0.0.0.0', porta), RenderHandler).serve_forever()

if __name__ == '__main__':
    # Dispara o site obrigatório direto na linha principal para abrir a porta correndo
    import threading
    threading.Thread(target=ligar_servidor_obrigatorio, daemon=True).start()
    
    # Inicia o robô de anúncios do Tarciso de forma estável
    application = ApplicationBuilder().token(TOKEN_ELETRONICOS).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, processar_foto_eletronico))
    application.run_polling()



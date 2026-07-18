import urllib.parse
import os
import asyncio
import httpx
import base64
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# DEFINA SUAS CHAVES AQUI
TOKEN_ELETRONICOS = "8645090278:AAG5drnx9dh414s7FFFKM0yU60Ci-mUab10" # Seu token limpo
GEMINI_KEY = "AQ.Ab8RN6Li4Ur45FCEDf_XdUHeTxrXmvtUbxv8ynFnfKUXKq0ujA" # Coloque aqui a sua chave do Gemini

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 *Bem-vindo ao Gerador Automático de Anúncios Tarciso!*\n\n"
        "Estou pronto para te ajudar com o seu lote de eletrônicos. "
        "Basta me enviar a *FOTO* de qualquer aparelho (iPhone, videogame, notebook, etc.) "
        "que eu vou analisar o mercado e criar o anúncio perfeito para você colar nas plataformas!"
    )

async def processar_foto_eletronico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        return
        
    mensagem_aguarde = await update.message.reply_text("📸 _Analisando a foto do eletrônico e pesquisando preços de mercado... Aguarde..._")
    
    # 1. Baixa a foto enviada pelo Tarciso no Telegram
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    img_bytes = await file.download_as_bytearray()
    
    # 2. Configura a chamada para o cérebro multimodal do Gemini
    url = f"https://googleapis.com{GEMINI_KEY}"
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        "Analise cuidadosamente a imagem deste produto eletrônico. Com base no modelo identificado, faça duas coisas separadas:\n\n"
        "BLOCO 1: RELATÓRIO DE PREÇOS\n"
        "Pesquise mentalmente os valores praticados atualmente no Mercado Livre e OLX do Brasil para este item usado e forneça:\n"
        "- Preço Menor (Venda Rápida/Desapego)\n"
        "- Preço Médio (Valor Justo de Mercado)\n"
        "- Preço Maior (Item Impecável com acessórios)\n\n"
        "BLOCO 2: ANÚNCIO PRONTO PARA PLATAFORMAS\n"
        "Crie uma descrição magnética de vendas (copywriting) perfeita para colar na OLX ou Mercado Livre. Inclua:\n"
        "- Um Título Matador e curto\n"
        "- Destaques do produto com emojis\n"
        "- Uma ficha técnica limpa (deixe espaços em branco como [Saúde da Bateria: __%] ou [Armazenamento: __GB] se não puder identificar na foto para eu preencher manual)\n"
        "- Gatilho de urgência para fechar negócio rápido.\n\n"
        "Seja muito direto, profissional e use emojis organizados. Remova todos os asteriscos do texto."
    )
    
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": img_base64
                    }
                }
            ]
        }]
    }
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, json=payload, headers=headers, timeout=25.0)
            if response.status_code == 200:
                dados = response.json()
                # CORREÇÃO DA LINHA 57: 'candidates' em vez de 'contents'
                texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
                texto_limpo = texto_ia.replace("**", "").replace("*", "").replace("#", "")
                
                # Divide o texto para enviar em dois balões separados, facilitando a cópia
                partes = texto_limpo.split("BLOCO 2:")
                
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=mensagem_aguarde.message_id)
                
                # Envia o Relatório de Preços (Bloco 1)
                await update.message.reply_text(f"📊 *ESTATÍSTICAS DE MERCADO:*\n\n{partes[0].strip()}")
                
                # Envia o Anúncio Pronto (Bloco 2)
                if len(partes) > 1:
                    await update.message.reply_text(f"✍️ *ANÚNCIO PRONTO PARA COPIAR E COLAR:*\n\n{partes[1].strip()}")
                return
                
            await update.message.reply_text(f"❌ Erro na análise do Google (Código HTTP {response.status_code})")
    except Exception as e:
        await update.message.reply_text("❌ Ocorreu um erro ao processar a imagem. Certifique-se de que a foto está nítida.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN_ELETRONICOS).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, processar_foto_eletronico))
    application.run_polling()

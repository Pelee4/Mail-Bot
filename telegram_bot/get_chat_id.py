from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config.settings import TELEGRAM_TOKEN

# Este bot de Telegram te permite obtener el chat_id de cualquier chat enviando un mensaje. Ya que
# el chat_id es necesario para enviar mensajes a un chat específico, este bot te facilita esa tarea.
async def mostrar_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title or "Chat privado o sin título"
    print(f"Mensaje recibido en chat '{chat_title}' con chat_id: {chat_id}")
    # Puedes hacer que responda al chat para avisar
    await update.message.reply_text(f"Este chat tiene chat_id: {chat_id}")

if __name__ == "__main__":
    import os
    token = TELEGRAM_TOKEN
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.ALL, mostrar_chat_id))
    print("Bot listo para obtener chat_id, envía un mensaje desde el chat deseado...")
    app.run_polling()

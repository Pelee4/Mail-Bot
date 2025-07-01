import requests
from dotenv import load_dotenv
import os


# Función para enviar mensajes a Telegram
# Utiliza la API REST de Telegram para enviar mensajes al chat especificado
def enviar_mensaje(mensaje: str):
    load_dotenv()  # Cargar las variables de entorno desde el archivo .env
    """Envía un mensaje a Telegram usando la API REST"""
    url = f"https://api.telegram.org/bot{os.getenv("TELEGRAM_TOKEN")}/sendMessage" # URL de la API de Telegram para enviar mensajes
    
    data = {
        'chat_id': os.getenv("TELEGRAM_CHAT_ID"), # ID del chat donde se enviará el mensaje
        'text': mensaje, # El mensaje a enviar
        'parse_mode': 'Markdown'  # Para que funcionen los emojis y formato
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        print(f"📤 Mensaje enviado a Telegram exitosamente")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Error enviando mensaje a Telegram: {e}")
        return False
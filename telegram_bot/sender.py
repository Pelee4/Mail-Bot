import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Función para enviar mensajes a Telegram
# Utiliza la API REST de Telegram para enviar mensajes al chat especificado
def enviar_mensaje(mensaje: str, es_notificacion: bool = False):
    """Envía un mensaje a Telegram al grupo correspondiente"""
    bot_token = os.getenv('TELEGRAM_TOKEN')
    
    # Debug: imprimir valores
    print(f"🔍 Bot token existe: {'Sí' if bot_token else 'No'}")
    
    # Seleccionar el chat_id según el tipo de correo
    if es_notificacion:
        chat_id = os.getenv('TELEGRAM_CHAT_ID_NOTIFICATIONS')
        print(f"🔔 Enviando notificación a: {chat_id}")
    else:
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        print(f"📧 Enviando correo normal a: {chat_id}")
    
    if not bot_token:
        print("❌ TELEGRAM_BOT_TOKEN no encontrado")
        return False
        
    if not chat_id:
        print(f"❌ Chat ID no encontrado para {'notificaciones' if es_notificacion else 'correos normales'}")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': mensaje,
    }
    
    try:
        print(f"🌐 Enviando a URL: {url}")
        print(f"📦 Payload: chat_id={chat_id}, longitud_mensaje={len(mensaje)}")
        
        response = requests.post(url, data=payload, timeout=10)
        
        print(f"📡 Status code: {response.status_code}")
        
        response.raise_for_status()
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al enviar mensaje: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"❌ Response text: {e.response.text}")
        return False
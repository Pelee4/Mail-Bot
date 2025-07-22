""" Configuración de grupos de Telegram """
import os
from dotenv import load_dotenv

load_dotenv()

# Mapeo de categorías a chat_ids de Telegram
GRUPOS_TELEGRAM = {
    "CLIENTE_CRITICO": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_CRITICO'),
        "nombre": "🚨 Críticos",
        "descripcion": "Problemas urgentes de clientes"
    },
    "COMERCIAL": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_COMERCIAL'),
        "nombre": "💰 Comercial", 
        "descripcion": "Nuevos clientes y presupuestos"
    },
    "HOSTING_DOMINIOS": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_HOSTING'),
        "nombre": "📊 Hosting",
        "descripcion": "Hosting, dominios y renovaciones"
    },
    "FACTURACION": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_FACTURACION'),
        "nombre": "💳 Facturación",
        "descripcion": "Pagos y facturas"
    },
    "SEGURIDAD": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_SEGURIDAD'),
        "nombre": "🔒 Seguridad",
        "descripcion": "Alertas de seguridad"
    },
    "MANTENIMIENTO": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_MANTENIMIENTO'),
        "nombre": "🔧 Mantenimiento",
        "descripcion": "Tareas de mantenimiento"
    },
    "FORMACION": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_FORMACION'),
        "nombre": "📚 Formación",
        "descripcion": "Newsletters y formación"
    },
    "GENERAL": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID'),
        "nombre": "📧 General",
        "descripcion": "Correos sin clasificar"
    },
    "SPAM": {
        "chat_id": os.getenv('TELEGRAM_CHAT_ID_SPAM'),
        "nombre": "🗑️ Spam",
        "descripcion": "Correo no deseado"
    }
}

def get_chat_id_for_category(categoria, prioridad=None):
    """ Obtiene el chat_id apropiado según la categoría y prioridad """
    # Si es urgente, siempre va al grupo crítico
    if prioridad == "URGENTE" and categoria != "SPAM":
        return GRUPOS_TELEGRAM["CLIENTE_CRITICO"]["chat_id"]
    
    # Si existe grupo específico para la categoría
    if categoria in GRUPOS_TELEGRAM and GRUPOS_TELEGRAM[categoria]["chat_id"]:
        return GRUPOS_TELEGRAM[categoria]["chat_id"]
    
    # Por defecto, grupo general
    return GRUPOS_TELEGRAM["GENERAL"]["chat_id"]

def get_grupo_info(categoria):
    """ Obtiene información completa del grupo """
    return GRUPOS_TELEGRAM.get(categoria, GRUPOS_TELEGRAM["GENERAL"])
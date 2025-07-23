from config import CATEGORIAS_INFORMATICO, TIPOS_PRIORIDAD
from utils.classifier import clasificar_correo_completo
from core.email_reader import conectar_imap, obtener_correos_no_leidos, extraer_contenido
from telegram_bot.sender import enviar_mensaje
import schedule
import time
from datetime import datetime
import re
from html import unescape
import html2text
from core.ai_processor import configurar_openai, resumir_correo

TIEMPO_REVISION = 15  # Tiempo en minutos entre revisiones

configurar_openai()  # Configurar OpenAI al inicio

def limpiar_texto_telegram(texto):
    """Limpia el texto para evitar errores en Telegram"""
    if not texto:
        return ""
    
    # Convertir de string si es necesario
    texto = str(texto)
    
    # Si es HTML, convertir a texto plano
    if '<html' in texto.lower() or '<!doctype' in texto.lower():
        # Usar html2text para convertir HTML a markdown/texto plano
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0  # No quebrar líneas
        texto = h.handle(texto)
    
    # Decodificar entidades HTML
    texto = unescape(texto)
    
    # Reemplazar caracteres de control y caracteres problemáticos
    texto_limpio = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', texto)
    
    # Limpiar múltiples saltos de línea
    texto_limpio = re.sub(r'\n\s*\n\s*\n', '\n\n', texto_limpio)
    
    # Limpiar espacios en blanco excesivos
    texto_limpio = re.sub(r' +', ' ', texto_limpio)
    
    # Limitar la longitud total del mensaje (Telegram tiene límite de 4096 caracteres)
    if len(texto_limpio) > 3000:  # Dejamos margen para el formato
        texto_limpio = texto_limpio[:3000] + "...\n\n[Mensaje truncado por longitud]"
    
    return texto_limpio.strip()

def es_correo_notificacion(autor):
    """Verifica si el correo es una notificación de un servicio"""
    if not autor:
        return False
    return "noreply" in autor.lower() or "no-reply" in autor.lower()

def formatear_mensaje_con_config(autor, asunto, cuerpo):
    """
    Formatea mensaje usando configuraciones centralizadas con IA
    """
    # Clasificar correo con IA
    clasificacion = clasificar_correo_completo(autor, asunto, cuerpo)
    
    # Obtener configuración de categoría y prioridad
    config_categoria = CATEGORIAS_INFORMATICO.get(clasificacion["categoria"], {})
    config_prioridad = TIPOS_PRIORIDAD.get(clasificacion["prioridad"], {})
    
    # Construir mensaje con emojis configurados
    emoji = config_categoria.get("emoji", "📧")
    emoji_prioridad = config_prioridad.get("emoji", "⚪")
    
    mensaje = f"{emoji} {clasificacion['categoria']}\n"
    mensaje += f"{emoji_prioridad} {clasificacion['prioridad']}\n"
    
    # Información del cliente si se identifica
    if clasificacion.get('cliente', 'No identificado') != 'No identificado':
        mensaje += f"👤 Cliente: {clasificacion['cliente']}\n"
    
    # Proyecto relacionado si existe
    if clasificacion.get('proyecto_relacionado'):
        mensaje += f"🌐 Proyecto: {clasificacion['proyecto_relacionado']}\n"
        
    # Tiempo de respuesta sugerido
    mensaje += f"⏱️ Responder en: {clasificacion.get('tiempo_estimado_respuesta', 'No especificado')}\n"
    
    # Tipo de problema
    mensaje += f"🎯 Problema: {clasificacion.get('tipo_problema', 'otro')}\n"
    
    # Gravedad del problema
    mensaje += f"📊 Gravedad: {clasificacion.get('gravedad', 5)}/10\n"
    
    # Acción inmediata si es necesaria
    if clasificacion.get('requiere_accion_inmediata', False):
        mensaje += f"⚡ ACCIÓN INMEDIATA REQUERIDA\n"
    
    # Resumen técnico
    if clasificacion.get('resumen_tecnico'):
        mensaje += f"\n💡 {clasificacion['resumen_tecnico']}\n"
    
    # Información básica del correo
    mensaje += f"\n👤 De: {limpiar_texto_telegram(autor)}\n"
    mensaje += f"📬 Asunto: {limpiar_texto_telegram(asunto)}\n\n"
    mensaje += f"📄 Contenido:\n{limpiar_texto_telegram(cuerpo)}"
    
    # Verificación final de longitud
    mensaje_final = limpiar_texto_telegram(mensaje)
    
    return mensaje_final, clasificacion

def formatear_mensaje_correo(autor, asunto, cuerpo, es_notificacion=False):
    """Formatea el mensaje del correo para Telegram (método simple)"""
    # Limpiar todos los campos
    if es_notificacion:
        mensaje = f"🔔 NOTIFICACIÓN \n\n"
    else:
        mensaje = f"📧 NUEVO CORREO\n\n"
    mensaje += f"👤 De: {limpiar_texto_telegram(autor)}\n"
    mensaje += f"📬 Asunto: {limpiar_texto_telegram(asunto)}\n\n"
    mensaje += f"📄 Contenido:\n{limpiar_texto_telegram(cuerpo)}"
    
    # Verificación final de longitud
    mensaje_final = limpiar_texto_telegram(mensaje)
    
    return mensaje_final

def revisar_correos():
    """Función que revisa los correos y los envía a Telegram"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"🕐 {timestamp} - Revisando correos nuevos...")
    
    try:
        # Conectar al servidor IMAP
        mail = conectar_imap()
        
        # Obtener correos no leídos
        correos = obtener_correos_no_leidos(mail)
        
        if not correos:
            print("📭 No se encontraron correos nuevos.")
        else:
            print(f"📬 Procesando {len(correos)} correos nuevos...")
            
            for uid in correos:
                try:
                    autor, asunto, cuerpo = extraer_contenido(mail, uid)
                    
                    # Limpiar texto para evitar errores en Telegram
                    cuerpo_limpio = limpiar_texto_telegram(cuerpo)

                    # Verificar si es notificación simple
                    es_notificacion = es_correo_notificacion(autor)
                    
                    if es_notificacion:
                        # Para notificaciones, usar método simple
                        mensaje_telegram = formatear_mensaje_correo(autor, asunto, cuerpo_limpio, es_notificacion=True)
                        enviar_mensaje(mensaje_telegram, es_notificacion=True)
                        print(f"✅ Notificación enviada a Telegram: {asunto}")
                    else:
                        # Para correos normales, usar clasificación IA
                        mensaje_telegram, clasificacion = formatear_mensaje_con_config(autor, asunto, cuerpo_limpio)
                        
                        # Enviar usando el chat_id específico de la clasificación
                        chat_id = clasificacion.get('chat_id')
                        enviar_mensaje(mensaje_telegram, chat_id_override=chat_id)
                        
                        print(f"✅ Correo {clasificacion['categoria']} ({clasificacion['prioridad']}) enviado: {asunto}")
                    
                except Exception as e:
                    print(f"❌ Error procesando correo {uid}: {e}")
            
            print("✅ Correos marcados como leídos")
        
        # Cerrar conexión
        mail.logout()
        print(f"✅ Revisión completada a las {timestamp}")
        
    except Exception as e:
        print(f"❌ Error durante la revisión: {e}")
        try:
            enviar_mensaje(f"❌ Error en el asistente de correos: {e}")
        except:
            print("❌ No se pudo enviar notificación de error a Telegram")

def main():
    """Función principal que configura el monitoreo continuo"""
    print(f"🚀 Iniciando monitoreo de correos cada {TIEMPO_REVISION} minutos...")
    print("💡 Presiona Ctrl+C para detener el programa")
    print("🤖 Clasificación inteligente con IA activada")
    
    # Programar la revisión cada X minutos
    schedule.every(TIEMPO_REVISION).minutes.do(revisar_correos)
    
    # Ejecutar una revisión inicial
    print("🔄 Ejecutando revisión inicial...")
    revisar_correos()
    print(f"⏰ Próxima revisión programada en {TIEMPO_REVISION} minutos...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Esperar 1 segundo antes de verificar de nuevo
            
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo el monitoreo de correos...")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        try:
            enviar_mensaje(f"🚨 El bot se ha detenido por un error crítico: {e}")
        except:
            print("❌ No se pudo enviar notificación de error crítico")

if __name__ == "__main__":
    main()
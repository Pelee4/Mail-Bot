from core.email_reader import conectar_imap, obtener_correos_no_leidos, extraer_contenido
from telegram_bot.sender import enviar_mensaje
import schedule
import time
from datetime import datetime

TIEMPO_REVISION = 15  # Tiempo en minutos entre revisiones

def formatear_mensaje_correo(autor, asunto, cuerpo):
    """Formatea el mensaje del correo para Telegram"""
    mensaje = f"📧 **NUEVO CORREO**\n\n"
    mensaje += f"👤 **De:** {autor}\n"
    mensaje += f"📬 **Asunto:** {asunto}\n\n"
    mensaje += f"📄 **Contenido:**\n{cuerpo[:1000]}"  # Limitamos a 1000 caracteres
    
    if len(cuerpo) > 1000:
        mensaje += "...\n\n*[Mensaje truncado]*"
    
    return mensaje

def revisar_correos():
    """Función que revisa los correos y los envía a Telegram"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"🕐 {timestamp} - Revisando correos nuevos...")
    
    try:
        # Conectar al servidor IMAP
        mail = conectar_imap()
        
        # Obtener correos destacados
        correos = obtener_correos_no_leidos(mail)
        
        if not correos:
            print("📭 No se encontraron correos nuevos.")
        else:
            print(f"📬 Procesando {len(correos)} correos nuevos...")
            
            for uid in correos:
                try:
                    autor, asunto, cuerpo = extraer_contenido(mail, uid)
                    
                    # Formatear y enviar a Telegram
                    mensaje_telegram = formatear_mensaje_correo(autor, asunto, cuerpo)
                    enviar_mensaje(mensaje_telegram)
                    print(f"✅ Correo enviado a Telegram: {asunto}")
                    
                except Exception as e:
                    print(f"❌ Error procesando correo {uid}: {e}")
            
            print ("✅ Correos marcados como leídos")
        
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
    
    # Programar la revisión cada 15 minutos
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
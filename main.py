from core.email_reader import conectar_imap, obtener_correos_no_leidos, extraer_contenido
from telegram_bot.sender import enviar_mensaje

def formatear_mensaje_correo(asunto, cuerpo):
    """Formatea el mensaje del correo para Telegram"""
    mensaje = f"📧 **NUEVO CORREO DESTACADO**\n\n"
    mensaje += f"📬 **Asunto:** {asunto}\n\n"
    mensaje += f"📄 **Contenido:**\n{cuerpo[:1000]}"  # Limitamos a 1000 caracteres
    
    if len(cuerpo) > 1000:
        mensaje += "...\n\n*[Mensaje truncado]*"
    
    return mensaje

if __name__ == "__main__":
    print("🚀 Iniciando asistente de correos con Telegram...")
    
    try:
        # Conectar al servidor IMAP
        mail = conectar_imap()
        
        # Obtener correos destacados
        correos = obtener_correos_no_leidos(mail)
        
        if not correos:
            print("📭 No se encontraron correos destacados.")
            enviar_mensaje("📭 No hay correos destacados nuevos.")
        else:
            print(f"📬 Procesando {len(correos)} correos destacados...")
            
            for uid in correos:
                try:
                    asunto, cuerpo = extraer_contenido(mail, uid)
                    
                    # Mostrar en consola
                    print("====================================")
                    print("📬 Asunto:", asunto)
                    print("📄 Cuerpo:", cuerpo[:500], "...")
                    print("====================================")
                    
                    # Formatear y enviar a Telegram
                    mensaje_telegram = formatear_mensaje_correo(asunto, cuerpo)
                    enviar_mensaje(mensaje_telegram)
                    print(f"✅ Correo enviado a Telegram: {asunto}")
                    
                except Exception as e:
                    print(f"❌ Error procesando correo {uid}: {e}")
                    
        # Cerrar conexión
        mail.logout()
        print("🔚 Proceso completado.")
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        enviar_mensaje(f"❌ Error en el asistente de correos: {e}")
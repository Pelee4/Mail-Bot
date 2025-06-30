from core.email_reader import conectar_imap, obtener_correos_no_leidos, extraer_contenido

if __name__ == "__main__":
    mail = conectar_imap()
    correos = obtener_correos_no_leidos(mail)

    for uid in correos:
        asunto, cuerpo = extraer_contenido(mail, uid)
        print("====================================")
        print("📬 Asunto:", asunto)
        print("📄 Cuerpo:", cuerpo[:500], "...")  # Solo mostramos los primeros 500 caracteres
        print("====================================")

    mail.logout()  # Cerrar la conexión al servidor IMAP
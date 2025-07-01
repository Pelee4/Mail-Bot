import imaplib
import email
from email.header import decode_header
from config import settings

# Función para conectarse al servidor IMAP
def conectar_imap():
    print ("Conectando al servidor IMAP para leer correos...")
    mail = imaplib.IMAP4_SSL(settings.IMAP_SERVER, settings.IMAP_PORT) # Conexión segura al servidor IMAP
    mail.login(settings.EMAIL_ACCOUNT, settings.EMAIL_PASSWORD) # Autenticación con el servidor IMAP
    return mail

# Función para obtener los correos no leídos
def obtener_correos_no_leidos(mail):
    print("Buscando correos no leídos...")
    # Seleccionar la bandeja de entrada (INBOX) en lugar de carpeta de destacados
    mail.select('INBOX') # esto lee la bandeja de entrada
    _, mensajes = mail.search(None, '(FLAGGED)') # Las posibles banderas son: UNSEEN, SEEN, FLAGGED, UNFLAGGED, DELETED, UNDELETED
    # Estoy eligiendo los correos destacados porque no leídos tengo muchos
    ids = mensajes[0].split()
    print(f"Encontrados {len(ids)} correos no leídos.")
    return ids

# Función para extraer el contenido de un correo
def extraer_contenido(mail, uid):
    print(f"Extrayendo contenido del correo con UID: {uid}")
    _, datos = mail.fetch(uid, '(RFC822)') #RFC822 es el formato completo del mensaje
    mensaje = email.message_from_bytes(datos[0][1]) #Esto saca el contenido del mensaje
    
    asunto, _ = decode_header(mensaje['Subject'])[0]
    if isinstance(asunto, bytes):
        asunto = asunto.decode(encoding= 'utf-8', errors='ignore') # Decodifica el asunto del mensaje

    cuerpo = ""
    if mensaje.is_multipart():
        for parte in mensaje.walk(): # Itera sobre las partes del mensaje
            tipo = parte.get_content_type()
            if tipo == "text/plain":
                cuerpo = parte.get_payload(decode=True).decode(errors='ignore') # Decodifica el cuerpo del mensaje
                break
    else:
        cuerpo = mensaje.get_payload(decode=True).decode(errors='ignore')
    return asunto, cuerpo
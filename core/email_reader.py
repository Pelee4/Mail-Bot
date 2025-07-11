import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# Función para conectarse al servidor IMAP
def conectar_imap():
    print ("Conectando al servidor IMAP para leer correos...")
    load_dotenv()  # Cargar las variables de entorno desde el archivo .env
    mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"), os.getenv("IMAP_PORT")) # Conexión segura al servidor IMAP
    mail.login(os.getenv("EMAIL_ACCOUNT"), os.getenv("EMAIL_PASSWORD")) # Autenticación con el servidor IMAP
    return mail

# Función para obtener los correos no leídos de hace 5 minutos
def obtener_correos_no_leidos(mail):
    print("Buscando correos no leídos...")
    mail.select('INBOX') # esto lee la bandeja de entrada
    
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
    _, mensajes = mail.search(None, f'(UNSEEN SINCE "{fecha_ayer}")') # Las posibles banderas son: UNSEEN, SEEN, FLAGGED, UNFLAGGED, DELETED, UNDELETED
    ids = mensajes[0].split()
    print(f"Encontrados {len(ids)} correos no leídos.")
    for uid in ids:
        mail.store(uid, '+FLAGS', '\\seen') #Los marca como leídos
    return ids

# Función para extraer el contenido de un correo
def extraer_contenido(mail, uid):
    print(f"Extrayendo contenido del correo con UID: {uid}")
    _, datos = mail.fetch(uid, '(RFC822)') #RFC822 es el formato completo del mensaje
    mensaje = email.message_from_bytes(datos[0][1]) #Esto saca el contenido del mensaje

    autor, _ = decode_header(mensaje['From'])[0]
    if isinstance(autor, bytes):
        autor = autor.decode(encoding= 'utf-8', errors='ignore') # Decodifica el autor del mensaje
    
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
    return autor, asunto, cuerpo
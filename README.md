# 📧 Mail Bot - Asistente de Correos con Telegram

Un bot automatizado que monitorea tu correo electrónico y envía notificaciones a Telegram, diferenciando entre correos normales y notificaciones de servicios.

## ✨ Características

- 📬 Monitoreo automático de correos no leídos vía IMAP
- 🔔 Diferenciación automática entre correos normales y notificaciones (noreply)
- 📱 Envío a diferentes grupos de Telegram según el tipo de correo
- 🧹 Limpieza automática de contenido HTML para mejor legibilidad
- ⏰ Revisión programada cada 15 minutos (configurable)
- 🤖 Integración con OpenAI para futuros resúmenes inteligentes

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/Mail-Bot.git
cd Mail-Bot
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:

```env
# Configuración del correo IMAP
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
EMAIL_ACCOUNT=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_aplicacion

# Configuración de Telegram
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_correos_normales
TELEGRAM_CHAT_ID_NOTIFICATIONS=tu_chat_id_notificaciones

# Configuración de OpenAI (opcional)
OPENAI_API_KEY=tu_api_key_openai
OPENAI_MODEL=gpt-4o-mini
```

### 4. Configurar Gmail (si usas Gmail)
1. Activar la verificación en 2 pasos
2. Generar una contraseña de aplicación específica
3. Usar esa contraseña en `EMAIL_PASSWORD`

### 5. Configurar Bot de Telegram
1. Crear un bot con @BotFather en Telegram
2. Obtener el token del bot
3. Añadir el bot a tus grupos de Telegram
4. Usar `telegram_bot/get_chat_id.py` para obtener los chat_ids:

```bash
python telegram_bot/get_chat_id.py
```

## 🔧 Uso

### Ejecutar el bot
```bash
python main.py
```

### Obtener chat_ids de Telegram
```bash
python telegram_bot/get_chat_id.py
```

## 📁 Estructura del proyecto

```
Mail-Bot/
├── main.py                    # Archivo principal
├── requirements.txt           # Dependencias
├── .env                      # Variables de entorno
├── README.md                 # Este archivo
├── core/
│   ├── email_reader.py       # Lector de correos IMAP
│   └── ai_processor.py       # Procesador de IA (OpenAI)
└── telegram_bot/
    ├── sender.py             # Enviador de mensajes
    └── get_chat_id.py        # Utilidad para obtener chat_ids
```

## 🎯 Funcionalidades

### Tipos de Correo
- **📧 Correos Normales**: Enviados al grupo principal de Telegram
- **🔔 Notificaciones**: Correos de "noreply" enviados a un grupo separado

### Limpieza de Contenido
- Conversión automática de HTML a texto plano
- Eliminación de caracteres de control
- Truncamiento automático para evitar límites de Telegram
- Decodificación de entidades HTML

### Programación
- Revisión automática cada 15 minutos (configurable en `TIEMPO_REVISION`)
- Manejo de errores con notificaciones a Telegram
- Reconexión automática en caso de fallos

## ⚙️ Configuración Avanzada

### Cambiar frecuencia de revisión
Modificar la variable `TIEMPO_REVISION` en `main.py`:
```python
TIEMPO_REVISION = 30  # Revisar cada 30 minutos
```

### Personalizar detección de notificaciones
Modificar la función `es_correo_notificacion()` en `main.py`:
```python
def es_correo_notificacion(autor):
    if not autor:
        return False
    return "noreply" in autor.lower() or "newsletter" in autor.lower()
```

## 🛠️ Dependencias

- `imaplib` - Conexión IMAP (built-in Python)
- `email` - Procesamiento de emails (built-in Python)
- `requests` - Peticiones HTTP para Telegram API
- `python-dotenv` - Manejo de variables de entorno
- `schedule` - Programación de tareas
- `html2text` - Conversión de HTML a texto
- `openai` - Integración con OpenAI (opcional)

## 🔍 Troubleshooting

### Error 400 en Telegram
- Verificar que los chat_ids sean correctos
- Comprobar que el bot tenga permisos en los grupos

### Error de conexión IMAP
- Verificar credenciales en `.env`
- Para Gmail, usar contraseña de aplicación, no la contraseña normal

### Bot no detecta correos
- Verificar que el correo tenga correos no leídos
- Comprobar la conexión a internet

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:
- Abre un issue en GitHub
- Revisa la sección de troubleshooting
- Verifica que todas las dependencias estén instaladas correctamente

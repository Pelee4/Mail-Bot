# Mail-Bot

Bot automático que monitorea correos electrónicos no leídos cada 15 minutos y los envía a un chat de Telegram con información detallada del remitente, asunto y contenido.

## 📋 Descripción

Mail-Bot es una aplicación que:
- Se conecta a tu cuenta de correo electrónico vía IMAP
- Monitorea automáticamente cada 15 minutos los correos no leídos
- Extrae información del remitente, asunto y contenido del correo
- Envía notificaciones detalladas a un chat de Telegram
- Marca automáticamente los correos como leídos después de procesarlos
- Maneja correctamente el cambio de día para no perder correos

## 🚀 Instalación desde GitHub

### Requisitos previos
- Python 3.7 o superior
- Una cuenta de correo electrónico con acceso IMAP
- Un bot de Telegram configurado

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Mail-Bot.git
   cd Mail-Bot
   ```

2. **Instalar las dependencias**
   ```bash
   pip install -r requirements.txt
   ```
   Esto instalará:
   - `requests`: Para las llamadas a la API de Telegram
   - `python-dotenv`: Para cargar variables de entorno desde el archivo .env
   - `schedule`: Para el monitoreo automático cada 15 minutos

3. **Configurar las variables de entorno**
   - Crear un archivo `.env` en la raíz del proyecto (mismo nivel que main.py)
   - Configurar las siguientes variables:
   ```env
   # Configuración del correo electrónico
   IMAP_SERVER=imap.gmail.com
   IMAP_PORT=993
   EMAIL_ACCOUNT=tu-email@gmail.com
   EMAIL_PASSWORD=tu-contraseña-de-aplicacion
   
   # Configuración de Telegram
   TELEGRAM_TOKEN=tu-token-del-bot
   TELEGRAM_CHAT_ID=tu-chat-id
   ```
   
   **Importante:** 
   - El archivo `.env` no debe subirse a GitHub (está en .gitignore)
   - Para Gmail, usa contraseñas de aplicación específicas, no tu contraseña personal
   - El `TELEGRAM_TOKEN` se obtiene de @BotFather en Telegram
   - El `TELEGRAM_CHAT_ID` se puede obtener ejecutando el script incluido

4. **Ejecutar el proyecto**
   ```bash
   python main.py
   ```
   
   El bot iniciará el monitoreo automático y:
   - Ejecutará una revisión inicial inmediatamente
   - Continuará revisando cada 15 minutos automáticamente
   - Mostrará timestamps de cada revisión
   - Se puede detener con Ctrl+C

## ⚙️ Configuración

### Configuración del intervalo de monitoreo
Por defecto, el bot revisa correos cada 15 minutos. Para cambiar este intervalo, modifica la variable `TIEMPO_REVISION` en `main.py`:
```python
TIEMPO_REVISION = 15  # Cambiar por el número de minutos deseado
```

### Obtener el Chat ID de Telegram
Puedes usar el script incluido para obtener tu chat ID:
```bash
python telegram_bot/get_chat_id.py
```

### Configuración del correo
- Asegúrate de habilitar el acceso IMAP en tu cuenta de correo
- Para Gmail, es recomendable usar contraseñas de aplicación específicas

## 📁 Estructura del proyecto

```
Mail-Bot/
├── main.py                 # Archivo principal
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── config/                # Configuración
│   ├── __init__.py
│   └── settings.py
├── core/                  # Lógica principal
│   ├── __init__.py
│   ├── ai_processor.py    # Procesamiento con IA
│   └── email_reader.py    # Lectura de correos
├── telegram_bot/          # Bot de Telegram
│   ├── __init__.py
│   ├── get_chat_id.py    # Obtener ID del chat
│   └── sender.py         # Envío de mensajes
└── utils/                # Utilidades
    ├── __init__.py
    └── helpers.py
```

## 🔧 Solución de problemas

### Error: "ModuleNotFoundError: No module named 'requests'", "No module named 'dotenv'" o "No module named 'schedule'"
Ejecuta: `pip install -r requirements.txt`

### El bot no encuentra correos nuevos
- Verifica que tengas correos no leídos en tu bandeja de entrada
- El bot busca correos desde ayer para evitar problemas con el cambio de día
- Los correos se marcan como leídos automáticamente después de procesarlos

### El bot se detiene o no continúa el monitoreo
- Verifica la conexión a internet
- Comprueba las credenciales del correo
- Revisa que el token de Telegram sea válido
- El bot se puede detener limpiamente con Ctrl+C

### Error: Variables de entorno no encontradas
- Asegúrate de que el archivo `.env` esté en la raíz del proyecto
- Verifica que las variables estén escritas correctamente (sin espacios extra)
- El archivo `.env` debe estar al mismo nivel que `main.py`

### Error de conexión IMAP
- Verifica las credenciales del correo en el archivo `.env`
- Asegúrate de que IMAP esté habilitado en tu cuenta
- Para Gmail: usa el servidor `imap.gmail.com` y puerto `993`
- Verifica que uses una contraseña de aplicación, no tu contraseña personal

### Error del bot de Telegram
- Verifica que el `TELEGRAM_TOKEN` en `.env` sea correcto
- Asegúrate de que el `TELEGRAM_CHAT_ID` sea válido
- Comprueba que el bot tenga permisos para enviar mensajes al chat

## 📝 Uso

Una vez configurado, simplemente ejecuta:
```bash
python main.py
```

### Funcionamiento del monitoreo automático:

1. **Revisión inicial**: El bot ejecuta una revisión inmediata al iniciar
2. **Monitoreo continuo**: Cada 15 minutos revisa automáticamente los correos
3. **Procesamiento**: Para cada correo no leído encontrado:
   - Extrae el remitente, asunto y contenido
   - Envía la información a Telegram con formato estructurado
   - Marca el correo como leído para evitar duplicados
4. **Logging**: Muestra timestamps y estado de cada operación
5. **Manejo de errores**: Continúa funcionando aunque haya errores puntuales

### Detener el bot:
Presiona `Ctrl+C` para detener el monitoreo de forma segura.

## 🔒 Seguridad

- **Nunca subas el archivo `.env` a GitHub** - contiene información sensible
- Usa contraseñas de aplicación específicas, no tu contraseña personal del correo
- Asegúrate de que tu archivo `.gitignore` incluya `.env`
- Mantén actualizado tu token de bot de Telegram
- El bot marca automáticamente los correos como leídos para evitar reprocesamiento

## ⏰ Características del monitoreo

- **Intervalo configurable**: Por defecto cada 15 minutos (modificable en `main.py`)
- **Búsqueda inteligente**: Busca correos desde ayer para evitar pérdidas en cambio de día
- **Gestión automática**: Marca correos como leídos después de procesarlos
- **Ejecución continua**: Funciona 24/7 hasta que se detenga manualmente
- **Manejo de errores**: Continúa funcionando aunque haya fallos puntuales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría realizar.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

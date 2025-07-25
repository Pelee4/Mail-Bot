# 📧 Mail Bot - Asistente de Correos con Telegram

Un bot automatizado que monitorea tu correo electrónico y envía notificaciones a Telegram con clasificación inteligente usando IA.

## ✨ Características

- 📬 Monitoreo automático de correos no leídos vía IMAP
- 🤖 **Clasificación inteligente con OpenAI** (crítico, comercial, hosting, etc.)
- 📱 Envío a diferentes grupos de Telegram según tipo y prioridad
- 🔧 **Sistema de filtros configurables** por archivo
- 🧹 Limpieza automática de contenido HTML para mejor legibilidad
- ⏰ Revisión programada cada 15 minutos (configurable)
- 🎯 **Optimizado para informáticos autónomos**

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

# Configuración de Telegram - Clasificación Inteligente
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui
TELEGRAM_CHAT_ID=-1001111111111                    # General
TELEGRAM_CHAT_ID_CRITICO=-1002222222222            # Urgentes
TELEGRAM_CHAT_ID_COMERCIAL=-1003333333333          # Comercial
TELEGRAM_CHAT_ID_HOSTING=-1004444444444            # Hosting/Dominios
TELEGRAM_CHAT_ID_FACTURACION=-1005555555555        # Facturas
TELEGRAM_CHAT_ID_SEGURIDAD=-1006666666666          # Seguridad

# Configuración de OpenAI
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

### 6. **Personalizar filtros**
Editar archivos en `config/`:
- `categories.py` - Categorías y prioridades
- `filters.py` - Filtros automáticos y clientes VIP
- `telegram_groups.py` - Configuración de grupos

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
├── config/                    # ⭐ Configuraciones
│   ├── __init__.py
│   ├── categories.py          # Categorías de correos
│   ├── filters.py             # Filtros y reglas automáticas
│   ├── telegram_groups.py     # Grupos de Telegram
│   └── prompts.py             # Prompts para IA
├── utils/
│   ├── __init__.py
│   └── classifier.py          # Lógica de clasificación
├── core/
│   ├── email_reader.py        # Lector de correos IMAP
│   └── ai_processor.py        # Procesador de IA (OpenAI)
└── telegram_bot/
    ├── sender.py              # Enviador de mensajes
    └── get_chat_id.py         # Utilidad para obtener chat_ids
```

## 🎯 Tipos de Clasificación

### Categorías Automáticas
- **🚨 CLIENTE_CRITICO**: Webs caídas, errores graves → Grupo urgente
- **💰 COMERCIAL**: Presupuestos, nuevos clientes → Grupo comercial
- **📊 HOSTING_DOMINIOS**: Renovaciones, DNS → Grupo hosting
- **💳 FACTURACION**: Pagos, facturas → Grupo facturación
- **🔒 SEGURIDAD**: Alertas, ataques → Grupo seguridad
- **🔧 MANTENIMIENTO**: Actualizaciones rutinarias
- **📚 FORMACION**: Newsletters, cursos

### Filtros Inteligentes
- **Clientes VIP**: Siempre prioritarios
- **Palabras críticas**: "error 500", "site down" → Urgente
- **Proveedores conocidos**: Hosting, dominios → Clasificación automática
- **Spam detection**: Filtrado automático

## ⚙️ Configuración Avanzada

### Cambiar frecuencia de revisión
Modificar la variable `TIEMPO_REVISION` en `main.py`:
```python
TIEMPO_REVISION = 30  # Revisar cada 30 minutos
```

### Añadir clientes VIP
Editar `config/filters.py`:
```python
"clientes_vip": [
    "cliente@importante.com",
    "admin@empresa-vip.com"
]
```

### Configurar nuevas reglas automáticas
```python
REGLAS_AUTOMATICAS = {
    "mi_regla": {
        "condiciones": ["palabra_clave"],
        "accion": {"categoria": "COMERCIAL", "prioridad": "URGENTE"}
    }
}
```

## 📝 Ejemplo de Mensaje Clasificado

```
🚨 CLIENTE_CRITICO
🔴 URGENTE

👤 Cliente: Hotel Mar Azul
🌐 Proyecto: hotelmarazul.com
⏱️ Responder en: inmediato
🎯 Problema: caida_web
📊 Gravedad: 9/10
⚡ ACCIÓN INMEDIATA REQUERIDA

💡 Web del hotel caída con error 500

👤 De: maria.garcia@hotelmarazul.com
📬 Asunto: URGENTE - Nuestra web no funciona

📄 Contenido:
Hola Jorge, nuestra página web no funciona desde hace 2 horas...
```

## 🛠️ Dependencias

- `requests>=2.31.0` - Peticiones HTTP para Telegram API
- `python-dotenv>=1.0.0` - Manejo de variables de entorno
- `schedule>=1.2.0` - Programación de tareas
- `html2text>=2020.1.16` - Conversión de HTML a texto
- `openai>=1.0.0` - Integración con OpenAI
- `python-telegram-bot>=20.0` - Para obtener chat_ids

## 🔍 Troubleshooting

### Error 400 en Telegram
- Verificar que los chat_ids sean correctos
- Comprobar que el bot tenga permisos en los grupos
- Revisar que no hay caracteres HTML problemáticos

### Error de conexión IMAP
- Verificar credenciales en `.env`
- Para Gmail, usar contraseña de aplicación, no la contraseña normal

### Bot no detecta correos
- Verificar que el correo tenga correos no leídos
- Comprobar la conexión a internet

### Clasificación IA no funciona
- Verificar OPENAI_API_KEY en `.env`
- Comprobar que tienes créditos en tu cuenta OpenAI

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

---

🎯 **¡Nunca más pierdas un cliente con un correo importante sin respuesta!**

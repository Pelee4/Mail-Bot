""" Definición de categorías y prioridades para clasificación de correos """

# Categorías específicas para informático autónomo
CATEGORIAS_INFORMATICO = {
    "CLIENTE_CRITICO": {
        "descripcion": "Problemas críticos de clientes (webs caídas, errores graves)",
        "prioridad_base": "URGENTE",
        "emoji": "🚨",
        "keywords": ["down", "caído", "error 500", "no funciona", "urgente", "emergency", "critical"],
        "tiempo_respuesta": "inmediato",
        "gravedad_minima": 8
    },
    "COMERCIAL": {
        "descripcion": "Nuevos clientes, presupuestos, propuestas",
        "prioridad_base": "IMPORTANTE",
        "emoji": "💰",
        "keywords": ["presupuesto", "proyecto", "web", "página", "cotización", "propuesta", "freelance"],
        "tiempo_respuesta": "4h",
        "gravedad_minima": 6
    },
    "MANTENIMIENTO": {
        "descripcion": "Tareas de mantenimiento, actualizaciones, backups",
        "prioridad_base": "NORMAL",
        "emoji": "🔧",
        "keywords": ["actualizar", "backup", "mantenimiento", "ssl", "certificado", "update"],
        "tiempo_respuesta": "24h",
        "gravedad_minima": 4
    },
    "HOSTING_DOMINIOS": {
        "descripcion": "Renovaciones, problemas de hosting, DNS",
        "prioridad_base": "IMPORTANTE",
        "emoji": "📊",
        "keywords": ["hosting", "dominio", "dns", "ssl", "certificado", "renovación", "expiration"],
        "tiempo_respuesta": "24h",
        "gravedad_minima": 5
    },
    "FACTURACION": {
        "descripcion": "Facturas, pagos, contabilidad",
        "prioridad_base": "NORMAL",
        "emoji": "💳",
        "keywords": ["factura", "pago", "transferencia", "recibo", "contabilidad", "invoice"],
        "tiempo_respuesta": "24h",
        "gravedad_minima": 3
    },
    "SEGURIDAD": {
        "descripcion": "Alertas de seguridad, ataques, vulnerabilidades",
        "prioridad_base": "URGENTE",
        "emoji": "🔒",
        "keywords": ["security", "attack", "vulnerability", "malware", "hacked", "breach", "suspicious"],
        "tiempo_respuesta": "inmediato",
        "gravedad_minima": 9
    },
    "FORMACION": {
        "descripcion": "Cursos, actualizaciones tecnológicas, newsletters",
        "prioridad_base": "BAJA",
        "emoji": "📚",
        "keywords": ["course", "tutorial", "webinar", "newsletter", "update", "training"],
        "tiempo_respuesta": "semana",
        "gravedad_minima": 1
    },
    "PERSONAL": {
        "descripcion": "Correos personales no relacionados con trabajo",
        "prioridad_base": "NORMAL",
        "emoji": "👤",
        "keywords": [],
        "tiempo_respuesta": "24h",
        "gravedad_minima": 2
    },
    "SPAM": {
        "descripcion": "Correo no deseado, marketing agresivo",
        "prioridad_base": "BAJA",
        "emoji": "🗑️",
        "keywords": ["unsubscribe", "offer", "discount", "free", "winner"],
        "tiempo_respuesta": "nunca",
        "gravedad_minima": 1
    }
}

# Tipos de prioridad con configuración visual
TIPOS_PRIORIDAD = {
    "URGENTE": {
        "emoji": "🔴",
        "color": "red",
        "notificacion_inmediata": True,
        "orden": 1
    },
    "IMPORTANTE": {
        "emoji": "🟡",
        "color": "yellow", 
        "notificacion_inmediata": False,
        "orden": 2
    },
    "NORMAL": {
        "emoji": "🟢",
        "color": "green",
        "notificacion_inmediata": False,
        "orden": 3
    },
    "BAJA": {
        "emoji": "⚫",
        "color": "gray",
        "notificacion_inmediata": False,
        "orden": 4
    }
}

# Tipos de problemas técnicos
TIPOS_PROBLEMA = {
    "caida_web": "Sitio web no accesible",
    "error_funcional": "Funcionalidad específica con errores",
    "consulta_comercial": "Solicitud de presupuesto o información",
    "mantenimiento": "Tareas de mantenimiento rutinario", 
    "renovacion": "Renovación de servicios (hosting, dominio)",
    "pago": "Asuntos relacionados con pagos",
    "seguridad": "Problemas o alertas de seguridad",
    "formacion": "Contenido educativo o informativo",
    "otro": "No clasificado en categorías anteriores"
}
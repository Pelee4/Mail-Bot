""" Filtros y reglas de clasificación automática """

# Filtros específicos para informático autónomo
FILTROS_INFORMATICO = {
    # Clientes VIP que siempre son prioritarios
    "clientes_vip": [
        "cliente1@empresa.com",
        "maria.garcia@hotelmarazul.com",
        "admin@construcciones-sl.com"
        # Añadir aquí tus clientes más importantes
    ],
    
    # Proveedores de hosting y servicios
    "proveedores_hosting": [
        "@siteground.com",
        "@godaddy.com", 
        "@hostinger.com",
        "@namecheap.com",
        "@cloudflare.com"
        # Añadir aquí tus proveedores de hosting
    ],
    
    # Palabras que indican problemas críticos
    "alertas_criticas": [
        "site down", "website down", "error 500", "error 503",
        "no funciona", "caído", "timeout", "database error",
        "internal server error", "connection refused", "dns error"
    ],
    
    # Keywords comerciales
    "comercial_keywords": [
        "presupuesto", "cotización", "proyecto nuevo",
        "página web", "desarrollo", "freelance", "proposal",
        "quote", "estimate", "budget", "new project"
    ],
    
    # Dominios de clientes conocidos
    "dominios_clientes": [
        "@hotelmarazul.com",
        "@construcciones-sl.com", 
        "@laesquina.es",
        "@modastyle.com",
        "@techstore.es"
        # Añadir dominios de tus clientes
    ],
    
    # Servicios de seguridad conocidos
    "servicios_seguridad": [
        "@wordfence.com",
        "@sucuri.net", 
        "@cloudflare.com",
        "@google.com",  # Google Security alerts
        "security@"
    ]
}

# Filtros para detección de spam
FILTROS_SPAM = {
    "spam_obvio": [
        "seo services", "cheap hosting", "website design offer",
        "increase your ranking", "buy followers", "make money fast",
        "lottery winner", "congratulations you won", "free money",
        "viagra", "casino", "dating site"
    ],
    
    "dominios_spam": [
        "@spam-domain.com",
        "@marketing-mass.com"
        # Añadir dominios conocidos de spam
    ],
    
    "asuntos_spam": [
        "re:", "fwd:", "urgent business proposal",
        "millions of dollars", "act now", "limited time"
    ]
}

# Reglas de auto-clasificación
REGLAS_AUTOMATICAS = {
    "urgente_siempre": {
        "condiciones": [
            "error 500",
            "site down", 
            "website down",
            "emergency",
            "critical"
        ],
        "accion": {
            "categoria": "CLIENTE_CRITICO",
            "prioridad": "URGENTE"
        }
    },
    
    "hosting_renovaciones": {
        "condiciones": [
            "expiration notice",
            "renewal notice", 
            "domain expir",
            "renovación"
        ],
        "accion": {
            "categoria": "HOSTING_DOMINIOS",
            "prioridad": "IMPORTANTE"
        }
    },
    
    "seguridad_alertas": {
        "condiciones": [
            "security alert",
            "suspicious activity",
            "login attempt",
            "brute force"
        ],
        "accion": {
            "categoria": "SEGURIDAD", 
            "prioridad": "URGENTE"
        }
    }
}
""" Lógica para la clasificación de correos electrónicos """

import json
import openai
import os 
from config import(
    CATEGORIAS_INFORMATICO,
    FILTROS_INFORMATICO,
    FILTROS_SPAM,
    REGLAS_AUTOMATICAS,
    PROMPT_CLASIFICACION_INFORMATICO,
    get_chat_id_for_category
)

def aplicar_filtros_previos(autor, asunto, cuerpo):
    """ Aplica filtros automáticos antes de enviar a la IA para el prompt """

    contenido_completo = f"{autor} {asunto} {cuerpo}".lower()

    # Cliente VIP = siempre importante
    if any(vip in autor.lower() for vip in FILTROS_INFORMATICO["clientes_vip"]):
        return {
            "categoria": "CLIENTE_CRITICO",
            "prioridad": "IMPORTANTE",
            "motivo": "Cliente VIP"
        }
    
    # Verificar reglas automáticas
    for regla_nombre, regla in REGLAS_AUTOMATICAS.items():
        if any(condicion in contenido_completo for condicion in regla["condiciones"]):
            return {
                "categoria": regla["accion"]["categoria"],
                "prioridad": regla["accion"]["prioridad"],
                "motivo": f"Regla: {regla_nombre}"
            }
        
    # Spam obvio
    if any(spam in contenido_completo for spam in FILTROS_SPAM["spam_obvio"]):
        return {
            "categoria": "SPAM",
            "prioridad": "BAJA",
            "motivo": "Detectado como spam"
        }

    return None


def clasificar_con_ia(autor, asunto, cuerpo):
    """ Clasifica el correo utilizando OPENAI """

    # Para limitar el tamaño del cuerpo
    cuerpo_truncado = cuerpo[:2000]  if len(cuerpo) > 2000 else cuerpo

    prompt = PROMPT_CLASIFICACION_INFORMATICO.format(
        autor=autor,
        asunto=asunto,
        cuerpo=cuerpo_truncado
    )

    try: 
        client = openai.OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
            messages = [
                {"role": "system", "content": "Eres un experto en clasificación de correos electrónicos. Responde SOLO con JSON válido"},
                {"role": "user", "content": prompt}
            ],
            max_tokens = 300,
            temperature= 0.2
        )

        clasificacion = json.loads(response.choices[0].message.content)
        clasificacion["motivo"] = "Clasificación por IA"
        return clasificacion
    
    except Exception as e:
        print(f" Error al clasificar con IA: {e}")
        return clasificacion_por_defecto()
    

def clasificacion_por_defecto():
    """ Clasificación por defecto en caso de error """
    return {
        "categoria": "PERSONAL",
        "prioridad": "NORMAL",
        "cliente": "No identificado",
        "proyecto_relacionado": "",
        "requiere_accion_inmediata": False,
        "tiempo_estimado_respuesta": "24h",
        "tipo_problema": "otro",
        "gravedad": 5,
        "resumen_tecnico": "Correo sin clasificar",
        "motivo": "Error en clasificación"
    }

def clasificar_correo_completo(autor, asunto, cuerpo):
    """ Función principal de clasificacion de los correos"""

    # 1. Aplicar filtros previos
    filtro_previo = aplicar_filtros_previos(autor, asunto, cuerpo)

    if filtro_previo:
        #Completar información faltante
        clasificacion = clasificacion_por_defecto()
        clasificacion.update(filtro_previo)
        return clasificacion

    # 2. Clasificar con IA
    clasificacion = clasificar_con_ia(autor, asunto, cuerpo)

    # 3. Obtener chat_id apropiado
    clasificacion["chat_id"] = get_chat_id_for_category(
        clasificacion["categoria"],
        clasificacion["prioridad"]
    )

    return clasificacion
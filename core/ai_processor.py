from openai import OpenAI
from dotenv import load_dotenv
import os

def configurar_openai():
    """Configura la API de OpenAI"""
    load_dotenv()
    global client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def resumir_correo(autor, asunto, cuerpo):
    """Envía el correo a OpenAI para resumirlo"""

    prompt = f"""
    Eres un asistente personal que resume correos electrónicos de forma clara y concisa.
    
    Correo recibido:
    - De: {autor}
    - Asunto: {asunto}
    - Contenido: {cuerpo}
    
    Por favor, proporciona un resumen breve y útil de este correo, destacando:
    - Los puntos principales
    - Cualquier acción requerida
    - Fechas importantes mencionadas
    - Nivel de urgencia (si aplica)
    
    Responde de forma natural, como si me estuvieras comentando el correo.
    """

    try:
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7  # Ajusta la temperatura para controlar la creatividad de la respuesta
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ Error al resumir el correo con OpenAI: {e}")
        return f"❌ Error al resumir el correo: {e}"
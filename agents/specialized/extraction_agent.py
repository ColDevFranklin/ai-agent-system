import sys
sys.path.append('../..')

from agents.base_agent import BaseAgent
import json

class ExtractionAgent(BaseAgent):
    """
    Agente especializado en extraer información estructurada
    de consultas de clientes en lenguaje natural.

    Entrada esperada: String con mensaje del cliente
    Salida: JSON con campos estructurados
    """

    def __init__(self):
        # Prompt diseñado específicamente para extracción
        prompt = """
Eres un experto en análisis de texto y extracción de información.

TU ÚNICA TAREA: Extraer información clave de consultas de clientes.

CAMPOS A EXTRAER:
- order_id: ID de orden (formato #XXXXX, solo números)
- problema: tipo de problema (cambio_direccion, reembolso, consulta_general, otro)
- nueva_direccion: dirección completa si se menciona cambio (null si no aplica)
- urgencia: nivel (alta, media, baja) basado en palabras como "urgente", "rápido", "cuando puedan"
- cliente_nombre: nombre del cliente si se menciona (null si no)

REGLAS CRÍTICAS:
1. Responde SOLO con JSON válido, sin texto adicional
2. Si un campo no está en el mensaje, usa null
3. Para order_id, extrae solo números (ej: "#12345" → "12345")
4. Para problema, usa exactamente las categorías definidas

EJEMPLO:
Entrada: "Hola soy María, necesito urgente cambiar dirección de orden #67890 a Calle Nueva 123"
Salida:
{
  "order_id": "67890",
  "problema": "cambio_direccion",
  "nueva_direccion": "Calle Nueva 123",
  "urgencia": "alta",
  "cliente_nombre": "María"
}
"""
        super().__init__("ExtractionAgent", prompt)

    def extract(self, message: str) -> dict:
        """
        Extrae información del mensaje del cliente.

        Args:
            message: Texto del cliente en lenguaje natural

        Returns:
            dict con campos estructurados o {} si falla
        """
        print(f"🔍 Extrayendo información del mensaje...")
        response = self.execute(message)

        try:
            # Intentar parsear JSON
            extracted_data = json.loads(response)
            print(f"✅ Extracción exitosa: {list(extracted_data.keys())}")
            return extracted_data
        except json.JSONDecodeError:
            # Si el LLM no respondió con JSON válido
            print(f"❌ Error: Respuesta no es JSON válido")
            print(f"Respuesta recibida: {response[:200]}...")
            return {}

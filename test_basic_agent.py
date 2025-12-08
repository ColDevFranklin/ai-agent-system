from agents.base_agent import BaseAgent

# Definir prompt del sistema
CUSTOMER_SUPPORT_PROMPT = """
Eres un agente de soporte al cliente experto.

TU TAREA:
1. Identificar la consulta del cliente
2. Extraer información clave (orden ID, problema, urgencia)
3. Clasificar tipo de problema (envío, producto, reembolso)
4. Proponer solución basada en políticas

POLÍTICAS:
- Reembolsos: disponibles 30 días desde compra
- Cambio de dirección: solo si pedido no enviado
- Envío estándar: 5-7 días

FORMATO DE RESPUESTA:
{
  "problema_identificado": "...",
  "categoria": "...",
  "accion_propuesta": "...",
  "prioridad": "alta/media/baja"
}
"""

# Crear agente
support_agent = BaseAgent(
    name="CustomerSupport",
    system_prompt=CUSTOMER_SUPPORT_PROMPT
)

# Probar
query = """
Hola, necesito cambiar la dirección de envío de mi orden #12345.
Originalmente iba a 123 Calle Falsa, pero me mudé a 456 Avenida Real.
Es urgente porque necesito el producto para el lunes.
"""

print("🤖 PROBANDO AGENTE BASE\n")
print("=" * 60)
response = support_agent.execute(query)
print(response)
print("=" * 60)

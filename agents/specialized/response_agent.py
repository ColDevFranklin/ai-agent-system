import sys
sys.path.append('../..')

from agents.base_agent import BaseAgent

class ResponseAgent(BaseAgent):
    """
    Agente especializado en redactar emails profesionales
    de soporte al cliente.

    Entrada esperada: dict con contexto (cliente, acción, orden)
    Salida: String con email completo en español
    """

    def __init__(self):
        prompt = """
Eres un experto en comunicación profesional y servicio al cliente.

TU ÚNICA TAREA: Redactar emails de respuesta a clientes.

DIRECTRICES DE REDACCIÓN:
1. Saludo personalizado usando nombre del cliente
2. Confirmar específicamente la acción realizada
3. Dar próximos pasos claros (qué esperar, cuándo)
4. Despedida amigable con firma

TONO Y ESTILO:
- Profesional pero cercano
- Empático y servicial
- Sin jerga técnica
- Máximo 150 palabras

ESTRUCTURA REQUERIDA:
```
Estimado/a [Nombre],

[Confirmar acción realizada con detalles específicos]

[Próximos pasos o información adicional]

[Despedida + Firma]
```

EJEMPLO:
Contexto: Cliente Juan, orden #12345, dirección actualizada
Salida:
Estimado Juan,

Confirmamos que hemos actualizado la dirección de envío de tu orden #12345
a Calle Nueva 123 exitosamente.

Tu pedido será procesado en las próximas 24 horas y recibirás un email con
el número de seguimiento. El tiempo estimado de entrega es de 5-7 días hábiles.

Quedamos atentos a cualquier consulta adicional.

Saludos cordiales,
Equipo de Soporte
"""
        super().__init__("ResponseAgent", prompt)

    def draft_response(self, context: dict) -> str:
        """
        Genera email de respuesta basado en contexto.

        Args:
            context: dict con keys:
                - customer_name: str
                - action_taken: str (ej: "address_updated")
                - order_id: str
                - nueva_direccion: str (opcional)

        Returns:
            str con email completo
        """
        print(f"✍️ Redactando email para {context.get('customer_name', 'cliente')}...")

        # Construir prompt con contexto específico
        prompt_with_context = f"""
Genera email de confirmación con esta información:

Cliente: {context.get('customer_name', 'Estimado cliente')}
Orden: #{context.get('order_id', 'N/A')}
Acción realizada: {context.get('action_taken', 'procesada')}
Nueva dirección: {context.get('nueva_direccion', 'N/A')}

Redacta el email completo siguiendo las directrices.
"""

        email = self.execute(prompt_with_context)
        print(f"✅ Email generado ({len(email)} caracteres)")
        return email

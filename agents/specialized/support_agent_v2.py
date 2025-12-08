import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from tools.database_tool import DatabaseTool
from tools.email_tool import EmailTool
from typing import Dict
import json

class CustomerSupportAgentV2(BaseAgent):
    """Agente con capacidad de usar herramientas"""

    def __init__(self):
        system_prompt = """
Eres un agente de soporte que puede usar herramientas.

HERRAMIENTAS DISPONIBLES:
1. get_order(order_id): Consulta información de orden
2. update_address(order_id, new_address): Actualiza dirección
3. send_email(to, subject, body): Envía email al cliente

PROCESO:
1. Extraer order_id del mensaje (formato #12345)
2. Usar get_order para verificar estado
3. Evaluar si puede actualizar dirección
4. Ejecutar update_address si aplica
5. Enviar email de confirmación

RESPONDE EN JSON VÁLIDO:
{
  "pensamiento": "análisis de la situación",
  "order_id": "12345",
  "nueva_direccion": "dirección completa extraída",
  "accion": "update_address o consulta_solamente",
  "mensaje_cliente": "respuesta amigable en español"
}
"""
        super().__init__("CustomerSupportV2", system_prompt)
        self.db_tool = DatabaseTool()
        self.email_tool = EmailTool()

    def execute_workflow(self, user_message: str) -> Dict:
        """Ejecuta workflow completo con herramientas"""

        # PASO 1: Analizar mensaje
        print("🔍 PASO 1: Analizando mensaje del cliente...")
        analysis = self.execute(user_message)

        try:
            plan = json.loads(analysis)
        except json.JSONDecodeError:
            return {"error": "No pudo generar plan válido", "raw": analysis}

        print(f"✅ Plan generado: {plan.get('accion')}\n")

        # PASO 2: Consultar orden
        results = []
        order_id = plan.get("order_id")

        if not order_id:
            return {"error": "No se pudo extraer order_id", "plan": plan}

        print(f"🔍 PASO 2: Consultando orden {order_id}...")
        order_info = self.db_tool.get_order(order_id)
        results.append({"tool": "get_order", "result": order_info})

        if not order_info:
            return {"error": f"Orden {order_id} no encontrada"}

        print(f"✅ Orden encontrada para: {order_info['customer']}\n")

        # PASO 3: Actualizar dirección si necesario
        if plan.get("accion") == "update_address" and plan.get("nueva_direccion"):
            print(f"🔧 PASO 3: Actualizando dirección...")
            new_address = plan["nueva_direccion"]
            update_result = self.db_tool.update_address(order_id, new_address)
            results.append({"tool": "update_address", "result": update_result})
            print(f"✅ Resultado: {update_result.get('message', update_result.get('error'))}\n")

            # PASO 4: Enviar confirmación
            if update_result.get("success"):
                print(f"📧 PASO 4: Enviando email de confirmación...")
                email_result = self.email_tool.send_email(
                    to=order_info["email"],
                    subject=f"Confirmación de actualización - Orden #{order_id}",
                    body=plan.get("mensaje_cliente", "Dirección actualizada correctamente")
                )
                results.append({"tool": "send_email", "result": email_result})

        return {
            "plan": plan,
            "execution_results": results,
            "final_message": plan.get("mensaje_cliente")
        }

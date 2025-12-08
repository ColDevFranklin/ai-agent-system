import sys
sys.path.append('..')

from agents.specialized.extraction_agent import ExtractionAgent
from agents.specialized.response_agent import ResponseAgent
from tools.database_tool import DatabaseTool
from tools.email_tool import EmailTool

class MultiAgentOrchestrator:
    """
    Orquestador que coordina workflow de soporte al cliente:

    Pipeline:
    1. ExtractionAgent: Procesa mensaje → JSON estructurado
    2. DatabaseTool: Consulta orden → Info completa
    3. DatabaseTool: Actualiza dirección (si aplica)
    4. ResponseAgent: Genera email profesional
    5. EmailTool: Envía email al cliente

    Ventajas:
    - Logging detallado de cada paso
    - Manejo de errores granular
    - Agentes reemplazables sin romper workflow
    """

    def __init__(self):
        # Inicializar agentes especializados
        self.extractor = ExtractionAgent()
        self.writer = ResponseAgent()

        # Inicializar herramientas
        self.db = DatabaseTool()
        self.email = EmailTool()

        # Estado del workflow
        self.execution_log = []

    def log_step(self, step_name: str, data: dict):
        """
        Registra cada paso para debugging.

        Args:
            step_name: Identificador del paso (ej: "extraction")
            data: Resultado del paso
        """
        self.execution_log.append({
            "step": step_name,
            "data": data
        })

    def execute(self, customer_message: str) -> dict:
        """
        Ejecuta workflow completo de soporte.

        Args:
            customer_message: Mensaje del cliente en texto libre

        Returns:
            dict con:
                - success: bool
                - extracted_info: datos extraídos
                - order_info: info de BD
                - actions_taken: actualizaciones realizadas
                - response_sent: email generado
                - execution_log: pasos ejecutados
        """
        # Resetear log
        self.execution_log = []

        # =============================================================
        # PASO 1: EXTRACCIÓN DE INFORMACIÓN (Agente Especializado)
        # =============================================================
        print("\n" + "="*60)
        print("🔍 PASO 1: EXTRAYENDO INFORMACIÓN")
        print("="*60)

        extracted = self.extractor.extract(customer_message)
        self.log_step("extraction", extracted)

        # Validar extracción
        if not extracted.get("order_id"):
            error_result = {
                "success": False,
                "error": "No se pudo identificar ID de orden en el mensaje",
                "execution_log": self.execution_log
            }
            print("❌ Error: Sin order_id")
            return error_result

        print(f"✅ Extraído order_id: {extracted['order_id']}")
        print(f"   Problema: {extracted.get('problema', 'N/A')}")
        print(f"   Urgencia: {extracted.get('urgencia', 'N/A')}")

        # =============================================================
        # PASO 2: CONSULTAR BASE DE DATOS (Herramienta)
        # =============================================================
        print("\n" + "="*60)
        print(f"🔍 PASO 2: CONSULTANDO ORDEN #{extracted['order_id']}")
        print("="*60)

        order_info = self.db.get_order(extracted["order_id"])
        self.log_step("database_lookup", order_info)

        if not order_info:
            error_result = {
                "success": False,
                "error": f"Orden #{extracted['order_id']} no encontrada en BD",
                "execution_log": self.execution_log
            }
            print(f"❌ Orden no encontrada")
            return error_result

        print(f"✅ Orden encontrada")
        print(f"   Cliente: {order_info['customer']}")
        print(f"   Estado: {order_info['status']}")
        print(f"   Dirección actual: {order_info['address']}")

        # =============================================================
        # PASO 3: ACTUALIZAR DIRECCIÓN (Herramienta - Condicional)
        # =============================================================
        result = {
            "action": "consulta_procesada",  # Default
            "details": {}
        }

        if extracted.get("nueva_direccion"):
            print("\n" + "="*60)
            print("🔧 PASO 3: ACTUALIZANDO DIRECCIÓN")
            print("="*60)
            print(f"   Nueva: {extracted['nueva_direccion']}")

            update_result = self.db.update_address(
                extracted["order_id"],
                extracted["nueva_direccion"]
            )
            self.log_step("address_update", update_result)

            if update_result.get("success"):
                result["action"] = "address_updated"
                result["details"] = update_result
                print(f"✅ {update_result['message']}")
            else:
                result["action"] = "update_failed"
                result["details"] = update_result
                print(f"❌ {update_result['error']}")
        else:
            print("\n" + "="*60)
            print("⏭️ PASO 3: OMITIDO (Sin cambio de dirección solicitado)")
            print("="*60)

        # =============================================================
        # PASO 4: REDACTAR RESPUESTA (Agente Especializado)
        # =============================================================
        print("\n" + "="*60)
        print("✍️ PASO 4: REDACTANDO EMAIL")
        print("="*60)

        # Preparar contexto para agente de redacción
        context = {
            "customer_name": order_info["customer"],
            "action_taken": result["action"],
            "order_id": extracted["order_id"],
            "nueva_direccion": extracted.get("nueva_direccion")
        }

        email_body = self.writer.draft_response(context)
        self.log_step("response_draft", {"body": email_body})

        # =============================================================
        # PASO 5: ENVIAR EMAIL (Herramienta)
        # =============================================================
        print("\n" + "="*60)
        print("📧 PASO 5: ENVIANDO EMAIL")
        print("="*60)

        email_result = self.email.send_email(
            to=order_info["email"],
            subject=f"Actualización orden #{extracted['order_id']}",
            body=email_body
        )
        self.log_step("email_sent", email_result)

        # =============================================================
        # RESULTADO FINAL
        # =============================================================
        return {
            "success": True,
            "extracted_info": extracted,
            "order_info": order_info,
            "actions_taken": result,
            "response_sent": email_body,
            "execution_log": self.execution_log
        }

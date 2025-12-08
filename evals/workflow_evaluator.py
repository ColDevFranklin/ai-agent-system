import sys
sys.path.append('..')

class WorkflowEvaluator:
    """
    Sistema de evaluación para workflows agentic

    Implementa verificaciones:
    - Objetivas: métricas medibles automáticamente
    - Por componente: cada paso del workflow
    - End-to-end: resultado final completo
    """

    def __init__(self):
        # Definir casos de prueba
        self.test_cases = [
            {
                "id": "TC001",
                "nombre": "Cambio de dirección exitoso",
                "descripcion": "Orden en procesamiento, cambio debe funcionar",
                "input": "Cambiar dirección orden #12345 a Calle Nueva 123, Bogotá",
                "expected": {
                    "order_extracted": True,
                    "action": "address_updated",
                    "email_sent": True
                }
            },
            {
                "id": "TC002",
                "nombre": "Orden ya enviada (debe fallar gracefully)",
                "descripcion": "Sistema debe manejar error sin romper workflow",
                "input": "Cambiar dirección orden #67890 a Plaza Central 456",
                "expected": {
                    "order_extracted": True,
                    "action": "update_failed",
                    "error_handled": True
                }
            },
            {
                "id": "TC003",
                "nombre": "Sin ID de orden",
                "descripcion": "Sistema debe fallar gracefully sin ID",
                "input": "Quiero cambiar mi dirección urgente por favor",
                "expected": {
                    "order_extracted": False,
                    "graceful_failure": True
                }
            },
            {
                "id": "TC004",
                "nombre": "Orden con caracteres especiales",
                "descripcion": "Sistema debe manejar direcciones con ñ, tildes, etc",
                "input": "Cambiar dirección orden #12345 a Cañón del Chicamocha 123, Santander",
                "expected": {
                    "order_extracted": True,
                    "action": "address_updated",
                    "email_sent": True,
                    "special_chars_handled": True
                }
            }
        ]

    def evaluate_objective(self, test_case: dict, result: dict) -> dict:
        """
        Evalúa métricas objetivas (medibles automáticamente)

        Args:
            test_case: Caso de prueba con valores esperados
            result: Resultado real del workflow

        Returns:
            Dict con score, porcentaje, y checks detallados
        """
        score = 0
        max_score = len(test_case["expected"])
        checks = {}

        # Evaluar cada expectativa
        for key, expected_value in test_case["expected"].items():

            # VERIFICACIÓN 1: ¿Se extrajo order_id?
            if key == "order_extracted":
                actual = bool(result.get("extracted_info", {}).get("order_id"))

            # VERIFICACIÓN 2: ¿Qué acción se tomó?
            elif key == "action":
                actual = result.get("actions_taken", {}).get("action")

            # VERIFICACIÓN 3: ¿Se envió email?
            elif key == "email_sent":
                actual = result.get("response_sent") is not None

            # VERIFICACIÓN 4: ¿Se manejó error correctamente?
            elif key == "error_handled":
                # Buscar si hubo error pero workflow continuó
                details = result.get("actions_taken", {}).get("details", {})
                actual = details.get("success") == False

            # VERIFICACIÓN 5: ¿Falló gracefully?
            elif key == "graceful_failure":
                # Sistema debe retornar error sin romper
                actual = "error" in result and result.get("success") != True

            else:
                actual = None

            # Registrar resultado de verificación
            checks[key] = {
                "expected": expected_value,
                "actual": actual,
                "pass": actual == expected_value,
                "description": self._get_check_description(key)
            }

            # Sumar punto si pasó
            if checks[key]["pass"]:
                score += 1

        return {
            "test_id": test_case["id"],
            "nombre": test_case["nombre"],
            "descripcion": test_case["descripcion"],
            "score": f"{score}/{max_score}",
            "percentage": (score/max_score)*100 if max_score > 0 else 0,
            "checks": checks,
            "passed": score == max_score
        }

    def _get_check_description(self, check_name: str) -> str:
        """Describe qué verifica cada check"""
        descriptions = {
            "order_extracted": "¿Agente extrajo order_id correctamente?",
            "action": "¿Acción ejecutada fue la correcta?",
            "email_sent": "¿Se generó y envió email?",
            "error_handled": "¿Sistema manejó error sin romper?",
            "graceful_failure": "¿Workflow falló elegantemente?"
        }
        return descriptions.get(check_name, "Verificación desconocida")

    def run_all_tests(self, orchestrator):
        """
        Ejecuta batería completa de tests

        Args:
            orchestrator: Instancia de MultiAgentOrchestrator

        Returns:
            Lista de resultados de evaluación
        """
        results = []

        print("\n" + "=" * 60)
        print("🧪 EJECUTANDO BATERÍA DE TESTS")
        print("=" * 60 + "\n")

        for i, test in enumerate(self.test_cases, 1):
            print(f"Test {i}/{len(self.test_cases)}: {test['id']}")
            print(f"Nombre: {test['nombre']}")
            print(f"Input: {test['input'][:50]}...")
            print("-" * 60)

            # Ejecutar workflow
            try:
                result = orchestrator.execute(test["input"])
            except Exception as e:
                result = {"error": str(e), "success": False}

            # Evaluar resultado
            eval_result = self.evaluate_objective(test, result)
            results.append(eval_result)

            # Mostrar resultado
            status = "✅ PASS" if eval_result["passed"] else "❌ FAIL"
            print(f"\n{status} - Score: {eval_result['score']} ({eval_result['percentage']:.0f}%)")

            # Mostrar checks que fallaron
            if not eval_result["passed"]:
                print("\nChecks fallidos:")
                for check_name, check_data in eval_result['checks'].items():
                    if not check_data['pass']:
                        print(f"  ❌ {check_data['description']}")
                        print(f"     Esperado: {check_data['expected']}, Actual: {check_data['actual']}")

            print("\n")

        return results

    def generate_report(self, results: list) -> dict:
        """
        Genera reporte consolidado de evaluación

        Args:
            results: Lista de resultados de run_all_tests

        Returns:
            Dict con métricas agregadas
        """
        total_tests = len(results)
        passed = sum(1 for r in results if r["passed"])
        failed = total_tests - passed

        # Identificar checks problemáticos
        failed_checks = {}
        for result in results:
            if not result["passed"]:
                for check_name, check_data in result["checks"].items():
                    if not check_data["pass"]:
                        if check_name not in failed_checks:
                            failed_checks[check_name] = 0
                        failed_checks[check_name] += 1

        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed/total_tests)*100 if total_tests > 0 else 0,
            "failed_checks": failed_checks,
            "results": results
        }

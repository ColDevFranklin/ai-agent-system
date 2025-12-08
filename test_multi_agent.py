from workflows.multi_agent_orchestrator import MultiAgentOrchestrator
import json

# Crear orquestador
orchestrator = MultiAgentOrchestrator()

# Caso de prueba end-to-end
customer_query = """
Hola, soy Juan Pérez y necesito urgentemente cambiar la dirección
de mi orden #12345. Me mudé a: 888 Tech Avenue, Silicon Valley.
Por favor confirmen que pueden hacerlo.
"""

print("\n" + "="*60)
print("🤖 EJECUTANDO SISTEMA MULTI-AGENTE COMPLETO")
print("="*60)

# Ejecutar workflow
result = orchestrator.execute(customer_query)

# Mostrar resultado final
print("\n" + "="*60)
print("📊 RESULTADO FINAL DEL WORKFLOW")
print("="*60)
print(json.dumps(result, indent=2, ensure_ascii=False))

# Mostrar log de ejecución
print("\n" + "="*60)
print("📝 LOG DE EJECUCIÓN DETALLADO")
print("="*60)
for i, step in enumerate(result["execution_log"], 1):
    print(f"\n{i}. {step['step'].upper()}")
    print(json.dumps(step['data'], indent=2, ensure_ascii=False))

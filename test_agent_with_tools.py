from agents.specialized.support_agent_v2 import CustomerSupportAgentV2
import json

# Crear agente con tools
agent = CustomerSupportAgentV2()

# Caso de prueba
query = """
Necesito cambiar la dirección de envío de mi orden #12345.
La nueva dirección es: 999 Calle Nueva, Ciudad Tech.
"""

print("\n🎯 EJECUTANDO WORKFLOW CON HERRAMIENTAS\n")
result = agent.execute_workflow(query)

print("\n📊 RESULTADO FINAL:")
print("=" * 60)
print(json.dumps(result, indent=2, ensure_ascii=False))
print("=" * 60)

from agents.specialized.response_agent import ResponseAgent

# Crear agente
writer = ResponseAgent()

# Casos de prueba
test_cases = [
    {
        "nombre": "Actualización exitosa",
        "context": {
            "customer_name": "Juan Pérez",
            "action_taken": "address_updated",
            "order_id": "12345",
            "nueva_direccion": "Calle Nueva 123, Ciudad Tech"
        }
    },
    {
        "nombre": "Actualización fallida",
        "context": {
            "customer_name": "María González",
            "action_taken": "update_failed",
            "order_id": "67890",
            "nueva_direccion": None
        }
    }
]

print("=" * 60)
print("✍️ PROBANDO AGENTE DE REDACCIÓN")
print("=" * 60 + "\n")

for test in test_cases:
    print(f"\n--- {test['nombre']} ---")
    print(f"Contexto: {test['context']}\n")

    email = writer.draft_response(test['context'])

    print("📧 EMAIL GENERADO:")
    print("-" * 60)
    print(email)
    print("-" * 60)

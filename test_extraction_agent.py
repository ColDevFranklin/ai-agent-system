from agents.specialized.extraction_agent import ExtractionAgent
import json

# Crear agente
extractor = ExtractionAgent()

# Casos de prueba
test_cases = [
    {
        "nombre": "Caso completo",
        "input": "Hola soy Juan Pérez, necesito urgente cambiar dirección de orden #12345 a Calle Nueva 123"
    },
    {
        "nombre": "Sin nombre de cliente",
        "input": "Cambiar dirección orden #67890 a Plaza Mayor 456"
    },
    {
        "nombre": "Sin order_id",
        "input": "Tengo un problema con mi pedido, llegó dañado"
    }
]

print("=" * 60)
print("🧪 PROBANDO AGENTE DE EXTRACCIÓN")
print("=" * 60 + "\n")

for test in test_cases:
    print(f"\n--- {test['nombre']} ---")
    print(f"Input: {test['input']}")

    result = extractor.extract(test['input'])

    print(f"\nOutput:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-" * 60)

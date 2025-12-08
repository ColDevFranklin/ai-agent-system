from evals.workflow_evaluator import WorkflowEvaluator
from workflows.multi_agent_orchestrator import MultiAgentOrchestrator
import json

def print_section(title):
    """Helper para imprimir secciones visuales"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

def main():
    # Crear evaluador y orquestador
    print("🔧 Inicializando sistema de evaluación...")
    evaluator = WorkflowEvaluator()
    orchestrator = MultiAgentOrchestrator()

    # Ejecutar tests
    results = evaluator.run_all_tests(orchestrator)

    # Generar reporte
    report = evaluator.generate_report(results)

    # SECCIÓN 1: Resumen ejecutivo
    print_section("📈 RESUMEN EJECUTIVO")
    print(f"\nTests totales:    {report['total_tests']}")
    print(f"Tests exitosos:   {report['passed']} ✅")
    print(f"Tests fallidos:   {report['failed']} ❌")
    print(f"Tasa de éxito:    {report['pass_rate']:.1f}%")

    # SECCIÓN 2: Checks problemáticos
    if report['failed_checks']:
        print_section("⚠️ COMPONENTES CON PROBLEMAS")
        print("\nVerificaciones que fallaron más frecuentemente:\n")
        for check_name, count in sorted(report['failed_checks'].items(),
                                       key=lambda x: x[1],
                                       reverse=True):
            print(f"  • {check_name}: {count} fallas")

    # SECCIÓN 3: Detalle por test
    print_section("🔍 DETALLE POR TEST")

    for r in report['results']:
        status_icon = "✅" if r['passed'] else "❌"
        print(f"\n{status_icon} {r['test_id']}: {r['nombre']}")
        print(f"   Descripción: {r['descripcion']}")
        print(f"   Score: {r['score']} ({r['percentage']:.0f}%)")

        if not r['passed']:
            print("   Verificaciones:")
            for check_name, check_data in r['checks'].items():
                check_icon = "✅" if check_data['pass'] else "❌"
                print(f"     {check_icon} {check_data['description']}")
                if not check_data['pass']:
                    print(f"        → Esperado: {check_data['expected']}")
                    print(f"        → Actual: {check_data['actual']}")

    # SECCIÓN 4: Recomendaciones
    print_section("💡 RECOMENDACIONES")

    if report['pass_rate'] == 100:
        print("\n🎉 ¡Excelente! Todos los tests pasaron.")
        print("Considera agregar más casos edge:")
        print("  • Múltiples órdenes en un mensaje")
        print("  • Direcciones internacionales")
        print("  • Caracteres especiales en nombres")

    elif report['pass_rate'] >= 66:
        print("\n👍 Sistema funcional con áreas de mejora.")
        print("Prioriza arreglar:")
        if 'error_handled' in report['failed_checks']:
            print("  • Manejo de errores más robusto")
        if 'graceful_failure' in report['failed_checks']:
            print("  • Mensajes de error más claros al usuario")

    else:
        print("\n⚠️ Sistema requiere atención urgente.")
        print("Problemas críticos detectados:")
        for check_name in report['failed_checks']:
            print(f"  • {check_name}")
        print("\nRevisa logs de ejecución en detalle.")

    # SECCIÓN 5: Exportar resultados
    print_section("💾 EXPORTANDO RESULTADOS")

    output_file = "eval_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Resultados guardados en: {output_file}")
    print("   Úsalo para trackear mejoras a lo largo del tiempo")

if __name__ == "__main__":
    main()

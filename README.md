# 🤖 Sistema Agentic AI Workflow

Sistema modular de agentes de IA especializados que automatizan tareas complejas mediante orquestación inteligente, herramientas personalizadas y evaluación continua.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Casos de Uso](#-casos-de-uso)
- [Evaluación](#-evaluación)
- [Personalización](#-personalización)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## 🎯 Descripción

Este proyecto implementa un sistema agentic AI completo que demuestra los conceptos fundamentales de agentes autónomos:

- **Agentes especializados** que ejecutan tareas específicas
- **Orquestación multi-agente** para workflows complejos
- **Herramientas personalizadas** (APIs, bases de datos, email)
- **Sistema de evaluación automática** (evals)
- **Arquitectura modular** fácil de extender

**Caso de uso de demostración:** Sistema de soporte al cliente que maneja cambios de dirección de envío de forma autónoma.

## ✨ Características

- ✅ **5 agentes especializados** con prompts optimizados
- ✅ **Workflow de 5 pasos** completamente automatizado
- ✅ **Sistema de evaluación** con 4+ casos de prueba
- ✅ **Logging detallado** para debugging
- ✅ **Manejo robusto de errores**
- ✅ **Arquitectura extensible** para agregar nuevos agentes
- ✅ **Tests automáticos** con métricas objetivas

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                   ORQUESTADOR                           │
│                (MultiAgentOrchestrator)                 │
└────┬──────────────────┬──────────────────┬──────────────┘
     │                  │                  │
     ▼                  ▼                  ▼
┌─────────┐      ┌──────────┐      ┌──────────┐
│ Agente  │      │  Agente  │      │  Agente  │
│Extractor│      │   BD     │      │ Redactor │
└────┬────┘      └────┬─────┘      └────┬─────┘
     │                │                  │
     └────────┬───────┴──────────────────┘
              ▼
      ┌───────────────┐
      │ HERRAMIENTAS  │
      │ - Database    │
      │ - Email       │
      │ - APIs        │
      └───────────────┘
```

### Workflow de Ejecución

```
Usuario envía consulta
       ↓
1. EXTRACCIÓN → Agente identifica: order_id, problema, urgencia
       ↓
2. CONSULTA BD → Herramienta recupera información de orden
       ↓
3. VALIDACIÓN → Verifica si acción es posible
       ↓
4. EJECUCIÓN → Actualiza dirección en BD
       ↓
5. REDACCIÓN → Agente genera email personalizado
       ↓
6. ENVÍO → Herramienta envía confirmación al cliente
```

## 📦 Requisitos

- **Python:** 3.8+
- **API Key:** OpenAI (GPT-4o-mini o superior)
- **Sistema Operativo:** Linux, macOS, Windows

### Dependencias

```
openai>=1.0.0
python-dotenv>=1.0.0
```

## 🚀 Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/ai_agent_system.git
cd ai_agent_system
```

### 2. Crear entorno virtual

**Linux/Mac:**

```bash
python3 -m venv ai_agent_env
source ai_agent_env/bin/activate
```

**Windows:**

```bash
python -m venv ai_agent_env
ai_agent_env\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, crear con:

```
openai>=1.0.0
python-dotenv>=1.0.0
```

## ⚙️ Configuración

### 1. Configurar credenciales

Crear archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Editar `.env` con tu API key:

```env
OPENAI_API_KEY=sk-proj-tu_clave_real_aqui
MODEL_NAME=gpt-4o-mini
```

### 2. Verificar configuración

```bash
python -c "from config import Config; print('✅ API Key configurada:', bool(Config.OPENAI_API_KEY))"
```

**Resultado esperado:** `✅ API Key configurada: True`

## 💻 Uso

### Ejecutar tests individuales

#### Test 1: Agente Base (Fase 2)

```bash
python test_basic_agent.py
```

#### Test 2: Agente con Herramientas (Fase 3)

```bash
python test_agent_with_tools.py
```

#### Test 3: Sistema Multi-Agente (Fase 4)

```bash
python test_multi_agent.py
```

#### Test 4: Evaluación Completa (Fase 5)

```bash
python run_evals.py
```

### Ejemplo de uso programático

```python
from workflows.multi_agent_orchestrator import MultiAgentOrchestrator

# Crear orquestador
orchestrator = MultiAgentOrchestrator()

# Ejecutar workflow
result = orchestrator.execute(
    "Cambiar dirección orden #12345 a Calle Nueva 123, Bogotá"
)

# Ver resultado
print(result["response_sent"])  # Email generado
print(result["execution_log"])   # Log detallado de pasos
```

## 📁 Estructura del Proyecto

```
ai_agent_system/
├── README.md                           # Este archivo
├── .env.example                        # Plantilla de configuración
├── .gitignore                          # Archivos ignorados por Git
├── config.py                           # Configuración global
├── requirements.txt                    # Dependencias Python
│
├── agents/                             # 🤖 Agentes de IA
│   ├── base_agent.py                   # Clase base para todos los agentes
│   └── specialized/                    # Agentes especializados
│       ├── extraction_agent.py         # Extrae información estructurada
│       ├── response_agent.py           # Redacta emails profesionales
│       └── support_agent_v2.py         # Agente con herramientas integradas
│
├── tools/                              # 🔧 Herramientas
│   ├── database_tool.py                # Simulación de base de datos
│   └── email_tool.py                   # Simulación de envío de emails
│
├── workflows/                          # 🔄 Orquestación
│   └── multi_agent_orchestrator.py    # Coordina múltiples agentes
│
├── evals/                              # 📊 Sistema de evaluación
│   └── workflow_evaluator.py          # Tests automáticos
│
└── tests/                              # 🧪 Scripts de prueba
    ├── test_basic_agent.py             # Test Fase 2
    ├── test_agent_with_tools.py        # Test Fase 3
    ├── test_multi_agent.py             # Test Fase 4
    └── run_evals.py                    # Test Fase 5
```

## 🎯 Casos de Uso

### 1. Soporte al Cliente (Implementado)

**Problema:** Cambios de dirección de envío
**Agentes:** Extracción, Consulta, Redacción
**Resultado:** 75-100% tasa de éxito en tests

### 2. Recursos Humanos (Extensión Posible)

**Problema:** Filtrado de CVs
**Agentes:** Extractor de skills, Evaluador de experiencia, Redactor de emails
**Herramientas:** ATS API, Calendar API

### 3. Análisis Financiero (Extensión Posible)

**Problema:** Reportes de ratios financieros
**Agentes:** Extractor de datos, Calculador, Generador de reportes
**Herramientas:** Yahoo Finance API, PDF Generator

### 4. Revisión Legal (Extensión Posible)

**Problema:** Análisis de contratos
**Agentes:** Extractor de cláusulas, Comparador, Detector de riesgos
**Herramientas:** Document Parser, Template Database

## 📊 Evaluación

### Ejecutar batería de tests

```bash
python run_evals.py
```

### Métricas Evaluadas

| Métrica | Descripción | Tipo |
|---------|-------------|------|
| `order_extracted` | ¿Se extrajo order_id correctamente? | Objetiva |
| `action` | ¿Acción ejecutada fue correcta? | Objetiva |
| `email_sent` | ¿Se generó y envió email? | Objetiva |
| `error_handled` | ¿Errores manejados sin romper? | Objetiva |
| `graceful_failure` | ¿Fallo elegante sin crash? | Objetiva |

### Interpretación de Resultados

**100% Pass Rate** ✅

- Sistema funciona perfectamente
- Listo para producción (con más tests)

**75-99% Pass Rate** ⚠️

- Sistema funcional con áreas de mejora
- Identificar componentes fallidos en reporte

**<75% Pass Rate** ❌

- Requiere atención urgente
- Revisar logs detallados de ejecución

### Ver resultados históricos

Los resultados se guardan en `eval_results.json`:

```bash
cat eval_results.json | python -m json.tool
```

## 🔧 Personalización

### Agregar nuevo agente

**1. Crear archivo:** `agents/specialized/mi_agente.py`

```python
from agents.base_agent import BaseAgent

class MiAgentePersonalizado(BaseAgent):
    def __init__(self):
        prompt = """
        Eres un agente experto en [tu dominio].

        TAREA: [descripción]
        FORMATO: JSON
        """
        super().__init__("MiAgente", prompt)

    def ejecutar_tarea(self, input_data):
        return self.execute(f"Procesa: {input_data}")
```

**2. Integrar en orquestador:**

```python
# workflows/multi_agent_orchestrator.py
from agents.specialized.mi_agente import MiAgentePersonalizado

class MultiAgentOrchestrator:
    def __init__(self):
        # ... agentes existentes
        self.mi_agente = MiAgentePersonalizado()
```

### Agregar nueva herramienta

**1. Crear archivo:** `tools/mi_herramienta.py`

```python
class MiHerramientaAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def ejecutar(self, params):
        # Implementar lógica
        return {"success": True, "data": "..."}
```

**2. Usar en agente:**

```python
from tools.mi_herramienta import MiHerramientaAPI

self.herramienta = MiHerramientaAPI(api_key="...")
result = self.herramienta.ejecutar({"param": "valor"})
```

### Agregar test personalizado

**Editar:** `evals/workflow_evaluator.py`

```python
self.test_cases.append({
    "id": "TC005",
    "nombre": "Mi caso de prueba",
    "input": "Input de ejemplo",
    "expected": {
        "nueva_metrica": True
    }
})
```

## 🗺️ Roadmap

### Corto Plazo (1-2 meses)

- [ ] RAG con ChromaDB para políticas dinámicas
- [ ] MCP para integración con APIs externas
- [ ] Memoria persistente con SQLite
- [ ] LLM-as-Judge para evaluaciones subjetivas
- [ ] Dashboard web con FastAPI

### Mediano Plazo (3-6 meses)

- [ ] Deploy en producción (Railway/Render)
- [ ] Integración con Slack/Discord
- [ ] Sistema de caché con Redis
- [ ] A/B testing de prompts
- [ ] Monitoreo con Langsmith

### Largo Plazo (6+ meses)

- [ ] Multi-tenancy (múltiples clientes)
- [ ] Fine-tuning de modelos especializados
- [ ] Arquitectura distribuida (microservicios)
- [ ] Interfaz de usuario completa
- [ ] Marketplace de agentes reutilizables

## 🤝 Contribuir

¡Contribuciones son bienvenidas!

### Proceso

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

### Guías de Contribución

- **Código:** Seguir PEP 8
- **Tests:** Agregar tests para nuevas funcionalidades
- **Documentación:** Actualizar README si es necesario
- **Commits:** Mensajes descriptivos en español

## 📄 Licencia

MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 📚 Recursos Adicionales

### Documentación

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)

### Cursos

- [CS230 Deep Learning - Stanford](https://cs230.stanford.edu/)
- [DeepLearning.AI - Building Agentic AI](https://www.deeplearning.ai/)

---

## 💬 Soporte

**¿Problemas o preguntas?**

- 🐛 **Reportar bug:** [Issues](https://github.com/ColDevFranklin/ai_agent_system/issues)
- 💡 **Sugerencias:** [Discussions](https://github.com/ColDevFranklin/ai_agent_system/discussions)
- 📧 **Email:** <franklinnrodriguez83@gmail.com>

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**

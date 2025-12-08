from openai import OpenAI
from typing import List, Dict, Optional
import json
import os
from dotenv import load_dotenv

# CARGAR VARIABLES DE ENTORNO
load_dotenv()

class BaseAgent:
    """
    Agente base con capacidades fundamentales:
    - Ejecutar prompts
    - Mantener contexto
    - Usar herramientas
    """

    def __init__(self, name: str, system_prompt: str, tools: Optional[List] = None):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []

        # Obtener API key de variables de entorno
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ ERROR: OPENAI_API_KEY no encontrada.\n"
                "Verifica que el archivo .env existe y contiene:\n"
                "OPENAI_API_KEY=sk-tu_clave_aqui"
            )

        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []

    def execute(self, user_message: str) -> str:
        """Ejecuta una tarea simple"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            temperature=0.7
        )

        assistant_message = response.choices[0].message.content

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset_memory(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []

from typing import Dict
import random

class EmailTool:
    """Simula envío de emails"""

    def send_email(self, to: str, subject: str, body: str) -> Dict:
        """Envía email (simulado)"""
        print("\n" + "=" * 60)
        print("📧 EMAIL ENVIADO")
        print("=" * 60)
        print(f"Para: {to}")
        print(f"Asunto: {subject}")
        print(f"\nCuerpo:\n{body}")
        print("=" * 60 + "\n")

        return {
            "success": True,
            "message_id": f"MSG-{random.randint(1000, 9999)}"
        }

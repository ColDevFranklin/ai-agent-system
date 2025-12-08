from typing import Dict, Optional

class DatabaseTool:
    """Simula acceso a base de datos de órdenes"""

    def __init__(self):
        self.orders = {
            "12345": {
                "status": "processing",
                "customer": "Juan Pérez",
                "email": "juan@example.com",
                "address": "123 Calle Falsa",
                "items": ["Laptop HP"],
                "total": 1200.00,
                "date": "2024-11-20"
            },
            "67890": {
                "status": "shipped",
                "customer": "María González",
                "email": "maria@example.com",
                "address": "789 Plaza Mayor",
                "items": ["Mouse Logitech", "Teclado Mecánico"],
                "total": 150.00,
                "date": "2024-11-15"
            }
        }

    def get_order(self, order_id: str) -> Optional[Dict]:
        """Recupera información de orden"""
        return self.orders.get(order_id)

    def update_address(self, order_id: str, new_address: str) -> Dict:
        """Actualiza dirección si orden no enviada"""
        order = self.orders.get(order_id)

        if not order:
            return {"success": False, "error": "Orden no encontrada"}

        if order["status"] == "shipped":
            return {"success": False, "error": "Orden ya enviada"}

        order["address"] = new_address
        return {
            "success": True,
            "message": f"Dirección actualizada a {new_address}"
        }

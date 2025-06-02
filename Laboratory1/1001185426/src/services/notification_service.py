from src.models import Notification
from src.channels.factory import HandlerFactory

class NotificationService:
    def __init__(self, user_service):
        # Inyectamos UserService para consultar usuarios
        self.user_service = user_service

    def send_notification(self, user_name: str, message: str, priority: str) -> dict:
        """
        Retorna un dict con el resultado general del envío.
        """
        user = self.user_service.get_user_by_name(user_name)
        if not user:
            return {"success": False, "error": f"Usuario '{user_name}' no encontrado."}

        notification = Notification(user_name, message, priority)
        # Construir cadena de handlers según el canal preferido y disponibles
        chain = HandlerFactory.get_chain(user.preferred_channel, user.available_channels)

        # Iniciar la cadena
        delivered = chain.handle(notification.to_dict())
        return {
            "success": delivered,
            "delivered_via": user.preferred_channel if delivered else "fallback",
            "user_name": user_name,
            "message": message,
            "priority": priority
        }

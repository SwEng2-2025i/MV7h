from storage import users
from models.user import User
from services.handlers.email_handler import EmailHandler
from services.handlers.sms_handler import SMSHandler
from services.handlers.smoke_handler import SmokeSignalHandler
from logger import LoggerSingleton

def send_notification(user_name, message, priority="normal"):
    if user_name not in users:
        return {"status": "error", "message": f"User {user_name} not found"}

    user_data = users[user_name]
    user = User(user_data.name, user_data.preferred_channel, user_data.available_channels)

    preferred = user.preferred_channel

    handler_map = {
        "email": EmailHandler,
        "sms": SMSHandler,
        "smoke": SmokeSignalHandler,
    }

    # Primer handler (preferido)
    chain = handler_map.get(preferred, EmailHandler)()
    current = chain

    # Encadenar los demás
    for channel in [c for c in user.available_channels if c != preferred]:
        next_handler = handler_map.get(channel, EmailHandler)()
        current = current.set_next(next_handler)  # actualizar current, pero mantener chain

    logger = LoggerSingleton()
    logger.log(f"Sending '{message}' to {user.name} with priority {priority}")
    
    success = chain.handle(user, message)

    return {
        "status": "success" if success else "failed",
        "message": "Notification sent" if success else "All channels failed"
    }

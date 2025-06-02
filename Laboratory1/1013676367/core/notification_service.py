from channels.email_channel import EmailChannel
from channels.sms_channel import SMSChannel
from channels.console_channel import ConsoleChannel
from core.notification_logger import NotificationLogger

class Notification_Service:
    def __init__(self):
        self.logger = NotificationLogger() 

    def _build_handler_chain(self, user):   
        channel_classes = {
            "email": EmailChannel,
            "sms": SMSChannel,
            "console": ConsoleChannel
        }

        ordered_channels = [user.preferred_channel]
        ordered_channels.extend([ch for ch in user.available_channels if ch != user.preferred_channel])

        handlers = []
        for channel_name in ordered_channels:
            if channel_name in channel_classes:
                handler = channel_classes[channel_name]()
                handlers.append(handler)
        
        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])
        
        return handlers[0] if handlers else None
    
    def send_notification(self, user, notification):
        self.handlers = self._build_handler_chain(user)
        state = self.handlers.handle(user, notification)
        return state
    
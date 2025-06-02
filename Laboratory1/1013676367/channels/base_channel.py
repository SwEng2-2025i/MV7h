from core.notification_logger import NotificationLogger

class BaseChannel:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
    
    def set_next(self, channel):
        self.next_handler = channel
        return self 

    def handle(self, user, message):
        if self._can_handle(user):
            logger = NotificationLogger() 
            channel_name = self.__class__.__name__

            if self._send(user, message):
                logger.log_attempt(user, channel_name, message.message, state=True)
                return True
            elif self.next_handler:
                logger.log_attempt(user, channel_name, message.message, state=False)
                return self.next_handler.handle(user, message)

        elif self.next_handler: 
            return self.next_handler.handle(user, message)
        return False # Fallo de envio en todos los canales

    def _can_handle(self, user):
        return self.__class__.__name__.lower().replace("channel", "") in user.available_channels
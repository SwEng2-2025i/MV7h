import random
class NotificationHandler:
    def __init__(self, next_handler=None):
        self.next = next_handler

    def handle(self,data):
        if self.next:
            return self.next.handle(data)
        else:
            return False

class NotificationEmail(NotificationHandler):
    def handle(self,data):
        canHandle=random.choice([True,False])
        if canHandle:
            data["medio"]="Email"
            return True
        else:
            return super().handle(data)

class NotificationSms(NotificationHandler):
    def handle(self,data):
        canHandle=random.choice([True,False])
        if canHandle:
            data["medio"]="SMS"
            return True
        else:
            return super().handle(data)

class NotificationCel(NotificationHandler):
    def handle(self,data):
        canHandle=random.choice([True,False])
        if canHandle:
            data["medio"]="CEL"
            return True
        else:
            return super().handle(data)

handler_map={
    "email": NotificationEmail,
    "sms":NotificationSms,
    "cel":NotificationCel
}

def crearCadenaResponsabilidad(preferred_channel,available_channels):
    full_chain=[preferred_channel]+ [ch for ch in available_channels if ch != preferred_channel]
    handler=None
    for channel in reversed(full_chain):  # Reversa para encadenar en orden correcto
        handler_class = handler_map.get(channel)
        if handler_class:
            handler = handler_class(handler)
    return handler

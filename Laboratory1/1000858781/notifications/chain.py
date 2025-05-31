from notifications.channels import EmailNotifier, SMSNotifier, ConsoleNotifier

class NotificationChain:
    def __init__(self):
        # Crear cadena por defecto (se puede parametrizar según user.channels)
        self.chain = None

    def build_chain(self, channels):
        handler = None
        for name in reversed(channels):
            if name == 'console':
                handler = ConsoleNotifier(successor=handler)
            elif name == 'sms':
                handler = SMSNotifier(successor=handler)
            elif name == 'email':
                handler = EmailNotifier(successor=handler)
        return handler

    def send(self, user, message, priority):
        chain = self.build_chain([user.preferred] + [c for c in user.channels if c != user.preferred])
        success = chain.notify(user, message, priority)
        return {'delivered': success}
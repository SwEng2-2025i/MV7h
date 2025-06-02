class NotificationChannel:
    def __init__(self, next_channel=None):
        self.next_channel = next_channel

    def send(self, user, message):
        raise NotImplementedError

    def try_next(self, user, message):
        if self.next_channel:
            return self.next_channel.send(user, message)
        return False

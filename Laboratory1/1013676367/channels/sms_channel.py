from channels.base_channel import BaseChannel

import random

class SMSChannel(BaseChannel):
    def _send(self, user, message):
        if random.choice([True, False]):
            print(f"SMS enviado a {user.name}: {message.message}")
            return True
        else:
            return False
from channels.base_channel import BaseChannel

import random

class EmailChannel(BaseChannel):
    def _send(self, user, message):
        if random.choice([True, False]):
            print(f"Email enviado a {user.name}: {message.message}")
            return True
        else:
            return False
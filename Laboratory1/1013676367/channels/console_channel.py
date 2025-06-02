from channels.base_channel import BaseChannel

import random

class ConsoleChannel(BaseChannel):
    def _send(self, user, message):
        if random.choice([True, False]):
            print(f"Consola enviado a {user.name}: {message.message}")
            return True
        else:
            return False
class User:
    def __init__(self, name, preferred, channels):
        self.name = name
        self.preferred = preferred
        self.channels = channels

    def to_dict(self):
        return {
            'name': self.name,
            'preferred_channel': self.preferred,
            'available_channels': self.channels
        }

class UserStore:
    def __init__(self):
        self._users = []

    def add_user(self, name, preferred, channels):
        user = User(name, preferred, channels)
        self._users.append(user)
        return user

    def get_all(self):
        return self._users

    def find_by_name(self, name):
        return next((u for u in self._users if u.name == name), None)
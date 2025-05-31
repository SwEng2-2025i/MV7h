from models.user import UserStore

class UserService:
    def __init__(self):
        self.store = UserStore()

    def create_user(self, data):
        user = self.store.add_user(
            name=data['name'],
            preferred=data['preferred_channel'],
            channels=data['available_channels']
        )
        return user.to_dict()

    def list_users(self):
        return [u.to_dict() for u in self.store.get_all()]
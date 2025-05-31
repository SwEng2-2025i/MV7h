from models.user import UserStore
from notifications.chain import NotificationChain

class NotificationService:
    def __init__(self):
        self.store = UserStore()
        self.chain = NotificationChain()

    def send_notification(self, data):
        user = self.store.find_by_name(data['user_name'])
        if not user:
            return {'error': 'User not found'}
        return self.chain.send(
            user=user,
            message=data['message'],
            priority=data.get('priority')
        )

class Notification():
    def __init__(self, user_name, message, priority):
        self.user_name = user_name
        self.message = message
        self.priority = priority
    
    def to_dict(self):
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }
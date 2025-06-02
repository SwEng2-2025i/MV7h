from src.models.user import User

class Users:
  def __init__(self):
    self.users = {}

  def new_user(self, user: User):
    self.users[user.name] = user
    return user

  def list_users(self):
    return list(self.users.keys())

  def get_user(self, name:str):
    try:
      return self.users[name]
    except Exception as e:
      return False
  

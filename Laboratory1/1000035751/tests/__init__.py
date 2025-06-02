
from src.core.logger.logger import Logger
from src.utils.users import Users
from src.utils.notification import Notification
from src.models.user import User

def user_test():
  x1 = User("Jose", "email", ["email", "sms"])
  x2 = User("Maria", "email", ["email", "phonecall"])
  x3 = User("Santiago", "sms", ["sms", "email"])
  y = Users()
  y.new_user(x1)
  y.new_user(x2)
  y.new_user(x3)
  z1 = y.get_user("Santiago")
  z2 = y.list_users()
  
  print(z1)
  print(z2)


def notification_test():
  logger = Logger()

  x1 = User("Santiago", "email", ["sms", "email", "phonecall"])
  x2 = User("Maria", "email", ["email", "phonecall"])
  y1 = Notification(x1, "The toilet is clogged again", "high")
  y2 = Notification(x2, "Mom is calling", "Medium")

  y1.send_notification()
  y2.send_notification()
  print(logger.logs())
  

  


#user_test()
notification_test()



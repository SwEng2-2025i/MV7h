class SingletonLogger(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      instance = super().__call__(*args, **kwargs)
      cls._instances[cls] = instance
    return cls._instances[cls]

class Logger(metaclass=SingletonLogger):
  notification_list = []

  def log_action(self, notification, channel, state):
    action = {"notification": notification, "channel": channel, "state": state}
    self.notification_list.append(action)
    return self.notification_list  
  
  def logs(self):
    return self.notification_list



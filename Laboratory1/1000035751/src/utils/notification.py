import random
from queue import Queue

from src.models.user import User

from src.utils.users import Users

from src.core.handlers.email_handler import EmailHandler
from src.core.handlers.sms_handler import SmsHandler
from src.core.handlers.phonecall_handler import PhonecallHandler

from dataclasses import dataclass

@dataclass
class Notification:
  receiver: User
  message: str
  priority: str

  def send_notification(self):
    #state = random.choice([True, False])
    handlers = {
      "sms": SmsHandler(), 
      "email": EmailHandler(), 
      "phonecall": PhonecallHandler()}

    preferred_channel = self.receiver.preferred_channel
    indx_pref_channel = self.receiver.avalible_channels.index(preferred_channel)

    temp = self.receiver.avalible_channels.copy()
    temp.pop(indx_pref_channel)

    ordered_channels = [preferred_channel] + temp
    
    for i in range(len(ordered_channels)-1):
      handlers[ordered_channels[i]].set_next(handlers[ordered_channels[i+1]])

    preferred_handler = handlers[preferred_channel]

    notification = Notification(self.receiver.name, self.message, self.priority)

    result = preferred_handler.handle(notification)
 
    return result






      




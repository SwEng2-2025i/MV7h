from .email_channel import EmailChannel
from .sms_channel import SMSChannel

def create_channel(name):
    if name == "email":
        return EmailChannel()
    elif name == "sms":
        return SMSChannel()
    else:
        raise ValueError(f"Unknown channel: {name}")
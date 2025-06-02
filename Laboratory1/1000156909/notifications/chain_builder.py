from .channel_factory import create_channel

def build_notification_chain(preferred, available):
    ordered = [preferred] + [ch for ch in available if ch != preferred]
    head = create_channel(ordered[0])
    current = head
    for ch_name in ordered[1:]:
        current = current.set_next(create_channel(ch_name))
    return head
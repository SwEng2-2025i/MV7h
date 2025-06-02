from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler:

  @abstractmethod
  def set_next(self, handler: Handler) -> Handler:
    pass
  
  @abstractmethod
  def handle(self, request) -> Optional[bool]:
    pass


class NotificationHandler(Handler):

  _next_handler: Handler = None

  def set_next(self, handler: Handler) -> Handler:
    self._next_handler = handler
    return handler
  
  @abstractmethod
  def handle(self, notification: Any) -> bool:
    if self._next_handler:
      return self._next_handler.handle(notification)
    print(f"Notification was not send due to errors in avalible channels")
    return False
  




from flask import Blueprint, request, jsonify
from models.notification import Notification
from controllers.user_controller import users
from services.notification_handler import EmailHandler, SMSHandler
from services.logger import Logger

notification_bp = Blueprint('notification_controller', __name__)

@notification_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Notification
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              example: "Juan"
            message:
              type: string
              example: "Your appointment is tomorrow"
            priority:
              type: string
              enum: [low, medium, high]
              example: "high"
    responses:
      200:
        description: Notification processed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Notification sent via sms"
      404:
        description: User not found
      400:
        description: Invalid request payload
    """
    data = request.json
    user = next((u for u in users if u.name == data['user_name']), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    notification = Notification(user, data['message'], data['priority'])

    # Construir la cadena de Handlers basada en el canal preferido del usuario
    handler_classes = {
        'email': EmailHandler,
        'sms': SMSHandler
    }
    
    # El canal preferido primero, seguido de los demás canales disponibles
    ordered_channels = [user.preferred_channel] + [
        ch for ch in user.available_channels if ch != user.preferred_channel
    ]

    first_handler = None
    current_handler = None

    for channel in ordered_channels:
        handler_instance = handler_classes[channel]()
        if first_handler is None:
            first_handler = handler_instance
        else:
            current_handler.set_next(handler_instance)
        current_handler = handler_instance

    success = first_handler.handle(notification)

    return jsonify({'message': 'Notification processed', 'status': 'success' if success else 'failed'})

from flask import Flask, request, jsonify
from flasgger import Swagger
from handlers.console_handler import ConsoleHandler
from handlers.email_handler import EmailHandler
from handlers.call_handler import CallHandler
from handlers.sms_handler import SMSHandler
from logger.logger import Logger
from models.user import users
import random

app = Flask(__name__)
swagger = Swagger(app)  # starts Flasgger

# notification handler methods 
channel_map = {
    "email": EmailHandler,
    "sms": SMSHandler,
    "call": CallHandler,
    "console": ConsoleHandler
}

def build_handler_chain(preferred, available_channels):
    # preferred goes first
    ordered_channels = [preferred] + [ch for ch in available_channels if ch != preferred]

    # instantiate handlers based on the ordered channels
    handlers = [channel_map[ch]() for ch in ordered_channels if ch in channel_map]

    # chain them together
    for i in range(len(handlers) - 1):
        handlers[i].set_next(handlers[i + 1])

    return handlers[0]  # Retorna primer handler en la cadena

@app.route('/users', methods=['POST'])
def register_user():
    """
    Register a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: Thomas
            preferred_channel:
              type: string
              enum: [email]
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms"]
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input
    """
    data = request.json
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels')
    users[name] = {
        "preferred": preferred,
        "channels": available
    }
    return jsonify({"message": f"User {name} registered successfully."}), 201


@app.route('/users', methods=['GET'])
def list_users():
    """
    List all registered users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
    """
    return jsonify(users), 200


@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Send a notification to a user
    ---
    tags:
      - Notifications
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
          properties:
            user_name:
              type: string
              example: Thomas
            message:
              type: string
              example: Your appointment is tomorrow.
    responses:
      200:
        description: Notification status
      404:
        description: User not found
    """
    data = request.json
    user_name = data['user_name']
    message = data['message']

    if user_name not in users:
        return jsonify({"error": "User not found"}), 404

    user = users[user_name]
    preferred = user['preferred']
    channels = user['channels']

    # create chain of priority 
    handler_chain = build_handler_chain(preferred, channels)

    # Send the notification
    success = handler_chain.handle(preferred, channels, user_name, message)

    return jsonify({"status": "Notification sent" if success else "Failed to deliver notification"}), 200


if __name__ == '__main__':
    app.run(debug=True)
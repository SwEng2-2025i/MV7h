from flask import Flask, jsonify, request
from flasgger import Swagger
from functools import wraps
import random

app = Flask(__name__)
swagger = Swagger(app)

# Middleware de autorización por header
def require_authorization(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.headers.get("Authorization"):
            return jsonify({"error": "Missing Authorization header"}), 401
        return f(*args, **kwargs)
    return decorated

# Estructura en memoria
users = {}

# Clase User
class User:
    def __init__(self, name, preferred_channel, available_channels):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }

# Canal base
class Channel:
    def __init__(self, name):
        self.name = name
        self.next_channel = None

    def set_next(self, next_channel):
        self.next_channel = next_channel
        return next_channel

    def send(self, message):
        success = random.choice([True, False])
        if success:
            return True, self.name
        elif self.next_channel:
            return self.next_channel.send(message)
        return False, None

@app.route('/users', methods=['POST'])
@require_authorization
def register_user():
    """
    Register a new user
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token required
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: Juan
            preferred_channel:
              type: string
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: ["email", "sms"]
    responses:
      201:
        description: User registered
      400:
        description: Invalid input
    """
    data = request.get_json()
    users[data["name"]] = User(data["name"], data["preferred_channel"], data["available_channels"])
    return jsonify({"message": "User registered"}), 201

@app.route('/users', methods=['GET'])
@require_authorization
def get_users():
    """
    Get all users
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token required
    responses:
      200:
        description: List of users
        examples:
          application/json: [{"name": "Juan", "preferred_channel": "email", "available_channels": ["email", "sms"]}]
    """
    return jsonify([user.to_dict() for user in users.values()])

@app.route('/notifications/send', methods=['POST'])
@require_authorization
def send_notification():
    """
    Send a notification to a user
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Token required
      - in: body
        name: body
        required: true
        schema:
          id: Notification
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              example: Juan
            message:
              type: string
              example: Your appointment is tomorrow.
            priority:
              type: string
              example: high
    responses:
      200:
        description: Notification sent result
        examples:
          application/json: {"message": "Notification sent via sms"}
      404:
        description: User not found
    """
    data = request.get_json()
    user = users.get(data["user_name"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Crear cadena de canales
    head = Channel(user.preferred_channel)
    current = head
    for ch in user.available_channels:
        if ch != user.preferred_channel:
            current = current.set_next(Channel(ch))

    success, used_channel = head.send(data["message"])
    if success:
        return jsonify({"message": f"Notification sent via {used_channel}"})
    return jsonify({"message": "All channels failed"}), 200

if __name__ == '__main__':
    app.run(debug=True)

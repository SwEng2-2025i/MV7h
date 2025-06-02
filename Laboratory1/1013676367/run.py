from models.user import User
from models.notification import Notification
from core.notification_service import Notification_Service
from core.notification_logger import NotificationLogger

from flask import Flask, jsonify, request
from flasgger import Swagger
from functools import wraps

app = Flask(__name__)
swagger = Swagger(app)

# Lista de Usuarios Inicial
users = {
    "Alice": User("Alice", "email", ["sms", "console"]),
    "Pedro": User("Pedro", "sms", ["sms", "console"])
}

# Clase de creacion de usuarios
@app.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: user
        in: body
        required: true
        schema:
          id: Create_user
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              description: Name of the user
              example: Juan
            preferred_channel:
                type: string
                description: Preferred channel
                example: email
            available_channels:
                type: array
                description: Available channel
                items:
                  type: string
                example: ["email", "sms"]
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid input
      409:
        description: User already exists
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing data"}), 400
    
    user_name = data["name"]
    user = [u for u in users if users.get(u).name == user_name] 
    if user:
        return jsonify({"error": "User already exists"}), 409

    new_user = User(data["name"], data["preferred_channel"], data["available_channels"])
    users.update({data["name"]: new_user})
    return jsonify({"message": "User created successfully"}), 201

# Obtencion de todos los usuarios 
@app.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    consumes:
      - application/json
    produces:
      - application/json
    responses:
      200:
        description: A list of users
        examples:
          application/json: [{"id":1,"name":"Alice"}]
      401:
        description: Missing list of users
    """
    return jsonify([user.to_dict() for user in users.values()])

@app.route('/notifications/send', methods=['POST'])
def send_notifications():
    """
    Send a notification with message and priority
    ---
    tags:
      - Notifications
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
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
              description: Name of the user
              example: Juan
            message:
                type: string
                description: Body of message 
                example: Your appointment is tomorrow.
            priority:
                type: string
                description: Priority of message
                example: high
    responses:
        200:
          description: Notification processing result
        400:
          description: Invalid request
        404:
          description: User not found
    """
    data = request.get_json()
    user_name = data["user_name"]
    user = None
    for u in users:
        if users.get(u).name == user_name:
            user = users.get(u)

    if not user:
        return jsonify({"error": "User not found"}), 404

    notification = Notification(data["user_name"], data["message"], data["priority"])

    service = Notification_Service()
    state = service.send_notification(user, notification)

    return jsonify({
        "status": "sent" if state else "failed"
    })

@app.route('/logs', methods=['GET'])
def get_logs():
    """
    Get notification logs
    ---
    tags:
      - Logs
    produces:
      - application/json
    responses:
      200:
        description: List of notification logs
        examples:
          application/json: [{"channel": "EmailChannel","message": "Hola","success": false,"timestamp": "2025-05-29T20:53:35.693151","user": "Alice"}]
      204:
        description: No logs available
    """
    
    try:
        logger = NotificationLogger()
        logs = logger.get_logs()
        
        if not logs:
            return jsonify("There are no records of notifications.")
        else:
            return jsonify(logs)
    except Exception as e:
        print(f"Error reading logs: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
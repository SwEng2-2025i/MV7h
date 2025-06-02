from flask import Flask, request, jsonify
from flasgger import Swagger
from src.services.user_service import UserService
from src.services.notification_service import NotificationService

app = Flask(__name__)
swagger = Swagger(app)

# Instancias de servicios en memoria
user_service = UserService()
notification_service = NotificationService(user_service)


@app.route("/users", methods=["POST"])
def create_user():
    """
    Registra un usuario con nombre, canal preferido y canales disponibles
    ---
    tags:
      - Usuarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            preferred_channel:
              type: string
            available_channels:
              type: array
              items:
                type: string
          example:
            name: "Juan"
            preferred_channel: "email"
            available_channels: ["email", "sms", "console"]
    responses:
      200:
        description: Usuario registrado exitosamente
        schema:
          type: object
          properties:
            name: { type: string }
            preferred_channel: { type: string }
            available_channels:
              type: array
              items: { type: string }
      400:
        description: Error en la creación del usuario
    """
    data = request.get_json()
    try:
        user = user_service.add_user(
            data["name"], data["preferred_channel"], data["available_channels"]
        )
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users", methods=["GET"])
def list_users():
    """
    Lista todos los usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            type: object
            properties:
              name: { type: string }
              preferred_channel: { type: string }
              available_channels:
                type: array
                items: { type: string }
    """
    users = user_service.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200


@app.route("/notifications/send", methods=["POST"])
def send_notification():
    """
    Envía una notificación al usuario por sus canales configurados
    ---
    tags:
      - Notificaciones
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            user_name:
              type: string
            message:
              type: string
            priority:
              type: string
          example:
            user_name: "Juan"
            message: "Tu cita es mañana."
            priority: "high"
    responses:
      200:
        description: Resultado del envío
        schema:
          type: object
          properties:
            success: { type: boolean }
            delivered_via: { type: string }
            user_name: { type: string }
            message: { type: string }
            priority: { type: string }
    """
    data = request.get_json()
    resultado = notification_service.send_notification(
        data["user_name"], data["message"], data["priority"]
    )
    status_code = 200 if resultado.get("success", False) else 400
    return jsonify(resultado), status_code


if __name__ == "__main__":
    app.run(debug=True, port=5000)

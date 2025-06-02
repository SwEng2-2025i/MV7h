from flask import Flask, request, jsonify
from flasgger import Swagger
from storage import users, add_user, list_users 
from models.user import User 
from services.notification_service import send_notification 

app = Flask(__name__)

# --- Configuración de Flasgger ---
template = {
    "swagger": "2.0",
    "info": {
        "title": "Lab 1: Sistema de Envio de Notificaciones",
        "description": "API para registrar usuarios y enviar notificaciones por medios definidos.",
        "version": "1.0"
    },
    "tags": [
        {
            "name": "Usuarios",
            "description": "Operaciones para crear y listar usuarios."
        },
        {
            "name": "Notificaciones",
            "description": "Operaciones para el envío de notificaciones a usuarios."
        },
    ],
    "definitions": {
        # --- Definición del Modelo de Usuario ---
        "User": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "El nombre completo del usuario.",
                    "example": "Toro"
                },
                "preferred_channel": {
                    "type": "string",
                    "description": "El canal de comunicación preferido para el usuario.",
                    "enum": ["email", "sms", "smoke"], 
                    "example": "smoke"
                },
                "available_channels": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["email", "sms", "smoke"] 
                    },
                    "description": "Lista de canales de comunicación disponibles para el usuario.",
                    "example": ["smoke", "sms", "email"]
                }
            },
            "required": ["name", "preferred_channel", "available_channels"],
            "example": { 
                "name": "Toro",
                "preferred_channel": "smoke",
                "available_channels": ["smoke", "sms", "email"]
            }
        },
        # --- Definición del Modelo de Solicitud de Notificación ---
        "NotificationRequest": {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                    "required": True,
                    "description": "El nombre del usuario al que se enviará la notificación.",
                    "example": "Toro"
                },
                "message": {
                    "type": "string",
                    "required": True,
                    "description": "El contenido del mensaje de la notificación.",
                    "example": "Esperar emboscada al amanecer"
                },
                "priority": {
                    "type": "string",
                    "required": False,
                    "default": "normal",
                    "enum": ["low", "normal", "high"],
                    "description": "La prioridad de la notificación.",
                    "example": "high"
                }
            },
            "required": ["user_name", "message"],
            "example": { 
                "user_name": "Toro",
                "message": "Esperar emboscada al amanecer",
                "priority": "high"
            }
        },
        # --- Definición del Modelo de Respuesta de Notificación ---
        "NotificationResponse": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "El estado de la operación.",
                    "enum": ["success", "failed", "error"] 
                },
                "message": {
                    "type": "string",
                    "description": "Un mensaje descriptivo sobre el resultado de la operación.",
                    "example": "Notification sent"
                }
            }
        },
        # --- Definición de Respuesta de Error Genérica ---
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "example": "error"},
                "message": {"type": "string", "example": "User Toro not found"}
            }
        }
    }
}

swagger = Swagger(app, template=template)


@app.route("/")
def index():
    """
    Ruta raíz para verificar que la aplicación está funcionando.
    """
    return "La aplicacion funciona, hay que buscar una ruta", 200

@app.route('/users', methods=['POST'])
def new_user():
    """
    Crea un nuevo usuario en el sistema.
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: user
        schema:
          $ref: '#/definitions/User' # Referencia al esquema User
        required: true
        description: Datos del nuevo usuario.
    responses:
      200:
        description: Usuario creado exitosamente.
        schema:
          type: string
          example: "Toro fue creado exitosamente"
      400:
        description: Datos de usuario inválidos o incompletos.
    """
    data = request.get_json()
    if not all(k in data for k in ["name", "preferred_channel", "available_channels"]):
        return jsonify({"status": "error", "message": "Faltan campos de usuario obligatorios"}), 400

    response_message = add_user(data) 
    return jsonify(response_message), 200

@app.route('/getusers', methods=['GET'])
def list_all_users():
    """
    Lista todos los usuarios registrados.
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios.
        schema:
          type: array
          items:
            $ref: '#/definitions/User' # Referencia al esquema User
    """
    users_list = list_users()
    return jsonify([user.to_dict() for user in users_list])

@app.route('/notifications/send', methods=['POST'])
def notify():
    """
    Envía una notificación a un usuario específico.
    ---
    tags:
      - Notificaciones
    parameters:
      - in: body
        name: notification
        schema:
          $ref: '#/definitions/NotificationRequest' # Referencia al esquema NotificationRequest
        required: true
        description: Datos para enviar la notificación.
    responses:
      200:
        description: Estado del envío de la notificación.
        schema:
          $ref: '#/definitions/NotificationResponse'
      400:
        description: Datos de la petición inválidos o incompletos.
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Usuario no encontrado para enviar la notificación.
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    data = request.get_json()
    user_name = data.get("user_name")
    message = data.get("message")
    priority = data.get("priority", "normal")

    if not user_name or not message:
        return jsonify({"status": "error", "message": "Faltan campos obligatorios"}), 400

    result = send_notification(user_name, message, priority)

    if result.get("status") == "error" and "not found" in result.get("message", "").lower():
        return jsonify(result), 404
    elif result.get("status") == "error":
   
        return jsonify(result), 400
    
    return jsonify(result), 200 

if __name__ == '__main__':
    app.run(debug=True)
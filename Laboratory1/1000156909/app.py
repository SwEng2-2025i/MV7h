from models.user import User
from flask import Flask, request, jsonify
from data.store import user_store
from notifications.chain_builder import build_notification_chain
from utils.logger import Logger
from flasgger import Swagger
from swagger.swagger_config import swagger_template

app = Flask(__name__)
logger = Logger.get_instance()
swagger = Swagger(app, template=swagger_template)


@app.route('/users', methods=['POST'])
def register_user():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: cuerpo
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
      200:
        description: Usuario registrado exitosamente
      400:
        description: Datos inválidos
    """

    data = request.json
    user = User(
        name=data['name'],
        preferred_channel=data['preferred_channel'],
        available_channels=data['available_channels']
    )
    user_store[user.name] = user
    return jsonify({'message': 'User registered'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    """
    Obtener la lista de usuarios registrados
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios en memoria
        schema:
          type: array
          items:
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
    """

    return jsonify({name: user.to_dict() for name, user in user_store.items()}), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    """
    Enviar una notificación a un usuario
    ---
    tags:
      - Notificaciones
    parameters:
      - in: body
        name: cuerpo
        required: true
        schema:
          type: object
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
              example: Tu cita es mañana.
            priority:
              type: string
              example: alta
    responses:
      200:
        description: Notificación procesada (éxito o fallo simulado)
      404:
        description: Usuario no encontrado
    """

    data = request.json
    name = data['user_name']
    message = data['message']

    user = user_store.get(name)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    chain = build_notification_chain(user.preferred_channel, user.available_channels)
    result = chain.handle(message, name)
    return jsonify({'status': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
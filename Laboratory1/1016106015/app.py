from flask import Flask, request
from flask_restx import Api, Resource, fields
from storage import USERS  # Diccionario en memoria que almacena los usuarios registrados
from handlers import build_chain  # Función que construye la cadena de manejadores (Chain of Responsibility)
from log_util import logger  # Logger singleton para registrar eventos del sistema

# Se crea la aplicación Flask
app = Flask(__name__)

# Se instancia la API REST usando Flask-RESTX con metadatos
api = Api(app, title="Multichannel Notification API", version="1.0",
          description="Envía notificaciones por email/SMS con fallback")

# Namespaces para organizar los endpoints relacionados con usuarios y notificaciones
ns_users = api.namespace('users', description='Gestión de usuarios')
ns_notif = api.namespace('notifications', description='Envío de notificaciones')

# Modelo de datos para el registro de usuario (usado por Swagger y validación automática)
user_model = api.model('User', {
    'name': fields.String(required=True),
    'preferred_channel': fields.String(required=True, enum=['email','sms']),
    'available_channels': fields.List(fields.String, required=True, 
                                      description="Lista de canales ['email','sms']")
})

# Modelo de datos para envío de notificación
notif_model = api.model('Notification', {
    'user_name': fields.String(required=True),
    'message': fields.String(required=True),
    'priority': fields.String(required=True, enum=['low','medium','high'])
})

@ns_users.route('')
class UserList(Resource):
    @ns_users.expect(user_model)
    def post(self):
        """Registra un usuario con canales"""
        data = api.payload
        USERS[data['name']] = {
            'preferred': data['preferred_channel'],
            'available': data['available_channels']
        }
        return {'msg': 'Usuario creado'}, 201

    def get(self):
        """Lista todos los usuarios"""
        return USERS, 200

@ns_notif.route('/send')
class SendNotification(Resource):
    @ns_notif.expect(notif_model)
    def post(self):
        """Envía una notificación usando la cadena de responsabilidad"""
        data = api.payload
        user = USERS.get(data['user_name'])

        # Verifica que el usuario exista
        if not user:
            api.abort(404, "Usuario no encontrado")

        # Construye la cadena de responsabilidad: primero el canal preferido, luego los demás
        channels = [user['preferred']] + [c for c in user['available'] if c != user['preferred']]
        chain = build_chain(channels)

        # Envía la notificación a través de la cadena
        delivered = chain.handle(user['preferred'], data['user_name'], data['message'], data['priority'])

        # Retorna respuesta dependiendo del éxito del envío
        if delivered:
            return {'msg': 'Notificación entregada'}, 200
        else:
            return {'msg': 'Todas las entregas fallaron'}, 500

# Ejecuta el servidor Flask en modo debug
if __name__ == '__main__':
    app.run(debug=True)

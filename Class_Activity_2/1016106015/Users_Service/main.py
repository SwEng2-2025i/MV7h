from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Permite solicitudes CORS desde el frontend

# -------------------------------------------------------------
# Configuración del servicio de usuarios (Users Service)
# -------------------------------------------------------------
service_a = Flask(__name__)
# Habilitamos CORS para que el frontend pueda llamar sin restricciones\CORS(service_a)

# Conexión a la base de datos SQLite (archivo users.db)
service_a.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Desactivamos las notificaciones de cambios para optimizar el rendimiento
service_a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Instancia de SQLAlchemy para mapear objetos Python a tablas en SQLite
db = SQLAlchemy(service_a)

# -------------------------------------------------------------
# Modelo de datos
# -------------------------------------------------------------
class User(db.Model):
    """
    Representa un usuario en la tabla 'user'.
    Campos:
    - id: clave primaria, entero auto-incremental.
    - name: nombre del usuario, cadena no nula.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# -------------------------------------------------------------
# Endpoints REST
# -------------------------------------------------------------

@service_a.route('/users', methods=['POST'])
def create_user():
    """
    Crea un nuevo usuario.
    Espera JSON con 'name'.
    Retorna 201 y los datos del usuario o 400 si faltan datos.
    """
    data = request.get_json()
    # Validación básica: el campo 'name' debe estar presente y no vacío
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'El nombre es requerido'}), 400

    # Creamos la instancia del usuario y la guardamos en la base de datos
    user = User(name=data['name'].strip())
    db.session.add(user)
    db.session.commit()

    # Opcional: imprimir en consola para debugging
    print({'id': user.id, 'name': user.name})
    # Devolvemos el ID y nombre del usuario creado
    return jsonify({'id': user.id, 'name': user.name}), 201


@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Obtiene un usuario por su ID.
    Retorna 200 y el usuario, o 404 si no existe.
    """
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name}), 200
    return jsonify({'error': 'User not found'}), 404


@service_a.route('/users', methods=['GET'])
def list_users():
    """
    Lista todos los usuarios registrados.
    Retorna un array de objetos {id, name}.
    """
    users = User.query.all()
    # Construimos la lista de diccionarios para jsonify
    result = [{'id': u.id, 'name': u.name} for u in users]
    return jsonify(result), 200


@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Elimina un usuario dado su ID.
    Retorna 200 si se borró, o 404 si no se encontró.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Realizamos la eliminación en la base de datos
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': f'User {user_id} deleted'}), 200


# -------------------------------------------------------------
# Arranque de la aplicación
# -------------------------------------------------------------
if __name__ == '__main__':
    # Creamos las tablas en la base de datos si no existen\    
    with service_a.app_context():
        db.create_all()
    # Ejecutamos el servidor en el puerto 5001
    service_a.run(port=5001)

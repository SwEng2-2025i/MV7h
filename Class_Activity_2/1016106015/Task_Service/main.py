from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

# Inicializamos la aplicación de Flask para el servicio de tareas
tasks_service = Flask(__name__)
# Habilitamos CORS para permitir peticiones desde otros orígenes (front-end)
CORS(tasks_service)

# Configuración de la base de datos SQLite localizada en 'tasks.db'
tasks_service.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
tasks_service.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creamos la instancia de SQLAlchemy ligada a la aplicación
db = SQLAlchemy(tasks_service)

# Definición del modelo Task que representa una tarea en la base de datos
class Task(db.Model):
    # Campo ID autoincremental como llave primaria
    id = db.Column(db.Integer, primary_key=True)
    # Título de la tarea, obligatorio y con máximo 100 caracteres
    title = db.Column(db.String(100), nullable=False)
    # ID del usuario asociado a esta tarea, obligatorio\    
    user_id = db.Column(db.Integer, nullable=False)

@tasks_service.route('/tasks', methods=['POST'])
def create_task():
    """
    Crea una nueva tarea. Espera un JSON con 'title' y 'user_id'.
    Valida que el usuario exista consultando al servicio de usuarios.
    """
    data = request.get_json()
    # Verificamos que se reciban los campos necesarios\    
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Datos inválidos'}), 400

    # Confirmamos la existencia del usuario llamando al servicio Users (puede fallar)
    try:
        user_resp = requests.get(f'http://localhost:5001/users/{data["user_id"]}')
    except Exception as e:
        return jsonify({'error': f'Error de conexión al verificar usuario: {e}'}), 500

    # Si el servicio de usuarios responde con código distinto de 200, consideramos inválido el ID\    
    if user_resp.status_code != 200:
        return jsonify({'error': 'ID de usuario inválido'}), 400

    # Creamos y almacenamos la nueva tarea en la base de datos\    
    new_task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(new_task)
    db.session.commit()

    # Devolvemos el ID de la tarea creada y sus detalles\    
    return jsonify({'id': new_task.id, 'title': new_task.title, 'user_id': new_task.user_id}), 201

@tasks_service.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Lista todas las tareas existentes.
    Devuelve un array JSON con ID, título y user_id de cada tarea.
    """
    tasks = Task.query.all()
    # Convertimos cada objeto Task en diccionario para jsonify
    tasks_list = [{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks]
    return jsonify(tasks_list), 200

@tasks_service.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Elimina la tarea con el ID especificado.
    Si la tarea no existe, retorna 404.
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Borramos la tarea encontrada\    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'msg': f'Task {task_id} deleted'}), 200

@tasks_service.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Recupera una única tarea por su ID.
    Si no existe, retorna 404.
    """
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    # Si existe, devolvemos sus datos
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 200

if __name__ == '__main__':
    # Al iniciar la app, nos aseguramos de crear las tablas en SQLite si no existen
    with tasks_service.app_context():
        db.create_all()
    # Ejecutamos el servidor en el puerto 5002\    
    tasks_service.run(port=5002)

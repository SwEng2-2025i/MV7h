from flask import Flask, request, jsonify
from flasgger import Swagger
from modelos.usuario import Usuario
from servicios.notificador import notificar_usuario

app = Flask(__name__)
swagger = Swagger(app)  

usuarios = {}  

@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    """
    Registrar un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id
            - nombre
            - canal_preferido
            - canales_disponibles
          properties:
            id:
              type: integer
            nombre:
              type: string
            canal_preferido:
              type: string
            canales_disponibles:
              type: array
              items:
                type: string
    responses:
      201:
        description: Usuario creado exitosamente
    """
    data = request.json
    usuario = Usuario(
        id=data["id"],
        nombre=data["nombre"],
        canal_preferido=data["canal_preferido"],
        canales_disponibles=data["canales_disponibles"]
    )
    usuarios[data["id"]] = usuario
    return jsonify({"mensaje": "Usuario registrado"}), 201


@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    """
    Obtener un usuario por ID
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del usuario
    responses:
      200:
        description: Usuario encontrado
      404:
        description: Usuario no encontrado
    """
    usuario = usuarios.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "canal_preferido": usuario.canal_preferido,
        "canales_disponibles": usuario.canales_disponibles
    }), 200


@app.route('/notificar/<int:id>', methods=['POST'])
def notificar(id):
    """
    Enviar una notificación a un usuario
    ---
    tags:
      - Notificaciones
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID del usuario
      - in: body
        name: mensaje
        required: true
        schema:
          type: object
          required:
            - mensaje
          properties:
            mensaje:
              type: string
    responses:
      200:
        description: Notificación enviada
      404:
        description: Usuario no encontrado
    """
    mensaje = request.json["mensaje"]
    usuario = usuarios.get(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    exito = notificar_usuario(usuario, mensaje)
    return jsonify({"exito": exito}), 200


if __name__ == "__main__":
    app.run(debug=True)

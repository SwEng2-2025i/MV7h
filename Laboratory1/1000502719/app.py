from flask import Flask,jsonify,request
from flasgger import Swagger
from ManejadorDB import ManejadorDB
from HandlerNotification.NotificationsHandlers import crearCadenaResponsabilidad

app=Flask(__name__)
swagger = Swagger(app,template={
    "info": {
        "title": "Api Doc Laboratory 1",
        "description": "Documentación del laboratorio 1. Julian Esteban Mendoza Wilches.",
        "version": "1.0.0"
    }
})

manejador=ManejadorDB()

@app.route("/users",methods=["GET"])
def getUsers():
    """
    Obtener todos los usuarios registrados
    ---
    tags:
      - Obtener Usuarios
    responses:
      200:
        description: Lista de todos los usuarios
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: Juan Pérez
                  preferred_channel:
                    type: string
                    example: sms
                  available_channels:
                    type: array
                    items:
                      type: string
                    example: ["email", "cel"]
      204:
        description: No hay ningún usuario registrado
    """
  
    if(manejador.getAllUsers()==[]):
        return jsonify({"message":"No hay usuarios registrados"}),204
    return jsonify(manejador.getAllUsers()),200

@app.route("/users",methods=["POST"])
def registerUser():
    """
    Registrar un nuevo usuario (el id se genera automáticamente)
    ---
    tags:
      - Registrar Usuarios
    consumes:
      - application/json
    parameters:
      - in: body
        name: user
        description: Datos para crear el usuario (sin id)
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
              example: Lucas
            preferred_channel:
              type: string
              enum: [sms, email, cel]
              example: email
            available_channels:
              type: array
              items:
                type: string
              example: ["sms", "cel"]
    responses:
      201:
        description: Registro exitoso
        schema:
          type: object
          properties:
            message:
              type: string
              example: Registro Exitoso
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 123
                name:
                  type: string
                  example: María Gómez
                preferred_channel:
                  type: string
                  example: email
                available_channels:
                  type: array
                  items:
                    type: string
                  example: ["sms", "cel"]
    """
    manejador.registerUser(request.json)
    return jsonify({"message":"Registro Exitoso ",
                    "user":request.json}),201

@app.route("/notifications/send",methods=["POST"])
def notificateUser():
    """
    Enviar notificación al usuario según su canal preferido y disponibles
    ---
    tags:
      - Notificar Usuario
    consumes:
      - application/json
    parameters:
      - in: body
        name: userId
        description: ID del usuario a notificar
        required: true
        schema:
          type: object
          required:
            - id
          properties:
            id:
              type: integer
              example: 123
    responses:
      200:
        description: Notificación enviada con éxito
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Notificación exitosa via: email"
      500:
        description: No fue posible enviar la notificación
        schema:
          type: object
          properties:
            message:
              type: string
              example: No fue posible notificar
      404:
        description: No se encontro un usuario con este id
        schema:
          type: object
          properties:
            message:
              type: string
              example: No se encontor un usuario con este id

    """
    usuario=manejador.getUserById(request.json["id"])
    if(usuario==None):
        return jsonify({"messagge":"No se encontor un usuario con este id"}),404
    data={"medio":""}
    cadena=crearCadenaResponsabilidad(usuario.preferred_channel,usuario.available_channels)
    if (cadena.handle(data)):
        manejador.updateUser(usuario.id,data["medio"])
        return jsonify({"message":"Notificación exitosa via: "+data["medio"],
                        "usuario":manejador.getUserById(usuario.id)}),200
    else:
        return jsonify({"message":"No fue posible notificar"}),500

if __name__=='__main__':
    app.run(debug=True,port=5000)

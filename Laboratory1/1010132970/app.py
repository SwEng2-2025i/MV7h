from flask import Flask, request, jsonify
from flasgger import Swagger
from services.chain_builder import build_chain
from services.logger import log

app = Flask(__name__)
swagger = Swagger(app)

users = {}

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    preferred = data.get("preferred_channel")
    available = data.get("available_channels")
    if not name or not preferred or not available:
        return jsonify({"error": "Faltan datos"}), 400
    users[name] = {
        "name": name,
        "preferred_channel": preferred,
        "available_channels": available
    }
    return jsonify({"message": f"Usuario {name} creado."}), 201

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users.values()))

@app.route("/notifications/send", methods=["POST"])
def send_notification():
    data = request.json
    user_name = data.get("user_name")
    message = data.get("message")
    user = users.get(user_name)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    chain = build_chain(user["preferred_channel"], user["available_channels"])
    success = chain.send(user, message)
    if success:
        return jsonify({"message": "Notificación enviada"}), 200
    return jsonify({"message": "Todos los canales fallaron"}), 500

if __name__ == "__main__":
    app.run(debug=True)

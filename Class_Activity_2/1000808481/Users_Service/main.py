from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Agregado
import requests  # 👈 Added for HTTP calls to Task Service

service_a = Flask(__name__)
CORS(service_a)  # 👈 Habilita CORS

service_a.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
service_a.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(service_a)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@service_a.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or not data["name"].strip():
        return jsonify({"error": "El nombre es requerido"}), 400

    user = User(name=data["name"].strip())
    db.session.add(user)
    db.session.commit()
    print({"id": user.id, "name": user.name})
    return jsonify({"id": user.id, "name": user.name}), 201


@service_a.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name})
    return jsonify({"error": "User not found"}), 404


@service_a.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name} for user in users])


# Added endpoint to delete a user and their associated tasks
@service_a.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        # First, check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Try to delete associated tasks by calling Task Service
        try:
            task_service_url = f"http://localhost:5002/tasks/user/{user_id}"
            task_response = requests.delete(task_service_url, timeout=5)
            print(f"Task service response: {task_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not reach Task Service: {e}")
            # Continue with user deletion even if task service is unavailable

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": f"User {user_id} and associated tasks deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)

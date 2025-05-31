from flask import Blueprint, request, jsonify
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)
service = UserService()

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = service.create_user(data)
    return jsonify(user), 201

@user_bp.route('/users', methods=['GET'])
def list_users():
    users = service.list_users()
    return jsonify(users), 200
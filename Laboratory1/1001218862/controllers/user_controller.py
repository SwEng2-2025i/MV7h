from flask import Blueprint, request, jsonify
from models.user import User

user_bp = Blueprint('user_controller', __name__)
users = [] # In memory store

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: User
          required:
            - name
            - preferred_channel
            - available_channels
          properties:
            name:
              type: string
              example: "Juan"
            preferred_channel:
              type: string
              example: "email"
            available_channels:
              type: array
              example: ["email", "sms"]
              items:
                type: string
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User created successfully"
    """
    data = request.json
    user = User(data['name'], data['preferred_channel'], data['available_channels'])
    users.append(user)
    return jsonify({'message': 'User created successfully'}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Get all users
    ---
    tags:
      - Users
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              name:
                type: string
                example: "Juan"
              preferred_channel:
                type: string
                example: "email"
              available_channels:
                type: array
                items:
                  type: string
                example: ["email", "sms"]
      500:
        description: Internal server error
    """
    return jsonify([u.to_dict() for u in users])
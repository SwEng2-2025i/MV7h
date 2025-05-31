from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from utils.logger import Logger

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Register a new user',
    'description': 'Registers a user with a name, preferred communication channel, and a list of available channels.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'UserRegistration',
                'required': ['name', 'preferred_channel', 'available_channels'],
                'properties': {
                    'name': {
                        'type': 'string',
                        'description': 'Unique name of the user.',
                        'example': 'Juan'
                    },
                    'preferred_channel': {
                        'type': 'string',
                        'description': 'The user\'s preferred notification channel (e.g., "email", "sms"). Must be in available_channels.',
                        'enum': ['email', 'sms'],
                        'example': 'email'
                    },
                    'available_channels': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'enum': ['email', 'sms']
                        },
                        'description': 'List of channels available for the user.',
                        'example': ['email', 'sms']
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': 'User "Juan" registered successfully.'},
                    'user': {'type': 'object'}
                }
            }
        },
        400: {
            'description': 'Invalid input or user already exists',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'User with name "Juan" already exists.'}
                }
            }
        }
    }
})
def register_user():
    """
    Register a user with name, preferred and available channels.
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON data."}), 400

    name = data.get('name')
    preferred_channel = data.get('preferred_channel')
    available_channels = data.get('available_channels')

    try:
        # Access user_service from current_app
        user = current_app.user_service.register_user(name, preferred_channel, available_channels)
        return jsonify({"status": "success", "message": f"User '{name}' registered successfully.", "user": user.to_dict()}), 201
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        Logger.log(f"Unexpected error during user registration: {e}")
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500

@api_bp.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'List all registered users',
    'description': 'Retrieves a list of all users currently registered in the system.',
    'responses': {
        200: {
            'description': 'A list of users',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'users': {
                        'type': 'array',
                        'items': {
                            '$ref': '#/definitions/User'
                        }
                    }
                }
            }
        }
    },
    'definitions': {
        'User': {
            'type': 'object',
            'properties': {
                'user_id': {'type': 'string', 'example': 'a1b2c3d4-e5f6-7890-1234-567890abcdef'},
                'name': {'type': 'string', 'example': 'Juan'},
                'preferred_channel': {'type': 'string', 'example': 'email'},
                'available_channels': {
                    'type': 'array',
                    'items': {'type': 'string'},
                    'example': ['email', 'sms']
                }
            }
        }
    }
})
def list_users():
    """
    List all users.
    """
    # Access user_service from current_app
    users = [user.to_dict() for user in current_app.user_service.get_all_users()]
    return jsonify({"status": "success", "users": users}), 200

@api_bp.route('/notifications/send', methods=['POST'])
@swag_from({
    'tags': ['Notifications'],
    'summary': 'Send a notification',
    'description': 'Sends a notification to a specified user with a message and priority. The system attempts delivery through available channels using a Chain of Responsibility.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'NotificationSend',
                'required': ['user_name', 'message', 'priority'],
                'properties': {
                    'user_name': {
                        'type': 'string',
                        'description': 'The name of the user to send the notification to.',
                        'example': 'Juan'
                    },
                    'message': {
                        'type': 'string',
                        'description': 'The content of the notification message.',
                        'example': 'Your appointment is tomorrow.'
                    },
                    'priority': {
                        'type': 'string',
                        'description': 'The priority of the notification.',
                        'enum': ['high', 'medium', 'low'],
                        'example': 'high'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Notification delivery attempt result',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'success'},
                    'message': {'type': 'string', 'example': 'Notification sent successfully.'},
                    'logs': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': 'Detailed logs of the notification delivery process.'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input or user not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string', 'example': 'error'},
                    'message': {'type': 'string', 'example': 'User "Juan" not found.'}
                }
            }
        }
    }
})
def send_notification():
    """
    Send a notification with message and priority.
    """
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON data."}), 400

    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority')

    if not user_name or not message or not priority:
        return jsonify({"status": "error", "message": "Missing required fields: user_name, message, priority."}), 400

    # Access notification_service from current_app
    result = current_app.notification_service.send_notification(user_name, message, priority)
    status_code = 200 if result["status"] in ["success", "failed"] else 400 # 400 for user/priority not found
    return jsonify(result), status_code



#import tests

from flask import Flask, jsonify, request
from flasgger import Swagger


from src.core.logger.logger import Logger
from src.utils.users import Users
from src.utils.notification import Notification
from src.models.user import User

users = Users()
logger = Logger()

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/users', methods=['POST'])
def new_user():
  """
    Create a new user
    ---
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          required:
            - name
            - preferred_channel
            - avalible_channels
          properties:
            name:
              type: string
              description: Name of the user
              example: "Pedro"
            preferred_channel:
              type: string
              description: Communication channel preferred by the user
              example: "sms"
            avalible_channels:
              type: array
              description: List of avalible channels
              example: ["sms", "email", "phonecall"]
            
    responses:
      201:
        description: User created
      400:
        description: Invalid input
    """
  data = request.json
  try: 
    user = User(
      data["name"], 
      data["preferred_channel"],
      data["avalible_channels"]
      )
    return jsonify(users.new_user(user)), 201
  except Exception as e:
     return jsonify({"error"}, str(e)), 400

@app.route('/users', methods=['GET'])  
def list_users():
   
  """
    List all users
    ---
            
    responses:
      201:
        description: Users Listed
    """
  return jsonify(users.list_users()), 201

@app.route('/notifications/send', methods=['POST'])
def send_notification():
  """
    Send a notification to an user
    ---
    parameters:
      - in: body
        name: notification
        required: true
        schema:
          type: object
          required:
            - user_name
            - message
            - priority
          properties:
            user_name:
              type: string
              description: Name of the user
              example: "Pedro"
            message:
              type: string
              description: Message of the notification
              example: "The toilet is clogged again"
            priority:
              type: array
              description: Assigns a priority to the notification
              example: "high"
            
    responses:
      201:
        description: Notification send
      404:
        description: User not found
      500:
        description: Notification not send
    """
  data = request.json
  user = users.get_user(data["user_name"])

  if user == False:
    return jsonify({"error": "User not found"}), 404

  notification = Notification(user, data["message"], data["priority"])

  result = notification.send_notification()

  if result:
    return jsonify(logger.logs()), 201
  return jsonify(logger.logs()), 500

if __name__=="__main__":
  app.run(debug=True)





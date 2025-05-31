from flask import Flask
from controllers.user_controller import user_bp
from controllers.notification_controller import notif_bp
from flask import Flask, request, jsonify
from models.user import UserStore
from notifications.chain import NotificationChain

app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(notif_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

app = Flask(__name__)
store = UserStore()
chain = NotificationChain()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = store.add_user(
        name=data['name'],
        preferred=data['preferred_channel'],
        channels=data['available_channels']
    )
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def list_users():
    return jsonify([u.to_dict() for u in store.get_all()]), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    result = chain.send(
        user=store.find_by_name(data['user_name']),
        message=data['message'],
        priority=data['priority']
    )
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
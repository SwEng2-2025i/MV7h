from flask import request, jsonify

# Antes: def create_http_handler(use_case) -> Flask
# Ahora: recibe app existente y registre ahí rutas:
def create_http_handler(app, use_case):
    @app.route("/users", methods=["POST"])
    def register_user():
        data = request.json
        use_case.register_user(
            name=data["name"],
            preferred_channel=data["preferred_channel"],
            available_channels=data["available_channels"]
        )
        return jsonify({"message": "User registered successfully"}), 201

    @app.route("/users", methods=["GET"])
    def list_users():
        users = use_case.get_all_users()
        return jsonify(users), 200

    @app.route("/notifications/send", methods=["POST"])
    def send_notification():
        data = request.json
        success = use_case.send_notification(
            user_name=data["user_name"],
            message=data["message"],
            priority=data.get("priority", "normal")
        )
        return jsonify({"success": success}), 200

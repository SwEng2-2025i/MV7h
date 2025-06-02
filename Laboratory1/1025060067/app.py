# app.py
from flask import Flask
from flasgger import Swagger
from api.api import api_bp
from services.user_service import UserService
from services.notification_service import NotificationService
from utils.logger import Logger

def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {
        "title": "Multichannel Notification System API",
        "uiversion": 3,
        "specs_route": "/swagger/"
    }

    # Initialize Swagger
    Swagger(app)

    # Initialize services (in-memory)
    # These instances will be shared across the application via app.config or a similar mechanism
    # For simplicity, we'll pass them directly to the blueprint's context if needed,
    # or rely on them being accessible in the global scope for the api.py routes.
    # A more robust solution for larger apps might use Flask's application context or a dependency injection container.
    app.user_service = UserService()
    app.notification_service = NotificationService(app.user_service)

    # Register the API blueprint
    app.register_blueprint(api_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    # Clear logs at application start for fresh testing
    Logger.clear_logs()
    app.run(debug=True, port=5000)



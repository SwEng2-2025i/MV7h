from flask import Flask
from flasgger import Swagger
from controllers.user_controller import user_bp
from controllers.notification_controller import notification_bp

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Notification API",
        "description": "API for sending notifications and managing users",
        "version": "1.0.0"
    }
}

app = Flask(__name__)
swagger = Swagger(app, template=swagger_template)
app.register_blueprint(user_bp)
app.register_blueprint(notification_bp)

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from adapters.memory_repo import InMemoryUserRepository
from adapters.http_handler.http_api import create_http_handler
from use_cases.notification_use_case import NotificationUseCase


app = Flask(__name__)


@app.route('/swagger.yaml')
def swagger_spec():
    return send_from_directory(os.getcwd(), 'swagger.yaml')


SWAGGER_URL = '/docs'
API_URL     = '/swagger.yaml'
swaggerui_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={ 'app_name': "Multichannel Notification System" }
)
app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

repo    = InMemoryUserRepository()
usecase = NotificationUseCase(repo)

create_http_handler(app, usecase)

if __name__ == "__main__":
    app.run(debug=True)

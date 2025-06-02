from flasgger import Swagger

def init_swagger(app):
    template = {
        "swagger": "2.0",
        "info": {
            "title": "API de Notificaciones",
            "description": "Sistema de notificaciones multicanal (Chain of Responsibility + Factory + Singleton)",
            "version": "1.0"
        },
        "schemes": [
            "http",
            "https"
        ]
    }
    Swagger(app, template=template)

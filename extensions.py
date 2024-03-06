from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flasgger import Swagger


db = SQLAlchemy()
jwt = JWTManager()

# swagger config 
# swagger = Swagger()
template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask API AUTH",
        "description": "A basic auth api with JWT token based authentication and swagger documentation",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your bearer token in the format **Bearer &lt;token>**"
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs1',
            "route": '/docs_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(template=template, config=swagger_config)

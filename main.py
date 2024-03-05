from flask import Flask, jsonify
from extensions import db, jwt, JWTManager
from auth import auth_bp
from users import user_bp
from models import User, TokenBlockList

def create_app():
    app = Flask(__name__)  # Create a Flask app with the current module name
    # app.config.from_prefixed_env()  # Load configuration from prefixed environment variables
    # db.init_app(app)

    # Load configuration settings into the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress the warning
    app.config['JWT_SECRET_KEY'] = 'f613421a23df8917e75a7dfb'
    
    db.init_app(app)  # Initialize the database with the Flask app
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/users')

    # load user
    @jwt.user_lookup_loader
    def user_lookup_callback(__jwt_headers, jwt_data):

        identity = jwt_data['sub']
        
        return User.query.filter_by(username=identity).one_or_none()

    # additional permissions to some users
    @jwt.additional_claims_loader
    def make_additional_permissions(identity):
        if identity == "user1":
            return {"employee": True }
        return {"employee": False }


    # jwt error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired", "error": "token_expired" }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"message": "Token is invalid", "error": "invalid_token" }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({"message": "Token is missing", "error": "authorization_required" }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return jsonify({"message": "Token is not fresh", "error": "fresh_token_required" }), 401

    @jwt.revoked_token_loader
    def revoked_token_loader_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token has been revoked", "error": "token_revoked" }), 401

    @jwt.token_in_blocklist_loader
    def token_in_blockkist(jwt_headers, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlockList).filter(TokenBlockList.jti==jti).scalar()
        return token is not None           

    # Shell context processor to automatically import "db" into shell
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}
    
    # You can add routes or other configurations here

    return app 

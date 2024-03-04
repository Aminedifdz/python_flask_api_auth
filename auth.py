from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt, current_user, 
                                get_jwt_identity
                                )
from models import User, TokenBlockList

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register_user():
    data = request.get_json()
    print(data)
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"message": "Missing username or password"}), 400

    user = User.get_user_by_username(data.get('username'))

    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    user = User(
        username=data.get('username'),
        # password=data.get('password'),
        email=data.get('email'),
    )

    user.set_password(password=data.get('password'))

    user.save()

    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201
    

@auth_bp.post('/login')
def login_user():
    data = request.get_json()
    print(data)
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Missing username or password"}), 400

    user = User.get_user_by_username(username=data.get('username'))

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not user.check_password(password=data.get('password')):
        return jsonify({"message": "Invalid password"}), 401

    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    return jsonify({
        "message": "Login successful",
        "tokens": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    }), 200


@auth_bp.get('/whoami')
@jwt_required() 
def whoami():
    claims = get_jwt()
    user = User.get_user_by_username(claims['sub'])
    
    return jsonify({"message": "Whoami successful", "user_details": {
        "username": current_user.username,
        "email": current_user.email
    } }), 200   


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200

@auth_bp.get('/revoke_token')
@jwt_required(verify_type=False)
def logout_user():
    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_blocklist = TokenBlockList(jti=jti)

    token_blocklist.save()

    return jsonify({"message": f"{token_type} revoked successfully "}), 200

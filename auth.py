from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import (create_access_token, create_refresh_token, 
                                jwt_required, get_jwt, current_user, 
                                get_jwt_identity
                                )
from models import User, TokenBlockList
from flask_restx import Resource, Namespace

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/register')
def register_user():

    """
    Register a new user
    ---
    tags:
      - Auth
    description: Create a new user account.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
              - password
            properties:
              username:
                type: string
                example: newuser
              email:
                type: string
                example: newuser@example.com
              password:
                type: string
                example: strongpassword
    responses:
      201:
        description: User registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User registered successfully
      400:
        description: Invalid request (missing required fields, user already exists, etc.)
    """

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

    """
    User login
    ---
    tags:
      - Auth
    description: Authenticate user and return access and refresh tokens.
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                example: johndoe
              password:
                type: string
                example: password123
    responses:
      200:
        description: Login successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Login successful
                tokens:
                  type: object
                  properties:
                    access_token:
                      type: string
                    refresh_token:
                      type: string
      400:
        description: Missing username or password
      401:
        description: Invalid password
      404:
        description: User not found
    """

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

    """
    Get current user information
    ---
    tags:
      - Auth
    description: Return current user details.
    security:
      - bearerAuth: []
    responses:
      200:
        description: Whoami successful
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Whoami successful
                user_details:
                  type: object
                  properties:
                    username:
                      type: string
                      example: johndoe
                    email:
                      type: string
                      example: johndoe@example.com
    """

    claims = get_jwt()
    user = User.get_user_by_username(claims['sub'])
    
    return jsonify({"message": "Whoami successful", "user_details": {
        "username": current_user.username,
        "email": current_user.email
    } }), 200   


@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh():

    """
    Refresh access token
    ---
    tags:
      - Auth
    description: Refresh the access token using the refresh token.
    security:
      - bearerAuth: []
    responses:
      200:
        description: Access token refreshed successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
    """

    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200

@auth_bp.get('/revoke_token')
@jwt_required(verify_type=False)
def logout_user():

    """
    Revoke a token (logout)
    ---
    tags:
      - Auth
    description: Revoke the current access or refresh token.
    security:
      - bearerAuth: []
    responses:
      200:
        description: Token revoked successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "<token_type> revoked successfully"
    """

    jwt = get_jwt()

    jti = jwt['jti']
    token_type = jwt['type']

    token_blocklist = TokenBlockList(jti=jti)

    token_blocklist.save()

    return jsonify({"message": f"{token_type} revoked successfully "}), 200

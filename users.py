from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required , get_jwt
from models import User
from schemas import UserSchema


user_bp = Blueprint('user', __name__)


@user_bp.get('/all')
@jwt_required()
def get_all_users():
    """
    Retrieves all users from the database based on pagination parameters.

    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - in: query
        name: page
        schema:
          type: integer
          default: 1
        description: Page number for pagination
      - in: query
        name: per_page
        schema:
          type: integer
          default: 3
        description: Users per page for pagination
    responses:
      200:
        description: A JSON object containing the list of users
        content:
          application/json:
            schema:
              type: object
              properties:
                users:
                  type: array
                  items:
                    type: object
      401:
        description: Unauthorized access
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    
    claims = get_jwt()

    if claims.get('employee') == True:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)

        users = User.query.paginate(
            page=page,
            per_page=per_page
        )
        
        users_schema = UserSchema(many=True)
        results = users_schema.dump(users)

        print(results)
        
        return jsonify({
            "users": results,
        }), 200


    return jsonify({"message": "Your not authorized to access this."}), 401

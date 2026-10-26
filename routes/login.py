from flask import current_app, jsonify, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from application.database import db
from application.models import User, UserRoles, Roles
from werkzeug.security import check_password_hash


class Login(Resource):
    def __init__(self):
        self.auth_imput_fields = reqparse.RequestParser()
        self.auth_imput_fields.add_argument('username', type=str, required=True)
        self.auth_imput_fields.add_argument('password', type=str, required=True)

    def get(self):
        # Implement the logic to handle GET requests for login
        return {"message": "Login GET endpoint"}, 200

    def post(self):
        args = self.auth_imput_fields.parse_args()
        username = args['username']
        password = args['password']

        existing_user = User.query.filter_by(name=username).first()
        if existing_user is None:
            return {"message": "User not found"}, 404

        isvalid_password = check_password_hash(existing_user.password_hash, password)
        if not isvalid_password:
            return {"message": "Invalid password"}, 401

        user_roles = UserRoles.query.filter_by(user_id=existing_user.id).all()
        role_names = [Roles.query.get(role.role_id).name for role in user_roles] 
        access_token = create_access_token(identity=username, additional_claims={"roles": role_names})
        refresh_token = create_refresh_token(identity=username)

        response = make_response(jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "roles": role_names,           # return names so Vue can read them
            "status_code": 200
        }), 200)
        response.set_cookie('refresh_token', refresh_token, httponly=True)  # refresh in cookie, not access
        return response

    def put(self):
        return {"message": "Login PUT endpoint"}, 200

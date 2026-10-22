from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from application.response import *


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
        existing_user = current_app.db.session.query(current_app.models.User).filter_by(name=username)
        if existing_user is None:
            return {"message": "User not found"}, 404
        else:
            isvalid_password = current_app.models.User.verify_password(existing_user.password_hash, password)
            if not isvalid_password:
                return {"message": "Invalid password"}, 401
            else:
                user_roles = current_app.db.session.query(current_app.models.UserRoles).filter_by(user_id=existing_user.id).all()
                access_token = create_access_token(identity=username, additional_claims={"roles": [role.role_id for role in user_roles]})
                refresh_token = create_refresh_token(identity=username)
                response = create_response("Login successful", 200)
                response.set_cookie('access_token', access_token, httponly=True)
                return response

    def put(self):
        
        return {"message": "Login PUT endpoint"}, 200
        
       
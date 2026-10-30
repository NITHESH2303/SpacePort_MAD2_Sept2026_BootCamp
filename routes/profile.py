from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse

from application.utils import jwt_required_with_roles

class Profile(Resource):
    
    def __init__(self):
        self.profile_input_fields = reqparse.RequestParser()
        self.profile_input_fields.add_argument('username', type=str, required=False, location='args')
    
    @jwt_required()
    @jwt_required_with_roles(['customer', 'admin', 'employee'])
    def get(self):
        args = self.profile_input_fields.parse_args()
        current_user = get_jwt_identity()
        arg_username = args.get('username') or current_user
        claims = get_jwt()
        roles = claims.get("roles", [])
        return {
            "message": f"Hello, {arg_username}! Your roles are: {roles}",
            "user": current_user,
            "roles": roles
        }, 200
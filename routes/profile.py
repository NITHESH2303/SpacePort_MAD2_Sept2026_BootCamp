from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse

class Profile(Resource):
    
    def __init__(self):
        self.profile_input_fields = reqparse.RequestParser()
        self.profile_input_fields.add_argument('username', type=str, required=True)
    
    @jwt_required()
    def get(self):
        args = self.profile_input_fields.parse_args()
        arg_username = args['username']
        current_user = get_jwt_identity()
        claims = get_jwt()
        roles = claims.get("roles", [])
        return {
            "message": f"Hello, {current_user}! Your roles are: {roles}"
        }, 200
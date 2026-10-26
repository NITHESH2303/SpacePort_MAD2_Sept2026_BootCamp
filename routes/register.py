from flask import current_app
from flask_restful import Resource, reqparse
from application.response import create_response
from application.database import db
from application.models import User, Roles, UserRoles
from werkzeug.security import generate_password_hash, check_password_hash

class Register(Resource):
    
    def __init__(self):
        self.register_input_fields = reqparse.RequestParser()
        self.register_input_fields.add_argument('username', type=str, required=True)
        self.register_input_fields.add_argument('password', type=str, required=True)

    def post(self):
        args = self.register_input_fields.parse_args()
        username = args['username']
        password = args['password']

        if not username or not password:
            return create_response("Username and password are required.", 400)

        existing_user = User.query.filter_by(name=username).first()
        if existing_user:
            return create_response("Username already exists.", 400)

        hashed_password = generate_password_hash(password)
        new_user = User(name=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        default_role = Roles.query.filter_by(name='customer').first()
        if not default_role:
            default_role = Roles(name='customer', description='Standard Customer')
            db.session.add(default_role)
            db.session.commit()

        new_user_role = UserRoles(user_id=new_user.id, role_id=default_role.id)
        db.session.add(new_user_role)
        db.session.commit()

        return create_response("User registered successfully.", 201)
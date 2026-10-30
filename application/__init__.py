from flask import Flask, g
import os
from application.database import db
from flask_migrate import Migrate
from application import models
from flask_jwt_extended import JWTManager,verify_jwt_in_request, get_jwt
from application.PreProcess import PreProcess
from flask_cors import CORS
from datetime import timedelta
from application.redis_client import redis_client

# /SpacePort/application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(f"BASE_DIR: {BASE_DIR}")
# /SpacePort
ROOT_DIR = os.path.dirname(BASE_DIR)
print(f"ROOT_DIR: {ROOT_DIR}")
# /SpacePort/db
DB_PATH = os.path.join(ROOT_DIR, "db", "spacePort.sqlite3")
print(f"DB_PATH: {DB_PATH}")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{DB_PATH}')
    app.config['FLASK_PASSWORD_SALT'] = os.environ.get('FLASK_PASSWORD_SALT', 'this is bad, change it')
    app.config['FLASK_PASSWORD_HASH'] = os.environ.get('FLASK_PASSWORD_HASH', 'argon2')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret-spaceport-jwt-token-key-2026')
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=15)
    
    
    # ref : https://manpages.debian.org/testing/python3-flask-cors/flask-cors.1#CORS_SUPPORTS_CREDENTIALS
    print(os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173"))
    allowes_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    cors = CORS(
        app, 
        resources={r"/*": {"origins": allowes_origins, "supports_credentials": True}},
    )
    
    jwt = JWTManager(app)
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    with app.app_context():
        db.init_app(app)
        migrate = Migrate(app, db)
        migrate.init_app(app, db)
        try:
            db.create_all()
            PreProcess()
            print("DB Creation Done!!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    @app.before_request
    def load_roles_jwt():
        try:
        # when user sign up -> if optional was false -> jwt token won't be available for new user -> 401 Exception (Unauthorised)
            verify_jwt_in_request(optional=True)
            claims = get_jwt()
            g.roles = claims.get("roles", [])
        except Exception as e:
            g.roles = []
    return app

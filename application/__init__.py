from flask import Flask
import os
from application.database import db
from flask_migrate import Migrate
from application import models

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
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    with app.app_context():
        db.init_app(app)
        migrate = Migrate(app, db)
        migrate.init_app(app, db)
        try:
           
            db.create_all()
        except Exception as e:
            print(f"Error creating database tables: {e}")
    return app

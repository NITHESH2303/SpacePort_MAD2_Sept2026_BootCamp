from flask import Flask
from application import create_app

app = create_app()

from flask_restful import Api
from routes.login import Login

api = Api(app)
api.add_resource(Login, '/login')

if __name__ == "__main__":
    app.run(debug=False)
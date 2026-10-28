from flask import Flask
from flask_restful import Api
from application import create_app
from routes.login import Login
from routes.register import Register
from routes.profile import Profile
from routes.booking import BookingSpaceCraft
from application.spacecraft import SpaceCraftResource

app = create_app()

api = Api(app)
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Profile, '/profile')
api.add_resource(SpaceCraftResource, '/spacecraft', '/spacecraft/<int:craft_id>')
api.add_resource(BookingSpaceCraft, '/booking')

if __name__ == "__main__":
    app.run(debug=False)

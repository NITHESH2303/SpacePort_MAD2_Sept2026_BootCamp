from flask import Flask
from flask_restful import Api
from application import create_app
from routes.login import Login
from routes.register import Register
from routes.profile import Profile
from routes.booking import BookingSpaceCraft
from application.spacecraft import SpaceCraftResource
from application.celery_app import celery, init_celery
import application.tasks
from routes.export import export_bp

app = create_app()

app.register_blueprint(export_bp)

api = Api(app)
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')
api.add_resource(Profile, '/profile')
api.add_resource(SpaceCraftResource, '/spacecraft', '/spacecraft/<int:craft_id>')
api.add_resource(BookingSpaceCraft, '/booking')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/14'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/14'

init_celery(celery, app)

if __name__ == "__main__":
    app.run(debug=False)

from application.database import db
from application.models import SpaceCraft as SpaceCraftModel
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

class SpaceCraftResource(Resource):
    def __init__(self):
        self.spacecraft_input_fields = reqparse.RequestParser()
        self.spacecraft_input_fields.add_argument('name', type=str, required=True, location='json')
        self.spacecraft_input_fields.add_argument('type', type=str, required=True, location='json')
        self.spacecraft_input_fields.add_argument('capacity', type=int, required=True, location='json')
        
    
    def get(self):
        spacecrafts = SpaceCraftModel.query.all()
        result = [
            {
                "id": spacecraft.id,
                "name": spacecraft.name,
                "type": spacecraft.type,
                "capacity": spacecraft.capacity
            } for spacecraft in spacecrafts
        ]
        return {"spacecrafts": result}, 200

    @jwt_required()
    def post(self):
        args = self.spacecraft_input_fields.parse_args()
        name = args['name']
        type = args['type']
        capacity = args['capacity']

        new_spacecraft = SpaceCraftModel(name=name, type=type, capacity=capacity)  # fixed
        db.session.add(new_spacecraft)
        db.session.commit()

        return {"message": "Spacecraft created successfully", "spacecraft": {
            "id": new_spacecraft.id,
            "name": new_spacecraft.name,
            "type": new_spacecraft.type,
            "capacity": new_spacecraft.capacity
        }}, 201
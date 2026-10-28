from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.database import db
from application.models import User, SpaceCraft, Booking
from datetime import datetime


class BookingSpaceCraft(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('spacecraft_id', type=int, required=True, location='json')

    @jwt_required()
    def get(self):
        current_username = get_jwt_identity()
        user = User.query.filter_by(name=current_username).first()
        if not user:
            return {"message": "User not found"}, 404

        bookings = Booking.query.filter_by(user_id=user.id).all()
        result = [
            {
                "id": b.id,
                "spacecraft_id": b.spacecraft_id,
                "spacecraft_name": b.spacecraft.name if b.spacecraft else "Unknown",
                "spacecraft_type": b.spacecraft.type if b.spacecraft else "N/A",
                "booking_date": b.booking_date.strftime("%Y-%m-%d %H:%M:%S") if b.booking_date else ""
            } for b in bookings
        ]
        return {"bookings": result}, 200

    @jwt_required()
    def post(self):
        args = self.parser.parse_args()
        spacecraft_id = args['spacecraft_id']

        current_username = get_jwt_identity()
        user = User.query.filter_by(name=current_username).first()
        if not user:
            return {"message": "User not found"}, 404

        craft = SpaceCraft.query.get(spacecraft_id)
        if not craft:
            return {"message": "Spacecraft not found"}, 404

        # Check if already booked by this user
        is_booked = Booking.query.filter_by(spacecraft_id=craft.id, user_id=user.id).first()
        if is_booked:
            return {"message": "You have already booked this spacecraft"}, 400

        # Check capacity
        current_count = Booking.query.filter_by(spacecraft_id=craft.id).count()
        if current_count >= craft.capacity:
            return {"message": "Spacecraft capacity limit exceeded"}, 400

        new_booking = Booking(
            user_id=user.id,
            spacecraft_id=craft.id,
            booking_date=datetime.utcnow()
        )
        db.session.add(new_booking)
        db.session.commit()

        return {
            "message": "Booked successfully",
            "booking": {
                "id": new_booking.id,
                "spacecraft_id": craft.id,
                "spacecraft_name": craft.name
            }
        }, 201

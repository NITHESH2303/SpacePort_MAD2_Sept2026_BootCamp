from flask import current_app
from application.database import db
from datetime import datetime
from flask_security import RoleMixin, UserMixin

class Model(db.Model):
    __abstract__ = True
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserRoles(Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

class User(Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Roles(Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))

class SpaceCraft(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class Booking(Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spacecraft_id = db.Column(db.Integer, db.ForeignKey('space_craft.id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    spacecraft = db.relationship('SpaceCraft', backref=db.backref('bookings', lazy=True))
    
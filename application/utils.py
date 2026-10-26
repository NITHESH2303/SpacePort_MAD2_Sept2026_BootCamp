from functools import wraps
from flask_jwt_extended import get_jwt
from flask import abort, jsonify
from flask import g

def jwt_required_with_roles(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not set(required_roles).intersection(set(g.roles)):
                abort(403, description="You do not have the required roles to access this resource.")
            return fn(*args, **kwargs)
        return wrapper
    return decorator
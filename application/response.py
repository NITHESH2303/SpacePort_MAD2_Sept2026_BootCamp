from flask import jsonify, make_response

def create_response(message, status_code):
    response = {
        "message": message,
        "status_code": status_code
    }
    return make_response(jsonify(response), status_code)
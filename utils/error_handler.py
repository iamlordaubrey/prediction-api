from datetime import datetime, timezone

from flask import jsonify


def handle_error(message, status_code, error_code=None):
    """
    Return a JSON response with the error message and status code.
    """
    error_response = {
        'error': message,
        'status_code': status_code,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }

    if error_code:
        error_response['error_code'] = error_code

    response = jsonify(error_response)
    response.status_code = status_code

    return response

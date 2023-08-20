from functools import wraps
import jwt
from flask import request, jsonify


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        if not token:
            return jsonify({'error': 'sem autorização para este acesso'}), 403
        decoded = jwt.decode(token, verify=False, options={'verify_signature': False})
        current_user = (decoded['id'])

        return f(current_user=current_user, *args, **kwargs)

    return wrapper
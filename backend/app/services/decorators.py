from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapped(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    "msg": "Access denied",
                    "required_roles": list(allowed_roles),
                    "your_role": user_role
                }), 403

            return fn(*args, **kwargs)
        return wrapped
    return decorator


def active_user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapped(*args, **kwargs):
        claims = get_jwt()
        user_role = claims.get('role')

        if user_role and user_role.startswith('BLOCKED_'):
            return jsonify({
                "msg": "Your account has been blocked. Please contact admin."
            }), 403

        return fn(*args, **kwargs)
    return wrapped
from functools import wraps

from flask import request
import jwt


class Middleware:
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]

            if not token:
                return {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

            try:
            	data = jwt.decode(token, key="secret", algorithms=["HS256"])

            	current_user=

import datetime
from functools import wraps

from flask import request
from flask.json import jsonify
import jwt

from controllers.UserController import Controller


def gen_token(data: dict, key: str, seconds: int):
    datetime_now = datetime.datetime.now()
    expiration_delta = datetime.timedelta(seconds=seconds)
    expiration_time = (datetime_now + expiration_delta).strftime('%s')

    payload = data | {
        "iat": datetime_now.strftime('%s'),
        "exp": expiration_time
    }

    return jwt.encode(payload, key, algorithm="HS256")


def renew_access_token(refresh_token: str):
    try:
        data = jwt.decode(refresh_token, key="secret1", algorithms=["HS256"])

        access_token = gen_token(
            {"email": data["email"]}, "secret", seconds=30)

        return access_token
    except Exception as e:
        return "Refresh token invalid, log in again"


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        controller = Controller()
        access_token = None
        user = None

        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

        if not access_token:
            return {
                "message": "Authentication token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        try:
            data = jwt.decode(access_token, key="secret", algorithms=["HS256"])

            user = controller.get_user(data["email"])

            if user is None:
                return jsonify({
                    "message": "User in access token doesn't exist!",
                    "data": None,
                    "error": "Unauthorized"
                })

        except Exception as e:
            return jsonify({
                "message": "Authentication token is invalid",
                "data": None,
                "erorr": str(e)
            })

        return f(user, *args, **kwargs)

    return decorated

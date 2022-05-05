from functools import wraps
from flask import request, jsonify, make_response
import jwt

from .controllers import *
from .utils import *
from .models import *

from Core import app


@app.route("/token", methods=["GET"])
def token():
    refresh_token = request.form["token"]
    refresh_token_controller = RefreshTokenController()

    if not refresh_token:
        return make_response(jsonify({
            "message": "Failed.",
            "data": None,
            "error": "Refresh token missing."
        }), 401)

    if not refresh_token_controller.get_by_token(refresh_token):
        return make_response(jsonify({
            "message": "Failed.",
            "data": None,
            "error": "Refresh token doesn't exist."
        }), 401)

    try:
        decode_refresh(refresh_token)

        access_token = renew_access(refresh_token)

        return make_response(jsonify({
            "message": "Successfully generated access token.",
            "data": {
                "token": access_token
            }
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "message": "Refresh token is invalid.",
            "data": None,
            "error": str(e)
        }), 401)


@app.route("/register", methods=["POST"])
def register():
    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    user_controller.add(email, password)

    return make_response(jsonify({
        "message": "Successfully registered",
        "data": {
            "email": email,
            "password": password
        }
    }), 200)


@app.route("/login", methods=["POST"])
def login():
    refresh_token_controller = RefreshTokenController()
    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    if user_controller.check_psw(email, password):
        access_token = gen_access_token({"email": email})
        refresh_token = gen_refresh_token({"email": email})

        refresh_token_controller.add(refresh_token)

        return make_response(jsonify({
            "message": "Successfully logged in",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }), 200)
    else:
        return make_response(jsonify({
            "message": "Log in failed",
            "data": None,
            "error": "Unauthorized"
        }), 401)


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        user = None

        user_controller = UserController()

        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

        if not access_token:
            return make_response(jsonify({
                "message": "Authentication token is missing!",
                "data": None,
                "error": "Unauthorized"
            }), 401)

        print("Is this happening?")

        try:
            data = decode_access(access_token)

            user = user_controller.get_by_email(data["email"])

            if user is None:
                return make_response(jsonify({
                    "message": "User in access token doesn't exist!",
                    "data": None,
                    "error": "Unauthorized"
                }), 401)

        except Exception as e:
            return make_response(jsonify({
                "message": "Authentication token is invalid",
                "data": None,
                "erorr": str(e)
            }), 401)

        return f(user, *args, **kwargs)

    return decorated

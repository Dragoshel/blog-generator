from functools import wraps
from http import HTTPStatus
from flask import request, jsonify, make_response
import jwt

from .controllers import *
from .utils import *
from .models import *

from Core import HttpRes, app


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        MISSING_TOKEN_RES = HttpRes(
            code=HTTPStatus.UNAUTHORIZED
        ).make_response()
        MISSING_TOKEN_RES.headers["WWW-Authenticate"] = "Bearer realm=\"Access to the builder website is protected.\""

        EXPIRED_TOKEN_RES = HttpRes(
            code=HTTPStatus.UNAUTHORIZED
        ).make_response()
        EXPIRED_TOKEN_RES.headers["WWW-Authenticate"] = "Bearer realm=\"Access to the builder website is protected.\",error=\"expired_token\",error_description=\"The token provided expired.\""

        access_token = None
        user = None

        if "Authorization" in request.headers:
            access_token = request.headers["Authorization"].split(" ")[1]

        if not access_token:
            return MISSING_TOKEN_RES

        user_controller = UserController()

        res_token = decode_access(access_token)

        if res_token.is_not_ok():
            if isinstance(res_token.err, jwt.ExpiredSignatureError):
                return EXPIRED_TOKEN_RES

            return MISSING_TOKEN_RES

        email = res_token.ok["email"]

        res_user = user_controller.get_by_email(email)

        if res_user.is_not_ok():
            return MISSING_TOKEN_RES

        user = res_user.ok

        return f(user, *args, **kwargs)

    return decorated


@app.route("/authenticate", methods=["GET"])
@require_login
def authenticate(user):
    return HttpRes(
        ok="Authenticated",
        data={
            "email": user.email
        }
    ).make_response()


@app.route("/token", methods=["POST"])
def token():
    MISSING_TOKEN_RES = HttpRes(
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()
    MISSING_TOKEN_RES.headers["WWW-Authenticate"] = "Bearer realm=\"Access to the builder website is protected.\""

    EXPIRED_TOKEN_RES = HttpRes(
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()
    EXPIRED_TOKEN_RES.headers["WWW-Authenticate"] = "Bearer realm=\"Access to the builder website is protected.\",error=\"expired_token\",error_description=\"The token provided expired.\""

    refresh_token = None

    if "Authorization" in request.headers:
        refresh_token = request.headers["Authorization"].split(" ")[1]

    if not refresh_token:
        return MISSING_TOKEN_RES

    refresh_token_controller = RefreshTokenController()

    res_token = decode_refresh(refresh_token)

    if res_token.is_not_ok():
        if isinstance(res_token.err, jwt.ExpiredSignatureError):
            return EXPIRED_TOKEN_RES
        return MISSING_TOKEN_RES

    if refresh_token_controller \
        .get_by_token(refresh_token) \
            .is_not_ok():
        return MISSING_TOKEN_RES

    email = res_token.ok["email"]

    res = renew_access(email)

    if res.is_not_ok():
        return MISSING_TOKEN_RES

    return HttpRes(
        ok="Successfully generated access token.",
        data={
            "token": res.ok
        }
    ).make_response()


@app.route("/register", methods=["POST"])
def register():
    ERR_HTTP_RES = HttpRes(
        err="Something went wrong while trying to register.",
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()

    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    if user_controller.add(email, password).is_not_ok():
        return ERR_HTTP_RES

    return HttpRes(
        ok="Successfully registered.",
        data={
            "email": email,
            "password": password
        }
    ).make_response()


@app.route("/login", methods=["POST"])
def login():
    ERR_HTTP_RES = HttpRes(
        err="Something went wrong while trying to log in.",
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()

    refresh_token_controller = RefreshTokenController()
    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    user_res = user_controller.get_by_email(email)

    if user_res.is_not_ok():
        return ERR_HTTP_RES

    pwd_res = user_controller.check_pwd(user_res.ok, password)

    if pwd_res.is_not_ok():
        return ERR_HTTP_RES

    access_token = gen_access_token({"email": email})
    refresh_token = gen_refresh_token({"email": email})

    if refresh_token_controller.add(refresh_token).is_not_ok():
        return ERR_HTTP_RES

    return HttpRes(
        ok="Successfully logged in.",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    ).make_response()

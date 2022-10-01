from functools import wraps
from http import HTTPStatus
from flask import request
import jwt

from .controllers import *
from .utils import *
from .models import *

from Core import HttpRes, app


def MISSING_TOKEN_RES():
    response = HttpRes(
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()
    response.headers["WWW-Authenticate"] = ("Bearer realm="
                                            "{\"error_title\": \"Access to this website is protected\"}")
    response.headers["Access-Control-Expose-Headers"] = "WWW-Authenticate"

    return response


def BAD_TOKEN_RES():
    return MISSING_TOKEN_RES()


def EXPIRED_TOKEN_RES():
    response = HttpRes(
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()
    response.headers["WWW-Authenticate"] = ("Bearer realm="
                                            "{\"error_title\": \"Access to this website is protected\","
                                            "\"error\": \"expired_token\","
                                            "\"error_description\": \"The token provided is expired\"}")
    response.headers["Access-Control-Expose-Headers"] = "WWW-Authenticate"

    return response


def BAD_REQUEST_RES():
    response = HttpRes(
        code=HTTPStatus.BAD_REQUEST
    ).make_response()
    response.headers["Content-Type"] = "application/problem+json"
    response.headers["Content-Language"] = "en"


def validate_authorization_header(authorization_header):
    data = authorization_header.split(" ")

    if len(data) != 2:
        return None

    if data[0] != "Bearer" or not data[1]:
        return None

    return data[1]


def require_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        user = None

        if "Authorization" in request.headers:
            access_token = validate_authorization_header(
                request.headers["Authorization"])

        if not access_token:
            return MISSING_TOKEN_RES()

        user_controller = UserController()

        res_token = decode_access(access_token)

        if res_token.is_err():
            if isinstance(res_token.err, jwt.ExpiredSignatureError):
                return EXPIRED_TOKEN_RES()

            return MISSING_TOKEN_RES()

        email = res_token.ok["email"]

        res_user = user_controller.get_by_email(email)

        if res_user.is_err():
            return MISSING_TOKEN_RES()

        user = res_user.ok

        return f(user, *args, **kwargs)

    return decorated


@app.route("/authorized", methods=["GET"])
@require_login
def authenticate(user):
    if user:
        return HttpRes(
            ok="Authorized",
            data={
                "email": user.email
            }).make_response()

    return HttpRes(
        err="Not Authorized",
    ).make_response()


@app.route("/token", methods=["POST"])
def token():
    refresh_token = None

    if "Authorization" in request.headers:
        refresh_token = validate_authorization_header(
            request.headers["Authorization"])

    if not refresh_token:
        return MISSING_TOKEN_RES()

    refresh_token_controller = RefreshTokenController()

    res_token = decode_refresh(refresh_token)

    if res_token.is_err():
        if isinstance(res_token.err, jwt.ExpiredSignatureError):
            return EXPIRED_TOKEN_RES()
        return MISSING_TOKEN_RES()

    if refresh_token_controller \
        .get_by_token(refresh_token) \
            .is_err():
        return MISSING_TOKEN_RES()

    email = res_token.ok["email"]

    res = renew_access(email)

    if res.is_err():
        return MISSING_TOKEN_RES()

    return HttpRes(
        ok="Successfully generated access token.",
        data={
            "token": res.ok
        }
    ).make_response()


@app.route("/register", methods=["POST"])
def register():
    ERR_HTTP_RES = HttpRes(
        err="Register failed",
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()

    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    if user_controller.create(email, password).is_err():
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
        err="Login failed",
        code=HTTPStatus.UNAUTHORIZED
    ).make_response()

    refresh_token_controller = RefreshTokenController()
    user_controller = UserController()

    email = request.form["email"]
    password = request.form["password"]

    user_res = user_controller.get_by_email(email)

    if user_res.is_err() or not user_res.is_ok():
        return ERR_HTTP_RES

    pwd_res = user_controller.check_pwd(user_res.ok, password)

    if pwd_res.is_err():
        return ERR_HTTP_RES

    access_token = gen_access_token({"email": email})
    refresh_token = gen_refresh_token({"email": email})

    if refresh_token_controller.add(refresh_token).is_err():
        return ERR_HTTP_RES

    return HttpRes(
        ok="Successfully logged in.",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    ).make_response()

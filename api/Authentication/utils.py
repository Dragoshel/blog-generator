import datetime
import jwt

from Core import app

SECRET_ACCESS = app.config["ACCESS_TOKEN_SECRET"]
SECRET_REFRESH = app.config["REFRESH_TOKEN_SECRET"]

EXP_ACCESS = app.config["ACCESS_TOKEN_EXP"]
EXP_REFRESH = app.config["REFRESH_TOKEN_EXP"]

ALGO = app.config["ALGORITHM"]


def _gen_token(data: dict, secret: str | None, exp: int):
    datetime_now = datetime.datetime.now()
    expiration_delta = datetime.timedelta(seconds=exp)
    expiration_time = (datetime_now + expiration_delta).strftime('%s')

    payload = data | {
        "iat": datetime_now.strftime('%s'),
        "exp": expiration_time
    }

    return jwt.encode(payload, secret, algorithm=ALGO)


def gen_access_token(data: dict):
    return _gen_token(data, SECRET_ACCESS, int(EXP_ACCESS))


def gen_refresh_token(data: dict):
    return _gen_token(data, SECRET_REFRESH, int(EXP_REFRESH))


def decode_access(access_token: str):
    return jwt.decode(access_token, key=SECRET_ACCESS, algorithms=[ALGO])


def decode_refresh(refresh_token: str):
    return jwt.decode(refresh_token, key=SECRET_REFRESH, algorithms=[ALGO])


def renew_access(refresh_token: str):
    try:
        data = decode_refresh(refresh_token)

        access_token = gen_access_token({"email": data["email"]})

        return access_token
    except Exception as e:
        return str(e)

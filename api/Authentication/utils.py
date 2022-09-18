import datetime
import jwt

from Core import app, Res

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
        "iat": int(datetime_now.strftime('%s')),
        "exp": int(expiration_time)
    }

    return jwt.encode(payload, secret, algorithm=ALGO)


def gen_access_token(data: dict):
    return _gen_token(data, SECRET_ACCESS, int(EXP_ACCESS))


def gen_refresh_token(data: dict):
    return _gen_token(data, SECRET_REFRESH, int(EXP_REFRESH))


def decode_access(access_token: str) -> Res:
    try:
        val = jwt.decode(access_token, key=SECRET_ACCESS, algorithms=[ALGO])
        return Res(val, None)
    except Exception as err:
        return Res(None, err)


def decode_refresh(refresh_token: str):
    try:
        val = jwt.decode(refresh_token, key=SECRET_REFRESH, algorithms=[ALGO])
        return Res(val, None)
    except Exception as err:
        return Res(None, err)


def renew_access(email: str) -> Res:
    access_token = gen_access_token({"email": email})

    return Res(access_token, None)

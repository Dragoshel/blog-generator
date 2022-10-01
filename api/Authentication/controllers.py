from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
import bcrypt

import traceback

from .models import *
from Core import Engine, Res


class UserController:
    def __init__(self):
        self.engine = Engine()

    def get_by_email(self, email) -> Res:
        try:
            with Session(self.engine) as session:
                stmt = (select(User).where(User.email == email))
                user = session.scalars(stmt).one_or_none()

                return Res(user, None)
        except Exception as err:
            traceback.print_exc()
            return Res(None, err)

    def create(self, email, password) -> Res:
        try:
            res_db_user = self.get_by_email(email)

            if res_db_user.is_err():
                return res_db_user

            if res_db_user.is_ok():
                return Res(None, Exception("Email taken"))

            with Session(self.engine) as session:
                psw = password.encode("utf-8")
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(psw, salt)

                user = User(email=email, password=hashed)

                session.add(user)
                session.commit()
            return Res(True, None)
        except Exception as err:
            traceback.print_exc()
            return Res(None, err)

    def check_pwd(self, user, pwd) -> Res:
        try:
            pwd = pwd.encode("utf-8")
            hash = user.password

            if bcrypt.checkpw(pwd, hash) is not True:
                raise Exception("Password is not matching.")

            return Res(True, None)
        except Exception as err:
            traceback.print_exc()
            return Res(None, err)


class RefreshTokenController:
    def __init__(self):
        self.engine = Engine()

    def add(self, refresh_token: str) -> Res:
        try:
            with Session(self.engine) as session:
                token = RefreshToken(token=refresh_token)

                session.add(token)
                session.commit()
            return Res(True, None)
        except Exception as err:
            traceback.print_exc()
            return Res(None, err)

    def get_by_token(self, refresh_token: str) -> Res:
        try:
            with Session(self.engine) as session:
                stmt = (select(RefreshToken).where(
                        RefreshToken.token == refresh_token))
                refresh_token = session.scalars(stmt).one()

                return Res(refresh_token, None)
        except Exception as err:
            traceback.print_exc()
            return Res(None, err)

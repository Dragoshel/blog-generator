from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
import bcrypt

from .models import *
from Core import Engine


class UserController:
    def __init__(self):
        self.engine = Engine()

    def add(self, email, password):
        with Session(self.engine) as session:
            psw = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(psw, salt)

            user = User(email=email, password=hashed)

            session.add(user)
            session.commit()

    def get_by_email(self, email):
        with Session(self.engine) as session:
            stmt = (select(User).where(User.email == email))
            user = session.scalars(stmt).one()

            return user

    def check_psw(self, email, password):
        with Session(self.engine) as session:
            stmt = (select(User).where(User.email == email))
            user = session.scalars(stmt).one()

            psw = password.encode("utf-8")
            hashed = user.password

            return bcrypt.checkpw(psw, hashed)


class RefreshTokenController:
    def __init__(self):
        self.engine = Engine()

    def add(self, refresh_token: str):
        with Session(self.engine) as session:
            token = RefreshToken(token=refresh_token)

            session.add(token)
            session.commit()

    def get_by_token(self, refresh_token):
        try:
            with Session(self.engine) as session:
                stmt = (select(RefreshToken).where(
                        RefreshToken.token == refresh_token))
                refresh_token = session.scalars(stmt).one()

                return refresh_token
        except Exception:
            return None

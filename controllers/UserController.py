from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select
from models import User, RefreshToken

import bcrypt


class Engine:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = create_engine(
                "sqlite:///data.db", echo=True, future=True)
        return cls.__instance


class Controller:
    def __init__(self):
        self.engine = Engine()

    def add_user(self, email, password):
        with Session(self.engine) as session:
            psw = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(psw, salt)

            user = User(email=email, password=hashed)

            session.add(user)
            session.commit()

    def check_psw(self, email, password):
        with Session(self.engine) as session:
            stmt = (select(User).where(User.email == email))
            user = session.scalars(stmt).one()

            psw = password.encode("utf-8")
            hashed = user.password

            return bcrypt.checkpw(psw, hashed)

    def get_user(self, email):
        with Session(self.engine) as session:
            stmt = (select(User).where(User.email == email))
            user = session.scalars(stmt).one()

            return user

    def add_token(self, token):
        with Session(self.engine) as session:
            refresh_token = RefreshToken(token=token)

            session.add(refresh_token)
            session.commit()

    def get_token(self, token):
        try:
            with Session(self.engine) as session:
                stmt = (select(RefreshToken).where(RefreshToken.token == token))
                token = session.scalars(stmt).one()

                return token
        except Exception:
            return None

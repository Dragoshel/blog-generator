from re import split
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import Session
import bcrypt
from sqlalchemy.sql.expression import select
from werkzeug.wrappers import Request, Response
import jwt
from models import User

class Middleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        auth_header = request.headers['authorization']
        token = auth_header.split(' ')[1] if auth_header else None

        if token is None or token == "":
            res = Response(status=401)
            return res(environ, start_response)

        decoded = jwt.decode(token, key="secret", algorithms=["HS256"])

        print(decoded)

        return self.app(environ, start_response)


class Engine:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = create_engine(
                "sqlite:///data.db", echo=True, future=True)
        return cls.__instance


class UserController:
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

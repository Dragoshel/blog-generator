from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String


AuthenticationModel = declarative_base()


class RefreshToken(AuthenticationModel):
    __tablename__ = "refresh_token"
    token = Column(String, primary_key=True)

class User(AuthenticationModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
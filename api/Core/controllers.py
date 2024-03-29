from sqlalchemy.orm.session import Session
from sqlalchemy.sql import select

from Authentication.models import User

from . import Engine
from .models import *


class ArticleController:
    def __init__(self):
        self.engine = Engine()

    def get(self, article_id: int):
        with Session(self.engine) as session:
            stmt = (select(Article).where(Article.id == article_id))
            article = session.scalars(stmt).one()

            return article

    def create(self, title, body):
        with Session(self.engine) as session:
            article = Article(title=title, body=body)

            session.add(article)
            session.commit()

            return article.id

    def get_all_by_user(self, user):
        with Session(self.engine) as session:
            stmt = (select(Article).where(User.email == user.email))
            articles = session.scalars(stmt).all()

            return articles

    def get_filtered(self, filter):
        with Session(self.engine) as session:
            stmt = select(Article).limit(filter)
            articles = session.scalars(stmt).all()

            return articles

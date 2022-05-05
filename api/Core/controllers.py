from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import select

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

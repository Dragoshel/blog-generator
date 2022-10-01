from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship

CoreModel = declarative_base()

article_author = Table('Article_Author', CoreModel.metadata,
	Column("article_author_fk", ForeignKey("Article.id"), primary_key=True),
	Column("author_article_fk", ForeignKey("Author.id"), primary_key=True)
)

class Article(CoreModel):
    __tablename__ = "Article"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    authors = relationship("Author", secondary=article_author)


class Author(CoreModel):
    __tablename__ = "Author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Image(CoreModel):
	__tablename__ = "Image"

	id = Column(Integer, primary_key=True)
	path = Column(String)

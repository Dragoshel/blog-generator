from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import relationship

CoreModel = declarative_base()

association_table = Table('Article_Author', CoreModel.metadata,
	Column("article_author_fk", ForeignKey("article.id")),
	Column("author_article_fk", ForeignKey("author.id"))
)


class Article(CoreModel):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    authors = relationship("Author",
                           secondary=association_table)


class Author(CoreModel):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Image(CoreModel):
	__tablename__ = "image"

	id = Column(Integer, primary_key=True)
	path = Column(String)

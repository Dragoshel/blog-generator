from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.create import create_engine

from models import Base

def migrate():
	engine = create_engine("sqlite:///data.db", echo=True, future=True)
	engine.connect()
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

def main():
	migrate()

if __name__ == '__main__':
	main()
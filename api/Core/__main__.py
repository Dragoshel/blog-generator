import sys

from . import Engine
from Authentication.models import AuthenticationModel
from .models import CoreModel

def make_db():
    engine = Engine()
    engine.connect()

    AuthenticationModel.metadata.drop_all(engine)
    AuthenticationModel.metadata.create_all(engine)
    
    CoreModel.metadata.drop_all(engine)
    CoreModel.metadata.create_all(engine)


def main():
    args = sys.argv

    if len(args) < 2:
        print("Not enough arguments.")
    elif args[1] == "makedb":
        make_db()
    else:
        print("Argument not recognized.")


if __name__ == '__main__':
    main()

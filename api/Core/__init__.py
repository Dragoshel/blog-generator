from sqlalchemy.engine.create import create_engine
from flask import Flask
from dotenv import load_dotenv
import json

app = Flask(__name__)

load_dotenv()
app.config.from_prefixed_env()

class Engine:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = create_engine(
                app.config["DB_URL"], echo=True, future=True)
        return cls.__instance

import Builder.handlers
import Authentication.handlers

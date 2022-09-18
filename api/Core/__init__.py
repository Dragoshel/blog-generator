from sqlalchemy.engine.create import create_engine
from http import HTTPStatus
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv

# Starting point of flask app
app = Flask(__name__)

# cors = CORS(app, resources={r"*": {"origins": "localhost:5000"}})

load_dotenv()
app.config.from_prefixed_env()


class Engine:
    __instance = None

    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = create_engine(
                app.config["DB_URL"], echo=True, future=True)
        return cls.__instance


class Res:
    def __init__(self, ok, err: Exception | None) -> None:
        self.ok = ok
        self.err = err

    def is_ok(self) -> bool:
        return self.ok != None

    def is_not_ok(self) -> bool:
        return self.ok == None


class HttpRes:
    def __init__(self, ok="", err="", data={}, code=HTTPStatus.OK):
        self.ok = ok
        self.err = err
        self.data = data
        self.code = code

    def make_response(self):
        return make_response(jsonify({
            "ok": self.ok,
            "data": self.data,
            "error": self.err
        }), self.code.value)

import Authentication.handlers
import Builder.handlers
from . import handlers
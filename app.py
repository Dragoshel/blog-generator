# from sqlalchemy import create_engine
# from sqlalchemy.engine.base import Engine
# from sqlalchemy.orm import Session
# from sqlalchemy import select

# from models import *


# def delete_user(id: int, engine: Engine):
#     with Session(engine) as session:
#         user = session.get(User, id)

#         session.delete(user)

#         session.commit()


# def add_email(username, engine: Engine):
#     with Session(engine) as session:
#         stmt = (select(User).where(User.name == username))

#         user = session.scalars(stmt).one()

#         user.addresses.append(
#             Address(email_address="captainredmetal@gmail.com"))

#         session.commit()


# def drop(engine: Engine):
#     Base.metadata.drop_all(engine)


# def get(engine: Engine):
#     session = Session(engine)

#     stmt = (select(Address)
#             .join(Address.user)
#             .where(Address.email_address == "captainredmetal@gmail.com")
#             )
#     print("------------------------")
#     for address in session.scalars(stmt):
#         print(address)
#     print("------------------------")

#     session.close()


# def init(engine: Engine):
#     with Session(engine) as session:
#         dragos = User(
#             name="Dragos",
#             fullname="Dragos Ionescu",
#             addresses=[
#                 Address(email_address="ionescu.dragos23@gmail.com"),
#                 Address(email_address="captainredmetal@gmail.com")
#             ]
#         )

#         spongebob = User(
#             name="SpongeBob",
#             fullname="SpongeBob Squarepants",
#             addresses=[
#                 Address(email_address="captainredmetal@gmail.com")
#             ]
#         )

#         session.add_all([dragos, spongebob])

#         session.commit()


# def main():
#     engine = create_engine("sqlite:///data.db", echo=True, future=True)

#     engine.connect()

#     Base.metadata.create_all(engine)

#     # delete_user(1, engine)

#     init(engine)

#     for i in range(10):
#         add_email("Dragos", engine)

#     delete_user(1, engine)

#     get(engine)
#     # drop(engine)


# if __name__ == "__main__":
#     main()


import datetime
from flask import Flask, json
from flask import request
from flask import jsonify
from controllers.Authentication import gen_token, renew_access_token
from controllers.Authentication import require_login
from controllers.UserController import Controller
import jwt

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/token', methods=['POST'])
def token():
    token = request.form['token']
    controller = Controller()

    if not token:
        return {
            "message": "Missing refresh token"
        }, 401

    if not controller.get_token(token):
        return {
            "message": "The refresh token doesn't exist"
        }, 401

    try:
        jwt.decode(token, key="secret1", algorithms=["HS256"])

        access_token = renew_access_token(token)

        return jsonify({"token": access_token})
    except Exception as e:
        return jsonify(
            {
                "message": "The refresh token is invalid",
                "data": None,
                "error": str(e)
            })


@ app.route('/login', methods=['GET', 'POST'])
def login():

    controller = Controller()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if controller.check_psw(email, password):
            access_token = gen_token({"email": email}, "secret", 30)
            refresh_token = gen_token({"email": email}, "secret1", 60)

            controller.add_token(refresh_token)

            return jsonify({"access_token": access_token, "refresh_token": refresh_token})
        else:
            return jsonify({"message": "Login failed"})
    else:
        return jsonify({"message": "Please login"})


@ app.route('/register', methods=['GET', 'POST'])
def register():
    controller = Controller()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        controller.add_user(email, password)

        return jsonify({"success": {"email": email, "password": password}})
    else:
        return jsonify({"message": "Please register"})


@ app.route('/user', methods=['GET'])
@ require_login
def user(user):
    return jsonify({"email": user.email})


def main():
    app.run()


if __name__ == '__main__':
    main()

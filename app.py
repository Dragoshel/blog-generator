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


from flask import Flask
from flask import request
from flask import jsonify
from controllers.UserController import UserController
from controllers.UserController import Middleware
import jwt

app = Flask(__name__)
app.config["DEBUG"] = True

app.wsgi_app = Middleware(app.wsgi_app)

@app.route('/login', methods=['GET', 'POST'])
def login():

    user_controller = UserController()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if user_controller.check_psw(email, password):
            key = "secret"
            encoded = jwt.encode({"email": email}, key, algorithm="HS256")
            return jsonify({"jwt": encoded})
        else:
            return jsonify({"mgs": "Log in failed"})
    else:
        return jsonify({"msg": "Please log in"})


@app.route('/register', methods=['GET', 'POST'])
def register():
    user_controller = UserController()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_controller.add_user(email, password)

        return jsonify({"Success": {"email": email, "psw": password}})

    else:
        return jsonify({"msg": "Please register"})


def main():
    app.run()


if __name__ == '__main__':
    main()

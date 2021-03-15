import re
from data.user import User
from blueprints.constants import *
# from data.db_session import create_session
from flask import jsonify, Blueprint, make_response, request
from utils import filling_all

blueprint = Blueprint("clients_api", __name__, template_folder="templates")


@blueprint.route("/client/restore/", methods=["POST"])
def restore():  # восстановление пароля
    phone = request.form.get("phone")
    if not filling_all(phone):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    return make_response({"result": "OK"}, 200)


@blueprint.route("/client/registration/", methods=["POST"])
def user_registration():
    name = request.form.get("name")
    surname = request.form.get("surname")
    last_name = request.form.get("last_name")

    is_male = request.form.get("is_male")
    email = request.form.get("email")
    password = request.form.get("password")

    if not filling_all(name, surname, last_name, is_male, email, password):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    name = name.capitalize()
    surname = surname.capitalize()
    last_name = last_name.capitalize()
    is_male = is_male == 'True'

    email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    pattern = re.compile(email_pattern)
    if not re.match(pattern, email):
        return make_response(EMAIL_INCORRECT, 400)

    session = create_session()
    user = User(
        name, surname, last_name,
        is_male, email, password
    )

    try:
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        print(f"Register user error: {e}")
        return make_response(INTERNAL_ERROR, 500)

    return make_response(RESULT_SUCCESS, 200)


@blueprint.route("/client/login/", methods=["POST"])
def user_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if not filling_all(email, password):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    session = create_session()
    user = session.query(User).filter(User.email == email).first()
    if user == None:
        return make_response(USER_NOT_FOUND, 401)

    if user.password == password:
        session.close()
        return make_response(RESULT_SUCCESS, 200)
    else:
        session.close()
        return make_response(FORM_INCORRECT, 401)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

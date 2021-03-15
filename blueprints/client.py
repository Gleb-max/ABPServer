import re
import json

from data.enrollee import Enrollee
from data.user import User
from blueprints.constants import *
# from data.db_session import create_session
from flask import jsonify, Blueprint, make_response, request
from utils import filling_all
from data.db_session import db

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

    user = User(
        name, surname, last_name,
        is_male, email, password
    )

    try:
        db.session.add(user)
        db.session.commit()
        db.session.close()
    except Exception as e:
        print(f"Register user error: {e}")
        return make_response(INTERNAL_ERROR, 500)

    return make_response(RESULT_SUCCESS, 200)


def check_field_and_set(field, model, value):
    if field not in [None, ""]:
        setattr(model, field, value)
        db.session.commit()


@blueprint.route("/client/add/enrollee-data/", methods=["POST"])
def add_enrollee_data():
    user_id = request.form.get("user_id")

    # personal info
    name = request.form.get("name")
    surname = request.form.get("surname")
    last_name = request.form.get("last_name")
    is_male = request.form.get("is_male")
    email = request.form.get("email")
    birthday = request.form.get("birthday")
    phone = request.form.get("phone")
    birthday_place = request.form.get("birthday_place")
    need_hostel = request.form.get("need_hostel")
    photo = request.form.get("photo")

    # passport
    passport_series = request.form.get("passport_series")
    passport_number = request.form.get("passport_number")
    who_issued = request.form.get("who_issued")
    when_issued = request.form.get("when_issued")
    department_code = request.form.get("department_code")
    passport_scan = request.form.get("passport_scan")
    registration_address = request.form.get("registration_address")
    enrollment_consent = request.form.get("enrollment_consent")

    # Education
    certificate_number = request.form.get("certificate_number")
    certificate_scan = request.form.get("certificate_scan")
    is_budgetary = request.form.get("is_budgetary")
    study_direction = request.form.get("study_direction")

    exams = request.form.get("exams")
    individual_achievements = request.form.get("individual_achievements")
    original_or_copy = request.form.get("original_or_copy")

    if not user_id:
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    name = name.capitalize()
    surname = surname.capitalize()
    last_name = last_name.capitalize()
    is_male = is_male == 'True'

    email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
    pattern = re.compile(email_pattern)
    if not re.match(pattern, email):
        return make_response(EMAIL_INCORRECT, 400)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response(USER_NOT_FOUND, 400)

    try:
        # User model
        check_field_and_set(str(name), user, name)
        check_field_and_set(str(surname), user, surname)
        check_field_and_set(str(last_name), user, last_name)
        check_field_and_set(str(is_male), user, is_male)
        check_field_and_set(str(email), user, email)

        # TODO setting enrollee, processing data, saving images, catch errors

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

    user = db.session.query(User).filter(User.email == email).first()
    if user == None:
        return make_response(USER_NOT_FOUND, 401)

    if user.password == password:

        answer = {"user_id": user.id, "user_name": user.name,
                  "user_surname": user.surname, "user_last_name": user.last_name,
                  "user_is_male": user.is_male, "user_email": user.email,
                  "user_account_type": user.account_type}
        db.session.close()
        return make_response(json.dumps(answer), 200)
    else:
        db.session.close()
        return make_response(FORM_INCORRECT, 401)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

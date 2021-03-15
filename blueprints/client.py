# from fns.api import FnsApi
from data.users import User
from data.receipts import Receipt
from blueprints.constants import *
from data.db_session import create_session
from flask import jsonify, Blueprint, make_response, request
from utils import filling_all, parse_scan_result, get_datetime


blueprint = Blueprint("clients_api", __name__, template_folder="templates")


@blueprint.route("/client/restore/", methods=["POST"])
def restore():        # восстановление пароля
    phone = request.form.get("phone")
    if not filling_all(phone):
        return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)

    phone = phone[1:]
    # result = FnsApi.restore(phone)
    # print(result.text, result.status_code)
    # if not result.text:
    #     return RESULT_SUCCESS
    return make_response({"result": "OK"}, 200)


@blueprint.route("/client/registration/", methods=["POST"])
def registration():       # регистрация пользователя
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    # if not filling_all(name, email, phone):
    #     return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)
    # phone = phone[1:]
    # result = FnsApi.register(phone, email, name)
    # print(result.text, result.status_code)
    #
    # if result.status_code == 204:
    #     session = create_session()
    #     user = User(phone=phone, name=name, email=email)
    #     session.add(user)
    #     session.commit()
    #     session.close()
    #     return RESULT_SUCCESS
    return make_response({"result": "OK"}, 200)


@blueprint.route("/client/login/", methods=["POST"])
def login():     # вход в систему
    phone = request.form.get("phone")
    password = request.form.get("password")
    # if not filling_all(phone, password):
    #     return make_response(REQUIRED_FIELDS_NOT_FILLING, 400)
    # phone = phone[1:]
    # result = FnsApi.login(phone, password)
    # print(result.text, result.status_code)
    #
    # if result.status_code == 403:
    #     return make_response({"result": result.text}, 403)
    # session = create_session()
    # user = session.query(User).filter(User.phone == phone).first()
    # if user is None:
    #     user = User(phone=phone)
    #     result_json = result.json()
    #     user.email = result_json["email"]
    #     user.name = result_json["name"]
    #     session.add(user)
    #     session.commit()
    # session.close()
    # return result.text
    return make_response({"result": "OK"}, 200)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

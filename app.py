import os
import pickle
# from fns.api import FnsApi
from data.users import User
from data import db_session
from blueprints import client
from constants import DB_NAME
from flask_restful import Api
from data.receipts import Receipt
# from utils import parse_scan_result, predict, get_datetime
# from resources.users import UsersListResource, UsersResource
from flask import Flask, render_template, redirect, abort, url_for
# from resources.receipts import ReceiptsListResource, ReceiptsResource
from flask_login import LoginManager, login_required, logout_user, current_user, login_user


app = Flask(__name__)
app.config["SECRET_KEY"] = "ABP_SECRET_KEY"
# login_manager = LoginManager()
# login_manager.init_app(app)
api = Api(app)


# @login_manager.user_loader
# def load_user(user_id):
#     session = db_session.create_session()
#     user = session.query(User).get(user_id)
#     session.close()
#     return user


@app.route("/")
def index():
    return "SGU API"
    # receipts = []
    # if current_user.is_authenticated:
    #     session = db_session.create_session()
    #     receipts = session.query(Receipt).filter(Receipt.user == current_user).order_by(Receipt.date.desc()).all()
    #     session.close()
    # return render_template("index.html", receipts=receipts, title="Receipts Pro")
#
#
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect("/")
#     form = LoginForm()
#     if form.validate_on_submit():
#         phone = str(form.phone.data)[1:]
#         password = form.password.data
#         result = FnsApi.login(phone, password)
#         print(result.text, result.status_code)
#
#         if result.status_code == 403:
#             return render_template("login.html",
#                                    message="Неправильный логин или пароль",
#                                    form=form)
#         elif result.status_code == 500:
#             return render_template("login.html",
#                                    message="ФНС поломался",
#                                    form=form)
#
#         session = db_session.create_session()
#         user = session.query(User).filter(User.phone == phone).first()
#         if user is None:
#             user = User(phone=phone)
#             result_json = result.json()
#             user.email = result_json["email"]
#             user.name = result_json["name"]
#             session.add(user)
#             session.commit()
#         login_user(user, remember=form.remember_me.data)
#         session.close()
#         return redirect("/")
#     return render_template("login.html", title="Авторизация", form=form)
#
#
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated:
#         return redirect("/")
#     form = RegisterForm()
#     if form.validate_on_submit():
#         phone = str(form.phone.data)[1:]
#         email = form.email.data
#         name = form.name.data
#         session = db_session.create_session()
#
#         if session.query(User).filter(User.phone == phone).first():
#             session.close()
#             return render_template("register.html", title="Регистрация",
#                                    form=form,
#                                    message="К этому номеру уже привязан аккаунт")
#
#         result = FnsApi.register(phone, email, name)
#         print(result.text, result.status_code)
#
#         if result.status_code == 204:
#             user = User(phone=phone, name=name, email=email)
#             session.add(user)
#             session.commit()
#             session.close()
#             return redirect("/login")
#         if result.status_code == 409:
#             session.close()
#             return render_template("register.html", title="Регистрация",
#                                    form=form,
#                                    message="К этому номеру уже привязан аккаунт")
#         if result.status_code == 500:
#             session.close()
#             return render_template("register.html", title="Регистрация",
#                                    form=form,
#                                    message="Неверно указан номер телефона")
#         # default:
#         session.close()
#         return render_template("register.html", title="Регистрация",
#                                form=form,
#                                message="К этому номеру уже привязан аккаунт")
#     return render_template("register.html", title="Регистрация", form=form)
#
#
# @app.route("/restore", methods=["GET", "POST"])
# def restore():
#     if current_user.is_authenticated:
#         return redirect("/")
#     form = RestoreForm()
#     if form.validate_on_submit():
#         phone = str(form.phone.data)[1:]
#         result = FnsApi.restore(phone)
#         print(result.text, result.status_code)
#
#         if not result.text:
#             return redirect("/login")
#
#         return render_template("restore.html",
#                                message="Неверный номер телефона",
#                                form=form)
#     return render_template("restore.html", title="Восстановление", form=form)
#
#
# @app.route("/receipt_add", methods=["GET", "POST"])
# @login_required
# def add_receipt():
#     form = ReceiptForm()
#     if form.validate_on_submit():
#         scan_code = form.scan_result.data
#
#         session = db_session.create_session()
#         # беру юзера из бд, потому что когда добавляю чеки вот так: 'current_user.receipts.append(receipt)',
#         # иногда возникает ошибка, что пользователь не содержится в сессии (
#         # sqlalchemy.orm.exc.DetachedInstanceError: Parent instance <User at 0x7fa33807f650> is not bound to a Session
#         # ), а иногда все нормально коммитится. Я предполагаю, что это сборщик мусора чистит,
#         # или сессия истекает и не удается получить чеки по пользователю и единственный вариант,
#         # который пришел мне на ум - это брать юзера из сессии (как в следующей строке)
#         user = session.query(User).filter(User.phone == current_user.phone).first()
#         receipt = session.query(Receipt).filter(Receipt.scan_code == scan_code).first()
#
#         if receipt:
#             if receipt in user.receipts:
#                 session.close()
#                 return render_template("addreceipt.html", title="Добавление чека",
#                                        form=form, message="Вы уже добавили этот чек")
#             user.receipts.append(receipt)
#             session.merge(user)
#             session.commit()
#             session.close()
#             return redirect("/")
#
#         try:
#             scan_result = parse_scan_result(scan_code)
#             fn = scan_result["fn"]
#             i = scan_result["i"]
#             fp = scan_result["fp"]
#             n = scan_result["n"]
#             date = scan_result["t"]
#             amount = int(float(scan_result["s"]) * 100)
#         except (ValueError, KeyError):
#             return render_template("addreceipt.html", title="Добавление чека",
#                                    form=form, message="Неверный результат сканирования")
#
#         result = FnsApi.receipt_existing(fn, n, i, fp, date, amount)
#         if result.status_code == 406:
#             return render_template("addreceipt.html", title="Добавление чека",
#                                    form=form, message="Неверный результат сканирования")
#
#         result = FnsApi.receive(current_user.phone, form.password.data, fn, i, fp)
#
#         if result.status_code == 403:  # the user was not found or the specified password was not correct 403
#             return render_template("addreceipt.html", title="Добавление чека",
#                                    form=form, message="Неверный пароль")
#         if result.status_code == 406:  # the ticket was not found 406
#             return render_template("addreceipt.html", title="Добавление чека",
#                                    form=form, message="Чек получен слишком давно и отсутствует в базе")
#         if result.status_code == 500:    # Unknown string format 500
#             return render_template("addreceipt.html", title="Добавление чека",
#                                    form=form, message="Неверный результат сканирования")
#
#         receipt = result.json()["document"]["receipt"]
#         product_fields = ["name", "sum", "price", "quantity"]
#
#         products = [
#             tuple(product[field] for field in product_fields)
#             for product in receipt["items"]
#         ]
#         predicted = predict(map(lambda x: x[0], products))
#
#         _receipt = {
#             "products": [
#                 {
#                     "name": name,
#                     "category": category,
#                     "quantity": quantity,
#                     "price": price,
#                     "amount": amount,
#                 } for (name, amount, price, quantity), category in zip(products, predicted)
#             ],
#             "dateTime": receipt["dateTime"],
#             "totalSum": receipt["totalSum"],
#         }
#
#         pickled_receipt = pickle.dumps(_receipt)
#
#         new_receipt = Receipt(scan_code=scan_code, receipt=pickled_receipt, date=get_datetime(receipt["dateTime"]))
#         user.receipts.append(new_receipt)
#         session.merge(user)
#         session.commit()
#         session.close()
#         return redirect("/")
#     return render_template("addreceipt.html", title="Добавление чека", form=form)
#
#
# @app.route('/receipt_delete/<int:receipt_id>', methods=["GET", "POST"])
# @login_required
# def receipt_delete(receipt_id):
#     session = db_session.create_session()
#     receipt = session.query(Receipt).filter(
#         Receipt.id == receipt_id, Receipt.user == current_user
#     ).first()
#     if receipt:
#         session.delete(receipt)
#         session.commit()
#     else:
#         abort(404)
#     session.close()
#     return redirect("/")
#
#
# @app.route("/receipts/<int:receipt_id>", methods=["POST"])
# @login_required
# def receipt_by_id(receipt_id):   # for ajax
#     session = db_session.create_session()
#     receipt = session.query(Receipt).get(receipt_id)
#     if receipt and receipt.user == current_user:
#         session.close()
#         return pickle.loads(receipt.receipt)
#     session.close()
#     abort(404)


# for favicon
@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="img/favicon.ico"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/policy")
def policy():
    return render_template("policy.html", title="Политика конфиденциальности")


# initialize db
db_session.global_init(os.environ.get("DATABASE_URL", DB_NAME))

# register blueprint for mobile and desktop clients
app.register_blueprint(client.blueprint)

# add resources
# api.add_resource(ReceiptsListResource, "/api/v2/receipts")
# api.add_resource(ReceiptsResource, "/api/v2/receipts/<int:receipt_id>")
# api.add_resource(UsersListResource, "/api/v2/users")
# api.add_resource(UsersResource, "/api/v2/users/<int:phone>")


if __name__ == "__main__":
    app.run()

import pickle
from data import db_session
from flask import jsonify, make_response
from flask_restful import abort, Resource

from data.enrollee import Enrollee
from utils import datetime_to_str
from utils import get_bounds_by_period, get_datetime
from parsers.receipts import parser_get_all, parser_receipt, parser_create
import json


# def abort_if_receipt_or_user_not_found(phone, receipt_id):
#     session = db_session.create_session()
#     user = session.query(User).filter(User.phone == phone).first()
#     if not user:
#         session.close()
#         abort(404, message=f"user not found")
#     if not any(filter(lambda x: x.id == receipt_id, user.receipts)):
#         session.close()
#         abort(404, message=f"receipt not found")
#     session.close()


# class ReceiptsResource(Resource):
#     def get(self, receipt_id):
#         args = parser_receipt.parse_args()
#         phone = args["phone"][1:]
#         abort_if_receipt_or_user_not_found(phone, receipt_id)
#         session = db_session.create_session()
#         user = session.query(User).filter(User.phone == phone).first()
#         receipt = list(filter(lambda x: x.id == receipt_id, user.receipts))[0]
#         session.close()
#         return jsonify({"receipt": dict(date=datetime_to_str(receipt.date), receipt=pickle.loads(receipt.receipt))})
#
#     def delete(self, receipt_id):
#         args = parser_receipt.parse_args()
#         phone = args["phone"][1:]
#         abort_if_receipt_or_user_not_found(phone, receipt_id)
#         session = db_session.create_session()
#         user = session.query(User).filter(User.phone == phone).first()
#         receipt = list(filter(lambda x: x.id == receipt_id, user.receipts))[0]
#         session.delete(receipt)
#         session.commit()
#         session.close()
#         return jsonify({"success": "OK"})


# class ReceiptsListResource(Resource):
#     def get(self):
#         args = parser_get_all.parse_args()
#         period = args["period"]
#         if period not in ["day", "week", "month", "year", "all"]:
#             abort(404, message="unknown period")
#         session = db_session.create_session()
#         user = session.query(User).filter(User.phone == args["phone"][1:]).first()
#         if user is None:
#             session.close()
#             abort(404, message="User not found")
#         receipts = session.query(Receipt).filter(Receipt.user == user).order_by(Receipt.date.desc()).all()
#         if period == "all":
#             answer = {"receipts": list(map(
#                 lambda x: dict(date=x.date, receipt=pickle.loads(x.receipt)),
#                 receipts
#             ))}
#             session.close()
#             return jsonify(answer)
#         start_date, end_date = get_bounds_by_period(period)
#         receipts = filter(lambda x: start_date <= x.date <= end_date, receipts)
#         session.close()
#         return jsonify({"receipts": list(map(lambda x: dict(
#             date=datetime_to_str(x.date),
#             receipt=pickle.loads(x.receipt)
#         ), receipts))})
#
#     def post(self):
#         args = parser_create.parse_args()
#         phone = args["phone"][1:]
#         password = args["password"]
#         scan_code = args["scan_result"]
#
#         session = db_session.create_session()
#         user = session.query(User).filter(User.phone == phone).first()
#
#         if user is None:
#             session.close()
#             return jsonify({"result": "user not registered"})
#
#         receipt = session.query(Receipt).filter(Receipt.scan_code == scan_code).first()
#
#         if receipt:
#             if receipt in user.receipts:
#                 session.close()
#                 return jsonify({"result": "receipt exist"})
#             user.receipts.append(receipt)
#             session.merge(user)
#             session.commit()
#             session.close()
#             return pickle.loads(receipt.receipt)
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
#             return jsonify({"result": "scan code has invalid format"})
#
#         result = FnsApi.receipt_existing(fn, n, i, fp, date, amount)
#         if result.status_code == 406:
#             return make_response(jsonify({"result": "invalid scan code"}), 406)
#
#         result = FnsApi.receive(phone, password, fn, i, fp)
#
#         if result.status_code == 403:  # the user was not found or the specified password was not correct
#             return make_response({"result": result.text}, 403)
#         if result.status_code == 406:  # the ticket was not found
#             return make_response(jsonify({"result": "receipt not found"}), 406)
#         if result.status_code == 500:  # Unknown string format 500
#             return make_response(jsonify({"result": "invalid scan code"}), 406)
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
#         return jsonify({"result": "success"})

class EnrollsList(Resource):
    def get(self):
        answer = []
        for enrollee in Enrollee.query.all():
            user_dict = enrollee.user.to_dict()
            combined_dict = enrollee.to_dict()
            combined_dict.update(user_dict)

            answer.append(combined_dict)

        return json.dumps({'enrolls': answer})



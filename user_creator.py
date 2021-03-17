import re

import requests
import json
import random

from data.db_session import db
from data.user import User
from utils import filling_all

url = "http://127.0.0.1:5000/client/add/enrolleeData/"
#
# files = {
#     'photo': open('test_img.jpg', 'rb'),
#     'passport_scan': open('test_img.jpg', 'rb'),
#     'certificate_scan': open('test_img.jpg', 'rb'),
#     'enrollment_consent': open('test-pdf.pdf', 'rb'),
#     'agreement_scan': open('test-pdf.pdf', 'rb'),
# }
#
# body = {
#     'user_id': ,
#     'is_male': 'true',
#     'birthday': "17.12.2005",
#     'phone': '8-800',
#     'birth_place': 'here',
#     'need_hostel': 'true',
#     'study_direction_id': '1',
#     'exams': json.dumps({'items': [{'Русский': random.randint(50, 100)}, {'Матеша': random.randint(50, 100)}]}),
#     'passport_series': '7517',
#     'passport_number': '397531',
#     'who_issued': 'Выдан тем-то, тем-то',
#     'when_issued': '15.05.2017',
#     'department_code': '123123',
#     'registration_address': 'адрес регистрации',
#     'certificate_number': '123123321',
#     'is_budgetary': 'true',
#     'original_or_copy': 'true',
#     'individual_achievements': json.dumps({'indexes': [1, 2, 3]})
# }
#
# response = requests.request("POST", url, data=body, files=files)
#
# print(response.text)


# def register_new_user(name, surname, last_name, is_male, email, password):
#     if not filling_all(name, surname, last_name, is_male, email, password):
#         return 'Field not filled'
#
#     name = name.capitalize()
#     surname = surname.capitalize()
#     last_name = last_name.capitalize()
#
#     email_pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
#     pattern = re.compile(email_pattern)
#     if not re.match(pattern, email):
#         return 'Incorrect email'
#
#     if User.query.filter_by(email=email).first():
#         return 'User already exist'
#
#     user = User(
#         name, surname, last_name,
#         is_male, email, password
#     )
#
#     try:
#         db.session.add(user)
#         db.session.commit()
#         db.session.close()
#         return 'Success'
#     except Exception as e:
#         return f"Register user error: {e}"
import re

import requests
import json
import random

from data.db_session import db
from data.user import User
from utils import filling_all


def fill_user(user_id):
    url = "http://127.0.0.1:5000/client/add/enrolleeData/"
    url = 'https://sgu-api.herokuapp.com/client/add/enrolleeData/'

    files = {
        'photo': open('test_img.jpg', 'rb'),
        'passport_scan': open('test_img.jpg', 'rb'),
        'certificate_scan': open('test_img.jpg', 'rb'),
        'enrollment_consent': open('test_img.jpg', 'rb'),
        'agreement_scan': open('test_img.jpg', 'rb'),
    }

    body = {
        'user_id': user_id,
        'is_male': 'true' if random.randint(0, 1) else 'false',
        'birthday': f"{random.randint(1, 20)}.{random.randint(1, 12)}.{random.randint(1900, 2005)}",
        'phone': f'8993674{random.randint(1000, 9999)}',
        'birth_place': 'Place ...',
        'need_hostel': 'true' if random.randint(0, 1) else 'false',
        'study_direction_id': random.randint(1, 5),
        'exams': json.dumps({'items': [{'Русский': random.randint(50, 100)}, {'Математика': random.randint(50, 100)}]}),
        'passport_series': random.randint(1000, 9999),
        'passport_number': f'3975{random.randint(10, 99)}',
        'who_issued': 'Выдан тем-то, тем-то',
        'when_issued': f"{random.randint(1, 20)}.{random.randint(1, 12)}.{random.randint(2007, 2015)}",
        'department_code': '321123',
        'registration_address': 'Живет там-то, там-то',
        'certificate_number': 213 * random.randint(1,30),
        'is_budgetary': 'true',
        'original_or_copy': f"{random.randint(1, 20)}.{random.randint(1, 12)}.{random.randint(2007, 2015)}",
        'individual_achievements': json.dumps({'indexes': [random.randint(0, 3)]})
    }

    response = requests.request("POST", url, data=body, files=files)

    print(response.text)

fill_user(16)

users_to_fill = [17, 10, 16, 15]
for i in users_to_fill:
    fill_user(i)
# fill_user(19) # дарья

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

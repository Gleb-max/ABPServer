import requests
import json
import random

url = "http://127.0.0.1:5000/client/add/enrolleeData/"

for i in range(10):
    files = {
        'photo': open('test_img.jpg', 'rb'),
        'passport_scan': open('test_img.jpg', 'rb'),
        'certificate_scan': open('test_img.jpg', 'rb'),
        'enrollment_consent': open('test-pdf.pdf', 'rb'),
        'agreement_scan': open('test_img.jpg', 'rb'),
    }

    body = {
        'user_id': 3 + i,
        'is_male': 'true',
        'birthday': "17.12.2005",
        'phone': '8-800',
        'birth_place': 'here',
        'need_hostel': 'true',
        'study_direction_id': '1',
        'exams': json.dumps({'items': [{'Русский': random.randint(50, 100)}, {'Матеша': random.randint(50, 100)}]}),
        'passport_series': '7517',
        'passport_number': '397531',
        'who_issued': 'Выдан тем-то, тем-то',
        'when_issued': '15.05.2017',
        'department_code': '123123',
        'registration_address': 'адрес регистрации',
        'certificate_number': '123123321',
        'is_budgetary': 'true',
        'original_or_copy': 'true',
        'individual_achievements': json.dumps({'indexes': [1, 2, 3]})
    }

    response = requests.request("POST", url, data=body, files=files)

    print(response.text)

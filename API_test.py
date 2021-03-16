import requests
import json

url = "http://127.0.0.1:5000/client/add/enrolleeData/"

files = {
    'photo': open('test_img.jpg', 'rb'),
    'passport_scan': open('test_img.jpg', 'rb'),
    'certificate_scan': open('test_img.jpg', 'rb'),
    'enrollment_consent': open('test_img.jpg', 'rb'),
    'agreement_scan': open('test_img.jpg', 'rb'),
}

body = {
    'user_id': '1',
    'name': 'Poser',
    'surname': 'Vova',
    'last_name': 'Kakov',
    'is_male': 'true',
    'email': 'popa123@mail.ru',
    'birthday': "17.12.2005",
    'phone': '8-800',
    'birth_place': 'here',
    'need_hostel': 'true',
    'study_direction_id': '1',
    'exams': json.dumps({'items': [{'Русский': 90}, {'Матеша': 100}]}),
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

import requests
import json

url = "http://127.0.0.1:5000/client/add/enrolleeData/"

# files = {'photo': open('test_img.jpg', 'rb')}
body = {
    'user_id': '1',
    'name': 'Poser',
    'study_direction_id': '1',
    'exams': json.dumps({'items': [{'Русский': 90}, {'Матеша': 100}]})
}

headers = {
    'authorization': "Bearer {token}"
}
response = requests.request("POST", url, data=body)

print(response.text)

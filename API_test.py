import requests

url = "http://127.0.0.1:5000/client/add/enrolleeData/"

files = {'photo': open('test_img.jpg', 'rb')}
body = {
    'user_id': '2',
    'name': 'Poser',
    'study_direction_id': '1',
}

headers = {
    'authorization': "Bearer {token}"
}
response = requests.request("POST", url, files=files, data=body)

print(response.text)
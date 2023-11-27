import requests

url = "http://127.0.0.1:8000/uploadfile/"

files = {'file': ('img_1.png', open('/home/ktp_user/Documents/Github_repo/image_quality_assessment/datasets/blurry/img_1.png', 'rb'))}
response = requests.post(url, files=files)

print(response.json())

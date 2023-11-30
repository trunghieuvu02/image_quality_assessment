import requests

url = "http://127.0.0.1:8000/uploadfile/"

files = {'file': ('img_1.png', open('/src/client-server/img_1.png', 'rb'))}
response = requests.post(url, files=files)

print(response.json())

# Check the response status code and content
if response.status_code == 200:
    # Successfully received a response
    json_response = response.json()
    print("Response:", json_response)
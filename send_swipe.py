import requests
import json

url = 'http://127.0.0.1:5000/swipe'
data = {
    "user_id": 1,
    "product_id": 123,
    "swipe_direction": "right"
}

#headers = {'Content-Type': 'application/json'}
#response = requests.post(url, data=json.dumps(data), headers=headers)

url = 'http://127.0.0.1:5000/recommendations?product_id=45'
response = requests.get(url)
print(response.json())


print(response.json())

import requests

product_id = 14399798  # Replace with the desired product ID

url = f'http://127.0.0.1:5000/recommendations/{product_id}'
response = requests.get(url)

if response.status_code == 200:
    recommendations = response.json()
    print(f"Recommendations for product ID {product_id}:")
    for rec in recommendations:
        print(rec)
else:
    print(f"Failed to get recommendations: {response.status_code}")
    print(response.json())
import requests

# URL of the FastAPI server
url = "http://127.0.0.1:8001"

# Sending a GET request
response = requests.get(url)
print("GET Response:", response.json())

# Sending a POST request
post_data = {"sample_key": "sample_value"}
response = requests.post(url + "/post", json=post_data)
print("POST Response:", response.json())

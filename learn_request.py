import requests

# 1. Ask the internet for a random cat fact
response = requests.get("https://catfact.ninja")

# 2. Print the status code (Should say 200)
print(f"Status Code: {response.status_code}")

# 3. Print the text data that came back
print(f"Data from internet: {response.text}")

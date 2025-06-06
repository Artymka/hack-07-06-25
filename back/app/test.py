import requests
from requests import Response


response: Response = requests.post(url="http://127.0.0.1/api/quest", json={"text": "teeext"}, stream=True)
for chunk in response.iter_content():
    print(chunk)
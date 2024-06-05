import requests

url='https://rugcheck.xyz/css/token.68ffae82.css'

response=requests.get(url)
print(response.json())
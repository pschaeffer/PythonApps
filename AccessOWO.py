import requests

url = 'https://oneworldobservatory.com/'

r = requests.get(url)
print(r.content)
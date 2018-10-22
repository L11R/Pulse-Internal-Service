import requests
import json

HDRS = {'Content-type': 'application/json', 'Encoding': 'utf-8'}

def send_file(url, payload):
    headers = HDRS.copy()
    return requests.post(url, verify=False, data=json.dumps(payload), headers=headers)

def get_data(token, url):
    headers = HDRS.copy()
    headers['Authorization'] = token
    return requests.get(url, verify=True, headers=headers)
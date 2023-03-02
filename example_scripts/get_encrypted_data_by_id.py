#!/bin/python
import requests
import base64
import mimetypes
import json

# configs
api_key='<api key>'
url = 'http://127.0.0.1:9101/api/get-encrypted-data/'+api_key+'/'
myobj = {'encrypt_id': '4'}

resp = requests.post(url, data = myobj)
print (resp.status_code)
print (resp.content)


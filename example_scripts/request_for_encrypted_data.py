#!/bin/python
import requests
import base64
import mimetypes
import json

# configs
api_key='<api key>'
url = 'http://127.0.0.1:9101/api/encrypt-data/'+api_key+'/'
myobj = {'data': "{'name' : 'Steve Blogs', 'Expiry Date': '20/02/2024', 'rego': '881GF34RS'} ", 'group': 'park_passes'}


resp = requests.post(url, data = myobj)
print (resp.status_code)
print (resp.content)


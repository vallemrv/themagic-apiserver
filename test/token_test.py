# -*- coding: utf-8 -*-
import requests
import sys
import os
import json
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

base = os.path.dirname(os.path.abspath(__file__))

files = {'docfile': open(base+'/get_test.py', 'rb')}
recordAdd = {
     'add':{
            'db': 'valleorm',
            'user':{
                'nombre': 'manolo cara bolo',

                }
     }
}

getTocken = {
  'username':'lolo',
  'password':'pepitolopez'
}
data = json.dumps(recordAdd)
token = {
    'user': 1,
    'token': '4n9-104e3bca8e294e1a17bb',
    'data': data
}



r = requests.post("http://localhost:8000/", data=token)
print r.content

# -*- coding: utf-8 -*-
import requests
import sys
import os
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

base = os.path.dirname(os.path.abspath(__file__))
print base

files = {'docfile': open(base+'/apps.pyc', 'rb')}
recordAdd = {
     'add':{
            'db': 'valleorm',
           'user':{
                'nombre': 'manolo cara bolo',
                'avatar':{
                    'descripcion': 'chupa cabras'
                }
           }
     }
}

recordModify =  {
    'add':{
        'db': 'valleorm',
        "user":{
               'ID': 1,
               'avatar':[{
                  'ID': 7,
                 'descripcion': "tu eres un crack"
               }]
            }
    }
}

getAvatar = {
    'get':{
        'db': 'valleorm',
        'avatar':{

        }

    }
}
import json
r = requests.post("http://localhost:8000/", data={'data':json.dumps(getAvatar)}, files=files)
print r.json()

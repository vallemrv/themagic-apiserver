# -*- coding: utf-8 -*-
import requests
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

paramsGetAll = {
    'get': {
        'db': 'valleorm',
        'user': {
            'columns': ['ID', 'Nombre'],
            'amigos':{
                'columns':["nombre"]
            }
        }
    }
}



import json
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsGetAll)})
for rows in r.json().get("get"):
    for row in rows:
        print rows[row]

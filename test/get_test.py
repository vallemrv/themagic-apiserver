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
                'ID': 1
            }
        }
    }
}

removeOneID ={
    'rm':{
     'db': 'valleorm',
     'user':{
        'ID': 1,
        'amigos':{

        }
        }
    },
    'get':{
        'db': 'valleorm',
         'user':{

         }
    }
}

import json
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsGetAll)})
print r.json()

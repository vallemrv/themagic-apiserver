# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   05-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 05-Sep-2017
# @License: Apache license vesion 2.0



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

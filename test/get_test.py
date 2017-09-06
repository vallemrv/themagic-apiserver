# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   05-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 05-Sep-2017
# @License: Apache license vesion 2.0


import requests
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import json
getAll = {
    'get': {
        'db': 'valleorm',
        'user': {
            'amigos':{}
        }
    }
}


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

data = json.dumps(getAll)

token = {
    'user': 1,
    'token': '4p7-591e4481a7e9dc398910',
    'data': data
}


r = requests.post("http://localhost:8000", data=token)
print r.json()

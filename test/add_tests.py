# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   05-Sep-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 06-Sep-2017
# @License: Apache license vesion 2.0

import requests
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import json

paramsRows = {
    'add':{
        "db":"valleorm",
        "user":[
               {
                    "nombre": "Rafael",
                    "apellido": "Perez",
                     }
               ,{
                    "nombre": "Aitor",
                    "apellido": "Rodriguez",
                    }
                ,{
                    "nombre": "Raul",
                    "apellido": "Blanco",
                    }
                ]
        }
}

paramsRow = {
    'add':{
        "db":"valleorm.db",
        'user':{
            "nombre": "Pepito",
            "apellido": "Lopez",
            }
        }
}

paramsNewChild = {
    'add':{
        "db":"valleorm",
        "user":{
            "nombre": "Loco",
            "apellido": "Dolores",
            "direcciones":[{
                "tipo":"calle",
                "nombre": "MARACENA",
                "localidad": "granada",
                "codigo": '18012'
               }]
            }
        }
}

paramsChild = {
    'add':{
        "db":"valleorm.db",
        "user":{
            "ID": 3,
            "direcciones":[{
                "tipo":"avd",
                "nombre": "Francisco Ayala",
                "localidad": "granada",
                "codigo": '18012'
               }]
            },
        }
}

paramsManyToMany = {
    'add': {
        'db': 'valleorm',
        'user':{
            "nombre": "Diego",
            "apellido": "Martinez",
            "amigos":[
               { "user":{
                   "nombre": "Amigito",
                   "apellido": "Feliz",
               }}
            ]
        }
    }
}


paramsManyToManyID = {
    'add': {
        'db': 'valleorm',
        'user':{
            'ID': 1,
            'amigos':[
               {
                 "user":{
                     'nombre': 'cocoroco',
                     'apellido': 'kikiriki',
                     'apodo': 'fernadiño'
                 }
               }
            ]
        }
    }
}


paramsMultiple = {
    'add':{
        'db': 'valleorm',
        'user':[
           {

                'nombre': 'Manolo',
                'apellido': 'Rodriguez'

           },
           {

                'nombre': 'Alvaro',
                'apellido': 'Rodriguez'

           },
           {
            'ID': 1,
            'hermanos':[
                    {
                  'user':{
                        'ID': 2
                        }
                    }
                    ]
           }
        ]
    }
}

data = json.dumps(paramsManyToManyID)

token = {
    'user': 1,
    'token': '4p7-591e4481a7e9dc398910',
    'data': data
}



r = requests.post("http://localhost:8000", data=token)
print r.json()

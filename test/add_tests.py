# -*- coding: utf-8 -*-
import requests
import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

paramsRows = {
    'add':{
        "db":"valleorm",
        "rows":[{
               "user":{
                    "nombre": "Rafael",
                    "apellido": "Perez",
                     }
               },{
                "user":{
                    "nombre": "Aitor",
                    "apellido": "Rodriguez",
                    }
                },{
                "user":{
                    "nombre": "Raul",
                    "apellido": "Blanco",
                    }
                }]
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
        'rows':[
           {
            'user': {
                'nombre': 'Manolo',
                'apellido': 'Rodriguez'
             }
           },
           {
            'user':{
                'nombre': 'Alvaro',
                'apellido': 'Rodriguez'
             }
           },
           {
              'user':{
                'ID': 1,
                'hermanos':[
                        {
                      'user':{
                            'ID': 2
                            }
                        }
                    ]
              }

           }
        ]
    }
}

import json
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsRow)})
print r.json()
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsRows)})
print r.json()
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsChild)})
print r.json()
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsNewChild)})
print r.json()
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsManyToMany)})
print r.json()
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsManyToManyID)})
print r.json()

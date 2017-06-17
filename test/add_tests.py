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
                    "apellido": "ñññ¢¢¢",
                    "telf": "6666",
                    "precio": 1233.0,
                    "casa": True,
                    "perro": "pdae"
                   }
               },{
                "user":{
                    "nombre": "Aitor",
                    "apellido": "Rodriguez",
                    "telf": "6666",
                    "precio": 1123.0,
                    "casa": True,
                    "perro": "pdae"
                    }
                },{
                "user":{
                    "nombre": "Raul",
                    "apellido": "Rodriguez",
                    "telf": "6666",
                    "precio": 103.0,
                    "casa": True,
                    "perro": "pdae"
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
            "telf": "6666",
            }
        }
}

paramsNewChild = {
    'add':{
        "db":"valleorm",
        "user":{
            "nombre": "Loco pitres",
            "apellido": "Rodriguez",
            "telf": "6666",
            "precio": 1233.0,
            "casa": True,
            "perro": "pdae",
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
            "nombre": "Loco pitres",
            "apellido": "Rodriguez",
            "telf": "6666",
            "precio": 1233.0,
            "casa": True,
            "perro": "pdae",
            "amigos":[
               { "user":{
                   "nombre": "amigito feliz",
                   "apellido": "Rodriguez",
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
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsMultiple)})
print r.json()

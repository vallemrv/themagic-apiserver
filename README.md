# themagic-apiserver
Server api generic. Deploy and now. Just worry about the client's logic.
Create databases according to queries in JSON format. Add columns on demand.
Create automatic relationships. etc. If you send files, 
the necessary fields are created to save the information of the file.

## Quickstart
Requirements
------------
* Django 1.5+
* valleorm
* django-tokenapi

for install packages
`$ pip install <packagename>`

:package: Installation
-----------------------

Clone repository
`$ git clone https://github.com/vallemrv/themagic-apiserver.git`
`$ link valleorm of python-ormsqlite on themagicapi folder`

Run server
`$ ./themagic-apiserver/server/manage.py runserver `
`open http://localhost:8000`

For more installation option see django deploy.

:arrow_forward: Payload
----------------------
Create table and add new record
```javascript
// Make the models and insert new record
insertVariousRow = {
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

//insert the new record and alter table for new columns
insertAndCreateTable = {
    'add':{
        "db":"valleorm.db",
        'user':{
            "nombre": "Pepito",
            "apellido": "Lopez",
            'telf': '777777',
            'email': 'lolo@ejemplo.com'
            }
        }
}
// Insert new row and create a new table child with new content
insertParentAndAddChild = {
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
//Add a new child the user know ID
addChildKnowIDParent = {
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

//Insert, create new user and create new relationship
createManyToManyRelation = {
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


ManyToManyWithID = {
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


multipleOperation = {
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
```
Query
-----
```javascript
allUser = {
    'get':{
      'db': 'valleorm',
      'user':{

      }
    }
}
byID = {
  get:{
    'db': 'valleorm',
    'user':{
        ID: 1
      }
    }
}

sameForChild = {
  get:{
    'db': 'valleorm',
    'user':{
        ID: 1
        'somechild':{
          'ID': 1,   //by ID
          "nombre":  "Lolo",  //for some query column
          "Joins": ["tablejoin", "relationjoin"],
          "columns": [`lis of columns],

        }
      }
    }
}

```

Requests example
----------------
```python
import requests
import json
data = json.dumps(***somedata***)
#for get token see https://github.com/jpulgarin/django-tokenapi.git
token = {
    'user': 1, #user number
    'token': 'some token',
    'data': data
}

r = requests.post("http://localhost:8000/", data=token)
print r.json()

```

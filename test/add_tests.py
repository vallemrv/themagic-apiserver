import requests

params = {
    'add':{
        "db":"valleorm",
        "tb":"user",
        "rows":[{
            "nombre": "Rafael",
            "apellido": "Rodriguez",
            "telf": "6666",
            "precio": 1233.0,
            "casa": True,
            "perro": "pdae"
            },{
                "nombre": "Aitor",
                "apellido": "Rodriguez",
                "telf": "6666",
                "precio": 1123.0,
                "casa": True,
                "perro": "pdae"
                },{
                    "nombre": "Raul",
                    "apellido": "Rodriguez",
                    "telf": "6666",
                    "precio": 103.0,
                    "casa": True,
                    "perro": "pdae"
                    }]
        }
}

paramsChild = {
    'add':{
        "db":"valleorm",
        "tb":"user",
        "row":{
            "ID": 1,
            "direcciones":[{
                "tipo":"avd",
                "nombre": "Francisco Ayala",
                "localidad": "granada"
               }]
            },
        }
}



'''
import json
r = requests.post("http://localhost:8000", {"data":json.dumps(paramsChild)})
print r.json()
'''
hola = [1,2,3]
adios = [4,5,6]
hola.append(adios)
print hola

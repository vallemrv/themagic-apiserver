import os
PATH_DBS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_DBS = os.path.join(PATH_DBS, "dbs/")



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from valleorm.models import Models
import json

# Create your views here.
@csrf_exempt
def index(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({"Error": "Este servidor solo acepta peticiones POST"}))
    response = {}
    data = json.loads(request.POST.get("data"))
    if "add" in data:
        post = data.get("add")
        db = post.get("db")+".db"
        tb = post.get("tb")
        multiple = "rows" in post
        if multiple:
            rows = post.get("rows")
            response['add'] = []
            for row in rows:
                response = actionAdd(response, row, db, tb, multiple)
        else:
            row = post.get("row")
            response = actionAdd(response, row, db, tb, multiple)
    if "get" in request.POST:
        response = get(response, data.get("get"))
    if "rm" in request.POST:
        response = rm(response, data.get("rm"))


    return send_response(HttpResponse(json.dumps(response)))

@csrf_exempt
def sendFiles(request):
    return HttpResponse("files download")



def send_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    response["Content-Type"] = "application/json"
    return response


def actionAdd(objResponse, row_req, db, tb, multiple):
    row, relations = modifyRow(row_req, db, tb)
    row_send = row.toJSON()
    for relation in relations:
        nameKey = relation["relationName"]
        if not nameKey in row_send:
            row_send[mameKey] = []
        row_send[name]
        getattr(row, mameKey).add(modifyRow(row_req[nameKey]))

    row = row.toJSON()

    if multiple:
        objResponse["add"].append(row_send)
    else:
        objResponse["add"] = row_send
    return objResponse

def repare_model(model, row, db, tb):
    for key, v in row.items():
        search = filter(lambda field: field['fieldName'] == key, model["fields"])
        if len(search) <= 0:
            default, tipo = getTipo(v)
            field = {
                'fieldName': key,
                'fieldDato': default,
                'fieldTipo': tipo
            }
            model['fields'].append(field)
            Models.alter(path=PATH_DBS, dbName=db, tableName=tb, field=field)

    return model



def create_model(row):
    model = {"fields":[], "relationship": []}
    for key, v in row.items():
        default, tipo = getTipo(v)

        model["fields"].append({
         'fieldName': key,
         'fieldDato': default,
         'fieldTipo': tipo
        })

    return model


def modifyRow(row_json, db, tb):
    model = {}
    row = None
    if "ID" in row_json:
        row = Models(path=PATH_DBS, dbName=db, tableName=tb)
        row.loadByPk(row_json.get("ID"))
    else:
        if Models.exitsTable(path=PATH_DBS, dbName=db, tableName=tb):
            model = Models.getModel(path=PATH_DBS, dbName=db, tableName=tb)
            model = repare_model(model=model, row=row_json,
                                 db=db, tb=tb)
        else:
            model = create_model(row_json)

        row = Models(path=PATH_DBS, dbName=db, tableName=tb, model=model)
    relations = []
    for key, v in row_json.items():
        typeField = type(getattr(row, key))
        if typeField is dict:
            relationship = {
                'relationName': key,
                'relationTipo': "ONE",
            }
            relations.append(relationship)
        elif typeField is list:
            relationship = {
                'relationName': key,
                'relationTipo': "MANY",
            }
            relations.append(relationship)
        else:
            setattr(row, key, v)

    row.save()
    row.appendRelations(relations)
    return row, relations

def getTipo(val):
    if type(val) is unicode:
        return ("'None'", "TEXT")
    elif type(val) is float:
        return (1.0, "REAL")
    elif type(val) is int:
        return (1, "INTEGER")
    else:
        return ("'None'", "TEXT")

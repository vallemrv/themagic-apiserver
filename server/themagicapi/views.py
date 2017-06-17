# -*- coding: utf-8 -*-
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
        if not "db" in post:
            return HttpResponse(json.dumps({"Error": "No se sabe el nombre de la db. Inique una con la Key='db'"}))

        db = post.get("db") if 'db' in post.get("db") else post.get("db")+".db"
        for k, v in post.items():
            if k == "db":
                pass
            elif k == "rows":
                rows = post.get("rows")
                response['add'] = []
                for row in rows:
                    for kr, vr in row.items():
                        response = actionAdd(response, vr, db, kr, True)
            else:
                response = actionAdd(response, v, db, k, False)

    if "get" in request.POST:
        response = get(response, data.get("get"))
    if "rm" in request.POST:
        response = rm(response, data.get("rm"))

    http = HttpResponse(json.dumps(response, ensure_ascii=False))
    return send_response(http)

@csrf_exempt
def sendFiles(request):
    return HttpResponse("files download")



def send_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    response["Content-Type"] = "application/json; charset=utf-8"
    return response


def actionAdd(objResponse, row_req, db, tb, multiple):
    row, relations = modifyRow(row_req, db, tb)
    row.save()
    row_send = row.toDICT()
    for relation in relations:
        nameKey = relation["fieldName"] if 'fieldName' in relation else relation["relationName"]
        if not nameKey in row_send:
            row_send[nameKey] = []
        for r in row_req[nameKey]:
            if relation["relationTipo"] == "MANY":
                child, relchild = modifyRow(r, db, nameKey, relationship={
                    'relationName': tb,
                    'relationTipo': "ONE",
                })
            else:
                tbName = relation["relationName"]
                child, relchild = modifyRow(r[tbName], db, tbName)
                child.save()

            getattr(row, nameKey).add(child)
            row_send[nameKey].append(child.toDICT())

    if multiple:
        objResponse["add"].append(row_send)
    else:
        objResponse["add"] = row_send
    return objResponse

def repare_model(model, row, db, tb):
    for key, v in row.items():
        if not type(v) is list:
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
        if not type(v) is list:
            default, tipo = getTipo(v)
            model["fields"].append({
             'fieldName': key,
             'fieldDato': default,
             'fieldTipo': tipo
            })

    return model


def modifyRow(row_json, db, tb, relationship=None):
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
            if relationship:
                model["relationship"].append(relationship)

        row = Models(path=PATH_DBS, dbName=db, tableName=tb, model=model)
    relations = []
    for key, v in row_json.items():
        if type(row_json[key]) is list:
            fieldName = key
            relationName = key
            child = row_json[key]
            tipo = "MANY"
            for kr, vr in  child[0].items():
                if type(vr) is dict:
                    tipo = "MANYTOMANY"
                    relationName = kr
                    break;
                else:
                    break;

            rship = {
                'fieldName': fieldName,
                'relationName': relationName,
                'relationTipo': tipo,
            }
            relations.append(rship)
        else:
            setattr(row, key, v)

    if len(relations) > 0:
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

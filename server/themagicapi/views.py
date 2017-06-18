# -*- coding: utf-8 -*-
import os
PATH_DBS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_DBS = os.path.join(PATH_DBS, "dbs/")



from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from controller.addcontroller import AddController
from controller.getcontroller import GetController
import json

# Create your views here.
@csrf_exempt
def index(request):
    if request.method != 'POST':
        return HttpResponseBadRequest(json.dumps({"Error": "Este servidor solo acepta peticiones POST"}))
    data = json.loads(request.POST.get("data"))
    JSONResponse = {}
    if "add" in data:
        JSONRequire = data.get("add")
        if not "db" in JSONRequire:
            return HttpResponseBadRequest(json.dumps({"Error":
                             "No se sabe el nombre de la db. Inique una con la Key='db'"}))
        AddController(JSONRequire=JSONRequire,
                              JSONResponse=JSONResponse, path=PATH_DBS)


    if "get" in data:
        JSONRequire = data.get("get")
        if not "db" in JSONRequire:
            return HttpResponseBadRequest(json.dumps({"Error":
                             "No se sabe el nombre de la db. Inique una con la Key='db'"}))
        GetController(JSONRequire=JSONRequire,
                              JSONResponse=JSONResponse, path=PATH_DBS)


    if "rm" in request.POST:
        response = rm(response, data.get("rm"))

    http = HttpResponse(json.dumps(JSONResponse, ensure_ascii=False))
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

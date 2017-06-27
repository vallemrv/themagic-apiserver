# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from controller.addcontroller import AddController
from controller.getcontroller import GetController
from controller.rmcontroller import RmController
from controller.filecontroller import FileController
import json

# Create your views here.
@csrf_exempt
def index(request):
    if request.method != 'POST' or not 'data' in request.POST:
        return HttpResponseBadRequest(json.dumps({"Error": "Este servidor solo acepta peticiones POST"}))
    data = json.loads(request.POST.get("data"))
    fichero = None if not 'docfile' in request.FILES else request.FILES["docfile"]
    JSONResponse = {}
    for name in data.keys():
        if "add" == name:
            JSONRequire = data.get("add")
            if not "db" in JSONRequire:
                return HttpResponseBadRequest(json.dumps({"Error":
                                 "No se sabe el nombre de la db. Indique una con la Key='db'"}))
            AddController(JSONRequire=JSONRequire,
                          JSONResponse=JSONResponse, path=settings.PATH_DBS, fichero=fichero)

        if "get" == name:
            JSONRequire = data.get("get")
            if not "db" in JSONRequire:
                return HttpResponseBadRequest(json.dumps({"Error":
                                 "No se sabe el nombre de la db. Indique una con la Key='db'"}))
            GetController(JSONRequire=JSONRequire,
                          JSONResponse=JSONResponse, path=settings.PATH_DBS)

        if "rm" == name:
            JSONRequire = data.get("rm")
            if not "db" in JSONRequire:
                return HttpResponseBadRequest(json.dumps({"Error":
                                 "No se sabe el nombre de la db. Indique una con la Key='db'"}))
            RmController(JSONRequire=JSONRequire,
                         JSONResponse=JSONResponse, path=settings.PATH_DBS)

    http = HttpResponse(json.dumps(JSONResponse, ensure_ascii=False))
    return send_response(http)

@csrf_exempt
def getfiles(request):
    pass

def send_response(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    response["Content-Type"] = "application/json; charset=utf-8"
    return response

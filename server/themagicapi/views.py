# -*- coding: utf-8 -*-
from django.conf import settings
from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError,
from django.http import HttpResponse
from controller.addcontroller import AddController
from controller.getcontroller import GetController
from controller.rmcontroller import RmController
from controller.filecontroller import FileController
import json

# Create your views here.
@token_required
def index(request):
    if request.method != 'POST' or not 'data' in request.POST:
        return JsonError({"Error": "Este servidor solo acepta peticiones POST"})
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
                return JsonError({"Error":
                                 "No se sabe el nombre de la db. Indique una con la Key='db'"})
            GetController(JSONRequire=JSONRequire,
                          JSONResponse=JSONResponse, path=settings.PATH_DBS)

        if "rm" == name:
            JSONRequire = data.get("rm")
            if not "db" in JSONRequire:
                return JsonError({"Error":
                                 "No se sabe el nombre de la db. Indique una con la Key='db'"})
            RmController(JSONRequire=JSONRequire,
                         JSONResponse=JSONResponse, path=settings.PATH_DBS)

    http = JsonResponse(JSONResponse)
    return http

@token_required
def getfiles(request):
    if request.method != 'POST' or not 'ID' in request.POST:
        return JsonError({"Error": "Este servidor solo acepta peticiones POST"})

    id_file = request.POST["ID"]
    path = FileController.getPath(id_file)
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

# -*- coding: utf-8 -*-
"""Controlador para themagicapi

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valleorm.models import Models
from filecontroller import FileController

class AddController():
    def __init__(self, JSONResponse, JSONRequire, path, fichero=None):
        self.JSONResponse = JSONResponse
        self.JSONRequire = JSONRequire
        self.path = path
        self.fichero = fichero

        self.db = JSONRequire.get("db") if 'db' in JSONRequire.get("db") else JSONRequire.get("db")+".db"
        for k, v in JSONRequire.items():
            if k == "db":
                pass
            elif k == "rows":
                rows = JSONRequire.get("rows")
                JSONResponse['add'] = []
                for row in rows:
                    for kr, vr in row.items():
                        self.actionAdd(vr, kr, True)
            else:
                self.actionAdd(v, k, False)

    def actionAdd(self, row_req, tb, multiple):
        row, relations = self.modifyRow(row_req, tb)
        row.save()
        row_send = row.toDICT()
        if len(relations) <= 0 and self.fichero:
            filecontroller = FileController(path=self.path, db=self.db)
            rowfile = filecontroller.addFile(row, self.fichero)
            row_send[row.tableName] = rowfile
        for relation in relations:
            nameKey = relation["fieldName"] if 'fieldName' in relation else relation["relationName"]
            _rows = []
            if not nameKey in row_send:
                row_send[nameKey] = []
            if type(row_req[nameKey]) is dict:
                _rows = [row_req[nameKey]]
            else:
                _rows = row_req[nameKey]
            for r in _rows:
                if relation["relationTipo"] == "MANY":
                    child, relchild = self.modifyRow(r, nameKey, relationship={
                        'relationName': tb,
                        'relationTipo': "ONE",
                    })
                else:
                    tbName = relation["relationName"]
                    child, relchild = self.modifyRow(r[tbName], tbName)
                    child.save()

                getattr(row, nameKey).add(child)
                child_send = child.toDICT()
                if self.fichero:
                    filecontroller = FileController(path=self.path, db=self.db)
                    rowfile = filecontroller.addFile(child, self.fichero)
                    child_send = rowfile

                row_send[nameKey].append(child_send)


        if multiple:
            self.JSONResponse["add"].append(row_send)
        else:
            self.JSONResponse["add"] = row_send

    def modifyRow(self, row_json, tb, relationship=None):
        model = {}
        row = None
        if "ID" in row_json:
            row = Models(path=self.path, dbName=self.db, tableName=tb)
            row.loadByPk(row_json.get("ID"))
        else:
            if Models.exitsTable(path=self.path, dbName=self.db, tableName=tb):
                model = Models.getModel(path=self.path, dbName=self.db, tableName=tb)
                model = self.repare_model(model=model, row=row_json, tb=tb)
            else:
                model = self.create_model(row_json)
                if relationship:
                    model["relationship"].append(relationship)
            row = Models(path=self.path, dbName=self.db, tableName=tb, model=model)
        relations = []
        for key, v in row_json.items():
            if type(row_json[key]) is list  or type(v) is dict:
                fieldName = key
                relationName = key
                childs = row_json[key]
                tipo = "MANY"
                child = childs[0] if type(v) is list else childs
                for kr, vr in  child.items():
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

    def repare_model(self, model, row, tb):
        for key, v in row.items():
            if not type(v) is list  and not type(v) is dict:
                search = filter(lambda field: field['fieldName'] == key, model["fields"])
                if len(search) <= 0:
                    default, tipo = self.getTipo(v)
                    field = {
                        'fieldName': key,
                        'fieldDato': default,
                        'fieldTipo': tipo
                    }
                    model['fields'].append(field)
                    Models.alter(path=self.path, dbName=self.db, tableName=tb, field=field)

        return model

    def create_model(self, row):
        model = {"fields":[], "relationship": []}

        for key, v in row.items():
            if not type(v) is list and not type(v) is dict:
                default, tipo = self.getTipo(v)
                model["fields"].append({
                 'fieldName': key,
                 'fieldDato': default,
                 'fieldTipo': tipo
                })

        return model




    def getTipo(self, val):
        if type(val) is unicode:
            return ("None", "TEXT")
        elif type(val) is float:
            return (None, "REAL")
        elif type(val) is int:
            return (None, "INTEGER")
        else:
            return ("None", "TEXT")

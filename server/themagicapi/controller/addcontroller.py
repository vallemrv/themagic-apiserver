# -*- coding: utf-8 -*-
"""Controlador para themagicapi

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valleorm.models import Models

class AddController():
    def __init__(self, JSONResponse, JSONRequire, path):
        self.JSONResponse = JSONResponse
        self.JSONRequire = JSONRequire
        self.path = path

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
        for relation in relations:
            nameKey = relation["fieldName"] if 'fieldName' in relation else relation["relationName"]
            if not nameKey in row_send:
                row_send[nameKey] = []
            for r in row_req[nameKey]:
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
                row_send[nameKey].append(child.toDICT())

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

    def repare_model(self, model, row, tb):
        for key, v in row.items():
            if not type(v) is list:
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
            if not type(v) is list:
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

# -*- coding: utf-8 -*-
"""Controlador para themagicapi

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valleorm.models import Models

class GetController():
    def __init__(self, JSONResponse, JSONRequire, path):
        self.JSONResponse = JSONResponse
        self.JSONRequire = JSONRequire
        self.path = path
        JSONResponse['get'] = []

        self.db = JSONRequire.get("db") if 'db' in JSONRequire.get("db") else JSONRequire.get("db")+".db"
        for k, v in JSONRequire.items():
            if k == "db":
                pass
            elif k == "rows":
                rows = JSONRequire.get("rows")
                for row in rows:
                    for kr, vr in row.items():
                        self.actionGet(vr, kr)
            else:
                self.actionGet(v, k)



    def actionGet(self, condition, tb):
        row = Models(path=self.path, dbName=self.db, tableName=tb)
        if "ID" in condition:
            row.loadByPk(condition["ID"])
            response = {tb:row.toDICT()}
            for col, val in condition.items():
                if type(condition[col]) is dict:
                    modelCondition, subQuery = self.getModelQuery(val)
                    rows = getattr(row, col).get(modelCondition)
                    response[col] = []
                    for child in rows:
                        response[col].append(child.toDICT())

            self.JSONResponse["get"].append(response)

        else:
            mainCondition, subQuery = self.getModelQuery(condition)
            for rowMain in row.getAll(condition=mainCondition):
                if len(subQuery) > 0:
                    for nodeCondition, fieldName in subQuery:
                        subNodeCondition, nothing = self.getModelQuery(nodeCondition)
                        rows = getattr(rowMain, fieldName).get(subNodeCondition)
                        if len(rows) > 0:
                            response = {tb:rowMain.toDICT()}
                            response[tb][fieldName] = []
                            for row in rows:
                                response[tb][fieldName].append(row.toDICT())

                            self.JSONResponse["get"].append(response)
                else:
                    self.JSONResponse["get"].append(rowMain.toDICT())

    def getModelQuery(self, condition):
        modelCondition = {}
        query = []
        subQuery = []
        for col, val in condition.items():
            isWordReserver = col == 'columns' or col == 'limit' or col == 'offset'
            isWordReserver = isWordReserver or col == 'query' or col == 'order'
            isWordReserver = isWordReserver or col == 'joins' or col == 'group'
            if isWordReserver:
               modelCondition[col] = val
            elif not isWordReserver and type(condition[col]) is dict :
                subQuery.append((condition[col], col))
            else:
               packQuery = self.getPackQuery(col, val)
               query.append(packQuery)
        if 'query' in modelCondition and len(query) > 0:
            modelCondition['query'] += " AND "+" AND ".join(query)
        elif len(query) > 0:
            modelCondition["query"] = " AND ".join(query)

        return modelCondition, subQuery

    def getPackQuery(self, col, val):
        if type(val) is unicode:
            return col + " LIKE '"+val+"'"
        elif type(val) is float:
            return col + "="+val
        elif type(val) is int:
            return col + "="+val
        else:
            return col + " LIKE '"+val+"'"

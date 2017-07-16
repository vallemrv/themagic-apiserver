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


class RmController():
    def __init__(self, JSONResponse, JSONRequire, path):
        self.JSONResponse = JSONResponse
        self.JSONRequire = JSONRequire
        self.path = path
        JSONResponse['rm'] = []

        self.db = JSONRequire.get("db") if 'db' in JSONRequire.get("db") else JSONRequire.get("db")+".db"
        for k, v in JSONRequire.items():
            if k == "db":
                pass
            else:
                self.actionGet(v, k)



    def actionGet(self, condition, tb):
        row = Models(path=self.path, dbName=self.db, tableName=tb)
        if "ID" in condition:
            row.loadByPk(condition["ID"])
            response = {tb:"remove:" +'1' if row.ID > 0 else '0' , 'ID': row.ID}
            rmRoot = True
            for col, val in condition.items():
                if type(condition[col]) is dict:
                    rmRoot = False
                    modelCondition, subQuery = self.getModelQuery(val)
                    rows = getattr(row, col).get(modelCondition)
                    response = {col:"remove "+str(len(rows)), 'IDs': []}

                    for child in rows:
                        response["IDs"].append(child.ID)
                        if FileController.hasFile(child):
                            fileController = FileController(path=self.path, db=self.db)
                            row_send = fileController.rmFile(child)

                        getattr(row, col).remove(child)

            if rmRoot:
                if FileController.hasFile(row):
                    fileController = FileController(path=self.path, db=self.db)
                    row_send = fileController.rmFile(row)

                row.remove()

            self.JSONResponse["rm"].append(response)

        else:
            mainCondition, subQuery = self.getModelQuery(condition)
            numRemoveRow = 0
            for rowMain in row.getAll(condition=mainCondition):
                if len(subQuery) > 0:
                    for nodeCondition, fieldName in subQuery:
                        subNodeCondition, nothing = self.getModelQuery(nodeCondition)
                        rows = getattr(rowMain, fieldName).get(subNodeCondition)
                        if len(rows) > 0:
                            response = {}
                            response[fieldName] = [{col:"remove "+str(len(rows)), 'IDs': []}]
                            for row in rows:
                                if FileController.hasFile(row):
                                    fileController = FileController(path=self.path, db=self.db)
                                    row_send = fileController.rmFile(row)

                                getattr(rowMain, fieldName).remove(row)
                                response[fieldName]['IDs'].append(row.ID)

                            self.JSONResponse["rm"].append(response)
                else:
                    numRemoveRow += 1
                    self.JSONResponse["rm"].append({tb:"remove: "+str(numRemoveRow), 'ID': rowMain.ID})
                    if FileController.hasFile(rowMain):
                        fileController = FileController(path=self.path, db=self.db)
                        row_send = fileController.rmFile(rowMain)

                    rowMain.remove()

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

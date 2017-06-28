# -*- coding: utf-8 -*-
"""Controlador para themagicapi

    Autor: Manuel Rodriguez
    Licencia: Apache v2.0

"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from valleorm.models import Models
from themagicapi.models import FilesUpload

class FileController():
    def __init__(self, path, db):
        self.path = path
        self.db = db

    def addFile(self, row, fichero):
        if not FileController.hasFile(row):
            field = {
                'fieldName': 'id_file_uploader',
                'fieldDato': None,
                'fieldTipo': 'INTEGER'
            }
            Models.alter(path=self.path, dbName=self.db, tableName=row.tableName, field=field)
            row.appnedField(field)
        else:
            id_search = row.id_file_uploader if row.id_file_uploader != 'None' else -1
            uploader = FilesUpload.objects.filter(pk=id_search)
            for u in uploader:
                u.delete()


        new_file = FilesUpload(docfile=fichero)
        new_file.save()
        row.id_file_uploader = new_file.id
        row.save()
        row_send = row.toDICT()
        row_send["file"] = {'ID': row.id_file_uploader, 'Name': new_file.docfile.name}
        del row_send["id_file_uploader"]
        return row_send

    def rmFile(self, row):
        id_search = row.id_file_uploader if row.id_file_uploader != 'None' else -1
        uploader = FilesUpload.objects.filter(pk=id_search)
        for u in uploader:
            u.delete()

        return 1


    def getFile(self, row):
        id_search = row.id_file_uploader if row.id_file_uploader != 'None'  else -1
        uploader = FilesUpload.objects.filter(pk=id_search)
        row_send = row.toDICT()
        if uploader.count() > 0:
            uploader = uploader.first()
            row_send["file"] = {'ID': row.id_file_uploader, 'Name': uploader.docfile.name}
            del row_send['id_file_uploader']

        return row_send

    @staticmethod
    def getPath(self, id_search):
        id_search = id_search if id_search != 'None'  else -1
        uploader = FilesUpload.objects.filter(pk=id_search)
        response = None
        if uploader.count() > 0:
            uploader = uploader.first()
            response = uploader.docfile.name

        return response



    @staticmethod
    def hasFile(row):
        return hasattr(row, 'id_file_uploader')

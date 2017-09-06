# -*- coding: utf-8 -*-
# @Author: Manuel Rodriguez <valle>
# @Date:   27-Jun-2017
# @Email:  valle.mrv@gmail.com
# @Filename: token_test.py
# @Last modified by:   valle
# @Last modified time: 05-Sep-2017
# @License: Apache license vesion 2.0



import requests
import sys
import os
import json
import ssl
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

base = os.path.dirname(os.path.abspath(__file__))

recordAdd = {
     'get':{
            'db': 'valleorm',
            'user':{
            }
     }
}

getTocken = {
  'username':'test',
  'password':'calamatraca'
}

data = json.dumps(recordAdd)

token = {
    'user': 1,
    'token': '4p7-591e4481a7e9dc398910',
    'data': data
}


r = requests.post("http://localhost:8000/token/new.json", data=getTocken )
print r.content

# @Author: Manuel Rodriguez <valle>
# @Date:   27-Jun-2017
# @Email:  valle.mrv@gmail.com
# @Filename: token_test.py
# @Last modified by:   valle
# @Last modified time: 19-Jul-2017
# @License: Apache license vesion 2.0


# -*- coding: utf-8 -*-
import requests
import sys
import os
import json
import ssl
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

base = os.path.dirname(os.path.abspath(__file__))

files = {'docfile': open(base+'/get_test.py', 'rb')}
recordAdd = {
     'get':{
            'db': 'valleorm',
            'user':{
            }
     }
}

getTocken = {
  'username':'pepito',
  'password':'pepitolopez'
}
data = json.dumps(recordAdd)
token = {
    'user': 1,
    'token': '4na-f85142bc46b22993427d',
    'data': data
}


r = requests.post("http://localhost:8000/", data=getTocken )
print r.content
